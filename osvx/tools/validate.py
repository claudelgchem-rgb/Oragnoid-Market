#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSVX 품질 게이트 — G1~G7 + 추가검사
exit 0 이 아니면 "완료" 선언 금지 (R6).

usage: python3 tools/validate.py [--json]
"""
import json
import os
import re
import sys
import glob
import collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
EVDIR = os.path.join(ROOT, "evidence")
DATA = os.path.join(ROOT, "data")
MODEL = os.path.join(ROOT, "model")
REPORT = os.path.join(ROOT, "report")

EID = re.compile(r"\[(E-\d{3}(?:-R)?)\]")

# ---- G1 기대 산출물 : (경로, 최소바이트, 담당에이전트) ----
EXPECTED = [
    ("docs/A_market_sizing.md", 4000, "A"),
    ("docs/B_regulatory.md", 4000, "B"),
    ("docs/C_competition.md", 4000, "C"),
    ("docs/D_voc_barriers.md", 4000, "D"),
    ("docs/E_cogs.md", 4000, "E"),
    ("docs/F_ip_fto.md", 4000, "F"),
    ("docs/G_gtm.md", 4000, "G"),
    ("docs/R_credibility.md", 2500, "R"),
    ("docs/V_audit.md", 2500, "V"),
    ("docs/X_redteam.md", 4000, "X"),
    ("docs/S_synthesis.md", 4000, "S"),
    ("docs/premise_audit.md", 1500, "B"),
    ("docs/assumptions.md", 800, "전체"),
    ("docs/gaps.md", 300, "전체"),
    ("data/price_table.csv", 2000, "C"),
    ("data/patent_table.csv", 2000, "F"),
    ("model/market_model.py", 1500, "A"),
    ("model/cogs_model.py", 1500, "E"),
    ("evidence/evidence.jsonl", 5000, "O"),
    ("report/OSVX_report.docx", 20000, "W"),
    ("model/OSVX_model.xlsx", 8000, "S"),
    ("evidence/evidence_ui.html", 20000, "O"),
]

# ---- G3 금지 표현 ----
FORBIDDEN = [
    ("추후 검토", None), ("추후 조사", None), ("향후 과제", None),
    ("범위를 벗어", None), ("데이터 부족으로 생략", None),
    ("일반적으로 알려진 바에 따르면", None), ("심층 분석 권장", None),
    ("데이터 확보 시 업데이트", None), ("추가 검증이 요구", None),
    ("TBD", None),
    # 조건부: 같은 줄에 근거 [E-###] 가 없을 때만 위반
    ("업계에서는", "needs_evidence"),
    ("추정됨", "needs_evidence"),
    ("것으로 보인다", "needs_evidence"),
    # 조건부: 사유 미기재 N/A
    ("N/A", "na_without_reason"),
]
# 금지표현 스캔 제외: 규칙서 자신, 도구, 감사보고서(위반을 인용해 보고하는 문서)
G3_EXCLUDE = {"AGENT_RULES.md", "V_audit.md", "validate.py",
              "merge_evidence.py", "build_evidence_ui.py", "osvx_pipeline.js"}

VERDICTS = ["Conditional-Go", "No-Go", "Go"]

res = {"gates": {}, "details": collections.defaultdict(list)}


def add(gate, ok, msg):
    res["details"][gate].append(("PASS" if ok else "FAIL", msg))
    if not ok:
        res["gates"][gate] = "FAIL"
    else:
        res["gates"].setdefault(gate, "PASS")


def rd(p):
    try:
        with open(p, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except OSError:
        return ""


def docx_text(p):
    try:
        from docx import Document
    except ImportError:
        return None
    try:
        d = Document(p)
        out = [x.text for x in d.paragraphs]
        for t in d.tables:
            for row in t.rows:
                for c in row.cells:
                    out.append(c.text)
        return "\n".join(out)
    except Exception as e:  # noqa: BLE001
        return "__DOCX_ERROR__ %s" % e


def md_corpus():
    """본문 문서 코퍼스 (계획서 제외)."""
    out = {}
    for p in sorted(glob.glob(os.path.join(DOCS, "*.md"))):
        if p.endswith("_plan.md"):
            continue
        out[os.path.relpath(p, ROOT)] = rd(p)
    return out


# ============================== G1 ==============================
def g1():
    for rel, minb, owner in EXPECTED:
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            add("G1", False, "누락: %s (담당 Agent %s)" % (rel, owner))
        else:
            sz = os.path.getsize(p)
            if sz < minb:
                add("G1", False, "빈약: %s = %d bytes (최소 %d, 담당 %s)" % (rel, sz, minb, owner))
            else:
                add("G1", True, "%s (%.1f KB)" % (rel, sz / 1024.0))
    # xlsx 시트 검증
    xp = os.path.join(MODEL, "OSVX_model.xlsx")
    if os.path.exists(xp):
        try:
            import openpyxl
            wb = openpyxl.load_workbook(xp)
            n = len(wb.sheetnames)
            add("G1", n >= 6, "OSVX_model.xlsx 시트 %d개: %s" % (n, wb.sheetnames))
            wbf = openpyxl.load_workbook(xp)
            nf = 0
            for ws in wbf.worksheets:
                for row in ws.iter_rows():
                    for c in row:
                        if isinstance(c.value, str) and c.value.startswith("="):
                            nf += 1
            add("G1", nf >= 20, "xlsx 살아있는 수식 %d개 (최소 20)" % nf)
        except Exception as e:  # noqa: BLE001
            add("G1", False, "xlsx 검증 실패: %s" % e)


# ============================== G2 ==============================
def g2():
    ep = os.path.join(EVDIR, "evidence.jsonl")
    if not os.path.exists(ep):
        add("G2", False, "evidence.jsonl 없음")
        return set()
    ids, dups, nourl, bad = set(), [], [], 0
    for i, line in enumerate(open(ep, encoding="utf-8"), 1):
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            bad += 1
            continue
        rid = r.get("id", "")
        if rid in ids:
            dups.append(rid)
        ids.add(rid)
        if not r.get("url"):
            nourl.append(rid)
    add("G2", bad == 0, "JSONL 파싱 오류 %d건" % bad)
    add("G2", not dups, "중복 ID %d건 %s" % (len(dups), dups[:10]))
    add("G2", not nourl, "url 빈 레코드 %d건 %s" % (len(nourl), nourl[:10]))
    add("G2", len(ids) >= 120, "총 근거 %d건 (최소 120 목표)" % len(ids))

    cited, missing = set(), collections.defaultdict(list)
    corpus = md_corpus()
    dp = os.path.join(REPORT, "OSVX_report.docx")
    if os.path.exists(dp):
        t = docx_text(dp)
        if t and not t.startswith("__DOCX_ERROR__"):
            corpus["report/OSVX_report.docx"] = t
    for rel, txt in corpus.items():
        for m in EID.findall(txt):
            cited.add(m)
            if m not in ids:
                missing[rel].append(m)
    for rel, ms in missing.items():
        add("G2", False, "%s: evidence.jsonl 에 없는 근거 %d건 %s"
            % (rel, len(set(ms)), sorted(set(ms))[:12]))
    if not missing:
        add("G2", True, "본문 인용 %d개 ID 전부 evidence.jsonl 에 존재" % len(cited))
    orphan = len(ids - cited)
    add("G2", True, "미인용(대장에만 존재) 근거 %d건 — 위반 아님(참고)" % orphan)
    return ids


# ============================== G3 ==============================
def g3():
    hits = []
    targets = md_corpus()
    dp = os.path.join(REPORT, "OSVX_report.docx")
    if os.path.exists(dp):
        t = docx_text(dp)
        if t and not t.startswith("__DOCX_ERROR__"):
            targets["report/OSVX_report.docx"] = t
    for rel, txt in targets.items():
        if os.path.basename(rel) in G3_EXCLUDE:
            continue
        for ln, line in enumerate(txt.split("\n"), 1):
            for phrase, cond in FORBIDDEN:
                if phrase not in line:
                    continue
                if cond == "needs_evidence" and EID.search(line):
                    continue
                if cond == "na_without_reason":
                    seg = line[line.index("N/A"):line.index("N/A") + 40]
                    if "사유" in seg or "(" in seg[:6]:
                        continue
                hits.append("%s:%d  «%s»  → %s" % (rel, ln, phrase, line.strip()[:110]))
    add("G3", not hits, "금지표현 %d건%s" % (len(hits), ("" if not hits else " (제외: %s)" % ", ".join(sorted(G3_EXCLUDE)))))
    for h in hits[:40]:
        res["details"]["G3"].append(("FAIL", "  " + h))


# ============================== G4 ==============================
def g4():
    need = {"docs/A_market_sizing.md": 8, "docs/E_cogs.md": 6, "docs/S_synthesis.md": 6}
    pat = re.compile(r"(계산식|=\s*[\d,\.]+\s*[x×\*])|(×\s*[\d,\.])|(\bCAGR\s*=)")
    for rel, minimum in need.items():
        txt = rd(os.path.join(ROOT, rel))
        n = len(pat.findall(txt))
        add("G4", n >= minimum, "%s 계산식 표기 %d건 (최소 %d)" % (rel, n, minimum))


# ============================== G5 ==============================
def g5():
    txt = rd(os.path.join(DOCS, "A_market_sizing.md"))
    paths = {"Bottom-up": ("Bottom-up" in txt or "상향식" in txt),
             "Top-down": ("Top-down" in txt or "하향식" in txt),
             "Proxy/역산": ("Proxy" in txt or "역산" in txt)}
    for k, v in paths.items():
        add("G5", v, "삼각측량 경로 '%s' %s" % (k, "존재" if v else "누락"))
    dev = ("편차" in txt) or ("괴리" in txt) or ("deviation" in txt.lower())
    add("G5", dev, "경로 간 편차 기록 %s" % ("존재" if dev else "누락"))
    for kw, label in (("TAM", "TAM"), ("SAM", "SAM"), ("SOM", "SOM")):
        add("G5", kw in txt, "%s 산출 %s" % (label, "존재" if kw in txt else "누락"))
    vol = ("L/년" in txt) or ("리터" in txt) or ("L/yr" in txt) or ("물량" in txt)
    add("G5", vol, "물량(L/년) 축 %s" % ("존재" if vol else "누락"))


# ============================== G6 ==============================
def g6():
    ep = os.path.join(EVDIR, "evidence.jsonl")
    if not os.path.exists(ep):
        add("G6", False, "evidence.jsonl 없음")
        return
    recs = [json.loads(l) for l in open(ep, encoding="utf-8") if l.strip()]
    if not recs:
        add("G6", False, "근거 0건")
        return
    # 핵심결론 지지 근거 = 핵심 문서에서 실제 인용된 것
    core_docs = ["docs/A_market_sizing.md", "docs/C_competition.md", "docs/E_cogs.md",
                 "docs/S_synthesis.md", "docs/F_ip_fto.md"]
    core_ids = set()
    for rel in core_docs:
        core_ids.update(EID.findall(rd(os.path.join(ROOT, rel))))
    core = [r for r in recs if r.get("id") in core_ids] or recs
    n = len(core)
    lo = sum(1 for r in core if r.get("confidence") == "하")
    t1 = sum(1 for r in core if r.get("tier") == "T1")
    lop, t1p = 100.0 * lo / n, 100.0 * t1 / n
    add("G6", lop <= 30.0, "핵심결론 지지근거 %d건 중 신뢰도'하' %d건 = %.1f%% (허용 <=30%%)" % (n, lo, lop))
    add("G6", t1p >= 40.0, "핵심결론 지지근거 T1 %d건 = %.1f%% (요구 >=40%%)" % (t1, t1p))
    nver = sum(1 for r in recs if r.get("verified_by") == "R")
    add("G6", nver >= min(60, len(recs)), "Agent R 검증 완료 %d / %d건" % (nver, len(recs)))


# ============================== G7 ==============================
def g7():
    s = rd(os.path.join(DOCS, "S_synthesis.md"))
    w = ""
    dp = os.path.join(REPORT, "OSVX_report.docx")
    if os.path.exists(dp):
        t = docx_text(dp)
        if t and not t.startswith("__DOCX_ERROR__"):
            w = t
    found_s = [v for v in VERDICTS if v in s]
    found_w = [v for v in VERDICTS if v in w]
    add("G7", bool(found_s), "S_synthesis.md 판정 문자열: %s" % (found_s or "없음"))
    add("G7", bool(found_w), "OSVX_report.docx 판정 문자열: %s" % (found_w or "없음"))
    if found_s and found_w:
        add("G7", found_s[0] == found_w[0], "S 와 W 의 판정 일치 (S=%s / W=%s)" % (found_s[0], found_w[0]))
    x = rd(os.path.join(DOCS, "X_redteam.md"))
    kc = len(re.findall(r"(?:KC|Kill\s*Criteri\w*)[\s\-–—]*#?\s*\d", x, re.I))
    if kc < 5:
        kc = max(kc, x.count("KC-"), len(re.findall(r"중단\s*(?:기준|조건)", x)))
    add("G7", kc >= 5, "Kill Criteria %d개 (요구 5개, X_redteam.md)" % kc)
    act = len(re.findall(r"(?:A[\-–]?\d|액션\s*\d|Action\s*\d)", s))
    has90 = ("90일" in s) or ("90-day" in s.lower())
    add("G7", has90, "90일 검증 계획 섹션 %s" % ("존재" if has90 else "누락"))
    add("G7", act >= 5, "90일 액션 항목 %d개 (요구 5개)" % act)


# ============================== 추가 검사 ==============================
def extra():
    a = rd(os.path.join(DOCS, "assumptions.md"))
    rows = [l for l in a.split("\n") if l.strip().startswith("|") and l.count("|") >= 4]
    # 가정 행만 추출 — 첫 열이 가정ID 형식(예: A-A01, C-A2c, X-A13)인 것.
    # 가정 항목 안에 중첩된 보조 표(채널별 계수 등)는 가정 자체가 아니므로 제외한다.
    ASSUM_ID = re.compile(r"^[A-Z]-A\d+[a-z]?$")
    body = [l for l in rows if not re.match(r"^\s*\|[\s\-:|]+\|\s*$", l)
            and "가정ID" not in l and "가정값" not in l
            and ASSUM_ID.match(l.split("|")[1].strip() if l.count("|") >= 2 else "")]
    # 민감도 영향 = 마지막 열. 키워드 매칭은 정당한 서술을 놓치므로(예: "FTO 판정이 중→상으로
    # 바뀌고 즉시 No-Go 사유가 된다") 서술의 실질성으로 판정한다: 20자 이상이면 충족,
    # "동상"·"해당없음" 같은 대체 표기나 절차 메모는 미충족.
    STUB = re.compile(r"^(동상|상동|위와\s*같음|해당\s*없음|없음|N/?A|-)\s*$")
    nosens = []
    for l in body:
        cell = l.split("|")[-2].strip() if l.count("|") >= 3 else ""
        cell = re.sub(r"[*`]", "", cell).strip()
        # 충족 = 대체표기가 아니면서, 서술형(20자+) 이거나 정량형("SOM x 0.60", "±40% 시 $23~$54/mL")
        if STUB.match(cell) or not (len(cell) >= 20 or re.search(r"\d", cell)):
            nosens.append(l)
    add("EXTRA", len(body) >= 8, "assumptions.md 가정 %d건 (최소 8)" % len(body))
    add("EXTRA", not nosens, "민감도 영향 미기재 가정 %d건" % len(nosens))
    for l in nosens[:8]:
        res["details"]["EXTRA"].append(("FAIL", "  " + l.strip()[:120]))

    g = rd(os.path.join(DOCS, "gaps.md"))
    blocks = re.split(r"\n(?=#{2,3}\s)", g)
    items = [b for b in blocks if re.match(r"#{2,3}\s*\[?(GAP|갭|G-)", b, re.I) or "GAP-" in b[:80]]
    incomplete = []
    for b in items:
        ok = (len(re.findall(r"(쿼리|query)", b, re.I)) >= 1
              and len(re.findall(r"(소스|source|URL|https?://)", b, re.I)) >= 1
              and re.search(r"(판단|부재|없는|존재하지)", b)
              and re.search(r"(대체\s*추정|오차|범위|±|\+/-)", b))
        if not ok:
            incomplete.append(b.split("\n")[0][:90])
    add("EXTRA", not incomplete, "gaps.md 4요소 미충족 항목 %d건" % len(incomplete))
    for l in incomplete[:8]:
        res["details"]["EXTRA"].append(("FAIL", "  " + l))

    for rel in ("model/market_model.py", "model/cogs_model.py"):
        p = os.path.join(ROOT, rel)
        if os.path.exists(p):
            import subprocess
            try:
                r = subprocess.run([sys.executable, p], capture_output=True,
                                   timeout=120, cwd=ROOT)
                add("EXTRA", r.returncode == 0, "%s 실행 %s%s" % (
                    rel, "성공" if r.returncode == 0 else "실패",
                    "" if r.returncode == 0 else " :: " + r.stderr.decode("utf-8", "ignore")[-300:]))
            except Exception as e:  # noqa: BLE001
                add("EXTRA", False, "%s 실행 예외: %s" % (rel, e))


def main():
    g1(); g2(); g3(); g4(); g5(); g6(); g7(); extra()

    names = {"G1": "산출물 존재", "G2": "근거 무결성", "G3": "금지표현",
             "G4": "숫자 재현성", "G5": "삼각측량", "G6": "신뢰도 분포",
             "G7": "판정 존재", "EXTRA": "추가검사"}
    order = ["G1", "G2", "G3", "G4", "G5", "G6", "G7", "EXTRA"]

    print("=" * 74)
    print("OSVX 품질 게이트 결과")
    print("=" * 74)
    failed = 0
    for g in order:
        st = res["gates"].get(g, "SKIP")
        if st == "FAIL":
            failed += 1
        print("\n[%s] %-12s : %s" % (g, names[g], st))
        for s, m in res["details"][g]:
            if s == "FAIL":
                print("   ✗ %s" % m)
        oks = [m for s, m in res["details"][g] if s == "PASS"]
        if oks:
            print("   ✓ %d개 항목 통과" % len(oks))

    print("\n" + "=" * 74)
    if failed:
        print("게이트 실패: %d / %d — R6 에 따라 '완료' 선언 금지" % (failed, len(order)))
    else:
        print("전 게이트 통과 (%d/%d)" % (len(order), len(order)))
    print("=" * 74)

    if "--json" in sys.argv:
        with open(os.path.join(ROOT, "tools", "validate_result.json"), "w", encoding="utf-8") as f:
            json.dump({"gates": dict(res["gates"]),
                       "details": {k: v for k, v in res["details"].items()}},
                      f, ensure_ascii=False, indent=2)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
