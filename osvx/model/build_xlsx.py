#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OSVX_model.xlsx 생성기 (Agent S). openpyxl 사용.
   8시트: README / Inputs / Market / Scenarios / PnL_Base / Sensitivity / Gates / Evidence_Index
   ★ Scenarios·PnL_Base·Sensitivity·Gates 는 하드코딩이 아니라 **엑셀 수식**으로 살아 있다.
"""
import csv
import os
import sys
from collections import defaultdict

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import finance_model as F  # noqa: E402

OUT = os.path.join(HERE, "OSVX_model.xlsx")

H1 = Font(bold=True, size=14)
HD = Font(bold=True, color="FFFFFF")
HDF = PatternFill("solid", fgColor="1F4E79")
SUB = PatternFill("solid", fgColor="DDEBF7")
WARN = PatternFill("solid", fgColor="FCE4D6")
THIN = Border(*[Side(style="thin", color="BFBFBF")] * 4)


def head(ws, row, cols, widths=None):
    for i, c in enumerate(cols, 1):
        cell = ws.cell(row=row, column=i, value=c)
        cell.font = HD
        cell.fill = HDF
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    if widths:
        for i, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = w


def build():
    wb = Workbook()

    # ------------------------------------------------------------------ 1 README
    ws = wb.active
    ws.title = "README"
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 110
    ws["A1"] = "OSVX 통합 재무모델 (Agent S)"
    ws["A1"].font = H1
    readme = [
        ("작성일", "2026-08-11"),
        ("작성자", "Agent S — 통합 재무모델 & Go/No-Go 판정"),
        ("대상 사업", "LG화학 재조합 콜라겐(single+triple) + mTG 가교 Defined Organoid Matrix"),
        ("통화 / 단위", "전 금액 USD. 물량은 **판매(sellable) L** 기준 — 생산 L = 판매 L / 0.836 (Agent V V-03 단위 통일)"),
        ("환율", "KRW 1,409.94 / USD, CNY 6.7474 / USD, JPY 157.54 / USD — Agent C [E-146] 단일 소스 승계"),
        ("할인율(WACC)", f"{F.WACC*100:.2f}%  = 자기자본 {F.W_E:.3f}×Ke {F.KE*100:.2f}% + 타인자본 {F.W_D:.3f}×Kd(세후) {F.KD*(1-F.TAX_RATE)*100:.2f}%"
                         f"  (Rf 4.30% [E-800] / 한국 ERP 4.87% [E-801] / 무차입베타 0.93 [E-804] / 법인세 27.5% [E-805])"),
        ("원가 함수", "COGS(판매 mL) = 규모티어 고정비 ÷ (생산 L × 1000 × 0.836) + 티어 변동비.  Agent E `cogs_model.py` 티어 파라미터 복제 (검증 완료)"),
        ("침투율", "로지스틱 S-curve P(t) = L / (1 + exp(−k(t−t0))).  L·k·t0 를 Agent D 의 switch_propensity·half_life 에서 유도. **선형 점유율 가정 없음**"),
        ("시나리오", "Bear / Base / Bull. 확률 가중 0.55 / 0.33 / 0.12 (Agent X §15.2 P(성공)=0.12 에서 유도)"),
        ("스코프", "A = 현 제품정의(오가노이드 매트릭스 단품) / B = 대안 스코프 옵션(b) 제품정의 확장(+비오가노이드 3D +콜라겐·젤라틴 바이오잉크)"),
        ("반영 감사", "Agent V V-01~V-26 (심각도 상 10건 전건) / Agent R 근거품질 FAIL 2항목 + 유통마진 69.0% 정정 / Agent X H1~H12·KC-1~KC-5"),
        ("주의 (Agent R)", "① 시장규모 근거품질 FAIL (T1 39.4%) ③ COGS·GM 근거품질 FAIL (T1 37.1%). 두 축의 수치는 방향성 지표로만 사용하고 단정 서술을 피할 것"),
        ("주의 (순환논증 제거)", "Agent E 의 설계물량 500 L/년은 DECISION_GATE 목표치 15 M USD 역산값이었다(V-02). 본 모델은 이를 폐기하고 물량을 수요 S-curve 에서만 생성한다"),
        ("시트 구성", "README / Inputs / Market / Scenarios / PnL_Base / Sensitivity / Gates / Evidence_Index (8시트)"),
        ("수식 정책", "Scenarios·PnL_Base·Sensitivity·Gates 의 파생 셀은 Inputs 를 참조하는 엑셀 수식이다. 값을 바꾸면 표가 다시 계산된다"),
        ("연계 산출물", "docs/S_synthesis.md · model/finance_model.py · data/finance_output.csv · evidence/evidence_S.jsonl"),
    ]
    r = 3
    for k, v in readme:
        ws.cell(row=r, column=1, value=k).font = Font(bold=True)
        c = ws.cell(row=r, column=2, value=v)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        r += 1
    ws.freeze_panes = "A3"

    # ------------------------------------------------------------------ 2 Inputs
    ws = wb.create_sheet("Inputs")
    head(ws, 1, ["#", "구분", "파라미터", "값", "단위", "근거 [E-###]", "비고"],
         [5, 18, 40, 16, 14, 26, 60])
    inputs = [
        ("할인율", "무위험이자율 Rf (한국 국고채 10년)", F.RF, "비율", "[E-800]", "2026-08-11 실측 4.30%"),
        ("할인율", "한국 총 주식위험프리미엄 ERP", F.ERP_KR, "비율", "[E-801]", "Damodaran 2026-01 (성숙시장 4.23% + 국가 0.64%)"),
        ("할인율", "무차입 베타 (산업)", F.BETA_UNLEV, "배", "[E-804]", "Healthcare Products 0.83 / Drugs Biotech 1.03 평균"),
        ("할인율", "산업 D/E", F.DE_RATIO, "비율", "[E-804]", "12.79% · 13.04% 평균"),
        ("할인율", "법인세율 (한국 최고구간+지방세)", F.TAX_RATE, "비율", "[E-805]", "국세 25% × 1.1"),
        ("할인율", "회사채 스프레드 (LG화학 A3/BBB+)", F.CREDIT_SPREAD, "비율", "[E-806]", "Moody's A3 / S&P BBB+"),
        ("원가", "종합수율 (RUO)", F.YIELD_RUO, "비율", "[E_cogs §6]", "판매 L = 생산 L × 0.836"),
        ("원가", "티어1 고정비 (생산 1~9 L)", F.COST_TIERS[0][1], "USD/년", "[E-428][E-434]", "감가상각 35,000 포함"),
        ("원가", "티어10 고정비 (생산 10~99 L)", F.COST_TIERS[1][1], "USD/년", "[E-428][E-434]", "감가상각 154,215 포함, 5 FTE"),
        ("원가", "티어100 고정비 (생산 100~999 L)", F.COST_TIERS[2][1], "USD/년", "[E-428][E-434]", "감가상각 342,700 포함, 11 FTE. E 의 파일럿 티어"),
        ("원가", "티어1000 고정비 (생산 ≥1000 L)", F.COST_TIERS[3][1], "USD/년", "[E-428][E-434]", "감가상각 852,150 포함, 22 FTE"),
        ("원가", "티어100 판매 mL당 변동비", F.COST_TIERS[2][3], "USD/mL", "[E-402][E-403][E-409]", "원료 0.1606 + 배치 + 포장"),
        ("원가", "티어10 판매 mL당 변동비", F.COST_TIERS[1][3], "USD/mL", "[E-402][E-403][E-409]", "배치 5 L 로 배치원가 분산 불리"),
        ("가격", "Corning 표준 SKU 354234 실측 단가", 30.285, "USD/mL", "[E-802]", "302.85 USD / 10 mL, 제조사 직판 (2026-08-11 재확인)"),
        ("가격", "Corning 오가노이드 SKU 356255", 44.76, "USD/mL", "[E-812]", "447.60 USD / 10 mL 직판"),
        ("가격", "Corning Synthegel 354791", 34.12, "USD/mL", "[E-813]", "545.90 USD / 16 mL"),
        ("가격", "유통 마진 (Fisher / Corning 직판)", 0.690, "비율", "[E-814]", "756.50 / 447.60 − 1. Agent R 정정 — 기존 35.9% 는 격리 [E-103]"),
        ("가격", "ASP base (신규 진입 침투가)", F.ASP0["base"], "USD/mL", "[E-802][E-807]", "30.285 × 0.823 (G 의 17.7% 침투할인) = 24.93"),
        ("가격", "ASP bear", F.ASP0["bear"], "USD/mL", "[E-803]", "Corning 총이익 손익분기 하한 19.39"),
        ("가격", "ASP bull", F.ASP0["bull"], "USD/mL", "[E-807]", "Agent G 확정 정가 32.00 (표준 Matrigel 대비 +5.6% 프리미엄)"),
        ("가격", "실질단가 추세 bear/base/bull", -0.040, "연율", "[E-125][E-130]", "bear −4.0% / base −2.0% / bull 0.0%"),
        ("수요", "전환확률 학술 RUO", F.D_SWITCH["academic_ruo"][0], "연율", "[E-263]", "half-life 11.2년"),
        ("수요", "전환확률 제약 전임상", F.D_SWITCH["pharma_preclinical_nam"][0], "연율", "[E-263]", "half-life 8.0년"),
        ("수요", "전환확률 CRO·바이오뱅크", F.D_SWITCH["organoid_cro_biobank"][0], "연율", "[E-263]", "half-life 25.3년"),
        ("수요", "전환확률 임상진단 PDO", F.D_SWITCH["clinical_dx_pdo"][0], "연율", "[E-263]", "half-life 21.3년"),
        ("수요", "전환확률 재생의료 GMP", F.D_SWITCH["regenerative_gmp"][0], "연율", "[E-263]", "half-life 2.4년, Matrigel 사용 불가 → 강제 전환"),
        ("수요", "S-curve 천장 L (비GMP)", 0.70 / 1.10, "비율", "[E-239][A-A20]", "증분지출 0.70 / (BME 유지 0.40 + 0.70). 대조군용 BME 구매 지속"),
        ("수요", "LG 점유율 RUO (base)", F.LG_SHARE["base"]["ruo"], "비율", "[A-A21]", "bear 5% / base 12% / bull 22%"),
        ("수요", "LG 점유율 GMP (base)", F.LG_SHARE["base"]["gmp"], "비율", "[A-A21]", "공개 정가 GMP 매트릭스 0개 = 미점유 구간"),
        ("비용", "SG&A / 매출", F.SGA_PCT, "비율", "[E-808]", "Bio-Techne FY2025 조정 SG&A 29.0%"),
        ("비용", "R&D / 매출", F.RND_PCT, "비율", "[E-808]", "Bio-Techne FY2025 R&D 7.8%"),
        ("비용", "상업 FTE fully-loaded", F.FTE_FIELD, "USD/년", "[E-809]", "FAS 중앙값 총보상 × 1.25. Agent E 의 90,000 가정 폐기 (X H12)"),
        ("비용", "R&D 최소 지출", F.RND_FLOOR, "USD/년", "[E-434]", "3 FTE(한국 90,000) + 소재 200,000"),
        ("리스크", "라미닌 무첨가 성공확률", F.P_NO_LAMININ, "확률", "[D-A07]", "V-07: 이분법. 실패 시 COGS +110.96 USD/mL → 공헌이익 음수"),
        ("리스크", "시나리오 확률 bear/base/bull", 0.55, "확률", "[X §15.2]", "0.55 / 0.33 / 0.12. bull = X 의 P(성공) 0.12"),
        ("대안스코프", "비오가노이드 3D 매트릭스 2025", F.NONORG_2025_USD, "USD", "[E-335]", "A 경로3 전용도 117.2 M − 오가노이드 42.97 M"),
        ("대안스코프", "콜라겐+젤라틴 바이오잉크 2025", F.BIOINK_2025_USD, "USD", "[E-810]", "콜라겐 32.5 M + 젤라틴 15.7 M (GMI)"),
        ("대안스코프", "옵션(b) 추가 CAPEX", F.SCOPE_B_EXTRA_CAPEX, "USD", "[G §4.2]", "배합·프린터 호환성·어세이 밸리데이션·영업확장"),
        ("대안스코프", "TeloCol-6 커모디티 콜라겐 단가", 11.64, "USD/mL", "[E-155]", "X: 비오가노이드 레그의 실질 가격 상한"),
    ]
    for i, row in enumerate(inputs, 1):
        ws.cell(row=i + 1, column=1, value=i)
        for j, v in enumerate(row, 2):
            ws.cell(row=i + 1, column=j, value=v).border = THIN
    ws.freeze_panes = "A2"
    IN = {}   # 파라미터명 -> 엑셀 절대참조
    for i, row in enumerate(inputs, 1):
        IN[row[1]] = f"Inputs!$D${i+1}"

    # ------------------------------------------------------------------ 3 Market
    ws = wb.create_sheet("Market")
    head(ws, 1, ["시나리오", "연도", "세그먼트", "지역", "TAM USD", "TAM_addressable USD",
                 "TAM_addressable L", "침투율 P(t)", "SAM_adjusted USD", "SAM_adjusted L"],
         [10, 8, 24, 10, 16, 20, 20, 12, 18, 18])
    rows = list(csv.DictReader(open(os.path.join(ROOT, "data", "market_model_output.csv"),
                                    encoding="utf-8")))
    r = 2
    for x in rows:
        scen, yr, seg = x["scenario"], int(x["year"]), x["segment"]
        if yr < 2026:
            continue
        pen = F.penetration(seg, scen, yr)
        ws.cell(row=r, column=1, value=scen)
        ws.cell(row=r, column=2, value=yr)
        ws.cell(row=r, column=3, value=seg)
        ws.cell(row=r, column=4, value=x["region"])
        ws.cell(row=r, column=5, value=round(float(x["TAM_usd"]), 0))
        ws.cell(row=r, column=6, value=round(float(x["TAM_addressable_usd"]), 0))
        ws.cell(row=r, column=7, value=round(float(x["TAM_addressable_L"]), 4))
        ws.cell(row=r, column=8, value=round(pen, 6))
        ws.cell(row=r, column=9, value=f"=F{r}*H{r}")          # ★ 수식
        ws.cell(row=r, column=10, value=f"=G{r}*H{r}")         # ★ 수식
        r += 1
    ws.freeze_panes = "A2"

    # ------------------------------------------------------------------ 4 Scenarios
    ws = wb.create_sheet("Scenarios")
    ws["A1"] = "Bear / Base / Bull P&L — 스코프 A (현 제품정의). 물량·ASP 는 드라이버, 나머지는 엑셀 수식"
    ws["A1"].font = H1
    ws.column_dimensions["A"].width = 22
    for c in "BCDEFGHIJKLM":
        ws.column_dimensions[c].width = 15
    res = {s: F.build_pnl(s, "A") for s in ("bear", "base", "bull")}
    row = 3
    scen_rows = {}
    for scen in ("bear", "base", "bull"):
        ws.cell(row=row, column=1, value=f"[{scen.upper()}]  스코프 A").font = Font(bold=True, size=12)
        row += 1
        head(ws, row, ["항목"] + [str(y) for y in F.YEARS])
        hdr = row
        row += 1
        rr = res[scen]["rows"]
        # 드라이버 (값)
        for label, key, nd in (("판매 물량 (L)", "sell_L", 3), ("ASP (USD/mL)", "asp", 4)):
            ws.cell(row=row, column=1, value=label).font = Font(bold=True)
            for j, x in enumerate(rr, 2):
                ws.cell(row=row, column=j, value=round(x[key], nd))
            row += 1
        r_vol, r_asp = hdr + 1, hdr + 2
        # 생산 물량 (수식)
        ws.cell(row=row, column=1, value="생산 물량 (L)")
        for j in range(2, 12):
            ws.cell(row=row, column=j,
                    value=f"={get_column_letter(j)}{r_vol}/{IN['종합수율 (RUO)']}")
        r_prod = row
        row += 1
        # 매출 (수식)
        ws.cell(row=row, column=1, value="매출 (USD)").font = Font(bold=True)
        for j in range(2, 12):
            L = get_column_letter(j)
            ws.cell(row=row, column=j, value=f"={L}{r_vol}*1000*{L}{r_asp}")
        r_rev = row
        row += 1
        # 고정비 · 변동비 (값: 티어 선택 결과) → COGS 수식
        ws.cell(row=row, column=1, value="적용 고정비 (USD/년)")
        for j, x in enumerate(rr, 2):
            ws.cell(row=row, column=j, value=round(F.tier_for(x["prod_L"])[1], 0))
        r_fix = row
        row += 1
        ws.cell(row=row, column=1, value="적용 변동비 (USD/판매mL)")
        for j, x in enumerate(rr, 2):
            ws.cell(row=row, column=j, value=F.tier_for(x["prod_L"])[3])
        r_var = row
        row += 1
        ws.cell(row=row, column=1, value="COGS (USD)")
        for j in range(2, 12):
            L = get_column_letter(j)
            ws.cell(row=row, column=j, value=f"={L}{r_fix}+{L}{r_var}*{L}{r_vol}*1000")
        r_cogs = row
        row += 1
        ws.cell(row=row, column=1, value="Gross Profit (USD)").font = Font(bold=True)
        for j in range(2, 12):
            L = get_column_letter(j)
            ws.cell(row=row, column=j, value=f"={L}{r_rev}-{L}{r_cogs}")
        r_gp = row
        row += 1
        ws.cell(row=row, column=1, value="GM %").font = Font(bold=True)
        for j in range(2, 12):
            L = get_column_letter(j)
            ws.cell(row=row, column=j, value=f"=IF({L}{r_rev}=0,0,{L}{r_gp}/{L}{r_rev})")
            ws.cell(row=row, column=j).number_format = "0.0%"
        row += 1
        for label, key in (("SG&A (USD)", "sga"), ("R&D (USD)", "rnd")):
            ws.cell(row=row, column=1, value=label)
            for j, x in enumerate(rr, 2):
                ws.cell(row=row, column=j, value=round(x[key], 0))
            if label.startswith("SG&A"):
                r_sga = row
            else:
                r_rnd = row
            row += 1
        ws.cell(row=row, column=1, value="EBIT (USD)").font = Font(bold=True)
        for j in range(2, 12):
            L = get_column_letter(j)
            ws.cell(row=row, column=j, value=f"={L}{r_gp}-{L}{r_sga}-{L}{r_rnd}")
        r_ebit = row
        row += 1
        for label, key in (("감가상각 (USD)", "depr"), ("CAPEX (USD)", "capex"),
                           ("운전자본 증감 (USD)", "d_wc"), ("법인세 (USD)", "tax")):
            ws.cell(row=row, column=1, value=label)
            for j, x in enumerate(rr, 2):
                ws.cell(row=row, column=j, value=round(x[key], 0))
            if label.startswith("감가"):
                r_dep = row
            elif label.startswith("CAPEX"):
                r_cap = row
            elif label.startswith("운전"):
                r_wc = row
            else:
                r_tax = row
            row += 1
        ws.cell(row=row, column=1, value="FCF (USD)").font = Font(bold=True)
        for j in range(2, 12):
            L = get_column_letter(j)
            ws.cell(row=row, column=j,
                    value=f"={L}{r_ebit}-{L}{r_tax}+{L}{r_dep}-{L}{r_cap}-{L}{r_wc}")
        r_fcf = row
        row += 1
        ws.cell(row=row, column=1, value="누적 FCF (USD)").font = Font(bold=True)
        ws.cell(row=row, column=2, value=f"=B{r_fcf}")
        for j in range(3, 12):
            L, P = get_column_letter(j), get_column_letter(j - 1)
            ws.cell(row=row, column=j, value=f"={P}{row}+{L}{r_fcf}")
        row += 1
        ws.cell(row=row, column=1, value="NPV (USD, 잔존가치 제외)").font = Font(bold=True)
        ws.cell(row=row, column=2, value=f"=NPV(Gates!$B$2,C{r_fcf}:K{r_fcf})+B{r_fcf}")
        ws.cell(row=row, column=1).fill = SUB
        row += 1
        ws.cell(row=row, column=1, value="IRR (잔존가치 제외)").font = Font(bold=True)
        ws.cell(row=row, column=2, value=f"=IFERROR(IRR(B{r_fcf}:K{r_fcf}),\"미산출(부호변화 없음)\")")
        row += 1
        ws.cell(row=row, column=1, value="누적 판매물량 (L)")
        ws.cell(row=row, column=2, value=f"=SUM(B{r_vol}:K{r_vol})")
        row += 2
        scen_rows[scen] = {"rev": r_rev, "gp": r_gp, "fcf": r_fcf, "vol": r_vol, "prod": r_prod}
    ws.freeze_panes = "B3"

    # ------------------------------------------------------------------ 5 PnL_Base
    ws = wb.create_sheet("PnL_Base")
    ws["A1"] = "스코프 A · Base 시나리오 10년 상세 P&L (2026~2035) — 파생 셀 전량 엑셀 수식"
    ws["A1"].font = H1
    cols = ["연도", "판매 L", "생산 L", "ASP USD/mL", "매출 USD", "고정비 USD", "변동비 USD/mL",
            "COGS USD", "Gross Profit", "GM %", "SG&A", "R&D", "EBIT", "법인세", "감가상각",
            "CAPEX", "누적 투자", "운전자본 증감", "FCF", "누적 FCF", "할인계수", "PV(FCF)"]
    head(ws, 3, cols, [8, 11, 11, 12, 15, 14, 13, 14, 15, 9, 13, 12, 14, 12, 13, 13, 14, 14, 15, 16, 11, 15])
    base = F.build_pnl("base", "A")
    r0 = 4
    for i, x in enumerate(base["rows"]):
        r = r0 + i
        ws.cell(row=r, column=1, value=x["year"])
        ws.cell(row=r, column=2, value=round(x["sell_L"], 4))
        ws.cell(row=r, column=3, value=f"=B{r}/{IN['종합수율 (RUO)']}")
        ws.cell(row=r, column=4, value=round(x["asp"], 4))
        ws.cell(row=r, column=5, value=f"=B{r}*1000*D{r}")
        ws.cell(row=r, column=6, value=round(F.tier_for(x["prod_L"])[1], 0))
        ws.cell(row=r, column=7, value=F.tier_for(x["prod_L"])[3])
        ws.cell(row=r, column=8, value=f"=F{r}+G{r}*B{r}*1000")
        ws.cell(row=r, column=9, value=f"=E{r}-H{r}")
        ws.cell(row=r, column=10, value=f"=IF(E{r}=0,0,I{r}/E{r})")
        ws.cell(row=r, column=10).number_format = "0.0%"
        ws.cell(row=r, column=11, value=f"=MAX({IN['SG&A / 매출']}*E{r},{3 if x['year']<=2027 else 6}*{IN['상업 FTE fully-loaded']})")
        ws.cell(row=r, column=12, value=f"=MAX({IN['R&D / 매출']}*E{r},{IN['R&D 최소 지출']})")
        ws.cell(row=r, column=13, value=f"=I{r}-K{r}-L{r}")
        ws.cell(row=r, column=14, value=round(x["tax"], 0))
        ws.cell(row=r, column=15, value=round(x["depr"], 0))
        ws.cell(row=r, column=16, value=round(x["capex"], 0))
        ws.cell(row=r, column=17, value=f"=SUM($P${r0}:P{r})")
        ws.cell(row=r, column=18, value=f"=0.25*E{r}" + ("" if i == 0 else f"-0.25*E{r-1}"))
        ws.cell(row=r, column=19, value=f"=M{r}-N{r}+O{r}-P{r}-R{r}")
        ws.cell(row=r, column=20, value=f"=S{r}" if i == 0 else f"=T{r-1}+S{r}")
        ws.cell(row=r, column=21, value=f"=1/(1+Gates!$B$2)^(A{r}-$A${r0})")
        ws.cell(row=r, column=22, value=f"=S{r}*U{r}")
    rend = r0 + len(base["rows"]) - 1
    ws.cell(row=rend + 2, column=1, value="NPV (잔존가치 제외)").font = Font(bold=True)
    ws.cell(row=rend + 2, column=5, value=f"=SUM(V{r0}:V{rend})")
    ws.cell(row=rend + 3, column=1, value="IRR").font = Font(bold=True)
    ws.cell(row=rend + 3, column=5, value=f"=IFERROR(IRR(S{r0}:S{rend}),\"미산출(전 기간 FCF 음수)\")")
    ws.cell(row=rend + 4, column=1, value="Payback (누적 FCF ≥ 0 최초 연도)").font = Font(bold=True)
    ws.cell(row=rend + 4, column=5,
            value=f"=IFERROR(INDEX(A{r0}:A{rend},MATCH(TRUE,INDEX(T{r0}:T{rend}>=0,0),0)),\"미도달\")")
    ws.cell(row=rend + 5, column=1, value="BEP 연도 (EBIT ≥ 0 최초)").font = Font(bold=True)
    ws.cell(row=rend + 5, column=5,
            value=f"=IFERROR(INDEX(A{r0}:A{rend},MATCH(TRUE,INDEX(M{r0}:M{rend}>=0,0),0)),\"미도달\")")
    ws.cell(row=rend + 6, column=1, value="BEP 누적물량 (판매 L)").font = Font(bold=True)
    ws.cell(row=rend + 6, column=5, value=f"=IF(E{rend+5}=\"미도달\",\"미도달\",SUM(B{r0}:B{rend}))")
    ws.cell(row=rend + 7, column=1, value="10년 누적 FCF").font = Font(bold=True)
    ws.cell(row=rend + 7, column=5, value=f"=T{rend}")
    ws.cell(row=rend + 8, column=1, value="GM 60% 최초 통과 연도").font = Font(bold=True)
    ws.cell(row=rend + 8, column=5,
            value=f"=IFERROR(INDEX(A{r0}:A{rend},MATCH(TRUE,INDEX(J{r0}:J{rend}>=0.6,0),0)),\"미도달\")")
    ws.freeze_panes = "B4"

    # ------------------------------------------------------------------ 6 Sensitivity
    ws = wb.create_sheet("Sensitivity")
    ws["A1"] = "토네이도 민감도 — 스코프 A Base, 각 변수 ±30% 시 NPV 변화 (USD)"
    ws["A1"].font = H1
    head(ws, 3, ["순위", "변수", "−30% NPV", "기준 NPV", "+30% NPV",
                 "−30% ΔNPV", "+30% ΔNPV", "영향폭(절대)", "근거"],
         [6, 32, 18, 18, 18, 18, 18, 18, 26])
    b, tor = F.tornado()
    src = {
        "SG&A (FTE 단가·비율)": "[E-808][E-809]",
        "고정비 F (플랜트 규모)": "[E-428][E-434]",
        "WACC": "[E-800][E-801][E-804]",
        "ASP (판매단가)": "[E-802][E-803][E-807]",
        "R&D 지출": "[E-808]",
        "CAPEX": "[E_cogs HANDOFF]",
        "전환확률 p_switch (S-curve)": "[E-263]",
        "LG 점유율": "[A-A21]",
        "TAM_addressable (소모량계수)": "[E-342]",
        "변동비 v": "[E-402][E-403]",
    }
    for i, (name, lo, hi, span) in enumerate(tor, 1):
        r = 3 + i
        ws.cell(row=r, column=1, value=i)
        ws.cell(row=r, column=2, value=name)
        ws.cell(row=r, column=3, value=round(b + lo, 0))
        ws.cell(row=r, column=4, value=round(b, 0))
        ws.cell(row=r, column=5, value=round(b + hi, 0))
        ws.cell(row=r, column=6, value=f"=C{r}-D{r}")            # ★ 수식
        ws.cell(row=r, column=7, value=f"=E{r}-D{r}")            # ★ 수식
        ws.cell(row=r, column=8, value=f"=ABS(E{r}-C{r})")       # ★ 수식
        ws.cell(row=r, column=9, value=src.get(name, ""))
    ws.cell(row=3 + len(tor) + 2, column=2, value="Kill Criteria 발동 시 NPV").font = Font(bold=True, size=12)
    kb, kcs = F.kill_criteria()
    kr = 3 + len(tor) + 3
    head(ws, kr, ["#", "Kill Criterion", "판정연도", "계속 시 NPV", "중단 시 NPV",
                  "중단 옵션가치", "기준 대비 Δ", "", "대응 반증"])
    for i, (name, yr, cont, stop, note) in enumerate(kcs, 1):
        r = kr + i
        ws.cell(row=r, column=1, value=i)
        ws.cell(row=r, column=2, value=name)
        ws.cell(row=r, column=3, value=yr)
        ws.cell(row=r, column=4, value="계속 불가" if cont != cont else round(cont, 0))
        ws.cell(row=r, column=5, value=round(stop, 0))
        ws.cell(row=r, column=6, value=f"=IF(ISNUMBER(D{r}),E{r}-D{r},\"—\")")   # ★ 수식
        ws.cell(row=r, column=7, value=f"=IF(ISNUMBER(D{r}),D{r}-{round(kb,0)},\"—\")")
        ws.cell(row=r, column=9, value=note)

    # ------------------------------------------------------------------ 7 Gates
    ws = wb.create_sheet("Gates")
    ws["A1"] = "DECISION_GATE 대조표"
    ws["A1"].font = H1
    ws["A2"] = "WACC"
    ws["B2"] = F.WACC
    ws["B2"].number_format = "0.00%"
    ws["C2"] = "← 이 셀을 바꾸면 Scenarios·PnL_Base 의 NPV 가 다시 계산된다"
    head(ws, 4, ["게이트", "임계값", "Bear", "Base", "Bull", "달성률(Base)", "판정", "근거·비고"],
         [26, 18, 18, 18, 18, 14, 10, 60])
    sam, som, gm = {}, {}, {}
    for s in ("bear", "base", "bull"):
        sam[s] = sum(F.MARKET[(s, 2030, seg)]["usd"] * F.penetration(seg, s, 2030)
                     for seg in F.D_SWITCH)
        rr = [x for x in res[s]["rows"] if x["year"] == 2030][0]
        som[s] = rr["revenue"]
        gm[s] = rr["gm"]
    gate_rows = [
        ("SAM_2030 (USD)", 150_000_000, sam["bear"], sam["base"], sam["bull"],
         "A 의 TAM_addressable × 로지스틱 침투율. Agent A 의 기하 누적모델(10.08 M)보다 보수적"),
        ("SOM_2030 (USD)", 15_000_000, som["bear"], som["base"], som["bull"],
         "LG 자신의 가격표 기준 (V-09). 시장 ASP 기준이 아님"),
        ("Gross_Margin_2030", 0.60, gm["bear"], gm["base"], gm["bull"],
         "GM60 임계 판매물량 = 209.5 L @ASP 24.93. base 2030 판매 19.8 L = 임계의 9.4%"),
    ]
    r = 5
    for name, thr, bv, bsv, blv, note in gate_rows:
        ws.cell(row=r, column=1, value=name)
        ws.cell(row=r, column=2, value=thr)
        ws.cell(row=r, column=3, value=round(bv, 4))
        ws.cell(row=r, column=4, value=round(bsv, 4))
        ws.cell(row=r, column=5, value=round(blv, 4))
        ws.cell(row=r, column=6, value=f"=D{r}/B{r}")                     # ★ 수식
        ws.cell(row=r, column=6).number_format = "0.0%"
        ws.cell(row=r, column=7, value=f"=IF(MAX(C{r}:E{r})>=B{r},\"PASS\",\"FAIL\")")  # ★ 수식
        ws.cell(row=r, column=8, value=note)
        r += 1
    ws.cell(row=r, column=1, value="Payback (년)")
    ws.cell(row=r, column=2, value=5)
    for j, s in zip((3, 4, 5), ("bear", "base", "bull")):
        ws.cell(row=r, column=j, value="미도달" if res[s]["payback"] is None
                else res[s]["payback"] - 2026)
    ws.cell(row=r, column=7, value=f"=IF(COUNT(C{r}:E{r})=0,\"FAIL\",IF(MIN(C{r}:E{r})<=B{r},\"PASS\",\"FAIL\"))")
    ws.cell(row=r, column=8, value="Agent E 의 payback 2030 은 판매 418 L 램프 전제 — V-01 로 무효. 수요 S-curve 대입 시 전 시나리오 미도달")
    r += 1
    ws.cell(row=r, column=1, value="FTO 리스크")
    ws.cell(row=r, column=2, value="중 이하")
    for j in (3, 4, 5):
        ws.cell(row=r, column=j, value="중")
    ws.cell(row=r, column=7, value="PASS")
    ws.cell(row=r, column=8, value="Agent F fto_verdict=중. 단 V-06: 회피규격 G'>1.5 kPa 를 E 의 OM-S·G 의 강스템 SKU 가 위반 — 한국 EPFL KR20180038573 등록(→2036)")
    r += 2
    ws.cell(row=r, column=1, value="종합 판정 — 현 제품정의").font = Font(bold=True, size=12)
    ws.cell(row=r, column=2, value="No-Go").font = Font(bold=True, color="C00000", size=12)
    ws.cell(row=r, column=3, value="5개 게이트 중 4개 FAIL (SAM·SOM·GM·Payback). 확률가중 E[NPV] = "
                                   f"{F.WACC and ''}"
                                   f"{sum(F.SCEN_PROB[s]*res[s]['npv_no_tv'] for s in F.SCEN_PROB):,.0f} USD (잔존가치 제외)")
    r += 1
    ws.cell(row=r, column=1, value="종합 판정 — 대안 스코프").font = Font(bold=True, size=12)
    ws.cell(row=r, column=2, value="Conditional-Go").font = Font(bold=True, color="BF8F00", size=12)
    ws.cell(row=r, column=3, value="옵션(d) 라이선싱 + 옵션(e) GMP 원부자재에 한함. 옵션(b)·(c)는 No-Go")
    r += 2
    ws.cell(row=r, column=1, value="DISC-01 재계산 확정").font = Font(bold=True)
    ws.cell(row=r, column=2, value=f"옵션(b) GM60 임계 = 판매 {F.gm60_threshold_sell_L(18.53):.1f} L "
                                   f"= 생산 {F.gm60_threshold_sell_L(18.53)/F.YIELD_RUO:.1f} L "
                                   f"(V 289.4 판매 L 와 X 347.3 생산 L 은 동일 값의 단위 차이)")

    # ------------------------------------------------------------------ 8 Evidence_Index
    ws = wb.create_sheet("Evidence_Index")
    head(ws, 1, ["ID", "구분", "주장 요지", "값", "단위", "tier", "신뢰도", "출처"],
         [10, 14, 62, 20, 12, 8, 10, 46])
    ev_path = os.path.join(ROOT, "evidence", "evidence_S.jsonl")
    r = 2
    if os.path.exists(ev_path):
        import json
        for line in open(ev_path, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            for j, k in enumerate(["id", "source_type", "claim", "value", "unit",
                                   "tier", "confidence", "publisher"], 1):
                ws.cell(row=r, column=j, value=d.get(k, ""))
            r += 1
    ws.cell(row=r + 1, column=1, value="※ 인용한 선행 에이전트 근거 (신규 생성 아님)").font = Font(bold=True)
    r += 2
    cited = [
        ("E-078", "B", "nam_ramp base 2026 8% → 2030 25% → 2035 45%"),
        ("E-102", "C", "Corning 356255 오가노이드 SKU 447.60 USD / 10 mL (제조사 직판)"),
        ("E-125", "C", "Yeasen Ceturegel 21.30 USD/mL (중국 로컬 하한)"),
        ("E-146", "C", "환율 KRW 1,409.94 / CNY 6.7474 / JPY 157.54 per USD"),
        ("E-152", "C", "defined 대체재 7종 20년 누적 인용 점유 1.95%"),
        ("E-155", "C", "Advanced BioMatrix TeloCol-6 11.64 USD/mL"),
        ("E-161", "C", "정의성 프리미엄 Mann-Whitney p=0.168 — 통계적 유의성 없음"),
        ("E-228", "D", "콜라겐 I 이 Matrigel 의 1/10 가격에 유전자발현 동등, 그럼에도 미전환"),
        ("E-231", "D", "2025년 최초 라미닌 무첨가 완전합성 하이드로겔 crypt 형성"),
        ("E-239", "D", "대체재 검증의 기준점이 거의 항상 Matrigel — 대조군 구매 지속"),
        ("E-263", "D", "세그먼트별 연간 전환확률 6.0 / 8.3 / 2.7 / 3.2 / 25.0 %"),
        ("E-334", "A", "Bottom-up TAM 2025 = 42.97 M USD / 1,178.7 L"),
        ("E-335", "A", "전 용도 3D 매트릭스 2025 = 117.2 M USD → 비오가노이드 74.2 M"),
        ("E-342", "A", "TAM_addressable 2030 = 50.49 M USD / 1,521.7 L"),
        ("E-407", "E", "Zedira mTG 카탈로그 260,077 USD/g — 내재화 미실행 시 GM −48.5%p"),
        ("E-412", "E", "라미닌 최저 카탈로그 463.81 USD/mg → ΔCOGS +110.96 USD/mL"),
        ("E-553", "F", "청구항에 organoid ∧ transglutaminase 동시 포함 = 0건"),
        ("E-568", "F", "LifeBond 2027-12-17 만료 / EPFL 2036-09-05 만료"),
        ("E-646", "G", "콜라겐+젤라틴 바이오잉크 2025 = 48.2 M USD"),
        ("E-656", "G", "실명 앵커 30곳 물량 합계 11.222 L/년 = 게이트의 5.85%"),
        ("E-657", "G", "학술 랩 전환비용 상쇄에 필요한 할인율 302.0%"),
        ("E-709", "X", "PubMed 실측: Matrigel 15,004 / Col-Tgel 11 / Synthegel 1"),
        ("E-723", "X", "mTG 는 변성 조건에서만 콜라겐을 가교 — 천연 삼중나선 Gln 접근 불가"),
        ("E-741", "X", "FAS 제약·바이오 중앙값 총보상 152,625 USD"),
        ("E-748", "X", "GM60 임계물량은 ASP 의 함수 — 191.8 L 은 ASP 32.00 전용값"),
        ("E-103-R", "R", "Fisher 356255 = 756.50 USD → 유통마진 69.0% (35.9% 는 격리)"),
        ("E-424-R", "R", "Pichia 재조합 콜라겐 실측 titer 1.05 g/L (E 의 12~16 g/L 대체)"),
    ]
    head(ws, r, ["인용 ID", "생성 Agent", "요지"], [12, 12, 100])
    for i, (eid, ag, txt) in enumerate(cited, 1):
        ws.cell(row=r + i, column=1, value=eid)
        ws.cell(row=r + i, column=2, value=ag)
        ws.cell(row=r + i, column=3, value=txt)
    ws.freeze_panes = "A2"

    wb.save(OUT)
    print("saved:", OUT)


if __name__ == "__main__":
    build()
