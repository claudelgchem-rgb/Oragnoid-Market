#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSVX Agent O — evidence_ui.html 생성기 (R2 Evidence-Chip Rule)
evidence/evidence.jsonl -> evidence/evidence_ui.html
외부 CDN 의존 없는 단일 파일 HTML. 검색창 + Tier 필터 + 신뢰도 필터 + 근거칩 펼침.
"""
import json
import os
import sys
import html
import re
import collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVDIR = os.path.join(ROOT, "evidence")
DOCS = os.path.join(ROOT, "docs")
SRC = os.path.join(EVDIR, "evidence.jsonl")
OUT = os.path.join(EVDIR, "evidence_ui.html")

EID = re.compile(r"\[(E-\d{3}(?:-R)?)\]")


def load():
    recs = []
    with open(SRC, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                recs.append(json.loads(line))
    return recs


def usage_map():
    """각 근거가 어느 문서에서 인용되었는지 역인덱스."""
    used = collections.defaultdict(set)
    for d, _, files in os.walk(ROOT):
        if os.sep + ".git" in d:
            continue
        for fn in files:
            if not fn.endswith((".md", ".csv", ".py")):
                continue
            p = os.path.join(d, fn)
            try:
                with open(p, "r", encoding="utf-8", errors="ignore") as f:
                    txt = f.read()
            except OSError:
                continue
            rel = os.path.relpath(p, ROOT)
            for m in EID.findall(txt):
                used[m].add(rel)
    return used


CSS = """
:root{--bg:#f7f8fa;--card:#fff;--ink:#14181f;--mute:#5d6673;--line:#e2e6ec;--accent:#1f6feb;
--t1:#0f7b3f;--t1b:#e3f5ea;--t2:#8a6100;--t2b:#fdf3dc;--t3:#98461f;--t3b:#fdeae0;
--hi:#0f7b3f;--hib:#e3f5ea;--mid:#8a6100;--midb:#fdf3dc;--lo:#b3261e;--lob:#fdeaea;--rej:#b3261e;}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0f1216;--card:#171c22;--ink:#e6eaf0;
--mute:#9aa4b2;--line:#2a323c;--accent:#589bff;--t1b:#12301f;--t1:#6ee7a0;--t2b:#332a10;--t2:#f0c96a;
--t3b:#3a2015;--t3:#f5a480;--hib:#12301f;--hi:#6ee7a0;--midb:#332a10;--mid:#f0c96a;--lob:#3a1a1a;--lo:#ff8a80;}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans KR","Malgun Gothic",sans-serif;}
.wrap{max-width:1180px;margin:0 auto;padding:28px 20px 80px}
h1{font-size:24px;margin:0 0 4px} .sub{color:var(--mute);font-size:13px;margin-bottom:22px}
.stats{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:20px}
.stat{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 14px;min-width:104px}
.stat b{display:block;font-size:20px;line-height:1.2}
.stat span{font-size:11px;color:var(--mute);text-transform:uppercase;letter-spacing:.4px}
.controls{position:sticky;top:0;z-index:5;background:var(--bg);padding:12px 0 14px;border-bottom:1px solid var(--line);margin-bottom:16px}
#q{width:100%;padding:11px 13px;font-size:15px;border:1px solid var(--line);border-radius:9px;
background:var(--card);color:var(--ink)}
.filters{display:flex;flex-wrap:wrap;gap:14px;margin-top:11px;align-items:center}
.fg{display:flex;gap:6px;align-items:center;flex-wrap:wrap}
.fg>em{font-style:normal;font-size:11px;color:var(--mute);text-transform:uppercase;letter-spacing:.4px;margin-right:2px}
.chip{cursor:pointer;user-select:none;border:1px solid var(--line);background:var(--card);color:var(--mute);
border-radius:999px;padding:4px 11px;font-size:12.5px}
.chip.on{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:600}
.count{color:var(--mute);font-size:12.5px;margin-left:auto}
.ev{background:var(--card);border:1px solid var(--line);border-radius:11px;margin-bottom:9px;overflow:hidden}
.ev.rej{border-color:var(--rej);border-left-width:4px}
.hd{display:flex;gap:11px;align-items:flex-start;padding:12px 14px;cursor:pointer}
.hd:hover{background:rgba(127,127,127,.05)}
.eid{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12.5px;font-weight:700;
color:var(--accent);white-space:nowrap;padding-top:1px}
.claim{flex:1;min-width:0}
.claim .val{color:var(--mute);font-size:12.5px;margin-top:2px}
.tags{display:flex;gap:5px;flex-wrap:wrap;justify-content:flex-end}
.tag{font-size:10.5px;font-weight:700;padding:2px 7px;border-radius:5px;white-space:nowrap}
.T1{background:var(--t1b);color:var(--t1)} .T2{background:var(--t2b);color:var(--t2)} .T3{background:var(--t3b);color:var(--t3)}
.c-hi{background:var(--hib);color:var(--hi)} .c-mid{background:var(--midb);color:var(--mid)} .c-lo{background:var(--lob);color:var(--lo)}
.tag.rejt{background:var(--lob);color:var(--rej)}
.bd{display:none;padding:0 14px 14px 14px;border-top:1px solid var(--line);font-size:13.5px}
.ev.open .bd{display:block}
.row{display:flex;gap:10px;padding:5px 0;border-bottom:1px dashed var(--line)}
.row:last-child{border-bottom:0}
.k{width:110px;flex:0 0 110px;color:var(--mute);font-size:12px;padding-top:1px}
.v{flex:1;min-width:0;word-break:break-word}
a{color:var(--accent)}
.none{text-align:center;color:var(--mute);padding:44px 0}
.legend{font-size:12px;color:var(--mute);margin-top:26px;padding-top:14px;border-top:1px solid var(--line)}
"""

JS = """
var EV=document.querySelectorAll('.ev');
var q=document.getElementById('q');
var state={tier:new Set(),conf:new Set(),ag:new Set(),rej:false};
function apply(){
  var s=q.value.trim().toLowerCase(), n=0;
  EV.forEach(function(e){
    var ok=true;
    if(s && e.dataset.search.indexOf(s)<0) ok=false;
    if(ok && state.tier.size && !state.tier.has(e.dataset.tier)) ok=false;
    if(ok && state.conf.size && !state.conf.has(e.dataset.conf)) ok=false;
    if(ok && state.ag.size && !state.ag.has(e.dataset.ag)) ok=false;
    if(ok && state.rej && e.dataset.rej!=='1') ok=false;
    e.style.display=ok?'':'none'; if(ok)n++;
  });
  document.getElementById('cnt').textContent=n+' / '+EV.length+' 건';
  document.getElementById('none').style.display=n?'none':'block';
}
document.querySelectorAll('.chip').forEach(function(c){
  c.addEventListener('click',function(){
    var g=c.dataset.g,v=c.dataset.v;
    if(g==='rej'){state.rej=!state.rej;c.classList.toggle('on');}
    else{var S=state[g];if(S.has(v)){S.delete(v);c.classList.remove('on');}else{S.add(v);c.classList.add('on');}}
    apply();
  });
});
q.addEventListener('input',apply);
document.querySelectorAll('.hd').forEach(function(h){
  h.addEventListener('click',function(){h.parentNode.classList.toggle('open');});
});
document.addEventListener('keydown',function(e){
  if(e.key==='/'&&document.activeElement!==q){e.preventDefault();q.focus();}
  if(e.key==='Escape'){q.value='';apply();q.blur();}
});
apply();
"""


def cclass(c):
    return {"상": "c-hi", "중": "c-mid", "하": "c-lo"}.get(c, "c-mid")


def main():
    if not os.path.exists(SRC):
        print("evidence.jsonl 없음 — merge_evidence.py 를 먼저 실행하라.", file=sys.stderr)
        return 1
    recs = load()
    used = usage_map()

    tiers = collections.Counter(r.get("tier", "T3") for r in recs)
    confs = collections.Counter(r.get("confidence", "하") for r in recs)
    ags = sorted({r.get("owner_agent", "?") for r in recs})
    nrej = sum(1 for r in recs if r.get("rejected"))
    t1p = 100.0 * tiers.get("T1", 0) / len(recs) if recs else 0
    lop = 100.0 * confs.get("하", 0) / len(recs) if recs else 0

    parts = []
    for r in recs:
        rid = r["id"]
        tier = r.get("tier", "T3")
        conf = r.get("confidence", "하")
        ag = r.get("owner_agent", "?")
        rej = "1" if r.get("rejected") else "0"
        url = r.get("url", "")
        blob = " ".join(str(r.get(k, "")) for k in
                        ("id", "claim", "value", "unit", "source_title", "publisher",
                         "url", "source_type", "note")).lower()
        rows = []

        def row(k, v, raw=False):
            if v in (None, "", "(미기재)"):
                return
            rows.append('<div class="row"><div class="k">%s</div><div class="v">%s</div></div>'
                        % (html.escape(k), v if raw else html.escape(str(v))))

        val = r.get("value", "")
        unit = r.get("unit", "")
        row("값", ("%s %s" % (val, unit)).strip())
        row("출처 제목", r.get("source_title", ""))
        row("발행처", r.get("publisher", ""))
        if url and url != "internal:calc":
            row("URL", '<a href="%s" target="_blank" rel="noopener">%s</a>'
                % (html.escape(url, quote=True), html.escape(url)), raw=True)
        else:
            row("URL", "내부 계산 (원자료 URL 없음)")
        row("접근일", r.get("access_date", ""))
        row("소스 유형", r.get("source_type", ""))
        row("Tier", "%s / 신뢰도 %s%s" % (tier, conf, " (Agent R 재판정)" if r.get("verified_by") == "R" else " (미검증 초안)"))
        row("접근 상태", r.get("access_status", "ok"))
        row("생성 에이전트", "Agent " + ag)
        if r.get("r_reason"):
            row("R 판정 사유", r["r_reason"])
        if r.get("note"):
            row("비고", r["note"])
        if r.get("rejected"):
            row("격리 사유", r.get("rejection_reason", "사유 미기재"))
        u = sorted(used.get(rid, []))
        row("인용 위치", ", ".join(u) if u else "본문 인용 없음")

        tags = ['<span class="tag %s">%s</span>' % (tier, tier),
                '<span class="tag %s">신뢰도 %s</span>' % (cclass(conf), conf),
                '<span class="tag">%s</span>' % html.escape(ag)]
        if r.get("rejected"):
            tags.append('<span class="tag rejt">격리</span>')

        valline = ("%s %s" % (val, unit)).strip()
        parts.append(
            '<div class="ev%s" data-tier="%s" data-conf="%s" data-ag="%s" data-rej="%s" data-search="%s">'
            '<div class="hd"><div class="eid">[%s]</div>'
            '<div class="claim"><div>%s</div>%s</div>'
            '<div class="tags">%s</div></div>'
            '<div class="bd">%s</div></div>'
            % (" rej" if r.get("rejected") else "", tier, conf, html.escape(ag, quote=True), rej,
               html.escape(blob, quote=True), html.escape(rid),
               html.escape(r.get("claim", "")),
               ('<div class="val">%s</div>' % html.escape(valline)) if valline else "",
               "".join(tags), "".join(rows)))

    tchips = "".join('<span class="chip" data-g="tier" data-v="%s">%s (%d)</span>' % (t, t, tiers.get(t, 0))
                     for t in ("T1", "T2", "T3"))
    cchips = "".join('<span class="chip" data-g="conf" data-v="%s">%s (%d)</span>' % (c, c, confs.get(c, 0))
                     for c in ("상", "중", "하"))
    achips = "".join('<span class="chip" data-g="ag" data-v="%s">%s</span>' % (a, a) for a in ags)

    doc = """<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>OSVX 근거 대장 (Evidence Ledger)</title><style>%s</style></head><body>
<div class="wrap">
<h1>OSVX 근거 대장 — Evidence Ledger</h1>
<div class="sub">콜라겐 기반 Defined Organoid Matrix 사업성 분석 · 근거칩을 클릭하면 원문 URL·출처·Tier·신뢰도가 펼쳐집니다 ·
<code>/</code> 검색 포커스, <code>Esc</code> 초기화</div>
<div class="stats">
<div class="stat"><b>%d</b><span>총 근거</span></div>
<div class="stat"><b>%d</b><span>T1 1차문서</span></div>
<div class="stat"><b>%.0f%%</b><span>T1 비중</span></div>
<div class="stat"><b>%.0f%%</b><span>신뢰도 하 비중</span></div>
<div class="stat"><b>%d</b><span>R 격리</span></div>
</div>
<div class="controls">
<input id="q" type="search" placeholder="검색: 주장 / 수치 / 출처 / URL / 발행처 …" autocomplete="off">
<div class="filters">
<div class="fg"><em>Tier</em>%s</div>
<div class="fg"><em>신뢰도</em>%s</div>
<div class="fg"><em>에이전트</em>%s</div>
<div class="fg"><span class="chip" data-g="rej" data-v="1">격리만</span></div>
<div class="count" id="cnt"></div>
</div></div>
%s
<div class="none" id="none">조건에 맞는 근거가 없습니다.</div>
<div class="legend">
<b>Tier 정의</b> — T1: 1차 문서(규제기관 원문, 상장사 공시, 특허 원문, 제조사 공식 카탈로그·CoA, 피어리뷰 논문) ·
T2: 2차(시장보고서, 업계지, 애널리스트, 유통사 가격) · T3: 3차(커뮤니티, 블로그, 내부 삼각추정).<br>
<b>신뢰도</b> — Agent R 이 출처 독립성 × 방법론 공개 × 최신성 × 재현가능성 × 이해상충 5축으로 독립 재판정 (R3 Independent Verification Rule).
"(미검증 초안)" 표기는 R 의 실검증 표본에 포함되지 않아 생성 에이전트의 초안 등급이 유지된 레코드입니다.<br>
<b>격리</b> — URL 접근 불가 또는 원문에 주장이 존재하지 않아 evidence_rejected.jsonl 로 분리된 레코드. 본문 인용에서 제외 대상.
</div>
</div><script>%s</script></body></html>""" % (
        CSS, len(recs), tiers.get("T1", 0), t1p, lop, nrej,
        tchips, cchips, achips, "\n".join(parts), JS)

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(doc)
    print("생성: %s (%d 레코드, %.1f KB)" % (OUT, len(recs), len(doc) / 1024.0))
    print("Tier: %s | 신뢰도: %s | 격리: %d" % (dict(tiers), dict(confs), nrej))
    return 0


if __name__ == "__main__":
    sys.exit(main())
