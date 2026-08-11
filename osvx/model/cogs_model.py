#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSVX Agent E — COGS / Unit-Economics model
LG Chem "recombinant collagen + mTG crosslinked Defined Organoid Matrix"

표준 라이브러리만 사용. 실행:  python3 model/cogs_model.py
출력: stdout 표  +  data/cogs_output.csv

모든 입력에 근거 ID 를 주석으로 병기한다 (AGENT_RULES R4 Show-Your-Math).
"""

import csv
import math
import os

# ----------------------------------------------------------------------------
# 0. 환율 (Agent C [E-146], Fed H.10 week ending 2026-08-07)
# ----------------------------------------------------------------------------
FX = {
    "USD_per_EUR": 1.1559,   # [E-146]
    "USD_per_GBP": 1.3498,   # [E-146]
    "CNY_per_USD": 6.7474,   # [E-146]
    "JPY_per_USD": 157.54,   # [E-146]
    "KRW_per_USD": 1409.94,  # [E-146]
}

# ----------------------------------------------------------------------------
# 1. 원료 단가 (BOM 입력) — 전부 실측 또는 실측에서 유도
# ----------------------------------------------------------------------------

# --- 1-1. 재조합 콜라겐 -------------------------------------------------------
COLLAGEN_PRICES_USD_PER_G = {
    # 연구용 카탈로그 (상한 참조, 원가 아님)
    "catalog_purecol_bovine":        1800.00,   # [E-400] 540 USD / 0.3 g
    "catalog_purecol_ezgel_bovine":  2742.86,   # [E-406] 480 USD / 0.175 g
    "catalog_humabiologics_human":   8701.67,   # [E-401] 522.10 USD / 0.06 g
    # 산업 벌크 (실제 원가 앵커)
    "bulk_recomb_high_purity":  200000/FX["CNY_per_USD"]/1000,  # [E-402] 20만CNY/kg -> 29.64 USD/g
    "bulk_recomb_current_mkt":   80000/FX["CNY_per_USD"]/1000,  # [E-403]  8만CNY/kg -> 11.86 USD/g
    "bulk_recomb_best_in_class": 10000/FX["CNY_per_USD"]/1000,  # [E-404]  1만CNY/kg ->  1.48 USD/g
}

# LG화학 내부 이전원가 산출 (가정 E-A1) — single 70% + triple-helix 30% 혼합
SINGLE_FRAC = 0.70
TRIPLE_FRAC = 0.30
SCALE_PENALTY = 1.45          # 수백 g/년 규모 vs 중국 공급자 톤 규모 (가정 E-A1)
COLLAGEN_BLEND_USD_PER_G = (
    SINGLE_FRAC * COLLAGEN_PRICES_USD_PER_G["bulk_recomb_current_mkt"]   # [E-403]
    + TRIPLE_FRAC * COLLAGEN_PRICES_USD_PER_G["bulk_recomb_high_purity"] # [E-402]
) * SCALE_PENALTY

# --- 1-2. mTG (microbial transglutaminase) ----------------------------------
MTG_PRICES_USD_PER_G = {
    # 식품급 (순효소 등가 환산)
    "food_grade_1000U_g":  178.00 / (1_000_000/30/1000),   # [E-409] 5.34 USD/g
    "food_grade_activa_rm": 149.99 / (50_000/30/1000),     # [E-408] 89.99 USD/g
    # 연구/제약용 카탈로그
    "zedira_andracon": (3750/500) * 30 * 1000 * FX["USD_per_EUR"],  # [E-407] 260,078 USD/g
}
# LG화학 내부 GMP mTG 이전가격 (가정 E-A3): 200 L 배치, titer 2 g/L, DSP 회수 40%,
# 배치 총원가 USD 80,000 -> 160 g -> 500 USD/g
MTG_INTERNAL_TRANSFER_USD_PER_G = 500.00

# --- 1-3. 재조합 라미닌 ------------------------------------------------------
LAMININ_PRICES_USD_PER_MG = {
    "imatrix511_silk_catalog": 463.81,   # [E-412] 487.00 / 1.05 mg  (조사 최저 카탈로그가)
    "gibco_mouse_ehs":         272.65,   # [E-411] 1 mg vial (단, 마우스 유래 -> defined 소구 불가)
    "corning_rlaminin521":     810.10,   # Agent C [E-144] 81.01 USD / 100 µg
    "biolamina_ln521_est":    1180.00,   # Agent C [E-158] 추정 118.00 USD / 100 µg
    # 벌크/내재화 가정 (가정 E-A5)
    "bulk_10x_discount":        46.38,   # 카탈로그 최저가의 1/10
    "internal_20x_discount":    23.19,   # 카탈로그 최저가의 1/20
}
LAMININ_CONC_MG_PER_ML = 0.20   # [E-410] Nature Protocols 2017: "0.2 mg/ml laminin-111"

# --- 1-4. 기타 BOM ----------------------------------------------------------
BUFFER_USD_PER_ML = 0.0100   # HEPES(세포배양급) + NaCl USP [E-437] + 당·아미노산 안정화제
WATER_USD_PER_ML  = 0.0010   # 정제수/WFI [E-431] 1.2 kWh/L x 0.10 USD/kWh + 감가
VIAL_USD_PER_UNIT = 0.30     # [E-420] RTU 멸균 2R/5R 유리바이알 + 스토퍼 + 씰
LABEL_USD_PER_UNIT= 0.25     # 라벨 + 카톤 + 사용설명서
FILTER_USD_PER_BATCH = 250.0 # [E-438] 0.22 µm 직렬 2단 + 프리필터
CONSUM_USD_PER_BATCH = 550.0 # 튜빙/백/세정제/EM 플레이트
SHIP_USD_PER_SHIPMENT = 95.0 # [E-422] 단열박스 25 + 익일 드라이아이스 특송 70
UNITS_PER_SHIPMENT = 6

# ----------------------------------------------------------------------------
# 2. 배합 설계 (SKU 3종으로 100 Pa ~ 34 kPa 커버 — Agent D [E-260])
# ----------------------------------------------------------------------------
FORMULATIONS = {
    # name        collagen mg/mL, mTG µg/mL, 목표 G' 대역
    "OM-S soft":   {"col_mg_ml": 3.0, "mtg_ug_ml": 30.0,  "stiffness": "100 Pa ~ 1.5 kPa"},
    "OM-M medium": {"col_mg_ml": 5.0, "mtg_ug_ml": 50.0,  "stiffness": "1.5 ~ 12 kPa"},
    "OM-F firm":   {"col_mg_ml": 8.0, "mtg_ug_ml": 100.0, "stiffness": "12 ~ 34 kPa"},
}
BASE_FORM = "OM-M medium"   # 단위경제 기준 배합. mTG 50 µg/mL 은 Agent C [E-164] 실측치

# ----------------------------------------------------------------------------
# 3. 공정 / 수율 / QC
# ----------------------------------------------------------------------------
PROC_LOSS = 0.12          # 홀드업·필터잔류·라인로스 (가정 E-A6)
REJECT_RUO = 0.05         # 로트 불합격률 RUO (가정 E-A6)
REJECT_GMP = 0.08         # 로트 불합격률 GMP
REWORK_RATE = 0.03        # 재작업률

FTE_USD_PER_YEAR = 90_000.0     # [E-434] 완전부담
FTE_USD_PER_HOUR = FTE_USD_PER_YEAR / 2000.0    # 45.00 USD/h
BATCH_LABOR_HOURS = 40.0        # 조제·가교·여과·충전·세정 (가정 E-A7)
FILL_SEC_PER_VIAL = 30.0        # 반자동 충전 (가정 E-A7)

QC_RUO = {   # USD / lot
    "무균 USP<71>":                 300.00,   # [E-415]
    "엔도톡신 LAL USP<85>":          325.00,   # [E-416]
    "마이코플라스마 PCR":             250.00,   # [E-417]
    "SDS-PAGE 순도 (외부요율 2x)":    150.00,   # [E-418] 75 x 2.0
    "LC-MS 조성확인 (외부요율 2x)":   260.00,   # [E-418] 130 x 2.0
    "HPLC 콜라겐 정량":              175.00,   # [E-419]
    "유변학 G'/G'' 3반복":            450.00,   # 가정 E-A8 (3 h x 150 USD/h 코어요율)
    "pH/오스몰/외관/충전량":          120.00,   # 가정 E-A8
    "오가노이드 형성효율 기능시험":    2800.00,   # 가정 E-A8 (2 라인 x 3 반복 + 2 FTE-day)
    "lot release QA 검토":           240.00,   # 4 h x 60 USD/h
}
QC_GMP_ADDER = {   # USD / lot — GMP 증분
    "확장 무균 + 용기밀폐완결성":     1200.00,
    "HCP ELISA + 잔류 DNA":         1500.00,
    "QP release / 배치기록 검토":    2500.00,
    "안정성 프로그램 배분(ICH)":     3000.00,
    "환경모니터링(배치당)":          1800.00,
    "연간제품품질평가 배분":         1000.00,
}

# ----------------------------------------------------------------------------
# 4. 규모별 고정비 구성 (CAPEX 감가 포함)
# ----------------------------------------------------------------------------
# CAPEX (USD)  — [E-428] ISO7 550~850/SF, ISO8 400~650/SF; [E-429] IQ/OQ/PQ 35~140k/장비
CAPEX = {
    "pilot": {
        "ISO8 스위트 1,400 SF @ 525":       735_000,
        "ISO7 코어 750 SF @ 700":           525_000,
        "반자동 충전라인":                   250_000,
        "조제·가교 스키드 50 L":             180_000,
        "TFF/정용여과 스키드":               150_000,
        "QC 장비(레오미터/HPLC/Endosafe 등)": 330_000,
        "냉장·냉동 보관 및 유틸리티":         200_000,
        "IQ/OQ/PQ 6종 @ 60,000":            360_000,
        "QMS·ISO20399/9001 구축":           250_000,
    },
    "commercial_add": {
        "ISO7 증설 1,500 SF @ 700":        1_050_000,
        "자동 충전라인":                     900_000,
        "내재화 발효 500 L + DSP":         1_600_000,
        "QC 장비 증설":                      400_000,
        "IQ/OQ/PQ 8종 @ 60,000":            480_000,
    },
    "gmp_add": {
        "ISO5 충전존 400 SF @ 1,200":        480_000,
        "아이솔레이터/RABS":                  650_000,
        "WFI 시스템":                        900_000,   # [E-431]
        "EMS/BMS 환경모니터링":               350_000,
        "eQMS/eBR (21 CFR Part 11)":         450_000,
        "안정성 챔버·밸리데이션 시험법":        500_000,
        "CQV 밸리데이션":                    800_000,
        "Type II DMF 준비·규제 컨설팅":       400_000,
    },
}
CONTINGENCY = 0.15
DEPREC_YEARS = 10

def capex_total(block):
    base = sum(CAPEX[block].values())
    return base * (1 + CONTINGENCY)

CAPEX_PILOT      = capex_total("pilot")
CAPEX_COMMERCIAL = capex_total("commercial_add")
CAPEX_GMP        = capex_total("gmp_add")
CAPEX_ALL        = CAPEX_PILOT + CAPEX_COMMERCIAL + CAPEX_GMP

GMP_CERT_MONTHS_FACILITY = 24    # [E-428] 18~30개월 중앙값
GMP_CERT_MONTHS_TO_FIRST_LOT = 30

# 규모 티어: (연간 L, FTE, 시설 OPEX, 감가 대상 CAPEX, 배치크기 L)
SCALE_TIERS = [
    {"L_per_year":    1, "fte":  2, "facility_opex": 120_000, "capex": 350_000,                     "batch_L": 1.0},
    {"L_per_year":   10, "fte":  5, "facility_opex": 240_000, "capex": CAPEX_PILOT*0.45,            "batch_L": 5.0},
    {"L_per_year":  100, "fte": 11, "facility_opex": 420_000, "capex": CAPEX_PILOT,                 "batch_L": 20.0},
    {"L_per_year": 1000, "fte": 22, "facility_opex": 900_000, "capex": CAPEX_PILOT+CAPEX_COMMERCIAL,"batch_L": 100.0},
]
OTHER_FIXED = {1: 40_000, 10: 90_000, 100: 180_000, 1000: 350_000}   # SW/감사/보험/QMS 유지
GMP_FTE_ADD = 9
GMP_FIXED_ADD_OTHER = 400_000    # EM·밸리데이션 유지

# ----------------------------------------------------------------------------
# 5. ASP (Agent C 제약 승계)
# ----------------------------------------------------------------------------
ASP_ANCHORS = {
    "china_floor":        21.30,   # [E-125 / E-442] Yeasen Ceturegel — 하한
    "base":               32.00,   # 본 모델 기준 (Col-Tgel 대비 -17.7% 침투가)
    "coltgel_parity":     38.90,   # [E-120 / E-442] 동일 아키텍처 선행품 — 실질 상한
    "matrigel_organoid":  44.76,   # [E-102 / E-442] Matrigel 오가노이드 SKU
    "defined_median":     60.47,   # [E-161] fully-defined 중앙값 (p=0.168 로 유의성 없음 -> 사용 지양)
}
GMP_MULTIPLE = 1.85              # Agent B H3 통합 권고 (1.75 [E-077] + 1.942 [E-159]) / 2
DISTRIBUTOR_MARKUP = 0.359       # [E-162]

# 소용량 프리미엄 (Agent C 실측: Matrigel 5mL/10mL = 1.288, Col-Tgel 2mL/10mL = 1.401)
SIZE_PREMIUM = {1.0: 1.55, 5.0: 1.288, 10.0: 1.00}
SKU_SIZES = [1.0, 5.0, 10.0]

GM_GATE = 0.60                   # DECISION_GATE
SOM_GATE_USD = 15_000_000        # DECISION_GATE SOM_2030 최소
DESIGN_VOLUME_L = 500            # = SOM_GATE / (ASP 32.00 x 1000 mL) = 469 L -> 설계 물량 500 L/년
RAMP_VOLUME_L = 100              # 램프업 초기(2027~2028) 물량


# ============================================================================
# 계산 엔진
# ============================================================================

def material_cost_per_ml(form_name=BASE_FORM, collagen_usd_g=None, mtg_usd_g=None,
                         laminin=False, laminin_usd_mg=None):
    """가공 전 원료비 (USD/mL)"""
    f = FORMULATIONS[form_name]
    cg = COLLAGEN_BLEND_USD_PER_G if collagen_usd_g is None else collagen_usd_g
    mg_ = MTG_INTERNAL_TRANSFER_USD_PER_G if mtg_usd_g is None else mtg_usd_g
    lm = LAMININ_PRICES_USD_PER_MG["internal_20x_discount"] if laminin_usd_mg is None else laminin_usd_mg

    col = (f["col_mg_ml"] / 1000.0) * cg
    mtg = (f["mtg_ug_ml"] / 1_000_000.0) * mg_
    lam = (LAMININ_CONC_MG_PER_ML * lm) if laminin else 0.0
    items = {
        "재조합 콜라겐 (single+triple)": col,
        "mTG 가교효소": mtg,
        "재조합 라미닌-111": lam,
        "완충액·안정화제": BUFFER_USD_PER_ML,
        "정제수/WFI": WATER_USD_PER_ML,
    }
    return sum(items.values()), items


def qc_cost_per_lot(grade="RUO"):
    base = sum(QC_RUO.values())
    if grade == "GMP":
        base += sum(QC_GMP_ADDER.values())
    return base


def scale_tier(L_per_year):
    for t in SCALE_TIERS:
        if t["L_per_year"] == L_per_year:
            return t
    # 보간 없이 가장 가까운 하위 티어
    cand = [t for t in SCALE_TIERS if t["L_per_year"] <= L_per_year]
    return cand[-1] if cand else SCALE_TIERS[0]


def fixed_opex(L_per_year, grade="RUO"):
    t = scale_tier(L_per_year)
    fte = t["fte"] + (GMP_FTE_ADD if grade == "GMP" else 0)
    capex = t["capex"] + (CAPEX_GMP if grade == "GMP" else 0)
    other = OTHER_FIXED[t["L_per_year"]] + (GMP_FIXED_ADD_OTHER if grade == "GMP" else 0)
    return {
        "인건비": fte * FTE_USD_PER_YEAR,
        "시설 OPEX": t["facility_opex"] * (1.35 if grade == "GMP" else 1.0),
        "감가상각": capex / DEPREC_YEARS,
        "기타 고정비": other,
        "_fte": fte, "_capex": capex,
    }


def cogs(L_per_year=100, grade="RUO", form_name=BASE_FORM, sku_mL=10.0,
         laminin=False, laminin_usd_mg=None, collagen_usd_g=None, mtg_usd_g=None,
         yield_mult=1.0, include_freight=False):
    """단위 COGS 빌드업. 반환: dict"""
    t = scale_tier(L_per_year)
    batch_L = min(t["batch_L"], L_per_year)
    n_lots = max(1, math.ceil(L_per_year / batch_L))

    reject = REJECT_GMP if grade == "GMP" else REJECT_RUO
    y = (1 - PROC_LOSS) * (1 - reject) * yield_mult
    y = min(y, 0.995)

    mat_ml, mat_items = material_cost_per_ml(form_name, collagen_usd_g, mtg_usd_g,
                                             laminin, laminin_usd_mg)
    mat_per_sellable_ml = mat_ml / y          # 수율 손실 반영

    # 배치 레벨 원가
    batch_labor = BATCH_LABOR_HOURS * FTE_USD_PER_HOUR * (1 + REWORK_RATE * 0.4)
    batch_consum = FILTER_USD_PER_BATCH + CONSUM_USD_PER_BATCH
    batch_qc = qc_cost_per_lot(grade)
    batch_total = batch_labor + batch_consum + batch_qc
    sellable_mL_per_batch = batch_L * 1000.0 * y
    batch_per_ml = batch_total / sellable_mL_per_batch

    # 고정비 배분
    fx = fixed_opex(L_per_year, grade)
    fixed_total = fx["인건비"] + fx["시설 OPEX"] + fx["감가상각"] + fx["기타 고정비"]
    sellable_mL_per_year = L_per_year * 1000.0 * y
    fixed_per_ml = fixed_total / sellable_mL_per_year

    # 유닛(패키지) 레벨
    fill_labor_unit = (FILL_SEC_PER_VIAL / 3600.0) * FTE_USD_PER_HOUR
    pack_unit = VIAL_USD_PER_UNIT + LABEL_USD_PER_UNIT + fill_labor_unit
    freight_unit = (SHIP_USD_PER_SHIPMENT / UNITS_PER_SHIPMENT) if include_freight else 0.0

    var_per_ml = mat_per_sellable_ml + batch_per_ml
    cogs_unit = var_per_ml * sku_mL + pack_unit + fixed_per_ml * sku_mL + freight_unit
    cogs_ml = cogs_unit / sku_mL

    return {
        "L_per_year": L_per_year, "grade": grade, "sku_mL": sku_mL, "form": form_name,
        "laminin": laminin, "yield": y, "n_lots": n_lots, "batch_L": batch_L,
        "mat_items": mat_items, "mat_per_ml_raw": mat_ml,
        "mat_per_ml": mat_per_sellable_ml, "batch_per_ml": batch_per_ml,
        "fixed_per_ml": fixed_per_ml, "pack_unit": pack_unit, "freight_unit": freight_unit,
        "batch_qc": batch_qc, "batch_labor": batch_labor, "batch_consum": batch_consum,
        "fixed_total": fixed_total, "fixed_breakdown": fx,
        "cogs_unit": cogs_unit, "cogs_ml": cogs_ml,
        "sellable_mL_per_year": sellable_mL_per_year,
    }


def asp_for(sku_mL, asp_base_10ml, grade="RUO"):
    a = asp_base_10ml * SIZE_PREMIUM[sku_mL]
    if grade == "GMP":
        a *= GMP_MULTIPLE
    return a


def gm_pct(asp_ml, cogs_ml):
    return (asp_ml - cogs_ml) / asp_ml * 100.0 if asp_ml > 0 else float("nan")


def bep(L_per_year, grade="RUO", asp_base=ASP_ANCHORS["base"], laminin=False,
        sku_mL=10.0, laminin_usd_mg=None):
    """손익분기 물량 (L/년, units/년, 매출 USD)"""
    r = cogs(L_per_year=L_per_year, grade=grade, sku_mL=sku_mL, laminin=laminin,
             laminin_usd_mg=laminin_usd_mg)
    asp_ml = asp_for(sku_mL, asp_base, grade)
    # 변동비 = 원료 + 배치 + 포장(=단위/ sku)
    var_ml = r["mat_per_ml"] + r["batch_per_ml"] + r["pack_unit"] / sku_mL
    cm_ml = asp_ml - var_ml
    if cm_ml <= 0:
        return {"cm_ml": cm_ml, "bep_L": float("inf"), "bep_units": float("inf"),
                "bep_rev": float("inf"), "asp_ml": asp_ml, "var_ml": var_ml,
                "fixed_total": r["fixed_total"]}
    bep_mL = r["fixed_total"] / cm_ml
    return {
        "cm_ml": cm_ml, "asp_ml": asp_ml, "var_ml": var_ml,
        "fixed_total": r["fixed_total"],
        "bep_L": bep_mL / 1000.0,
        "bep_units": bep_mL / sku_mL,
        "bep_rev": bep_mL * asp_ml,
    }


# ============================================================================
# 출력
# ============================================================================
def CM(x, nd=0):
    return format(x, ",.%df" % nd)


def line(c="-", n=112):
    print(c * n)


def main():
    rows_csv = []

    print("=" * 112)
    print("OSVX Agent E — COGS / 단위경제 모델   (LG화학 재조합콜라겐 + mTG Defined Organoid Matrix)")
    print("기준일 2026-08-11 · 통화 USD · 환율 KRW/USD %.2f, CNY/USD %.4f, USD/EUR %.4f  [E-146]"
          % (FX["KRW_per_USD"], FX["CNY_per_USD"], FX["USD_per_EUR"]))
    print("=" * 112)

    # ---------- 1. 원료 단가 실측표 ----------
    print("\n[1] 원료 단가 실측표 (BOM 입력)")
    line()
    print("%-46s %18s  %s" % ("항목", "단가", "근거"))
    line()
    print("%-46s %18s  %s" % ("PureCol 소 콜라겐 (연구 카탈로그)", CM(COLLAGEN_PRICES_USD_PER_G["catalog_purecol_bovine"]) + " USD/g", "[E-400]"))
    print("%-46s %18s  %s" % ("PureCol EZ Gel (사전중화형)", CM(COLLAGEN_PRICES_USD_PER_G["catalog_purecol_ezgel_bovine"]) + " USD/g", "[E-406]"))
    print("%-46s %18s  %s" % ("Humabiologics 인체 콜라겐", CM(COLLAGEN_PRICES_USD_PER_G["catalog_humabiologics_human"]) + " USD/g", "[E-401]"))
    print("%-46s %18s  %s" % ("재조합 콜라겐 벌크 (고순도 상단)", "%.2f USD/g" % COLLAGEN_PRICES_USD_PER_G["bulk_recomb_high_purity"], "[E-402]"))
    print("%-46s %18s  %s" % ("재조합 콜라겐 벌크 (현행 시장가)", "%.2f USD/g" % COLLAGEN_PRICES_USD_PER_G["bulk_recomb_current_mkt"], "[E-403]"))
    print("%-46s %18s  %s" % ("재조합 콜라겐 벌크 (best-in-class)", "%.2f USD/g" % COLLAGEN_PRICES_USD_PER_G["bulk_recomb_best_in_class"], "[E-404]"))
    print("%-46s %18s  %s" % ("→ LG화학 내부 블렌드 이전원가", "%.2f USD/g" % COLLAGEN_BLEND_USD_PER_G, "가정 E-A1"))
    line(".")
    print("%-46s %18s  %s" % ("mTG 식품급 1000 U/g (순효소 등가)", "%.2f USD/g" % MTG_PRICES_USD_PER_G["food_grade_1000U_g"], "[E-409]"))
    print("%-46s %18s  %s" % ("mTG Activa RM (순효소 등가)", "%.2f USD/g" % MTG_PRICES_USD_PER_G["food_grade_activa_rm"], "[E-408]"))
    print("%-46s %18s  %s" % ("mTG Zedira Andracon (제약 카탈로그)", CM(MTG_PRICES_USD_PER_G["zedira_andracon"]) + " USD/g", "[E-407]"))
    print("%-46s %18s  %s" % ("→ LG화학 내부 GMP mTG 이전가격", "%.2f USD/g" % MTG_INTERNAL_TRANSFER_USD_PER_G, "가정 E-A3"))
    line(".")
    for k, v in LAMININ_PRICES_USD_PER_MG.items():
        ev = {"imatrix511_silk_catalog": "[E-412]", "gibco_mouse_ehs": "[E-411]",
              "corning_rlaminin521": "[E-144,C]", "biolamina_ln521_est": "[E-158,C]",
              "bulk_10x_discount": "가정 E-A5", "internal_20x_discount": "가정 E-A5"}[k]
        print("%-46s %18s  %s" % ("라미닌 " + k, "%.2f USD/mg" % v, ev))
    print("%-46s %18s  %s" % ("라미닌 필요 농도 (문헌)", "%.2f mg/mL" % LAMININ_CONC_MG_PER_ML, "[E-410]"))
    line()

    # ---------- 2. BOM 표 (라미닌 무/유) ----------
    print("\n[2] BOM 표 — 배합 %s (콜라겐 %.1f mg/mL, mTG %.0f µg/mL), USD per mL"
          % (BASE_FORM, FORMULATIONS[BASE_FORM]["col_mg_ml"], FORMULATIONS[BASE_FORM]["mtg_ug_ml"]))
    line()
    _, items_nolam = material_cost_per_ml(laminin=False)
    _, items_lam_int = material_cost_per_ml(laminin=True,
                        laminin_usd_mg=LAMININ_PRICES_USD_PER_MG["internal_20x_discount"])
    _, items_lam_cat = material_cost_per_ml(laminin=True,
                        laminin_usd_mg=LAMININ_PRICES_USD_PER_MG["imatrix511_silk_catalog"])
    print("%-32s %14s %16s %18s" % ("BOM 항목", "A: 라미닌無", "B1: 라미닌(내재)", "B2: 라미닌(카탈로그)"))
    line(".")
    for k in items_nolam:
        print("%-32s %14.4f %16.4f %18.4f" % (k, items_nolam[k], items_lam_int[k], items_lam_cat[k]))
    line(".")
    print("%-32s %14.4f %16.4f %18.4f" % ("원료비 소계 (USD/mL)",
          sum(items_nolam.values()), sum(items_lam_int.values()), sum(items_lam_cat.values())))
    line()
    for k, v in [("A", sum(items_nolam.values())), ("B1", sum(items_lam_int.values())),
                 ("B2", sum(items_lam_cat.values()))]:
        rows_csv.append({"section": "BOM", "key": "materials_usd_per_mL_" + k, "value": round(v, 4)})

    # ---------- 3. COGS 빌드업 ----------
    print("\n[3] COGS 빌드업 — 생산량 100 L/년, 10 mL SKU")
    line()
    print("%-34s %14s %14s %16s %16s" % ("구성요소", "RUO 라미닌無", "GMP 라미닌無", "RUO 라미닌(내재)", "RUO 라미닌(카탈로그)"))
    line(".")
    scen = {
        "RUO_nolam": cogs(100, "RUO", laminin=False),
        "GMP_nolam": cogs(100, "GMP", laminin=False),
        "RUO_lam_int": cogs(100, "RUO", laminin=True,
                            laminin_usd_mg=LAMININ_PRICES_USD_PER_MG["internal_20x_discount"]),
        "RUO_lam_cat": cogs(100, "RUO", laminin=True,
                            laminin_usd_mg=LAMININ_PRICES_USD_PER_MG["imatrix511_silk_catalog"]),
    }
    order = ["RUO_nolam", "GMP_nolam", "RUO_lam_int", "RUO_lam_cat"]
    def row(label, fn):
        print("%-34s %14s %14s %16s %16s" % (label, *[fn(scen[k]) for k in order]))
    row("원료비 (수율보정 후) USD/mL", lambda r: "%.4f" % r["mat_per_ml"])
    row("배치원가(인건·소모품·QC) USD/mL", lambda r: "%.4f" % r["batch_per_ml"])
    row("  └ 그중 QC USD/lot", lambda r: format(r["batch_qc"], ",.0f"))
    row("고정비 배분 USD/mL", lambda r: "%.4f" % r["fixed_per_ml"])
    row("포장(바이알/라벨/충전) USD/unit", lambda r: "%.4f" % r["pack_unit"])
    row("종합수율", lambda r: "%.1f%%" % (r["yield"] * 100))
    line(".")
    row("COGS USD/unit (10 mL)", lambda r: "%.2f" % r["cogs_unit"])
    row("COGS USD/mL", lambda r: "%.3f" % r["cogs_ml"])
    line()
    for k in order:
        rows_csv.append({"section": "COGS_100L_10mL", "key": k + "_usd_per_mL",
                         "value": round(scen[k]["cogs_ml"], 4)})
        rows_csv.append({"section": "COGS_100L_10mL", "key": k + "_usd_per_unit",
                         "value": round(scen[k]["cogs_unit"], 2)})

    print("고정비 내역 (100 L/년, RUO): " + ", ".join(
        "%s %s" % (k, CM(v)) for k, v in scen["RUO_nolam"]["fixed_breakdown"].items()
        if not k.startswith("_")))
    print("  FTE %d명, 감가대상 CAPEX %s USD, 로트 수 %d/년, 배치 %.0f L"
          % (scen["RUO_nolam"]["fixed_breakdown"]["_fte"],
             CM(scen["RUO_nolam"]["fixed_breakdown"]["_capex"]),
             scen["RUO_nolam"]["n_lots"], scen["RUO_nolam"]["batch_L"]))
    print("고정비 내역 (100 L/년, GMP): " + ", ".join(
        "%s %s" % (k, CM(v)) for k, v in scen["GMP_nolam"]["fixed_breakdown"].items()
        if not k.startswith("_")))
    print("→ GMP/RUO 원가 배수 = %.3f  (ASP 프리미엄 배수 %.2f [Agent B H3] 대비 %s)"
          % (scen["GMP_nolam"]["cogs_ml"] / scen["RUO_nolam"]["cogs_ml"], GMP_MULTIPLE,
             "원가배수 < 가격배수 → GMP 전환 시 GM 개선"
             if scen["GMP_nolam"]["cogs_ml"] / scen["RUO_nolam"]["cogs_ml"] < GMP_MULTIPLE
             else "원가배수 > 가격배수 → GMP 전환 시 GM 악화"))
    rows_csv.append({"section": "COGS_100L_10mL", "key": "gmp_over_ruo_cost_multiple",
                     "value": round(scen["GMP_nolam"]["cogs_ml"] / scen["RUO_nolam"]["cogs_ml"], 4)})

    # ---------- 4. 단위경제표 1/5/10 mL ----------
    print("\n[4] 단위경제표 — 규격별 (생산량 100 L/년, 라미닌 無, ASP 기준 %.2f USD/mL @10 mL)"
          % ASP_ANCHORS["base"])
    line()
    print("%-6s %-6s %11s %11s %11s %11s %9s %12s %14s" %
          ("규격", "등급", "COGS/unit", "COGS/mL", "ASP/unit", "ASP/mL", "GM%", "BEP(L/년)", "BEP매출(USD)"))
    line(".")
    for grade in ("RUO", "GMP"):
        for s in SKU_SIZES:
            r = cogs(100, grade, sku_mL=s, laminin=False)
            a_ml = asp_for(s, ASP_ANCHORS["base"], grade)
            b = bep(100, grade, ASP_ANCHORS["base"], laminin=False, sku_mL=s)
            g = gm_pct(a_ml, r["cogs_ml"])
            print("%-6s %-6s %11.2f %11.3f %11.2f %11.2f %8.1f%% %12.1f %14s" %
                  ("%.0f mL" % s, grade, r["cogs_unit"], r["cogs_ml"], a_ml * s, a_ml, g,
                   b["bep_L"], format(b["bep_rev"], ",.0f")))
            rows_csv += [
                {"section": "UnitEcon_100L", "key": "%s_%.0fmL_cogs_per_unit" % (grade, s), "value": round(r["cogs_unit"], 2)},
                {"section": "UnitEcon_100L", "key": "%s_%.0fmL_cogs_per_mL" % (grade, s), "value": round(r["cogs_ml"], 4)},
                {"section": "UnitEcon_100L", "key": "%s_%.0fmL_asp_per_mL" % (grade, s), "value": round(a_ml, 2)},
                {"section": "UnitEcon_100L", "key": "%s_%.0fmL_gm_pct" % (grade, s), "value": round(g, 2)},
                {"section": "UnitEcon_100L", "key": "%s_%.0fmL_bep_L_per_year" % (grade, s), "value": round(b["bep_L"], 2)},
                {"section": "UnitEcon_100L", "key": "%s_%.0fmL_bep_revenue_usd" % (grade, s), "value": round(b["bep_rev"], 0)},
            ]
    line()
    print("소용량 프리미엄 적용 (Agent C 실측): 1 mL x%.2f, 5 mL x%.3f, 10 mL x1.000" %
          (SIZE_PREMIUM[1.0], SIZE_PREMIUM[5.0]))
    print("GM 게이트 %.0f%% 판정:" % (GM_GATE * 100))
    for grade in ("RUO", "GMP"):
        res = []
        for s in SKU_SIZES:
            r = cogs(100, grade, sku_mL=s, laminin=False)
            g = gm_pct(asp_for(s, ASP_ANCHORS["base"], grade), r["cogs_ml"])
            res.append("%.0f mL %s(%.1f%%)" % (s, "PASS" if g >= GM_GATE * 100 else "FAIL", g))
        print("   %-4s: %s" % (grade, " · ".join(res)))

    # ---------- 4b. 설계 물량(500 L/년) 단위경제표 ----------
    print("\n[4b] 단위경제표 — 설계 물량 %d L/년 (= DECISION_GATE SOM_2030 %s USD / ASP %.2f USD/mL / 1000)"
          % (DESIGN_VOLUME_L, CM(SOM_GATE_USD), ASP_ANCHORS["base"]))
    line()
    print("%-6s %-6s %11s %11s %11s %11s %9s %12s %14s" %
          ("규격", "등급", "COGS/unit", "COGS/mL", "ASP/unit", "ASP/mL", "GM%", "BEP(L/년)", "BEP매출(USD)"))
    line(".")
    for grade in ("RUO", "GMP"):
        for sz in SKU_SIZES:
            r = cogs(DESIGN_VOLUME_L, grade, sku_mL=sz, laminin=False)
            a_ml = asp_for(sz, ASP_ANCHORS["base"], grade)
            b = bep(DESIGN_VOLUME_L, grade, ASP_ANCHORS["base"], laminin=False, sku_mL=sz)
            g = gm_pct(a_ml, r["cogs_ml"])
            print("%-6s %-6s %11.2f %11.3f %11.2f %11.2f %8.1f%% %12.1f %14s" %
                  ("%.0f mL" % sz, grade, r["cogs_unit"], r["cogs_ml"], a_ml * sz, a_ml, g,
                   b["bep_L"], CM(b["bep_rev"])))
            rows_csv += [
                {"section": "UnitEcon_500L", "key": "%s_%.0fmL_cogs_per_unit" % (grade, sz), "value": round(r["cogs_unit"], 2)},
                {"section": "UnitEcon_500L", "key": "%s_%.0fmL_cogs_per_mL" % (grade, sz), "value": round(r["cogs_ml"], 4)},
                {"section": "UnitEcon_500L", "key": "%s_%.0fmL_asp_per_mL" % (grade, sz), "value": round(a_ml, 2)},
                {"section": "UnitEcon_500L", "key": "%s_%.0fmL_gm_pct" % (grade, sz), "value": round(g, 2)},
                {"section": "UnitEcon_500L", "key": "%s_%.0fmL_bep_L_per_year" % (grade, sz), "value": round(b["bep_L"], 2)},
                {"section": "UnitEcon_500L", "key": "%s_%.0fmL_bep_revenue_usd" % (grade, sz), "value": round(b["bep_rev"], 0)},
            ]
    line()
    print("GM 게이트 %.0f%% 판정 (설계 물량 %d L/년):" % (GM_GATE * 100, DESIGN_VOLUME_L))
    for grade in ("RUO", "GMP"):
        res = []
        for sz in SKU_SIZES:
            r = cogs(DESIGN_VOLUME_L, grade, sku_mL=sz, laminin=False)
            g = gm_pct(asp_for(sz, ASP_ANCHORS["base"], grade), r["cogs_ml"])
            res.append("%.0f mL %s(%.1f%%)" % (sz, "PASS" if g >= GM_GATE * 100 else "FAIL", g))
        print("   %-4s: %s" % (grade, " · ".join(res)))
    rd5 = cogs(DESIGN_VOLUME_L, "RUO", sku_mL=10.0)
    gd5 = cogs(DESIGN_VOLUME_L, "GMP", sku_mL=10.0)
    print("→ 설계 물량에서의 GMP/RUO 원가 배수 = %.3f (가격 배수 %.2f) → %s"
          % (gd5["cogs_ml"] / rd5["cogs_ml"], GMP_MULTIPLE,
             "GMP 전환 시 GM 개선" if gd5["cogs_ml"]/rd5["cogs_ml"] < GMP_MULTIPLE else "GMP 전환 시 GM 악화"))
    rows_csv.append({"section": "UnitEcon_500L", "key": "gmp_over_ruo_cost_multiple",
                     "value": round(gd5["cogs_ml"] / rd5["cogs_ml"], 4)})
    print("  라미닌 포함 시(내재 23.19 USD/mg): COGS %.3f USD/mL, GM %.1f%%  |  카탈로그(463.81): COGS %.3f, GM %.1f%%"
          % (cogs(DESIGN_VOLUME_L, "RUO", sku_mL=10.0, laminin=True,
                  laminin_usd_mg=LAMININ_PRICES_USD_PER_MG["internal_20x_discount"])["cogs_ml"],
             gm_pct(ASP_ANCHORS["base"], cogs(DESIGN_VOLUME_L, "RUO", sku_mL=10.0, laminin=True,
                  laminin_usd_mg=LAMININ_PRICES_USD_PER_MG["internal_20x_discount"])["cogs_ml"]),
             cogs(DESIGN_VOLUME_L, "RUO", sku_mL=10.0, laminin=True,
                  laminin_usd_mg=LAMININ_PRICES_USD_PER_MG["imatrix511_silk_catalog"])["cogs_ml"],
             gm_pct(ASP_ANCHORS["base"], cogs(DESIGN_VOLUME_L, "RUO", sku_mL=10.0, laminin=True,
                  laminin_usd_mg=LAMININ_PRICES_USD_PER_MG["imatrix511_silk_catalog"])["cogs_ml"])))
    line()

    # ---------- 5. ASP 시나리오 ----------
    print("\n[5] ASP 시나리오별 GM% (RUO, 램프 100 L/년, 10 mL SKU)")
    line()
    r10 = cogs(100, "RUO", sku_mL=10.0, laminin=False)
    r10l = cogs(100, "RUO", sku_mL=10.0, laminin=True,
                laminin_usd_mg=LAMININ_PRICES_USD_PER_MG["internal_20x_discount"])
    r10lc = cogs(100, "RUO", sku_mL=10.0, laminin=True,
                 laminin_usd_mg=LAMININ_PRICES_USD_PER_MG["imatrix511_silk_catalog"])
    print("%-24s %10s %12s %14s %16s" % ("ASP 앵커", "USD/mL", "GM% 라미닌無", "GM% 라미닌(내재)", "GM% 라미닌(카탈로그)"))
    line(".")
    for k, v in ASP_ANCHORS.items():
        print("%-24s %10.2f %11.1f%% %13.1f%% %15.1f%%" %
              (k, v, gm_pct(v, r10["cogs_ml"]), gm_pct(v, r10l["cogs_ml"]), gm_pct(v, r10lc["cogs_ml"])))
        rows_csv.append({"section": "ASP_scenarios", "key": "gm_pct_nolam_" + k,
                         "value": round(gm_pct(v, r10["cogs_ml"]), 2)})
        rows_csv.append({"section": "ASP_scenarios", "key": "gm_pct_lam_internal_" + k,
                         "value": round(gm_pct(v, r10l["cogs_ml"]), 2)})
        rows_csv.append({"section": "ASP_scenarios", "key": "gm_pct_lam_catalog_" + k,
                         "value": round(gm_pct(v, r10lc["cogs_ml"]), 2)})
    line()

    # 설계 물량에서의 ASP 시나리오
    print("\n[5b] ASP 시나리오별 GM%% (RUO, 설계 %d L/년, 10 mL SKU)" % DESIGN_VOLUME_L)
    line()
    d0 = cogs(DESIGN_VOLUME_L, "RUO", sku_mL=10.0, laminin=False)
    d1 = cogs(DESIGN_VOLUME_L, "RUO", sku_mL=10.0, laminin=True,
              laminin_usd_mg=LAMININ_PRICES_USD_PER_MG["internal_20x_discount"])
    d2 = cogs(DESIGN_VOLUME_L, "RUO", sku_mL=10.0, laminin=True,
              laminin_usd_mg=LAMININ_PRICES_USD_PER_MG["imatrix511_silk_catalog"])
    print("%-24s %10s %12s %14s %16s" % ("ASP 앵커", "USD/mL", "GM% 라미닌無", "GM% 라미닌(내재)", "GM% 라미닌(카탈로그)"))
    line(".")
    for k, v in ASP_ANCHORS.items():
        print("%-24s %10.2f %11.1f%% %13.1f%% %15.1f%%" %
              (k, v, gm_pct(v, d0["cogs_ml"]), gm_pct(v, d1["cogs_ml"]), gm_pct(v, d2["cogs_ml"])))
        rows_csv.append({"section": "ASP_scenarios_500L", "key": "gm_pct_nolam_" + k,
                         "value": round(gm_pct(v, d0["cogs_ml"]), 2)})
        rows_csv.append({"section": "ASP_scenarios_500L", "key": "gm_pct_lam_internal_" + k,
                         "value": round(gm_pct(v, d1["cogs_ml"]), 2)})
        rows_csv.append({"section": "ASP_scenarios_500L", "key": "gm_pct_lam_catalog_" + k,
                         "value": round(gm_pct(v, d2["cogs_ml"]), 2)})
    line()

    # ---------- 6. 규모의 경제 곡선 ----------
    print("\n[6] 규모의 경제 곡선 (RUO, 10 mL SKU, 라미닌 無)")
    line()
    print("%-10s %6s %8s %10s %11s %11s %11s %11s %9s %12s" %
          ("생산량", "FTE", "로트/년", "고정비(USD)", "원료/mL", "배치/mL", "고정비/mL", "COGS/mL", "GM%@32", "매출(USD)"))
    line(".")
    for t in SCALE_TIERS:
        L = t["L_per_year"]
        r = cogs(L, "RUO", sku_mL=10.0, laminin=False)
        g = gm_pct(ASP_ANCHORS["base"], r["cogs_ml"])
        rev = r["sellable_mL_per_year"] * ASP_ANCHORS["base"]
        print("%-10s %6d %8d %10s %11.4f %11.4f %11.4f %11.3f %8.1f%% %12s" %
              ("%d L/년" % L, r["fixed_breakdown"]["_fte"], r["n_lots"],
               format(r["fixed_total"], ",.0f"), r["mat_per_ml"], r["batch_per_ml"],
               r["fixed_per_ml"], r["cogs_ml"], g, format(rev, ",.0f")))
        rows_csv += [
            {"section": "ScaleCurve_RUO", "key": "L%d_cogs_per_mL" % L, "value": round(r["cogs_ml"], 4)},
            {"section": "ScaleCurve_RUO", "key": "L%d_fixed_per_mL" % L, "value": round(r["fixed_per_ml"], 4)},
            {"section": "ScaleCurve_RUO", "key": "L%d_gm_pct_at_32" % L, "value": round(g, 2)},
        ]
    line()
    print("고정비 배분 로직: 고정비/mL = (인건비 + 시설OPEX + 감가상각[CAPEX/%d년] + 기타) / (연간 L x 1000 x 종합수율)"
          % DEPREC_YEARS)
    # GM 60% 를 달성하는 최소 연간 물량 (10 mL SKU, ASP 32.00, RUO)
    lo_v, hi_v = 100.0, 1000.0
    for _ in range(60):
        mid = (lo_v + hi_v) / 2
        rr = cogs(mid, "RUO", sku_mL=10.0, laminin=False)
        if gm_pct(ASP_ANCHORS["base"], rr["cogs_ml"]) >= GM_GATE * 100:
            hi_v = mid
        else:
            lo_v = mid
    v60 = hi_v
    r60 = cogs(v60, "RUO", sku_mL=10.0, laminin=False)
    print("→ GM 게이트 60%% 를 넘기는 최소 연간 물량 = %.0f L/년 (COGS %.3f USD/mL, 매출 %s USD @32.00)"
          % (v60, r60["cogs_ml"], CM(v60 * 1000 * r60["yield"] * ASP_ANCHORS["base"])))
    for extra in (250.0, 500.0):
        re_ = cogs(extra, "RUO", sku_mL=10.0, laminin=False)
        print("   보간: %.0f L/년 → COGS %.3f USD/mL, GM %.1f%% @32.00"
              % (extra, re_["cogs_ml"], gm_pct(ASP_ANCHORS["base"], re_["cogs_ml"])))
        rows_csv.append({"section": "ScaleCurve_RUO", "key": "L%d_cogs_per_mL" % extra, "value": round(re_["cogs_ml"], 4)})
    rows_csv.append({"section": "ScaleCurve_RUO", "key": "min_volume_L_for_GM60", "value": round(v60, 1)})
    print("외부 검증 [E-425] 정밀발효 COGS 곡선 (titer 20 g/L): 1,000 L=120 / 10,000 L=48 / 100,000 L=20 USD/kg")
    print("  → 규모 100배 확대 시 원가 1/6 로 감소하는 형태. 본 모델은 1→1000 L 에서 %.2f→%.2f USD/mL (%.1f배 감소)"
          % (cogs(1, "RUO", sku_mL=10.0)["cogs_ml"], cogs(1000, "RUO", sku_mL=10.0)["cogs_ml"],
             cogs(1, "RUO", sku_mL=10.0)["cogs_ml"] / cogs(1000, "RUO", sku_mL=10.0)["cogs_ml"]))

    # ---------- 7. Matrigel 원가구조 비교 ----------
    print("\n[7] Matrigel(마우스 EHS 육종 배양) 원가구조 추정 — 비교군")
    line()
    # 입력: 종양 4 g/마우스 [E-432], per diem 1.05 USD/cage/day [E-433], 5마리/케이지,
    #       사육 28일, 마우스 구입 35 USD, EHS 종양 4 g -> BME 약 4 mL (10 mg/mL 환산 가정 E-A9)
    mouse_purchase = 35.00
    per_diem = 1.05                    # [E-433]
    days = 28                          # [E-432] 3~4주
    mice_per_cage = 5
    tumor_g = 4.0                      # [E-432]
    mL_per_g_tumor = 1.0               # 가정 E-A9
    housing_per_mouse = per_diem * days / mice_per_cage
    animal_cost_per_mouse = mouse_purchase + housing_per_mouse
    mL_per_mouse = tumor_g * mL_per_g_tumor
    animal_cost_per_mL = animal_cost_per_mouse / mL_per_mouse
    # 추출·투석·QC·충전: 동물원가의 2.2배 (가정 E-A9; 노동집약 추출 + 로트별 QC)
    downstream_mult = 2.2
    matrigel_cogs_ml = animal_cost_per_mL * (1 + downstream_mult)
    matrigel_asp = ASP_ANCHORS["matrigel_organoid"]
    print("  마우스 구입 %.2f + 사육 %.2f(=%.2f USD/케이지/일 x %d일 / %d마리) = %.2f USD/마리  [E-432][E-433]"
          % (mouse_purchase, housing_per_mouse, per_diem, days, mice_per_cage, animal_cost_per_mouse))
    print("  종양 %.1f g/마리 → BME %.1f mL/마리 (가정 E-A9) → 동물원가 %.2f USD/mL"
          % (tumor_g, mL_per_mouse, animal_cost_per_mL))
    print("  + 추출·투석·무균여과·QC·충전 = 동물원가 x %.1f → Matrigel COGS 추정 %.2f USD/mL"
          % (downstream_mult, matrigel_cogs_ml))
    print("  Matrigel 오가노이드 SKU 직판가 %.2f USD/mL [E-102] → 추정 GM %.1f%%"
          % (matrigel_asp, gm_pct(matrigel_asp, matrigel_cogs_ml)))
    print("  우리 제품(RUO, 100 L/년) COGS %.3f USD/mL → Matrigel 대비 %.2f배"
          % (r10["cogs_ml"], r10["cogs_ml"] / matrigel_cogs_ml))
    print("  ※ 구조적 함의: Matrigel 원가는 '동물 마리수'에 선형 비례하여 규모의 경제가 거의 없다.")
    print("     우리 원가는 고정비 배분이 지배하므로 물량 확대 시 급격히 하락한다 → 장기 원가 우위는 우리 쪽.")
    line()
    rows_csv += [
        {"section": "Matrigel_compare", "key": "matrigel_cogs_usd_per_mL_est", "value": round(matrigel_cogs_ml, 3)},
        {"section": "Matrigel_compare", "key": "matrigel_gm_pct_est", "value": round(gm_pct(matrigel_asp, matrigel_cogs_ml), 2)},
        {"section": "Matrigel_compare", "key": "our_cogs_over_matrigel_ratio", "value": round(r10["cogs_ml"] / matrigel_cogs_ml, 3)},
    ]

    # ---------- 8. 민감도 ----------
    print("\n[8] 민감도 분석 (RUO, 100 L/년, 10 mL SKU, ASP %.2f USD/mL)" % ASP_ANCHORS["base"])
    line()
    base_cogs = r10["cogs_ml"]
    base_gm = gm_pct(ASP_ANCHORS["base"], base_cogs)
    print("기준: COGS %.3f USD/mL, GM %.1f%%" % (base_cogs, base_gm))
    line(".")
    print("%-38s %12s %12s %10s %10s" % ("변수", "COGS/mL", "ΔCOGS", "GM%", "ΔGM%p"))
    line(".")

    def sens(label, **kw):
        asp_override = kw.pop("_asp", None)
        Lv = kw.pop("L_per_year", 100)
        r = cogs(Lv, "RUO", sku_mL=10.0, **kw)
        a = asp_override if asp_override else ASP_ANCHORS["base"]
        g = gm_pct(a, r["cogs_ml"])
        print("%-38s %12.4f %+12.4f %9.1f%% %+9.1f" %
              (label, r["cogs_ml"], r["cogs_ml"] - base_cogs, g, g - base_gm))
        rows_csv.append({"section": "Sensitivity", "key": label, "value": round(r["cogs_ml"], 4)})
        rows_csv.append({"section": "Sensitivity", "key": label + " | GM%", "value": round(g, 2)})

    sens("① 콜라겐 단가 -50%", collagen_usd_g=COLLAGEN_BLEND_USD_PER_G * 0.5)
    sens("① 콜라겐 단가 +50%", collagen_usd_g=COLLAGEN_BLEND_USD_PER_G * 1.5)
    sens("② 수율 -30%", yield_mult=0.70)
    sens("② 수율 +30% (상한 99.5%)", yield_mult=1.30)
    sens("③ ASP -30% (COGS 불변)", _asp=ASP_ANCHORS["base"] * 0.70)
    sens("③ ASP +30% (COGS 불변)", _asp=ASP_ANCHORS["base"] * 1.30)
    sens("④ mTG 단가 -50%", mtg_usd_g=MTG_INTERNAL_TRANSFER_USD_PER_G * 0.5)
    sens("④ mTG 단가 +50%", mtg_usd_g=MTG_INTERNAL_TRANSFER_USD_PER_G * 1.5)
    sens("④' mTG = Zedira 카탈로그가", mtg_usd_g=MTG_PRICES_USD_PER_G["zedira_andracon"])
    sens("④'' mTG = 식품급 순효소 등가", mtg_usd_g=MTG_PRICES_USD_PER_G["food_grade_1000U_g"])
    sens("⑤ 라미닌 포함 (내재화 23.19 USD/mg)", laminin=True,
         laminin_usd_mg=LAMININ_PRICES_USD_PER_MG["internal_20x_discount"])
    sens("⑤ 라미닌 포함 (벌크 46.38 USD/mg)", laminin=True,
         laminin_usd_mg=LAMININ_PRICES_USD_PER_MG["bulk_10x_discount"])
    sens("⑤ 라미닌 포함 (카탈로그 463.81)", laminin=True,
         laminin_usd_mg=LAMININ_PRICES_USD_PER_MG["imatrix511_silk_catalog"])
    sens("⑥ 생산량 10 L/년", L_per_year=10)
    sens("⑥ 생산량 1000 L/년", L_per_year=1000)
    sens("⑦ 배합 OM-S soft (3 mg/mL)", form_name="OM-S soft")
    sens("⑦ 배합 OM-F firm (8 mg/mL)", form_name="OM-F firm")
    sens("⑧ 냉장체인 운임 COGS 내부화", include_freight=True)
    line()

    # 라미닌 손익분기 단가 — GM 게이트를 통과 가능한 규모(1000 L/년)에서 계산
    print("라미닌 손익분기 단가 (GM %.0f%% 를 유지하는 최대 라미닌 단가):" % (GM_GATE * 100))
    for Lv in (100, 1000):
        for asp in (ASP_ANCHORS["base"], ASP_ANCHORS["coltgel_parity"]):
            lo, hi = 0.0, 500.0
            base_ok = gm_pct(asp, cogs(Lv, "RUO", sku_mL=10.0, laminin=False)["cogs_ml"]) >= GM_GATE * 100
            if not base_ok:
                print("   %5d L/년 @ASP %.2f → 라미닌 0 USD/mg 에서도 GM %.1f%% 로 게이트 미달 (허용단가 없음)"
                      % (Lv, asp, gm_pct(asp, cogs(Lv, "RUO", sku_mL=10.0, laminin=False)["cogs_ml"])))
                rows_csv.append({"section": "Sensitivity",
                                 "key": "laminin_breakeven_usd_per_mg_GM60_%dL_asp%.2f" % (Lv, asp),
                                 "value": 0.0})
                continue
            for _ in range(60):
                mid = (lo + hi) / 2
                rr = cogs(Lv, "RUO", sku_mL=10.0, laminin=True, laminin_usd_mg=mid)
                if gm_pct(asp, rr["cogs_ml"]) >= GM_GATE * 100:
                    lo = mid
                else:
                    hi = mid
            cat = LAMININ_PRICES_USD_PER_MG["imatrix511_silk_catalog"]
            print("   %5d L/년 @ASP %.2f → 허용 최대 라미닌 단가 %.2f USD/mg "
                  "(카탈로그 최저 %.2f 의 %.1f%%, 즉 %.1f배 원가절감 필요)"
                  % (Lv, asp, lo, cat, lo / cat * 100, cat / lo if lo > 0 else float("inf")))
            rows_csv.append({"section": "Sensitivity",
                             "key": "laminin_breakeven_usd_per_mg_GM60_%dL_asp%.2f" % (Lv, asp),
                             "value": round(lo, 3)})
    line()

    # ---------- 9. BEP ----------
    print("\n[9] 손익분기(BEP) — 고정비 / 단위 공헌이익")
    line()
    print("%-30s %10s %10s %10s %12s %14s %14s" %
          ("시나리오", "ASP/mL", "변동비/mL", "공헌이익", "고정비(USD)", "BEP(L/년)", "BEP매출(USD)"))
    line(".")
    bep_cases = [
        ("RUO 100L 10mL @32.00", dict(L_per_year=100, grade="RUO", asp_base=32.00, sku_mL=10.0)),
        ("RUO 100L 10mL @38.90", dict(L_per_year=100, grade="RUO", asp_base=38.90, sku_mL=10.0)),
        ("RUO 100L 10mL @21.30", dict(L_per_year=100, grade="RUO", asp_base=21.30, sku_mL=10.0)),
        ("RUO 100L 5mL  @32.00", dict(L_per_year=100, grade="RUO", asp_base=32.00, sku_mL=5.0)),
        ("RUO 500L 10mL @32.00", dict(L_per_year=500, grade="RUO", asp_base=32.00, sku_mL=10.0)),
        ("RUO 1000L 10mL @32.00", dict(L_per_year=1000, grade="RUO", asp_base=32.00, sku_mL=10.0)),
        ("GMP 100L 10mL @59.20", dict(L_per_year=100, grade="GMP", asp_base=32.00, sku_mL=10.0)),
        ("RUO+라미닌(내재) @32.00", dict(L_per_year=100, grade="RUO", asp_base=32.00, sku_mL=10.0,
                                        laminin=True, laminin_usd_mg=LAMININ_PRICES_USD_PER_MG["internal_20x_discount"])),
        ("RUO+라미닌(카탈로그) @32.00", dict(L_per_year=100, grade="RUO", asp_base=32.00, sku_mL=10.0,
                                        laminin=True, laminin_usd_mg=LAMININ_PRICES_USD_PER_MG["imatrix511_silk_catalog"])),
    ]
    for name, kw in bep_cases:
        b = bep(**kw)
        bl = "무한(공헌이익 음수)" if math.isinf(b["bep_L"]) else CM(b["bep_L"], 1)
        br = "N/A(사유: 공헌이익 음수)" if math.isinf(b["bep_rev"]) else CM(b["bep_rev"], 0)
        print("%-30s %10.2f %10.4f %10.3f %12s %14s %14s" %
              (name, b["asp_ml"], b["var_ml"], b["cm_ml"], format(b["fixed_total"], ",.0f"), bl, br))
        rows_csv.append({"section": "BEP", "key": name + " | bep_L_per_year",
                         "value": None if math.isinf(b["bep_L"]) else round(b["bep_L"], 2)})
        rows_csv.append({"section": "BEP", "key": name + " | bep_revenue_usd",
                         "value": None if math.isinf(b["bep_rev"]) else round(b["bep_rev"], 0)})
    line()

    # ---------- 10. CAPEX ----------
    print("\n[10] CAPEX 및 인력")
    line()
    for blk, label in [("pilot", "파일럿 (RUO, ~100 L/년)"),
                       ("commercial_add", "상업 증설 (RUO, ~1,000 L/년)"),
                       ("gmp_add", "GMP 업그레이드 (2029~)")]:
        print("  %s" % label)
        for k, v in CAPEX[blk].items():
            print("      %-38s %14s" % (k, format(v, ",.0f")))
        print("      %-38s %14s  (예비비 %.0f%% 포함)" %
              ("소계", format(capex_total(blk), ",.0f"), CONTINGENCY * 100))
    print("  %-42s %14s" % ("CAPEX 합계 (파일럿+상업+GMP)", format(CAPEX_ALL, ",.0f")))
    print("  GMP 시설 소요기간: %d개월 (신축·밸리데이션) / 첫 GMP 로트 출하까지 %d개월  [E-428]"
          % (GMP_CERT_MONTHS_FACILITY, GMP_CERT_MONTHS_TO_FIRST_LOT))
    print("  인력: 파일럿 11 FTE / 상업 22 FTE / GMP 추가 +%d FTE (총 31 FTE), 완전부담 %s USD/년 [E-434]"
          % (GMP_FTE_ADD, CM(FTE_USD_PER_YEAR)))
    rows_csv += [
        {"section": "CAPEX", "key": "capex_pilot_usd", "value": round(CAPEX_PILOT, 0)},
        {"section": "CAPEX", "key": "capex_commercial_add_usd", "value": round(CAPEX_COMMERCIAL, 0)},
        {"section": "CAPEX", "key": "capex_gmp_add_usd", "value": round(CAPEX_GMP, 0)},
        {"section": "CAPEX", "key": "capex_total_usd", "value": round(CAPEX_ALL, 0)},
        {"section": "CAPEX", "key": "gmp_cert_months_facility", "value": GMP_CERT_MONTHS_FACILITY},
        {"section": "CAPEX", "key": "gmp_cert_months_to_first_lot", "value": GMP_CERT_MONTHS_TO_FIRST_LOT},
    ]
    line()

    # ---------- 11. Payback (DECISION_GATE: <= 5년) ----------
    print("\n[11] 투자 회수(Payback) — DECISION_GATE 기준 <= 5년")
    line()
    # 램프 계획 (가정 E-A10) · SKU 믹스 프리미엄 1.10 (1 mL 15% / 5 mL 40% / 10 mL 45%)
    SKU_MIX_UPLIFT = 0.15*SIZE_PREMIUM[1.0] + 0.40*SIZE_PREMIUM[5.0] + 0.45*SIZE_PREMIUM[10.0]
    ramp = [(2027, 40, "RUO"), (2028, 120, "RUO"), (2029, 260, "RUO"),
            (2030, 500, "RUO"), (2031, 700, "MIX"), (2032, 900, "MIX")]
    capex_sched = {2026: CAPEX_PILOT, 2029: CAPEX_COMMERCIAL, 2030: CAPEX_GMP}
    SGA_PCT = 0.25   # 판관비+R&D (가정 E-A10)
    print("SKU 믹스 ASP 배수 = 0.15x%.2f + 0.40x%.3f + 0.45x1.000 = %.3f  → 실효 ASP %.2f USD/mL"
          % (SIZE_PREMIUM[1.0], SIZE_PREMIUM[5.0], SKU_MIX_UPLIFT, ASP_ANCHORS["base"]*SKU_MIX_UPLIFT))
    print("%-6s %8s %12s %12s %10s %12s %12s %14s" %
          ("연도", "물량(L)", "매출(USD)", "COGS(USD)", "GM%", "판관비·R&D", "CAPEX", "누적FCF(USD)"))
    line(".")
    cum = -capex_sched.get(2026, 0.0)
    print("%-6s %8s %12s %12s %10s %12s %12s %14s" %
          (2026, "-", "-", "-", "-", "-", CM(capex_sched[2026]), CM(cum)))
    payback_year = None
    for yr, L, mode in ramp:
        gmix = "GMP" if mode == "MIX" else "RUO"
        r = cogs(L, "RUO", sku_mL=10.0, laminin=False)
        sellable = L * 1000 * r["yield"]
        asp_eff = ASP_ANCHORS["base"] * SKU_MIX_UPLIFT
        if mode == "MIX":   # 2031~ GMP 20% 믹스 (Agent B: GMP 매출 비중 2029까지 10% 미만)
            rg = cogs(L, "GMP", sku_mL=10.0, laminin=False)
            rev = sellable*0.8*asp_eff + sellable*0.2*asp_eff*GMP_MULTIPLE
            cg = sellable*0.8*r["cogs_ml"] + sellable*0.2*rg["cogs_ml"]
        else:
            rev = sellable * asp_eff
            cg = sellable * r["cogs_ml"]
        gp = rev - cg
        sga = rev * SGA_PCT
        cap = capex_sched.get(yr, 0.0)
        fcf = gp - sga - cap
        cum += fcf
        if payback_year is None and cum >= 0:
            payback_year = yr
        print("%-6s %8d %12s %12s %9.1f%% %12s %12s %14s" %
              (yr, L, CM(rev), CM(cg), gp/rev*100, CM(sga), CM(cap) if cap else "-", CM(cum)))
        rows_csv.append({"section": "Payback", "key": "%d_revenue_usd" % yr, "value": round(rev, 0)})
        rows_csv.append({"section": "Payback", "key": "%d_cum_fcf_usd" % yr, "value": round(cum, 0)})
    line(".")
    if payback_year:
        yrs = payback_year - 2026
        print("→ 투자 회수 연도 = %d (투자 개시 2026 기준 %d년) → DECISION_GATE(<=5년) %s"
              % (payback_year, yrs, "PASS" if yrs <= 5 else "FAIL"))
    else:
        print("→ 2032년까지 누적 FCF 가 음수 — DECISION_GATE(<=5년) FAIL")
        yrs = 99
    rows_csv.append({"section": "Payback", "key": "payback_year", "value": payback_year})
    rows_csv.append({"section": "Payback", "key": "payback_years_from_2026", "value": yrs})
    line()

    # ---------- CSV ----------
    outdir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "cogs_output.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["section", "key", "value"])
        w.writeheader()
        for r in rows_csv:
            w.writerow(r)
    print("\n[CSV] %s 에 %d행 기록 완료." % (path, len(rows_csv)))

    # ---------- HANDOFF ----------
    print("\n[HANDOFF]")
    line()
    D = DESIGN_VOLUME_L
    hv = {
        "design_volume_L_per_year": D,
        "asp_base_usd_per_mL_10mL": ASP_ANCHORS["base"],
        "cogs_usd_per_mL_ruo": round(cogs(D, "RUO", sku_mL=10.0)["cogs_ml"], 3),
        "cogs_usd_per_mL_gmp": round(cogs(D, "GMP", sku_mL=10.0)["cogs_ml"], 3),
        "cogs_usd_per_mL_ruo_ramp100L": round(scen["RUO_nolam"]["cogs_ml"], 3),
        "cogs_usd_per_mL_gmp_ramp100L": round(scen["GMP_nolam"]["cogs_ml"], 3),
        "gm_pct_1mL": round(gm_pct(asp_for(1.0, 32.00), cogs(D, "RUO", sku_mL=1.0)["cogs_ml"]), 1),
        "gm_pct_5mL": round(gm_pct(asp_for(5.0, 32.00), cogs(D, "RUO", sku_mL=5.0)["cogs_ml"]), 1),
        "gm_pct_10mL": round(gm_pct(asp_for(10.0, 32.00), cogs(D, "RUO", sku_mL=10.0)["cogs_ml"]), 1),
        "gm_pct_1mL_ramp100L": round(gm_pct(asp_for(1.0, 32.00), cogs(100, "RUO", sku_mL=1.0)["cogs_ml"]), 1),
        "gm_pct_5mL_ramp100L": round(gm_pct(asp_for(5.0, 32.00), cogs(100, "RUO", sku_mL=5.0)["cogs_ml"]), 1),
        "gm_pct_10mL_ramp100L": round(gm_pct(asp_for(10.0, 32.00), cogs(100, "RUO", sku_mL=10.0)["cogs_ml"]), 1),
        "min_volume_L_for_GM60": round(v60, 1),
        "bep_volume_L_per_year": round(bep(D, "RUO", 32.00, sku_mL=10.0)["bep_L"], 1),
        "bep_revenue_usd": round(bep(D, "RUO", 32.00, sku_mL=10.0)["bep_rev"], 0),
        "bep_volume_L_per_year_ramp100L": round(bep(100, "RUO", 32.00, sku_mL=10.0)["bep_L"], 1),
        "bep_revenue_usd_ramp100L": round(bep(100, "RUO", 32.00, sku_mL=10.0)["bep_rev"], 0),
        "capex_pilot_usd": round(CAPEX_PILOT, 0),
        "capex_total_usd": round(CAPEX_ALL, 0),
        "gmp_cert_months": GMP_CERT_MONTHS_FACILITY,
        "gmp_over_ruo_cost_multiple_at_design": round(cogs(D,"GMP",sku_mL=10.0)["cogs_ml"]/cogs(D,"RUO",sku_mL=10.0)["cogs_ml"], 3),
        "laminin_impact_usd_per_mL_internal": round(scen["RUO_lam_int"]["cogs_ml"] - scen["RUO_nolam"]["cogs_ml"], 3),
        "laminin_impact_usd_per_mL_catalog": round(scen["RUO_lam_cat"]["cogs_ml"] - scen["RUO_nolam"]["cogs_ml"], 3),
        "laminin_conc_required_mg_per_mL": LAMININ_CONC_MG_PER_ML,
        "matrigel_cogs_usd_per_mL_est": round(matrigel_cogs_ml, 3),
    }
    for k, v in hv.items():
        print("  %-38s %s" % (k, v))
        rows_csv.append({"section": "HANDOFF", "key": k, "value": v})
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["section", "key", "value"])
        w.writeheader()
        for r in rows_csv:
            w.writerow(r)
    line()


if __name__ == "__main__":
    main()
