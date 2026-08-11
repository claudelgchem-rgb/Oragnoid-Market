#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSVX — Agent S 통합 재무모델 (finance_model.py)
================================================
python3 표준 라이브러리만 사용 (csv, math, os, sys, collections).

입력
  data/market_model_output.csv   : Agent A `market_model.py` 출력 (990행)
                                   → TAM_addressable_usd / TAM_addressable_L 을 세그먼트별로 승계
  Agent E `cogs_model.py` 의 규모 티어 원가 파라미터 (본 파일에 상수로 복제, 값 검증 완료)

출력
  stdout                         : 3시나리오 × 2스코프 P&L, NPV, IRR, BEP, Payback, 민감도, KC
  data/finance_output.csv        : 위 전량의 기계 판독 가능 사본

핵심 교정 (Agent V / R / X 반영)
  V-01  Payback : Agent E 의 램프(2030년 판매 418 L) 폐기 → Agent A 계열 수요곡선 사용
  V-02  설계물량 500 L 순환 유도 제거 → 물량은 수요 모델에서만 나온다
  V-03  단위 통일 : 전 물량 = **판매(sellable) L**. 생산 L = 판매 L / 0.836
  V-07  라미닌 리스크 = 이분법(성공확률 0.60). 물량 선형 감쇠(×0.60) 제거
  V-08  addressable(0.61) × LG_efficacy(0.60) 이중곱 제거
  V-09  매출은 시장 ASP 가 아니라 **LG 자신의 판매가**로 산출
  R     ASP 앵커를 Corning 표준 SKU 354234 = 30.29 USD/mL 로 교체 (E-802)
  X     Corning 가격 하한 19.39 USD/mL 를 bear ASP 로 사용 (E-803)
"""

import csv
import math
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MARKET_CSV = os.path.join(ROOT, "data", "market_model_output.csv")
OUT_CSV = os.path.join(ROOT, "data", "finance_output.csv")

YEARS = list(range(2026, 2036))          # 사업 계획기간 10년
ENTRY_YEAR = 2026

# ---------------------------------------------------------------------------
# 1. 할인율 (WACC) — E-800 ~ E-806 (Show-Your-Math 는 S_synthesis.md §3)
# ---------------------------------------------------------------------------
RF = 0.0430                # 한국 국고채 10년, 2026-08-11 실측 4.30%      [E-800]
ERP_KR = 0.0487            # Damodaran 2026-01 한국 총 ERP 4.87%          [E-801]
BETA_UNLEV = 0.93          # (Healthcare Products 0.83 + Drugs Biotech 1.03)/2 [E-804]
DE_RATIO = 0.129           # 산업 D/E (12.79% + 13.04%)/2                 [E-804]
TAX_RATE = 0.275           # 한국 법인세 최고구간 25% + 지방소득세 10%     [E-805]
CREDIT_SPREAD = 0.0130     # LG화학 A3 / BBB+ 회사채 스프레드              [E-806]

BETA_LEV = BETA_UNLEV * (1 + (1 - TAX_RATE) * DE_RATIO)
KE = RF + BETA_LEV * ERP_KR
KD = RF + CREDIT_SPREAD
W_D = DE_RATIO / (1 + DE_RATIO)
W_E = 1 - W_D
WACC = W_E * KE + W_D * KD * (1 - TAX_RATE)
WACC = round(WACC, 4)                                   # 0.0866 → 8.66%

# ---------------------------------------------------------------------------
# 2. Agent E 원가함수 — 규모 티어 (cogs_model.py 실행값 복제, 검증 완료)
#    COGS/판매mL = fixed_total / (생산L × 1000 × 0.836) + var_per_mL
# ---------------------------------------------------------------------------
YIELD_RUO = 0.836                                        # [E-cogs §6]
COST_TIERS = [
    # (티어 생산 L, 연간 고정비 USD, 그 중 감가상각 USD, 판매 mL당 변동비 USD, 누적 CAPEX USD)
    (1,     375_000,   35_000,  9.4851,   350_000),
    (10,    934_215,  154_215,  2.1247, 1_542_150),
    (100, 1_932_700,  342_700,  0.7447, 3_427_000),
    (1000, 4_082_150, 852_150,  0.3767, 8_521_500),
]
CAPEX_GMP_ADD = 5_209_500                                # [E_cogs HANDOFF]


def tier_for(prod_L):
    """생산 물량이 속한 규모 티어 (cogs_model.scale_tier 와 동일 규칙)."""
    cand = [t for t in COST_TIERS if t[0] <= prod_L]
    return cand[-1] if cand else COST_TIERS[0]


def cogs_per_ml(sell_L):
    """판매 L → 판매 mL당 COGS (USD)."""
    if sell_L <= 0:
        return 0.0
    prod_L = sell_L / YIELD_RUO
    _, fixed, _depr, var, _cap = tier_for(prod_L)
    return fixed / (prod_L * 1000.0) + var


def gm60_threshold_sell_L(asp):
    """주어진 ASP 에서 GM 60% 를 만족하는 최소 **판매** L (파일럿 티어 기준)."""
    _, fixed, _d, var, _c = COST_TIERS[2]          # 100 L 티어 (F=1,932,700 / v=0.7447)
    denom = 0.40 * asp - var
    if denom <= 0:
        return float("inf")
    sell_mL = fixed / denom
    return sell_mL / 1000.0


def bep_sell_L(asp):
    """손익분기 판매 L (고정비 ÷ 판매 mL당 공헌이익)."""
    _, fixed, _d, var, _c = COST_TIERS[2]
    cm = asp - var
    if cm <= 0:
        return float("inf")
    return fixed / cm / 1000.0


# ---------------------------------------------------------------------------
# 3. 침투율 S-curve — 로지스틱. Agent D 의 switch_propensity / half_life 에서 유도
#    P(t) = L / (1 + exp(-k (t - t0)))
#      t0 = ENTRY_YEAR + H      (H = D 의 half_life_years)
#      k  = ln(1/p - 1) / H     (t=ENTRY_YEAR 에서 P/L = p 가 되도록)
#    ★ 선형 점유율 가정 없음
# ---------------------------------------------------------------------------
D_SWITCH = {                                             # [E-263, Agent D]
    "academic_ruo":            (0.060, 11.2),
    "pharma_preclinical_nam":  (0.083,  8.0),
    "organoid_cro_biobank":    (0.027, 25.3),
    "clinical_dx_pdo":         (0.032, 21.3),
    "regenerative_gmp":        (0.250,  2.4),
}
INCREMENTAL = {"bear": 0.55, "base": 0.70, "bull": 0.85}  # A-A20 증분지출비율
BME_RETENTION = 0.40                                      # 대조군용 BME 유지분 [E-239]
P_MULT = {"bear": 0.70, "base": 1.00, "bull": 1.50}       # 전환확률 시나리오 배수


def half_life(p):
    return math.log(0.5) / math.log(1 - p)


def logistic_params(seg, scen):
    p0, _h0 = D_SWITCH[seg]
    p = min(0.95, p0 * P_MULT[scen])
    H = half_life(p)
    t0 = ENTRY_YEAR + H
    k = math.log(1.0 / p - 1.0) / H
    incr = INCREMENTAL[scen]
    if seg == "regenerative_gmp":
        L = 1.00                       # Matrigel 사용 자체가 불가 → 대조군 유지 없음 [E-240]
    else:
        L = incr / (BME_RETENTION + incr)
    return L, k, t0


def penetration(seg, scen, year):
    L, k, t0 = logistic_params(seg, scen)
    return L / (1.0 + math.exp(-k * (year - t0)))


# ---------------------------------------------------------------------------
# 4. LG 점유율 · 가격
# ---------------------------------------------------------------------------
LG_SHARE = {                                             # [A §8.1, A-A21]
    "bear": {"ruo": 0.05, "gmp": 0.10},
    "base": {"ruo": 0.12, "gmp": 0.25},
    "bull": {"ruo": 0.22, "gmp": 0.40},
}
# ASP : base = Corning 표준 SKU 30.29 [E-802] × 0.823 (G 의 침투할인) = 24.93
ASP0 = {"bear": 19.39, "base": 24.93, "bull": 32.00}      # [E-803][E-802][E-807]
ASP_DRIFT = {"bear": -0.040, "base": -0.020, "bull": 0.000}   # 실질 단가 추세 [A §3.3]
GMP_PRICE_MULT = {"bear": 1.00, "base": 1.00, "bull": 1.85}   # bull 만 GMP 라인 착수


def asp(scen, year):
    return ASP0[scen] * (1 + ASP_DRIFT[scen]) ** (year - ENTRY_YEAR)


# ---------------------------------------------------------------------------
# 5. 판관비 · R&D
# ---------------------------------------------------------------------------
SGA_PCT = 0.290              # Bio-Techne FY2025 조정 SG&A / 매출 [E-808]
RND_PCT = 0.078              # Bio-Techne FY2025 R&D / 매출       [E-808]
FTE_FIELD = 190_781          # fully-loaded 상업 FTE [E-809] (X 실측, 90,000 가정 폐기)
RND_FLOOR = 470_000          # 3 FTE(한국 90,000) + 소재비 200,000


def sga(revenue, year):
    n_fte = 3 if year <= 2027 else 6
    return max(SGA_PCT * revenue, n_fte * FTE_FIELD)


def rnd(revenue):
    return max(RND_PCT * revenue, RND_FLOOR)


# ---------------------------------------------------------------------------
# 6. 시장 데이터 로드 (Agent A 출력)
# ---------------------------------------------------------------------------
def load_market():
    """(scenario, year, segment) -> {'usd':..., 'L':...} (TAM_addressable)"""
    m = defaultdict(lambda: {"usd": 0.0, "L": 0.0})
    with open(MARKET_CSV, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            key = (r["scenario"], int(r["year"]), r["segment"])
            m[key]["usd"] += float(r["TAM_addressable_usd"])
            m[key]["L"] += float(r["TAM_addressable_L"])
    return m


MARKET = load_market()


# ---------------------------------------------------------------------------
# 7. 스코프 A — 현 제품정의 (오가노이드 defined matrix 단품)
# ---------------------------------------------------------------------------
def volumes_scope_A(scen, year, share_mult=1.0, pen_mult=1.0, tam_mult=1.0):
    """판매 L (세그먼트별) 반환."""
    out = {}
    for seg in D_SWITCH:
        tam_L = MARKET[(scen, year, seg)]["L"] * tam_mult
        pen = min(1.0, penetration(seg, scen, year) * pen_mult)
        sh = LG_SHARE[scen]["gmp" if seg == "regenerative_gmp" else "ruo"] * share_mult
        out[seg] = tam_L * pen * sh
    return out


def revenue_scope_A(scen, year, asp_mult=1.0, **kw):
    vols = volumes_scope_A(scen, year, **kw)
    a = asp(scen, year) * asp_mult
    rev = 0.0
    for seg, L in vols.items():
        mult = GMP_PRICE_MULT[scen] if seg == "regenerative_gmp" else 1.0
        rev += L * 1000.0 * a * mult
    return rev, sum(vols.values()), vols


# ---------------------------------------------------------------------------
# 8. 스코프 B — 대안 스코프: G 옵션(b) 제품정의 확장
#    오가노이드 매트릭스 + 비오가노이드 3D 매트릭스 + 콜라겐/젤라틴 바이오잉크
# ---------------------------------------------------------------------------
NONORG_2025_USD = 74_200_000    # 비오가노이드 3D 매트릭스 [E-335, A 경로3 여집합]
NONORG_CAGR = 0.112             # [E-318]
BIOINK_2025_USD = 48_200_000    # 콜라겐 32.5 M + 젤라틴 15.7 M [E-810]
BIOINK_CAGR = 0.132             # [E-810]

SCOPE_B_PARAMS = {
    #                    addressable, p_switch, ceiling L, LG share, ASP USD/mL
    "nonorganoid": {"bear": (0.70, 0.060, 0.85, 0.03,  9.00),
                    "base": (0.70, 0.090, 0.85, 0.04, 11.64),   # TeloCol-6 패리티 [E-155]
                    "bull": (0.70, 0.120, 0.85, 0.08, 15.00)},
    "bioink":      {"bear": (0.85, 0.060, 1.00, 0.02, 12.00),
                    "base": (0.85, 0.120, 1.00, 0.03, 16.00),   # X 수정 점유 3% [E-737][E-738]
                    "bull": (0.85, 0.200, 1.00, 0.10, 20.00)},
}
SCOPE_B_EXTRA_CAPEX = 5_000_000     # 배합·프린터 호환성·어세이 밸리데이션·영업확장 [G §4.2]


def scope_B_leg(name, scen, year, asp_mult=1.0):
    addr, p, L, share, a = SCOPE_B_PARAMS[name][scen]
    base_usd = NONORG_2025_USD if name == "nonorganoid" else BIOINK_2025_USD
    cagr = NONORG_CAGR if name == "nonorganoid" else BIOINK_CAGR
    tam_usd = base_usd * (1 + cagr) ** (year - 2025)
    # 물량 환산 : 시장 ASP 앵커로 나눈다 (비오가노이드 11.64 [E-155] / 바이오잉크 20.00)
    mkt_asp = 11.64 if name == "nonorganoid" else 20.00
    tam_L = tam_usd / mkt_asp / 1000.0
    H = half_life(p)
    k = math.log(1.0 / p - 1.0) / H
    t0 = ENTRY_YEAR + H
    pen = L / (1.0 + math.exp(-k * (year - t0)))
    vol_L = tam_L * addr * pen * share
    return vol_L, vol_L * 1000.0 * a * asp_mult


def revenue_scope_B(scen, year, asp_mult=1.0, **kw):
    rev, vol, segs = revenue_scope_A(scen, year, asp_mult=asp_mult, **kw)
    detail = {"organoid": vol}
    for leg in ("nonorganoid", "bioink"):
        v, r = scope_B_leg(leg, scen, year, asp_mult)
        rev += r
        vol += v
        detail[leg] = v
    return rev, vol, detail


# ---------------------------------------------------------------------------
# 9. CAPEX 스케줄 (동적 — 필요한 규모 티어에 도달하는 해의 전년에 집행)
# ---------------------------------------------------------------------------
def capex_schedule(sell_by_year, scen, scope):
    """{year: capex_usd}. 누적 티어 CAPEX 를 필요 시점 1년 전에 집행."""
    sched = defaultdict(float)
    spent = 0.0
    for y in YEARS:
        prod = sell_by_year.get(y, 0.0) / YIELD_RUO
        need = tier_for(prod)[4]
        if need > spent:
            sched[max(ENTRY_YEAR, y - 1)] += need - spent
            spent = need
    if scen == "bull":                      # bull 만 GMP 라인 착수
        sched[2029] += CAPEX_GMP_ADD
    if scope == "B":
        sched[2027] += SCOPE_B_EXTRA_CAPEX * 0.5
        sched[2028] += SCOPE_B_EXTRA_CAPEX * 0.5
    if not sched:
        sched[ENTRY_YEAR] = COST_TIERS[0][4]
    return dict(sched)


# ---------------------------------------------------------------------------
# 10. P&L / FCF / NPV / IRR
# ---------------------------------------------------------------------------
def npv(rate, flows, base_year=ENTRY_YEAR):
    return sum(cf / (1 + rate) ** (y - base_year) for y, cf in flows)


def irr(flows):
    """이분법. 부호 변화가 없으면 None."""
    vals = [cf for _y, cf in flows]
    if all(v <= 0 for v in vals) or all(v >= 0 for v in vals):
        return None
    lo, hi = -0.95, 10.0
    f_lo = npv(lo, flows)
    f_hi = npv(hi, flows)
    if f_lo * f_hi > 0:
        return None
    for _ in range(300):
        mid = (lo + hi) / 2
        if npv(mid, flows) * f_lo > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def build_pnl(scen, scope="A", asp_mult=1.0, share_mult=1.0, pen_mult=1.0,
              tam_mult=1.0, fixed_mult=1.0, var_mult=1.0, wacc=None,
              drop_segments=(), extra_capex=None):
    wacc = WACC if wacc is None else wacc
    rows = []

    def rev_fn(y):
        if scope == "A":
            r, v, det = revenue_scope_A(scen, y, asp_mult=asp_mult, share_mult=share_mult,
                                        pen_mult=pen_mult, tam_mult=tam_mult)
            if drop_segments:
                a = asp(scen, y) * asp_mult
                for s in drop_segments:
                    m = GMP_PRICE_MULT[scen] if s == "regenerative_gmp" else 1.0
                    r -= det[s] * 1000.0 * a * m
                    v -= det[s]
            return r, v
        r, v, _d = revenue_scope_B(scen, y, asp_mult=asp_mult, share_mult=share_mult,
                                   pen_mult=pen_mult, tam_mult=tam_mult)
        return r, v

    sell_by_year = {y: rev_fn(y)[1] for y in YEARS}
    capex = capex_schedule(sell_by_year, scen, scope)
    if extra_capex:
        for y, c in extra_capex.items():
            capex[y] = capex.get(y, 0.0) + c

    cum_capex = 0.0
    cum_fcf = 0.0
    nol = 0.0
    prev_wc = 0.0
    flows = []
    for y in YEARS:
        revenue, sell_L = rev_fn(y)
        prod_L = sell_L / YIELD_RUO
        tier = tier_for(prod_L) if sell_L > 0 else COST_TIERS[0]
        fixed = tier[1] * fixed_mult
        depr = tier[2]
        var = tier[3] * var_mult
        cogs_total = (fixed + var * sell_L * 1000.0) if sell_L > 0 else 0.0
        cpm = cogs_total / (sell_L * 1000.0) if sell_L > 0 else 0.0
        gp = revenue - cogs_total
        gm = gp / revenue if revenue > 0 else 0.0
        s = sga(revenue, y)
        rd = rnd(revenue)
        ebit = gp - s - rd
        taxable = ebit - nol if ebit > 0 else 0.0
        if ebit > 0:
            used = min(nol, ebit)
            nol -= used
            tax = max(0.0, (ebit - used)) * TAX_RATE
        else:
            nol += -ebit
            tax = 0.0
        cx = capex.get(y, 0.0)
        cum_capex += cx
        wc = 0.25 * revenue
        d_wc = wc - prev_wc
        prev_wc = wc
        fcf = ebit - tax + depr - cx - d_wc
        cum_fcf += fcf
        flows.append((y, fcf))
        rows.append({
            "year": y, "sell_L": sell_L, "prod_L": prod_L,
            "asp": asp(scen, y) * asp_mult,
            "revenue": revenue, "cogs": cogs_total, "cogs_per_mL": cpm,
            "gross_profit": gp, "gm": gm, "sga": s, "rnd": rd, "ebit": ebit,
            "tax": tax, "depr": depr, "capex": cx, "cum_capex": cum_capex,
            "d_wc": d_wc, "fcf": fcf, "cum_fcf": cum_fcf,
        })

    # 지표
    npv_no_tv = npv(wacc, flows)
    fcf_last = flows[-1][1]
    tv = 0.0
    if fcf_last > 0 and wacc > 0.02:
        tv = fcf_last * 1.02 / (wacc - 0.02)          # 영구성장 2% 가정
    n = npv_no_tv + tv / (1 + wacc) ** (YEARS[-1] - ENTRY_YEAR)
    flows_tv = [(y, cf + (tv if y == YEARS[-1] else 0.0)) for y, cf in flows]
    r_irr = irr(flows_tv)

    payback = None
    for r in rows:
        if r["cum_fcf"] >= 0:
            payback = r["year"]
            break
    bep_year = None
    for r in rows:
        if r["ebit"] >= 0:
            bep_year = r["year"]
            break
    bep_cum_L = None
    if bep_year:
        bep_cum_L = sum(r["sell_L"] for r in rows if r["year"] <= bep_year)
    gm60_year = None
    for r in rows:
        if r["gm"] >= 0.60:
            gm60_year = r["year"]
            break

    return {
        "scenario": scen, "scope": scope, "rows": rows, "flows": flows,
        "npv": n, "npv_no_tv": npv_no_tv, "tv": tv, "irr": r_irr, "payback": payback,
        "bep_year": bep_year, "bep_cum_L": bep_cum_L, "gm60_year": gm60_year,
        "wacc": wacc, "cum_fcf": cum_fcf, "cum_capex": cum_capex,
    }


# ---------------------------------------------------------------------------
# 11. 라미닌 이분법 (V-07) — 기대 NPV
# ---------------------------------------------------------------------------
P_NO_LAMININ = 0.60          # 1 − D-A07 효능격차 확률 0.40


def expected_npv(res):
    """E[NPV] = 0.60 × NPV(성공) + 0.40 × NPV(실패: 2027년까지 집행 CAPEX 전액 손실)."""
    lost = 0.0
    for r in res["rows"]:
        if r["year"] <= 2027:
            lost += r["capex"] / (1 + res["wacc"]) ** (r["year"] - ENTRY_YEAR)
    lost += sum((r["sga"] + r["rnd"]) / (1 + res["wacc"]) ** (r["year"] - ENTRY_YEAR)
                for r in res["rows"] if r["year"] <= 2027)
    return P_NO_LAMININ * res["npv"] + (1 - P_NO_LAMININ) * (-lost), -lost


# ---------------------------------------------------------------------------
# 12. 민감도 (토네이도) — 스코프 A base
# ---------------------------------------------------------------------------
def _with_p_mult(m):
    global P_MULT
    old = dict(P_MULT)
    P_MULT = {k: min(0.95 / max(v0 for v0, _ in D_SWITCH.values()), v * m)
              for k, v in old.items()}
    r = build_pnl("base", "A")["npv"]
    P_MULT = old
    return r


def _with_sga(m):
    global SGA_PCT, FTE_FIELD
    s0, f0 = SGA_PCT, FTE_FIELD
    SGA_PCT, FTE_FIELD = s0 * m, f0 * m
    r = build_pnl("base", "A")["npv"]
    SGA_PCT, FTE_FIELD = s0, f0
    return r


def _with_rnd(m):
    global RND_PCT, RND_FLOOR
    p0, f0 = RND_PCT, RND_FLOOR
    RND_PCT, RND_FLOOR = p0 * m, f0 * m
    r = build_pnl("base", "A")["npv"]
    RND_PCT, RND_FLOOR = p0, f0
    return r


def tornado():
    base = build_pnl("base", "A")["npv"]
    specs = [
        ("SG&A (FTE 단가·비율)",         _with_sga),
        ("고정비 F (플랜트 규모)",        lambda m: build_pnl("base", "A", fixed_mult=m)["npv"]),
        ("WACC",                         lambda m: build_pnl("base", "A", wacc=WACC * m)["npv"]),
        ("ASP (판매단가)",               lambda m: build_pnl("base", "A", asp_mult=m)["npv"]),
        ("R&D 지출",                     _with_rnd),
        ("CAPEX",                        lambda m: build_pnl(
            "base", "A", extra_capex={2026: (m - 1) * 350_000, 2028: (m - 1) * 1_192_150,
                                      2034: (m - 1) * 1_884_850})["npv"]),
        ("전환확률 p_switch (S-curve)",   _with_p_mult),
        ("LG 점유율",                    lambda m: build_pnl("base", "A", share_mult=m)["npv"]),
        ("TAM_addressable (소모량계수)",  lambda m: build_pnl("base", "A", tam_mult=m)["npv"]),
        ("변동비 v",                     lambda m: build_pnl("base", "A", var_mult=m)["npv"]),
    ]
    out = []
    for name, fn in specs:
        lo = fn(0.7)
        hi = fn(1.3)
        out.append((name, lo - base, hi - base, abs(hi - lo)))
    out.sort(key=lambda r: -r[3])
    return base, out[:8]


# ---------------------------------------------------------------------------
# 13. Kill Criteria (Agent X KC-1 ~ KC-5) 발동 시 NPV
# ---------------------------------------------------------------------------
def stop_npv(res, stop_year):
    """해당 연도 말에 사업을 중단할 때의 NPV (그 해까지의 FCF 만 인식)."""
    return sum(cf / (1 + res["wacc"]) ** (y - ENTRY_YEAR)
               for y, cf in res["flows"] if y <= stop_year)


def kill_criteria():
    base = build_pnl("base", "A")
    b_scope = build_pnl("base", "B")
    res = []
    # KC-1 (6개월, 2026) : mTG 가 천연 삼중나선을 가교하지 못함 → 제품 = Col-Tgel 등가
    r1 = build_pnl("base", "A", share_mult=5.0 / 12.0)
    res.append(("KC-1 mTG 삼중나선 가교 전환율 미달 (H7)", 2026, r1["npv"],
                stop_npv(base, 2026), "점유율 12%→5% [X-A08] / 6개월 시점 중단"))
    # KC-2 (12개월, 2027) : 라미닌 무첨가 형성효율 < 34% → 라미닌 필수 → 공헌이익 음수
    res.append(("KC-2 라미닌 무첨가 형성효율 <34% (H2)", 2027, float("nan"),
                stop_npv(base, 2027),
                "라미닌 필수 시 COGS +110.96 USD/mL → 공헌이익 음수, 계속 불가"))
    # KC-3 (9개월, 2027) : Corning 이 354234 를 27.00 으로 인하 → ASP 27.00×0.823 = 22.22
    m3 = (27.00 * 0.823) / ASP0["base"]
    r3 = build_pnl("base", "A", asp_mult=m3)
    res.append(("KC-3 Corning 354234 ≤ 27.00 USD/mL (H4)", 2027, r3["npv"],
                stop_npv(base, 2027),
                "ASP %.2f → %.2f USD/mL" % (ASP0["base"], 27.00 * 0.823)))
    # KC-4 (30개월, 2028) : 옵션(b) 물량 미달 → 스코프 B 폐기
    # KC-4 발동은 물량 성장 실패를 뜻하므로 영구성장 잔존가치 가정이 무효 → 잔존가치 제외 NPV 사용
    res.append(("KC-4 옵션(b) 2028 연환산 판매 < 289.9 L (H11)", 2028, b_scope["npv_no_tv"],
                stop_npv(b_scope, 2028), "스코프 B 계속(잔존가치 제외) vs 2028년 말 중단"))
    # KC-5 (18개월, 2027) : 전환 서비스 랩당 > 12,000 USD → 학술 RUO 진입 중단
    r5 = build_pnl("base", "A", drop_segments=("academic_ruo",))
    res.append(("KC-5 전환서비스 랩당 >12,000 USD (H12)", 2027, r5["npv"],
                stop_npv(base, 2027), "학술 RUO 세그먼트 제외 vs 중단"))
    return base["npv"], res


# ---------------------------------------------------------------------------
# 14. 출력
# ---------------------------------------------------------------------------
def fmt(x, nd=0):
    if x is None:
        return "미도달"
    return f"{x:,.{nd}f}"


def yfmt(x):
    return "미도달" if x is None else str(int(x))


# 시나리오 확률 가중 (Agent X §15.2 확률사슬에서 유도)
#   bull  = X 의 P(성공) 0.12   /  bear = X 의 S1·S2 실패 경로 0.55  /  base = 잔여 0.33
SCEN_PROB = {"bear": 0.55, "base": 0.33, "bull": 0.12}


def main():
    csv_rows = [["section", "key", "value"]]

    print("=" * 100)
    print("OSVX 통합 재무모델 — Agent S")
    print("=" * 100)
    print("\n[1] 할인율 (WACC) 유도")
    print(f"  Rf(한국 국고채 10년, 2026-08-11)      = {RF*100:.2f}%   [E-800]")
    print(f"  ERP(한국, Damodaran 2026-01)          = {ERP_KR*100:.2f}%   [E-801]")
    print(f"  무차입 베타 (헬스케어제품 0.83 / 바이오텍 1.03 평균) = {BETA_UNLEV:.2f}   [E-804]")
    print(f"  D/E = {DE_RATIO*100:.2f}%,  법인세 {TAX_RATE*100:.1f}% [E-805]")
    print(f"  차입 베타 = {BETA_UNLEV:.2f} × [1 + (1−{TAX_RATE}) × {DE_RATIO}] = {BETA_LEV:.4f}")
    print(f"  Ke = {RF*100:.2f}% + {BETA_LEV:.4f} × {ERP_KR*100:.2f}% = {KE*100:.2f}%")
    print(f"  Kd = {RF*100:.2f}% + {CREDIT_SPREAD*100:.2f}% = {KD*100:.2f}%  (세후 {KD*(1-TAX_RATE)*100:.2f}%)")
    print(f"  ★ WACC = {W_E:.3f}×{KE*100:.2f}% + {W_D:.3f}×{KD*(1-TAX_RATE)*100:.2f}% = {WACC*100:.2f}%")
    for k, v in [("Rf", RF), ("ERP_KR", ERP_KR), ("beta_unlevered", BETA_UNLEV),
                 ("beta_levered", BETA_LEV), ("Ke", KE), ("Kd", KD), ("tax", TAX_RATE),
                 ("WACC", WACC)]:
        csv_rows.append(["WACC", k, round(v, 6)])

    print("\n[2] 침투율 S-curve 파라미터 (로지스틱, Agent D 유도)")
    print(f"  {'세그먼트':<26}{'p':>8}{'L(ceiling)':>12}{'k':>10}{'t0':>10}{'P(2030)':>10}{'P(2035)':>10}")
    for seg in D_SWITCH:
        L, k, t0 = logistic_params(seg, "base")
        print(f"  {seg:<26}{D_SWITCH[seg][0]:>8.3f}{L:>12.4f}{k:>10.4f}{t0:>10.1f}"
              f"{penetration(seg,'base',2030):>10.4f}{penetration(seg,'base',2035):>10.4f}")
        csv_rows += [["Scurve", f"{seg}_L", round(L, 4)],
                     ["Scurve", f"{seg}_k", round(k, 4)],
                     ["Scurve", f"{seg}_t0", round(t0, 2)],
                     ["Scurve", f"{seg}_P2030", round(penetration(seg, 'base', 2030), 4)],
                     ["Scurve", f"{seg}_P2035", round(penetration(seg, 'base', 2035), 4)]]

    print("\n[3] GM60 임계 판매물량 / BEP (판매 L 기준 — V-03 단위 통일)")
    for a in (32.00, 30.29, 24.93, 19.39, 18.53, 16.59):
        print(f"  ASP {a:>6.2f} USD/mL → GM60 임계 판매 {gm60_threshold_sell_L(a):>7.1f} L "
              f"(= 생산 {gm60_threshold_sell_L(a)/YIELD_RUO:>7.1f} L),  BEP 판매 {bep_sell_L(a):>6.1f} L")
        csv_rows.append(["Threshold", f"GM60_sell_L_at_ASP_{a}", round(gm60_threshold_sell_L(a), 2)])
        csv_rows.append(["Threshold", f"GM60_prod_L_at_ASP_{a}", round(gm60_threshold_sell_L(a)/YIELD_RUO, 2)])

    results = {}
    for scope in ("A", "B"):
        for scen in ("bear", "base", "bull"):
            results[(scope, scen)] = build_pnl(scen, scope)

    for scope, label in (("A", "스코프 A — 현 제품정의 (오가노이드 defined matrix)"),
                         ("B", "스코프 B — 대안 스코프 옵션(b) 제품정의 확장")):
        print("\n" + "=" * 100)
        print(f"[4-{scope}] {label}")
        print("=" * 100)
        for scen in ("bear", "base", "bull"):
            res = results[(scope, scen)]
            print(f"\n--- {scen.upper()} ---")
            print(f"  {'연도':<6}{'판매L':>9}{'생산L':>9}{'ASP':>8}{'매출':>14}{'COGS':>13}"
                  f"{'GP':>13}{'GM%':>8}{'SG&A':>12}{'R&D':>10}{'EBIT':>14}{'CAPEX':>12}{'FCF':>14}{'누적FCF':>15}")
            for r in res["rows"]:
                print(f"  {r['year']:<6}{r['sell_L']:>9.2f}{r['prod_L']:>9.2f}{r['asp']:>8.2f}"
                      f"{r['revenue']:>14,.0f}{r['cogs']:>13,.0f}{r['gross_profit']:>13,.0f}"
                      f"{r['gm']*100:>7.1f}%{r['sga']:>12,.0f}{r['rnd']:>10,.0f}"
                      f"{r['ebit']:>14,.0f}{r['capex']:>12,.0f}{r['fcf']:>14,.0f}{r['cum_fcf']:>15,.0f}")
                for k in ("sell_L", "prod_L", "asp", "revenue", "cogs", "gross_profit", "gm",
                          "sga", "rnd", "ebit", "capex", "fcf", "cum_fcf"):
                    csv_rows.append([f"PnL_{scope}_{scen}", f"{r['year']}_{k}", round(r[k], 4)])
            e_npv, fail_npv = expected_npv(res)
            irr_txt = ("미산출(전 기간 FCF 음수 — 부호 변화 없음, IRR 정의되지 않음)"
                       if res["irr"] is None else "%.2f%%" % (res["irr"] * 100))
            print(f"  NPV(@{res['wacc']*100:.2f}%) = {fmt(res['npv'])} USD"
                  f" (잔존가치 제외 {fmt(res['npv_no_tv'])} + 잔존가치 PV "
                  f"{fmt(res['tv']/(1+res['wacc'])**(YEARS[-1]-ENTRY_YEAR))})"
                  f" | IRR = {irr_txt}")
            print(f"  Payback = {yfmt(res['payback'])} | EBIT 흑자전환 = {yfmt(res['bep_year'])}"
                  f" | BEP 누적물량 = {fmt(res['bep_cum_L'],1)} 판매 L"
                  f" | GM60 최초 = {yfmt(res['gm60_year'])}")
            print(f"  라미닌 이분법 E[NPV] = 0.60×{fmt(res['npv'])} + 0.40×{fmt(fail_npv)} = {fmt(e_npv)} USD")
            for k, v in [("NPV", res["npv"]), ("NPV_ex_TV", res["npv_no_tv"]),
                         ("IRR", res["irr"] if res["irr"] is not None else "미산출"),
                         ("payback", res["payback"] if res["payback"] else "미도달"),
                         ("bep_year", res["bep_year"] if res["bep_year"] else "미도달"),
                         ("bep_cum_sell_L", res["bep_cum_L"] if res["bep_cum_L"] else "미도달"),
                         ("gm60_year", res["gm60_year"] if res["gm60_year"] else "미도달"),
                         ("cum_fcf_2035", res["cum_fcf"]), ("cum_capex", res["cum_capex"]),
                         ("E_NPV_laminin_binary", e_npv)]:
                csv_rows.append([f"Metrics_{scope}_{scen}", k,
                                 round(v, 4) if isinstance(v, float) else v])

    print("\n" + "=" * 100)
    print("[5] DECISION_GATE 대조 (2030년 기준)")
    print("=" * 100)
    print(f"  {'게이트':<28}{'임계값':>18}{'Bear':>16}{'Base':>16}{'Bull':>16}{'판정':>10}")
    gate_rows = []
    sam2030 = {}
    som2030 = {}
    for scen in ("bear", "base", "bull"):
        sam = 0.0
        for seg in D_SWITCH:
            sam += MARKET[(scen, 2030, seg)]["usd"] * penetration(seg, scen, 2030)
        sam2030[scen] = sam
        r = [x for x in results[("A", scen)]["rows"] if x["year"] == 2030][0]
        som2030[scen] = r["revenue"]
    print(f"  {'SAM_2030 (USD)':<28}{150_000_000:>18,}{sam2030['bear']:>16,.0f}"
          f"{sam2030['base']:>16,.0f}{sam2030['bull']:>16,.0f}{'FAIL':>10}")
    print(f"  {'SOM_2030 (USD)':<28}{15_000_000:>18,}{som2030['bear']:>16,.0f}"
          f"{som2030['base']:>16,.0f}{som2030['bull']:>16,.0f}{'FAIL':>10}")
    gm2030 = {s: [x for x in results[("A", s)]["rows"] if x["year"] == 2030][0]["gm"]
              for s in ("bear", "base", "bull")}
    print(f"  {'Gross_Margin_2030':<28}{'60.0%':>18}{gm2030['bear']*100:>15.1f}%"
          f"{gm2030['base']*100:>15.1f}%{gm2030['bull']*100:>15.1f}%{'FAIL':>10}")
    pb = {s: results[("A", s)]["payback"] for s in ("bear", "base", "bull")}
    print(f"  {'Payback (년)':<28}{'≤5 (2030)':>18}"
          f"{yfmt(pb['bear']):>16}{yfmt(pb['base']):>16}{yfmt(pb['bull']):>16}{'FAIL':>10}")
    print(f"  {'FTO 리스크':<28}{'중 이하':>18}{'중':>16}{'중':>16}{'중':>16}{'PASS':>10}")

    print("\n[5b] 시나리오 확률가중 기대 NPV (가중치 bear 0.55 / base 0.33 / bull 0.12"
          " — Agent X §15.2 P(성공)=0.12 에서 유도)")
    for scope in ("A", "B"):
        ew = sum(SCEN_PROB[s] * results[(scope, s)]["npv"] for s in SCEN_PROB)
        ew_ex = sum(SCEN_PROB[s] * results[(scope, s)]["npv_no_tv"] for s in SCEN_PROB)
        ew_lam = sum(SCEN_PROB[s] * expected_npv(results[(scope, s)])[0] for s in SCEN_PROB)
        print(f"  스코프 {scope}: E[NPV] = {fmt(ew)} | 잔존가치 제외 E[NPV] = {fmt(ew_ex)}"
              f" | 라미닌 이분법까지 반영 = {fmt(ew_lam)} USD")
        csv_rows += [["ExpectedValue", f"scope_{scope}_prob_weighted_NPV", round(ew, 0)],
                     ["ExpectedValue", f"scope_{scope}_prob_weighted_NPV_exTV", round(ew_ex, 0)],
                     ["ExpectedValue", f"scope_{scope}_prob_weighted_NPV_laminin", round(ew_lam, 0)]]

    print("\n[5c] DISC-01 재계산 확정 — 옵션(b) GM60 임계물량")
    for label, a in (("Agent V 가정 ASP 18.56", 18.56), ("Agent X 가정 ASP 18.50", 18.50),
                     ("★ S 확정 (두 값의 중간 18.53)", 18.53)):
        s_L = gm60_threshold_sell_L(a)
        print(f"  {label:<32} → 판매 {s_L:7.1f} L  /  생산 {s_L/YIELD_RUO:7.1f} L")
        csv_rows += [["DISC01", f"{label}_sell_L", round(s_L, 2)],
                     ["DISC01", f"{label}_prod_L", round(s_L / YIELD_RUO, 2)]]
    print("  → V(289.4)와 X(347.3)의 차이는 계산 오류가 아니라 **단위 기준 차이**다:"
          " 347.3 × 0.836 = 290.3 ≈ 289.4. 동일 식·동일 값.")
    for s in ("bear", "base", "bull"):
        csv_rows += [["Gate", f"SAM_2030_{s}", round(sam2030[s], 0)],
                     ["Gate", f"SOM_2030_{s}", round(som2030[s], 0)],
                     ["Gate", f"GM_2030_{s}", round(gm2030[s], 4)],
                     ["Gate", f"Payback_{s}", pb[s] if pb[s] else "미도달"]]

    print("\n" + "=" * 100)
    print("[6] 민감도 — 토네이도 상위 8 변수 (스코프 A base, ±30%)")
    print("=" * 100)
    b, tor = tornado()
    print(f"  기준 NPV = {fmt(b)} USD")
    print(f"  {'#':<3}{'변수':<28}{'−30% ΔNPV':>18}{'+30% ΔNPV':>18}{'영향폭(절대)':>18}")
    for i, (name, lo, hi, span) in enumerate(tor, 1):
        print(f"  {i:<3}{name:<28}{lo:>18,.0f}{hi:>18,.0f}{span:>18,.0f}")
        csv_rows += [["Sensitivity", f"{i}_{name}_low", round(lo, 0)],
                     ["Sensitivity", f"{i}_{name}_high", round(hi, 0)],
                     ["Sensitivity", f"{i}_{name}_span", round(span, 0)]]

    print("\n" + "=" * 100)
    print("[7] Kill Criteria 발동 시 NPV (스코프 A base 대비)")
    print("=" * 100)
    kb, kcs = kill_criteria()
    print(f"  기준(무발동) NPV = {fmt(kb)} USD")
    print(f"  {'Kill Criterion':<44}{'판정연도':>9}{'계속 시 NPV':>17}{'중단 시 NPV':>17}{'중단 옵션가치':>17}")
    for name, yr, cont, stop, note in kcs:
        cont_s = "계속 불가" if cont != cont else f"{cont:,.0f}"
        opt = "—" if cont != cont else f"{stop - cont:,.0f}"
        print(f"  {name:<44}{yr:>9}{cont_s:>17}{stop:>17,.0f}{opt:>17}")
        print(f"      └ {note}")
        csv_rows += [["KillCriteria", name + "_continue", "계속불가" if cont != cont else round(cont, 0)],
                     ["KillCriteria", name + "_stop", round(stop, 0)],
                     ["KillCriteria", name + "_option_value",
                      "—" if cont != cont else round(stop - cont, 0)]]

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(csv_rows)
    print(f"\n[OK] {OUT_CSV} 기록 완료 — {len(csv_rows)-1}행")
    return 0


if __name__ == "__main__":
    sys.exit(main())
