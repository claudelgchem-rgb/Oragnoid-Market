#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSVX Agent O — evidence 병합기
evidence/evidence_<AGENT>.jsonl 들을 evidence/evidence.jsonl 로 병합한다.
Agent R 의 evidence_verified.jsonl 이 있으면 그 tier/confidence/verified_by 를 우선 적용한다.
evidence_rejected.jsonl 에 있는 ID 는 rejected 플래그를 달아 병합본에 남긴다(추적 가능성).
"""
import json
import os
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVDIR = os.path.join(ROOT, "evidence")

REQUIRED = ["id", "claim", "source_title", "publisher", "url", "access_date",
            "source_type", "tier", "confidence"]

AGENT_ORDER = ["B", "C", "D", "A", "E", "F", "G", "X", "S"]


def load_jsonl(path):
    """관대한 JSONL 로더 — 깨진 줄은 건너뛰되 사유를 보고한다."""
    recs, bad = [], []
    if not os.path.exists(path):
        return recs, bad
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("//") or line.startswith("#"):
                continue
            try:
                obj = json.loads(line)
                if isinstance(obj, dict) and obj.get("id"):
                    recs.append(obj)
                else:
                    bad.append((path, i, "id 필드 없음"))
            except json.JSONDecodeError as e:
                bad.append((path, i, "JSON 파싱 실패: %s" % e))
    return recs, bad


def main():
    merged = {}
    order = []
    bad_all = []
    per_agent = {}

    for ag in AGENT_ORDER:
        p = os.path.join(EVDIR, "evidence_%s.jsonl" % ag)
        recs, bad = load_jsonl(p)
        bad_all.extend(bad)
        per_agent[ag] = len(recs)
        for r in recs:
            rid = r["id"].strip()
            r["id"] = rid
            r.setdefault("owner_agent", ag)
            if rid in merged:
                bad_all.append((p, 0, "중복 ID %s (기존 owner=%s) — 후행 레코드 무시"
                                % (rid, merged[rid].get("owner_agent"))))
                continue
            merged[rid] = r
            order.append(rid)

    # 기타 evidence_*.jsonl (agent 범위 밖 파일) 도 흡수
    for p in sorted(glob.glob(os.path.join(EVDIR, "evidence_*.jsonl"))):
        base = os.path.basename(p)
        if base in ("evidence_verified.jsonl", "evidence_rejected.jsonl"):
            continue
        tag = base[len("evidence_"):-len(".jsonl")]
        if tag in AGENT_ORDER:
            continue
        recs, bad = load_jsonl(p)
        bad_all.extend(bad)
        per_agent[tag] = len(recs)
        for r in recs:
            rid = r["id"].strip()
            r["id"] = rid
            r.setdefault("owner_agent", tag)
            if rid not in merged:
                merged[rid] = r
                order.append(rid)

    # Agent R 재판정 반영
    ver, badv = load_jsonl(os.path.join(EVDIR, "evidence_verified.jsonl"))
    bad_all.extend(badv)
    r_applied = 0
    r_added = 0
    for v in ver:
        rid = v["id"].strip()
        if rid in merged:
            for k in ("tier", "confidence", "verified_by", "access_status",
                      "r_reason", "note"):
                if v.get(k) not in (None, ""):
                    if k == "note" and merged[rid].get("note"):
                        merged[rid]["note"] = merged[rid]["note"] + " || R: " + str(v[k])
                    else:
                        merged[rid][k] = v[k]
            merged[rid]["verified_by"] = "R"
            r_applied += 1
        else:
            v["owner_agent"] = v.get("owner_agent", "R")
            v["verified_by"] = "R"
            merged[rid] = v
            order.append(rid)
            r_added += 1

    # 거절 레코드 플래그
    rej, badr = load_jsonl(os.path.join(EVDIR, "evidence_rejected.jsonl"))
    bad_all.extend(badr)
    rejected_ids = set()
    for r in rej:
        rid = r["id"].strip()
        rejected_ids.add(rid)
        if rid in merged:
            merged[rid]["rejected"] = True
            merged[rid]["rejection_reason"] = r.get("rejection_reason", r.get("note", "사유 미기재"))
            merged[rid]["confidence"] = "하"
        else:
            r["rejected"] = True
            r["owner_agent"] = r.get("owner_agent", "?")
            merged[rid] = r
            order.append(rid)

    # 필수 필드 보정 (빈칸 금지 — 사유를 남긴다)
    for rid in order:
        r = merged[rid]
        for k in REQUIRED:
            if k not in r or r[k] in (None, ""):
                if k == "url":
                    r[k] = "internal:calc"
                    r["access_status"] = r.get("access_status", "no-url")
                    r["note"] = (r.get("note", "") + " || O: url 미기재 → internal:calc 로 표기").strip(" |")
                elif k == "tier":
                    r[k] = "T3"
                elif k == "confidence":
                    r[k] = "하"
                elif k == "access_date":
                    r[k] = "2026-08-11"
                else:
                    r[k] = "(미기재)"
        r.setdefault("value", "")
        r.setdefault("unit", "")
        r.setdefault("verified_by", "")
        r.setdefault("note", "")
        r.setdefault("access_status", "ok")
        r.setdefault("rejected", False)

    out = os.path.join(EVDIR, "evidence.jsonl")
    with open(out, "w", encoding="utf-8") as f:
        for rid in sorted(order, key=lambda x: (x[:2], x)):
            f.write(json.dumps(merged[rid], ensure_ascii=False) + "\n")

    tiers, confs, types = {}, {}, {}
    for r in merged.values():
        tiers[r["tier"]] = tiers.get(r["tier"], 0) + 1
        confs[r["confidence"]] = confs.get(r["confidence"], 0) + 1
        types[r["source_type"]] = types.get(r["source_type"], 0) + 1

    print("=" * 62)
    print("OSVX evidence 병합 결과")
    print("=" * 62)
    print("병합 레코드 수 : %d" % len(merged))
    print("에이전트별     : %s" % ", ".join("%s=%d" % (k, v) for k, v in per_agent.items() if v))
    print("R 재판정 적용  : %d건 / R 신규 보강: %d건" % (r_applied, r_added))
    print("R 거절(격리)   : %d건" % len(rejected_ids))
    print("Tier 분포      : %s" % tiers)
    print("신뢰도 분포    : %s" % confs)
    print("소스타입 분포  : %s" % types)
    print("출력           : %s" % out)
    if bad_all:
        print("\n[경고] 처리 불가/중복 %d건:" % len(bad_all))
        for p, i, m in bad_all[:40]:
            print("  - %s:%s %s" % (os.path.basename(p), i, m))
    return 0


if __name__ == "__main__":
    sys.exit(main())
