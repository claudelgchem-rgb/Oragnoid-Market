#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSVX Agent A — 오가노이드 지지체(3D 매트릭스) 시장규모 모델
=============================================================
금액(USD) + 물량(L/년) 동시 산출. 세그먼트 5 × 지역 6 × 연도 2025~2035.

실행:  python3 model/market_model.py [bear|base|bull]
출력:  stdout 표 + data/market_model_output.csv

표준 라이브러리만 사용 (외부 의존 없음).
모든 입력 파라미터는 아래 PARAMS 섹션에 노출되어 있으며 각 값에 [E-###] 근거 ID 주석이 붙는다.
선행 에이전트 근거([E-0xx] B / [E-1xx] C / [E-2xx] D)는 인용, 신규 근거는 [E-3xx].
"""

import csv
import os
import sys

# =====================================================================
# PARAMS — 전 입력 파라미터 (각 값 옆 [E-###])
# =====================================================================

SCENARIOS = ("bear", "base", "bull")

YEARS = list(range(2025, 2036))
REPORT_YEARS = (2025, 2026, 2030, 2035)

SEGMENTS = (
    "academic_ruo",            # 학술연구(RUO)
    "pharma_preclinical_nam",  # 제약 전임상 NAM 스크리닝
    "organoid_cro_biobank",    # 오가노이드 CRO/바이오뱅크
    "clinical_dx_pdo",         # 임상진단 (PDO 약물감수성)
    "regenerative_gmp",        # 재생의료/이식용 (GMP)
)

REGIONS = ("US", "EU", "China", "Japan", "Korea", "RoW")   # Global = 합계

# ---------------------------------------------------------------------
# 1. 지역 가중 — PubMed organoid 2025 affiliation 실측 (fractional attribution)
#    US 1393 / EU+CH+NO 1536 / China 1990 / Japan 321 / Korea 288 / RoW 1164
#    Σ = 6692                                                        [E-305]
# ---------------------------------------------------------------------
REGION_PUB_COUNT_2025 = {
    "US": 1393,      # [E-305] PubMed esearch organoid AND 2025[dp] AND (United States[ad] OR USA[ad])
    "EU": 1536,      # [E-305] EU-27 + CH + NO OR-query (중복 제거된 unique count)
    "China": 1990,   # [E-305]
    "Japan": 321,    # [E-305]
    "Korea": 288,    # [E-305]
    "RoW": 1164,     # [E-305] UK368+CA165+AU136+IN117+SG62+TW55+IL63+BR46=1012, 기타 +15% → 1164 (가정 A-A05)
}

# 제약 전임상은 논문 수가 아니라 제약 R&D 집중도로 가중 (GERD + 파이프라인 소재지)  [E-326][E-321]
REGION_WEIGHT_PHARMA = {"US": 0.45, "EU": 0.25, "China": 0.15, "Japan": 0.07, "Korea": 0.03, "RoW": 0.05}
# CRO/바이오뱅크: Tracxn 국가별 기업 수(US 37 / China 7 / UK 7 …) + 중국 로컬 CRO 실재  [E-322]
REGION_WEIGHT_CRO = {"US": 0.40, "EU": 0.20, "China": 0.22, "Japan": 0.06, "Korea": 0.05, "RoW": 0.07}
# 임상진단 PDO: ClinicalTrials.gov PDO 시험의 중국 편중 반영                            [E-308]
REGION_WEIGHT_CLIN = {"US": 0.25, "EU": 0.15, "China": 0.45, "Japan": 0.06, "Korea": 0.05, "RoW": 0.04}
# 재생의료 GMP: 세계 최초 인체 오가노이드 이식이 일본(TMDU 2022-07-05) [E-066, Agent B]
REGION_WEIGHT_GMP = {"US": 0.25, "EU": 0.20, "China": 0.10, "Japan": 0.40, "Korea": 0.05, "RoW": 0.00}

# ---------------------------------------------------------------------
# 2. 단가 (USD/mL) — Agent C 실측 42개 제품 (data/price_table.csv)
# ---------------------------------------------------------------------
ASP_BME_USD_PER_ML = 48.24        # [E-161, Agent C] median(undefined-BME, n=14)
ASP_DEFINED_USD_PER_ML = 60.47    # [E-161, Agent C] median(fully-defined, n=14) — p=0.168 유의성 없음
ASP_GMP_USD_PER_ML = 117.43       # [E-160][E-159, Agent C] = 60.47 × 1.942
CHINA_LOCAL_USD_PER_ML = 21.30    # [E-125, Agent C] Yeasen Ceturegel 40192ES

# 세그먼트별 실지불 단가 배수 (대량계약 할인). 학술=정가, 제약 0.85, CRO 0.75 (COGS 민감)
SEG_ASP_BASE = {
    "academic_ruo":           ASP_BME_USD_PER_ML,          # [E-161]
    "pharma_preclinical_nam": ASP_BME_USD_PER_ML * 0.85,   # 가정 A-A08
    "organoid_cro_biobank":   ASP_BME_USD_PER_ML * 0.75,   # 가정 A-A08
    "clinical_dx_pdo":        ASP_BME_USD_PER_ML,          # 가정 A-A08
    "regenerative_gmp":       ASP_GMP_USD_PER_ML,          # [E-160]
}
# 지역 단가 배수. China = 21.30/48.24 = 0.4415 실측                       [E-125][E-161]
REGION_ASP_MULT = {"US": 1.00, "EU": 1.00, "China": 0.4415, "Japan": 0.95, "Korea": 0.90, "RoW": 0.80}

# 실질 단가 추세 (중국 로컬 침투 + Corning Synthegel $37.08 방어가격)      [E-125][E-130, Agent C]
ASP_DRIFT_PER_YEAR = {"bear": -0.040, "base": -0.020, "bull": 0.000}      # 가정 A-A09

# ---------------------------------------------------------------------
# 3. 세그먼트 모집단 (2025 기준값)
# ---------------------------------------------------------------------
# 3.1 학술 랩 수 — 2경로 수렴
#   경로A: NIH FY2025 organoid 과제 908 / PI당 1.3과제 = 698 PI ÷ NIH 커버리지 0.65
#          = 1,074 US 랩 ÷ US 논문 점유 0.2082 = 5,163
#   경로B: PubMed organoid 2025 5,492 × 학술비중 0.88 ÷ 랩당 1.30편 × 미발표 계수 1.35 = 5,019
#   → 중앙 5,100                                       [E-300][E-306][E-305] 가정 A-A01~A-A04
ACADEMIC_LABS_GLOBAL_2025 = 5100

# 3.2 제약 전임상 — 전임상 단계 자산 수 (Citeline)                          [E-321]
PRECLINICAL_ASSETS_2025 = 12704
PRECLINICAL_ASSET_GROWTH = {"bear": -0.005, "base": 0.015, "bull": 0.030}  # [E-320] 2026 파이프라인 소폭 감소

# 3.3 CRO/바이오뱅크 — Tracxn 오가노이드 연구모델 기업 107 + 대형 CRO 오가노이드 조직 25
CRO_ORGS_2025 = 132                                                        # [E-322] 가정 A-A06

# 3.4 임상진단 PDO — 연간 PDO 검사 건수
#   ClinicalTrials.gov "patient-derived organoid" 214건 × 검체 40건/년 = 8,560
#   + 상용 CLIA 검사(SEngine PARIS 등) 추정 1,440 = 10,000                 [E-308][E-333] 가정 A-A07
PDO_TESTS_2025 = 10000

# 3.5 재생의료 GMP — 오가노이드 이식 개입시험 수 (≤4건, 최고 Phase 2)       [E-067, Agent B]
GMP_TRIALS_2025 = 4

# ---------------------------------------------------------------------
# 4. 단위당 매트릭스 소모량 (mL/년)
# ---------------------------------------------------------------------
# 4.1 학술 랩: dome 배양 50 µL/well (24-well) [E-309]
#     유지 = 12 well/line/주 × 50 µL × 52주 × 3 line = 93.6 mL
#     실험 = 20회/년 × 36 well × 50 µL          = 36.0 mL
#     합계 129.6 → 130 mL/lab/년 (= 10 mL 병 13개)                         [E-309][E-310] 가정 A-A10
ML_PER_ACADEMIC_LAB_YEAR = 130.0

# 4.2 제약 프로그램: HTS 384-well 6 µL/well [E-311]
#     스크리닝 40 plate × 320 well × 6 µL = 76.8 mL
#     모델 확립·확장 5 line × 31.2 mL      = 156.0 mL
#     2차/검증                              = 100.0 mL
#     합계 332.8 → 330 mL/program/년                                       [E-311][E-309] 가정 A-A11
ML_PER_PHARMA_PROGRAM_YEAR = 330.0

# 4.3 CRO 조직당 (산업 규모, 중앙값. 상위 소수에 심하게 편중)               가정 A-A12
ML_PER_CRO_ORG_YEAR = 1800.0

# 4.4 PDO 검사 1건 (생검→확장 48 well + 384-well 약물패널)                  [E-309][E-311] 가정 A-A13
ML_PER_PDO_TEST = 2.5

# 4.5 GMP 이식 시험 1건/년 (배치 제조 + 공정 검증)                          가정 A-A14
ML_PER_GMP_TRIAL_YEAR = 200.0

# ---------------------------------------------------------------------
# 5. 성장률
# ---------------------------------------------------------------------
# 학술 랩 수 CAGR — 2개 독립 프록시:
#   NIH RePORTER organoid 과제 FY2020 508 → FY2025 908 : CAGR = (908/508)^(1/5)-1 = 12.3%  [E-307]
#   PubMed organoid 2020 2,141 → 2025 5,492            : CAGR = (5492/2141)^(1/5)-1 = 20.7% [E-302][E-300]
#   FY2024 939 → FY2025 908 = -3.3% 정체 신호 반영해 base = 12.3 × 0.75 ≈ 9.0%             [E-306][E-307]
ACADEMIC_LAB_CAGR_25_30 = {"bear": 0.040, "base": 0.090, "bull": 0.150}
ACADEMIC_LAB_CAGR_30_35 = {"bear": 0.020, "base": 0.045, "bull": 0.080}

CRO_ORG_CAGR_25_30 = {"bear": 0.080, "base": 0.150, "bull": 0.220}   # 가정 A-A15
CRO_ORG_CAGR_30_35 = {"bear": 0.040, "base": 0.100, "bull": 0.150}
PDO_TEST_CAGR_25_30 = {"bear": 0.120, "base": 0.250, "bull": 0.400}  # 가정 A-A16
PDO_TEST_CAGR_30_35 = {"bear": 0.080, "base": 0.200, "bull": 0.320}

# ---------------------------------------------------------------------
# 6. NAM 램프 (Agent B HANDOFF H1) — 스텝 변화 금지, 기하 보간
#    정의: 제약 전임상 프로그램 중 complex 3D 인체모델 데이터를 실제 규제제출에 포함하는 비율
# ---------------------------------------------------------------------
NAM_RAMP = {                                                          # [E-078, Agent B]
    "bear": {2026: 0.04, 2030: 0.12, 2035: 0.25},   # conservative
    "base": {2026: 0.08, 2030: 0.25, 2035: 0.45},
    "bull": {2026: 0.12, 2030: 0.40, 2035: 0.65},   # aggressive
}

# ---------------------------------------------------------------------
# 7. GMP/이식 트랙 (Agent B HANDOFF H4) — clinical_timing_year
# ---------------------------------------------------------------------
CLINICAL_TIMING_YEAR = {"bear": 2036, "base": 2033, "bull": 2031}     # [E-079, Agent B]
GMP_TRIAL_CAGR_PRE = {"bear": 0.25, "base": 0.45, "bull": 0.65}       # 승인 전 임상 진입 증가율 가정 A-A17
GMP_TRIAL_CAGR_POST = {"bear": 0.20, "base": 0.35, "bull": 0.50}      # 최초 승인 후 가속 가정 A-A17

# ---------------------------------------------------------------------
# 8. Addressable subset — 기술적 대체가능 비율 (Agent D 효능 격차 근거)
#    장기 믹스: 소장 28.65% [E-336] + 간 23.34% [E-335] + 위 5% = 57% (동등성 입증 장기)
#    입증 장기 대체가능 0.80 / 미입증(뇌·신장·폐·췌장내분비·종양PDO) 0.35
#    → 0.57×0.80 + 0.43×0.35 = 0.607
#    2024년까지 모든 합성 매트릭스가 외인성 라미닌 필수 [E-231, Agent D]
# ---------------------------------------------------------------------
ADDRESSABLE_RATIO = {
    "academic_ruo":           0.61,   # [E-231][E-336][E-335] 가정 A-A18
    "pharma_preclinical_nam": 0.55,   # 종양 PDO 비중 높아 하향
    "organoid_cro_biobank":   0.50,   # 7장기 커버리지 요구 [E-260, Agent D]
    "clinical_dx_pdo":        0.45,   # 종양 PDO 중심, 동등성 입증 최소
    "regenerative_gmp":       1.00,   # Matrigel 사용 자체 불가 [E-240, Agent D]
}
# LG화학 제품(콜라겐+mTG, 라미닌 부재) 고유 감쇠 = 1 − B6 효능격차 발생확률 0.40
LG_EFFICACY_FACTOR = 0.60                                             # [E-231][D-A07, Agent D]

# ---------------------------------------------------------------------
# 9. SAM — "증분 지출 수용률" 모델 (Agent D 강제 지시)
#    SAM 은 Matrigel 잠식률이 아니다. 전환 후에도 리뷰어가 Matrigel 대조군을 요구하므로
#    우리 제품은 기존 지출 위에 얹히는 증분 지출이 된다. [E-239][E-238][E-237, Agent D]
# ---------------------------------------------------------------------
SWITCH_PROPENSITY = {                                                 # [E-263, Agent D] %/년
    "academic_ruo":           0.060,
    "pharma_preclinical_nam": 0.083,
    "organoid_cro_biobank":   0.027,
    "clinical_dx_pdo":        0.032,
    "regenerative_gmp":       0.250,
}
SWITCH_MULT = {"bear": 0.70, "base": 1.00, "bull": 1.50}              # 시나리오 감도 가정 A-A19
ENTRY_YEAR = 2026                                                     # LG 시장 진입 연도
INCREMENTAL_SPEND_RATIO = {"bear": 0.55, "base": 0.70, "bull": 0.85}  # 가정 A-A20

# ---------------------------------------------------------------------
# 10. SOM — LG화학 5년차(2030) 현실 점유율
#     근거: defined 대체재 7종 PubMed 합계 292건 = Matrigel 의 1.95% [E-152, Agent C];
#     그중 PuraMatrix 단독 228건(78%) — 20년 걸린 결과.
#     신규 진입 5년차에 defined 카테고리 내 10~15%가 현실 상한.
#     GMP 구간은 공개 정가 제품 0개 = 미점유 [E-160, Agent C] → 점유율 상향.
# ---------------------------------------------------------------------
LG_SHARE_RUO = {"bear": 0.05, "base": 0.12, "bull": 0.22}             # 가정 A-A21
LG_SHARE_GMP = {"bear": 0.10, "base": 0.25, "bull": 0.40}             # 가정 A-A21

# ---------------------------------------------------------------------
# 11. 경로2·경로3 삼각측량 상수 (문서 병기용)
# ---------------------------------------------------------------------
PATH2_ORGANOID_MARKET_2025_USD = 1_180_000_000    # 5개 보고서 중앙값 [E-312][E-314][E-315][E-319]
PATH2_MATRIX_SHARE = 0.195                        # (1-0.5121 조직모델비중)×0.40 [E-335] 가정 A-A22
PATH3_MATRIGEL_CATEGORY_2024_USD = 97_000_000     # QYResearch Matrigel(BME) 카테고리 [E-318]
PATH3_MATRIGEL_CAGR = 0.112                       # [E-318]
PATH3_DEFINED_REV_SHARE = 0.08                    # defined 대체재 매출 점유 가정 A-A23 [E-152]
PATH3_ACADEMIC_APP_SHARE = 0.28                   # QYR 응용 분할: 학술·연구기관 28% (상용 72%) [E-318]


# =====================================================================
# 계산 엔진
# =====================================================================

def cagr(end, start, n):
    """CAGR = (End/Start)^(1/n) - 1"""
    if start <= 0 or n <= 0:
        return 0.0
    return (end / start) ** (1.0 / n) - 1.0


def geometric_ramp(anchors, year):
    """3점 앵커(2026/2030/2035)를 구간별 기하 보간해 연속 램프 함수로 만든다.
       ramp(t) = ramp(t0) * ((ramp(t1)/ramp(t0))^(1/(t1-t0)))^(t-t0)   — 스텝 변화 금지."""
    ys = sorted(anchors)
    y0, y1, y2 = ys[0], ys[1], ys[2]
    if year <= y0:
        g = cagr(anchors[y1], anchors[y0], y1 - y0)
        return anchors[y0] * (1 + g) ** (year - y0)
    if year <= y1:
        g = cagr(anchors[y1], anchors[y0], y1 - y0)
        return anchors[y0] * (1 + g) ** (year - y0)
    g = cagr(anchors[y2], anchors[y1], y2 - y1)
    return anchors[y1] * (1 + g) ** (year - y1)


def grow(base_val, year, g_25_30, g_30_35):
    if year <= 2030:
        return base_val * (1 + g_25_30) ** (year - 2025)
    v2030 = base_val * (1 + g_25_30) ** 5
    return v2030 * (1 + g_30_35) ** (year - 2030)


def region_weights_academic():
    tot = sum(REGION_PUB_COUNT_2025.values())
    return {r: REGION_PUB_COUNT_2025[r] / tot for r in REGIONS}


def units_by_year(scenario, year):
    """세그먼트별 모집단 단위 수."""
    u = {}
    u["academic_ruo"] = grow(ACADEMIC_LABS_GLOBAL_2025, year,
                             ACADEMIC_LAB_CAGR_25_30[scenario], ACADEMIC_LAB_CAGR_30_35[scenario])

    assets = PRECLINICAL_ASSETS_2025 * (1 + PRECLINICAL_ASSET_GROWTH[scenario]) ** (year - 2025)
    ramp = geometric_ramp(NAM_RAMP[scenario], year)
    u["pharma_preclinical_nam"] = assets * ramp

    u["organoid_cro_biobank"] = grow(CRO_ORGS_2025, year,
                                     CRO_ORG_CAGR_25_30[scenario], CRO_ORG_CAGR_30_35[scenario])
    u["clinical_dx_pdo"] = grow(PDO_TESTS_2025, year,
                                PDO_TEST_CAGR_25_30[scenario], PDO_TEST_CAGR_30_35[scenario])

    ct = CLINICAL_TIMING_YEAR[scenario]
    if year <= ct:
        n = GMP_TRIALS_2025 * (1 + GMP_TRIAL_CAGR_PRE[scenario]) ** (year - 2025)
    else:
        n_ct = GMP_TRIALS_2025 * (1 + GMP_TRIAL_CAGR_PRE[scenario]) ** (ct - 2025)
        n = n_ct * (1 + GMP_TRIAL_CAGR_POST[scenario]) ** (year - ct)
    u["regenerative_gmp"] = n
    return u


ML_PER_UNIT = {
    "academic_ruo": ML_PER_ACADEMIC_LAB_YEAR,
    "pharma_preclinical_nam": ML_PER_PHARMA_PROGRAM_YEAR,
    "organoid_cro_biobank": ML_PER_CRO_ORG_YEAR,
    "clinical_dx_pdo": ML_PER_PDO_TEST,
    "regenerative_gmp": ML_PER_GMP_TRIAL_YEAR,
}


def segment_region_weights(seg):
    if seg == "academic_ruo":
        return region_weights_academic()
    if seg == "pharma_preclinical_nam":
        return REGION_WEIGHT_PHARMA
    if seg == "organoid_cro_biobank":
        return REGION_WEIGHT_CRO
    if seg == "clinical_dx_pdo":
        return REGION_WEIGHT_CLIN
    return REGION_WEIGHT_GMP


def cumulative_adoption(seg, year, scenario):
    """증분 지출 수용률의 시간축: 누적채택 = 1 - (1 - P)^(t)
       t = year - ENTRY_YEAR + 1 (진입 연도에 1년치 전환 창이 열린다고 본다)."""
    if year < ENTRY_YEAR:
        return 0.0
    t = year - ENTRY_YEAR + 1
    p = min(0.95, SWITCH_PROPENSITY[seg] * SWITCH_MULT[scenario])
    return 1.0 - (1.0 - p) ** t


def build(scenario):
    rows = []
    drift = ASP_DRIFT_PER_YEAR[scenario]
    inc = INCREMENTAL_SPEND_RATIO[scenario]
    for year in YEARS:
        units = units_by_year(scenario, year)
        for seg in SEGMENTS:
            w = segment_region_weights(seg)
            asp_base = SEG_ASP_BASE[seg] * (1 + drift) ** (year - 2025)
            for reg in REGIONS:
                u = units[seg] * w[reg]
                vol_ml = u * ML_PER_UNIT[seg]
                vol_L = vol_ml / 1000.0
                asp = asp_base * REGION_ASP_MULT[reg]
                tam = vol_ml * asp

                add_ratio = ADDRESSABLE_RATIO[seg]
                tam_add = tam * add_ratio
                tam_add_L = vol_L * add_ratio

                sam_naive = tam_add                                   # 전환확률 미반영 (참고용)
                adopt = cumulative_adoption(seg, year, scenario)
                sam_adj = tam_add * adopt * inc
                sam_adj_L = tam_add_L * adopt * inc

                lg_share = LG_SHARE_GMP[scenario] if seg == "regenerative_gmp" else LG_SHARE_RUO[scenario]
                som_pre = sam_adj * lg_share                      # LG 효능격차 감쇠 적용 전
                som = som_pre * LG_EFFICACY_FACTOR                # 라미닌 부재 리스크 반영 후
                som_L = sam_adj_L * lg_share * LG_EFFICACY_FACTOR

                rows.append({
                    "scenario": scenario, "year": year, "segment": seg, "region": reg,
                    "units": round(u, 2),
                    "asp_usd_per_mL": round(asp, 3),
                    "volume_L": round(vol_L, 4),
                    "TAM_usd": round(tam, 0),
                    "TAM_addressable_usd": round(tam_add, 0),
                    "TAM_addressable_L": round(tam_add_L, 4),
                    "SAM_naive_usd": round(sam_naive, 0),
                    "cum_adoption": round(adopt, 4),
                    "SAM_adjusted_usd": round(sam_adj, 0),
                    "SAM_adjusted_L": round(sam_adj_L, 4),
                    "SOM_pre_efficacy_usd": round(som_pre, 0),
                    "SOM_usd": round(som, 0),
                    "SOM_L": round(som_L, 4),
                })
    return rows


def agg(rows, year=None, seg=None, reg=None, key="TAM_usd"):
    s = 0.0
    for r in rows:
        if year is not None and r["year"] != year:
            continue
        if seg is not None and r["segment"] != seg:
            continue
        if reg is not None and r["region"] != reg:
            continue
        s += r[key]
    return s


def money(x):
    return "%10.2f" % (x / 1e6)


def main():
    scenario = sys.argv[1] if len(sys.argv) > 1 else "base"
    if scenario not in SCENARIOS:
        print("usage: python3 model/market_model.py [bear|base|bull]")
        sys.exit(1)

    rows = build(scenario)

    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)
    outdir = os.path.join(root, "data")
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, "market_model_output.csv")

    all_rows = []
    for sc in SCENARIOS:
        all_rows.extend(rows if sc == scenario else build(sc))
    with open(outpath, "w", newline="", encoding="utf-8") as f:
        wcsv = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()))
        wcsv.writeheader()
        wcsv.writerows(all_rows)

    print("=" * 108)
    print("OSVX Agent A — 오가노이드 3D 매트릭스 시장 모델   scenario = %s   (금액 단위: 백만 USD, 물량: L/년)" % scenario)
    print("=" * 108)

    # ---- 표1: 세그먼트 × 연도 (금액 + 물량)
    print("\n[표1] TAM  세그먼트 × 연도")
    hdr = "%-26s" % "segment"
    for y in REPORT_YEARS:
        hdr += "%12d USD" % y + "%11d L" % y
    print(hdr)
    print("-" * 108)
    for seg in SEGMENTS:
        line = "%-26s" % seg
        for y in REPORT_YEARS:
            line += money(agg(rows, year=y, seg=seg, key="TAM_usd")) + "    "
            line += "%10.1f " % agg(rows, year=y, seg=seg, key="volume_L")
        print(line)
    line = "%-26s" % "TOTAL (Global)"
    for y in REPORT_YEARS:
        line += money(agg(rows, year=y, key="TAM_usd")) + "    "
        line += "%10.1f " % agg(rows, year=y, key="volume_L")
    print(line)

    # ---- 표2: 지역 × 연도
    print("\n[표2] TAM  지역 × 연도")
    hdr = "%-26s" % "region"
    for y in REPORT_YEARS:
        hdr += "%12d USD" % y + "%11d L" % y
    print(hdr)
    print("-" * 108)
    for reg in REGIONS:
        line = "%-26s" % reg
        for y in REPORT_YEARS:
            line += money(agg(rows, year=y, reg=reg, key="TAM_usd")) + "    "
            line += "%10.1f " % agg(rows, year=y, reg=reg, key="volume_L")
        print(line)
    line = "%-26s" % "Global"
    for y in REPORT_YEARS:
        line += money(agg(rows, year=y, key="TAM_usd")) + "    "
        line += "%10.1f " % agg(rows, year=y, key="volume_L")
    print(line)

    # ---- 표3: TAM / Addressable / SAM(전·후) / SOM
    print("\n[표3] TAM → Addressable → SAM(전환확률 반영 전/후) → SOM   (백만 USD / L)")
    print("%-34s%s" % ("metric", "".join("%16d" % y for y in REPORT_YEARS)))
    print("-" * 108)
    metrics = [
        ("TAM (USD M)", "TAM_usd", 1e6),
        ("TAM 물량 (L/년)", "volume_L", 1.0),
        ("TAM_addressable (USD M)", "TAM_addressable_usd", 1e6),
        ("TAM_addressable 물량 (L/년)", "TAM_addressable_L", 1.0),
        ("SAM_naive 전환確 미반영 (USD M)", "SAM_naive_usd", 1e6),
        ("SAM_adjusted 반영후 (USD M)", "SAM_adjusted_usd", 1e6),
        ("SAM_adjusted 물량 (L/년)", "SAM_adjusted_L", 1.0),
        ("SOM 효능감쇠 전 (USD M)", "SOM_pre_efficacy_usd", 1e6),
        ("SOM (USD M)", "SOM_usd", 1e6),
        ("SOM 물량 (L/년)", "SOM_L", 1.0),
    ]
    for label, key, div in metrics:
        line = "%-34s" % label
        for y in REPORT_YEARS:
            line += "%16.2f" % (agg(rows, year=y, key=key) / div)
        print(line)

    naive30 = agg(rows, year=2030, key="SAM_naive_usd")
    adj30 = agg(rows, year=2030, key="SAM_adjusted_usd")
    print("\n  → SAM 과대평가 배수 (2030) = SAM_naive / SAM_adjusted = %.2f 배" % (naive30 / adj30 if adj30 else 0))

    # ---- 표4: CAGR (직접 계산)
    print("\n[표4] CAGR = (End/Start)^(1/n) - 1  — 직접 계산")
    for label, key in (("TAM USD", "TAM_usd"), ("TAM 물량 L", "volume_L"),
                       ("SAM_adjusted USD", "SAM_adjusted_usd"), ("SOM USD", "SOM_usd")):
        a25 = agg(rows, year=2025, key=key)
        a26 = agg(rows, year=2026, key=key)
        a30 = agg(rows, year=2030, key=key)
        a35 = agg(rows, year=2035, key=key)
        def fmt(end, start, n):
            if start <= 0:
                return "  n/a*"   # * 진입 전(2025) 값이 0 → CAGR 정의 불가
            return "%6.2f%%" % (cagr(end, start, n) * 100)
        print("  %-20s 25→30 %s   30→35 %s   25→35 %s   26→35 %s"
              % (label, fmt(a30, a25, 5), fmt(a35, a30, 5), fmt(a35, a25, 10), fmt(a35, a26, 9)))
    print("  * SAM/SOM 의 2025 값은 0 (LG 진입연도 = %d) 이므로 2025 기산 CAGR 은 정의되지 않는다." % ENTRY_YEAR)

    # ---- 표5: NAM 램프 (연속 함수 확인 — 스텝 없음)
    print("\n[표5] nam_ramp(t) 기하 보간 (%s) — 제약 세그먼트 구동 함수" % scenario)
    print("  " + "  ".join("%d:%5.1f%%" % (y, geometric_ramp(NAM_RAMP[scenario], y) * 100) for y in YEARS))

    # ---- 표6: 3경로 삼각측량
    print("\n[표6] 3경로 삼각측량 (2025 기준, 백만 USD)")
    p1 = agg(rows, year=2025, key="TAM_usd")
    p1_acad = agg(rows, year=2025, seg="academic_ruo", key="TAM_usd")
    p1_L = agg(rows, year=2025, key="volume_L")
    p2 = PATH2_ORGANOID_MARKET_2025_USD * PATH2_MATRIX_SHARE
    p3_total = PATH3_MATRIGEL_CATEGORY_2024_USD * (1 + PATH3_MATRIGEL_CAGR) / (1 - PATH3_DEFINED_REV_SHARE)
    p3_acad = p3_total * PATH3_ACADEMIC_APP_SHARE
    blended_asp = p1 / (p1_L * 1000.0)
    print("  경로1 Bottom-up  (오가노이드 스코프)      : %8.1f M USD  /  %7.1f L  (블렌디드 ASP %.2f USD/mL)"
          % (p1 / 1e6, p1_L, blended_asp))
    print("  경로2 Top-down   (시장보고서 × 매트릭스비중): %8.1f M USD  /   물량 미제공 → 부적합"
          % (p2 / 1e6))
    print("  경로3 Proxy      (전체 3D 매트릭스 스코프)  : %8.1f M USD  /  %7.1f L (블렌디드 ASP 역산)"
          % (p3_total / 1e6, p3_total / blended_asp / 1000.0))
    print("  ── 동일 스코프 비교 (학술 세그먼트) ──")
    print("     경로1 학술 %.1f M USD  vs  경로3 학술(QYR 응용분할 28%%) %.1f M USD  → 편차 %.2f 배"
          % (p1_acad / 1e6, p3_acad / 1e6, max(p1_acad, p3_acad) / min(p1_acad, p3_acad)))
    print("     경로1 전체 %.1f M USD  vs  경로2 %.1f M USD  → 편차 %.2f 배  (2배 초과 → gaps.md)"
          % (p1 / 1e6, p2 / 1e6, max(p1, p2) / min(p1, p2)))

    # ---- 표7: DECISION_GATE 판정
    print("\n[표7] DECISION_GATE 판정")
    sam30 = agg(rows, year=2030, key="SAM_adjusted_usd")
    som30 = agg(rows, year=2030, key="SOM_usd")
    print("  SAM_2030 = %10.2f M USD   기준 150.00 M USD   → %s" % (sam30 / 1e6, "PASS" if sam30 >= 150e6 else "FAIL"))
    print("  SOM_2030 = %10.2f M USD   기준  15.00 M USD   → %s" % (som30 / 1e6, "PASS" if som30 >= 15e6 else "FAIL"))

    print("\nCSV 기록: %s   (행 수 %d, 3 시나리오 전량)" % (outpath, len(all_rows)))


if __name__ == "__main__":
    main()
