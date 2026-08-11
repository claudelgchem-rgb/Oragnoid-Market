# Agent S — 작업 계획서 (통합 재무모델 & Go/No-Go 판정)

작성일 **2026-08-11** / 근거 ID 범위 **E-800 ~ E-849** / evidence 파일 `evidence/evidence_S.jsonl`
작업 루트 `/home/user/Oragnoid-Market/osvx`

---

## 0. 임무 정의

> 선행 12개 산출물(A~G, R, V, X)의 수치를 **하나의 재무모델로 봉합**하고, `DECISION_GATE` 5개 항목에 대해
> **현 제품정의**와 **대안 스코프**를 분리해 `Go` / `Conditional-Go` / `No-Go` 중 하나를 명시적으로 선언한다.
> **판정 유보는 실패다** (R1 No-Deferral).

---

## 1. 선행 문서 Read 목록 (전건 필수)

| # | 파일 | 목적 |
|---|---|---|
| 1 | `AGENT_RULES.md` | 규칙·근거 ID 범위·금지표현 |
| 2 | `docs/A_market_sizing.md` | TAM/SAM/SOM, 물량 곡선, 시나리오 3종 |
| 3 | `docs/B_regulatory.md` | nam_ramp (수요 드라이버), GMP/ATMP 타이밍 |
| 4 | `docs/C_competition.md` | ASP 앵커, 환율, 유통마진 |
| 5 | `docs/D_voc_barriers.md` | switching_cost, switch_propensity → S-curve 유도 입력 |
| 6 | `docs/E_cogs.md` | 원가함수, CAPEX, BEP, GM 임계물량 |
| 7 | `docs/F_ip_fto.md` | FTO 등급, 회피 규격 |
| 8 | `docs/G_gtm.md` | 채널 물량, 가격표, 재정의 옵션 (a)~(e) |
| 9 | `docs/R_credibility.md` | 근거품질 FAIL 2항목, 유통마진 정정 69.0% |
| 10 | `docs/V_audit.md` | V-01~V-26 수정 지시 (심각도 상 10건 전건 반영) |
| 11 | `docs/X_redteam.md` | H1~H12 반증, KC-1~KC-5, bear SOM |
| 12 | `docs/premise_audit.md` `assumptions.md` `gaps.md` | 전제·가정·갭 |
| 13 | `data/*.csv`, `model/market_model.py`, `model/cogs_model.py`, `run_state.json` | 수치 재현 |

---

## 2. 조사 계획 (WebSearch / WebFetch — 실제 수행)

신규 근거가 필요한 항목은 **할인율(WACC)** 과 **가격·인건비 재확인** 뿐이다. 나머지는 선행 근거를 인용한다.

| # | 조사 쿼리 | 목적 | 목표 근거 ID |
|---|---|---|---|
| Q1 | `LG Chem WACC cost of capital 2026` | 주체의 자본비용 | E-800대 |
| Q2 | `LG화학 가중평균자본비용 WACC 손상검사 할인율` | 공시 기반 할인율 | 〃 |
| Q3 | `Korea 10-year government bond yield 2026` | 무위험이자율 | 〃 |
| Q4 | `Damodaran cost of capital life sciences / drugs biotechnology 2026` | 산업 벤치마크 | 〃 |
| Q5 | `Korea corporate tax rate 2026` | 세후 부채비용·EBIT→FCF | 〃 |
| Q6 | `LG Chem credit rating bond yield 2026` | 부채비용 | 〃 |
| Q7 | `Corning Matrigel 354234 price` / `Synthegel 354791 price` | X 의 가격 기준선 재확인 | 〃 |
| Q8 | `Field Application Scientist salary biotech 2026` | X 의 FTE 단가 재확인 | 〃 |
| Q9 | `bioink market size collagen 2026` | 옵션(b) 인접시장 재확인 | 〃 |
| Q10 | `microbial transglutaminase collagen triple helix crosslinking` | H7 재확인 | 〃 |
| Q11 | `LG Chem Life Sciences 2025 revenue operating profit` | 조직 규모 | 〃 |
| Q12 | `equity risk premium Korea 2026` | CAPM 입력 | 〃 |

목표 **25회 이상**. 접근 실패 시 `access_status:"failed"` 로 기록하고 대체 소스를 찾는다.

---

## 3. 반영 의무 항목 (체크리스트)

### 3.1 Agent V — 심각도 '상' 10건 (V-01~V-10) 전건 반영 + V-11~V-26 반영표
- V-01 Payback FAIL 로 전환, A SOM 기준 재계산
- V-02 설계물량 500 L 순환논증 제거, 15 M USD 판매엔 생산 561 L
- V-03 판매 L / 생산 L 통일 (판매 기준), G 도달연도 2042 → 2040
- V-04 옵션(b) GM60 FAIL, 임계 289.4 L (V) — DISC-01 재계산 대상
- V-05 옵션(c) GM60 FAIL (41.1%)
- V-06 F 회피규격 위반 (OM-S, 강스템 SKU, 한국 EPFL 등록)
- V-07 라미닌 리스크 이분법 통일
- V-08 addressable × LG_efficacy 이중곱 교정 (SOM +21.7%)
- V-09 LG 가격표 적용 SOM 630,682 USD (−15.5%)
- V-10 옵션(b) SOM 의 91.8%가 가정 산출 → 하방 시나리오 필수

### 3.2 Agent R — FAIL 2항목 + 정정
- 시장규모 FAIL (T1 39.4%), COGS·GM FAIL (T1 37.1%) → 서술 완화 + 표시
- 유통마진 35.9% → **69.0%** [E-103-R] 반영, G 채널 순단가표 전량 재계산
- `evidence_rejected.jsonl` 21건 의존 주장 사용 금지 (E-103, E-306, E-307, E-410, E-414, E-424 등)
- `evidence_verified.jsonl` 의 재판정 tier/confidence 기준 적용

### 3.3 Agent X — 반증 12건 + KC 5개
- H7 (mTG × 천연 삼중나선) 을 하방 시나리오 및 현 제품정의 판정의 핵심 축으로
- Bear SOM 2030 = 314,900 USD / 9.1 L
- 종합 실패확률 88% (82~93%)
- DISC-01 (V 289.4 L vs X 347.3 L) 재계산 확정
- 서비스 상쇄 FTE 190,781 USD → 랩당 18,249 USD
- Corning 가격 하한 19.39 / 26.82 USD/mL

---

## 4. 산출물

| # | 파일 | 내용 |
|---|---|---|
| 1 | `docs/S_plan.md` | 본 문서 |
| 2 | `docs/S_synthesis.md` | 통합 재무모델·판정 본문 |
| 3 | `model/finance_model.py` | 표준 라이브러리 전용, 3시나리오 P&L·NPV·IRR |
| 4 | `data/finance_output.csv` | 위 모델 출력 |
| 5 | `model/OSVX_model.xlsx` | 8시트, 살아있는 수식 ≥20개 |
| 6 | `evidence/evidence_S.jsonl` | E-800~E-849 |

---

## 5. 방법론 — 시나리오 구동 변수

```
1. NAM 램프        : B 의 nam_ramp (bear 12% / base 25% / bull 40% @2030)
2. 침투율 S-curve  : 로지스틱 P(t) = L / (1 + exp(-k(t - t0)))
                     L·k·t0 를 D 의 switching_cost / switch_propensity 에서 유도 (§S_synthesis §2.2)
                     ★ 선형 점유율 가정 금지
3. ASP             : X 의 Corning 실측 하한 반영 (bear 19.39 / base 24.00~28.00 / bull 32.00)
4. 우리 점유율     : G 의 앵커 실물량(30곳 11.222 L) 기반 상한 제약
5. 원가            : E 원가함수 COGS(V) = F/V + v (F=2,312,325, v=0.740) — V-02 순환논증 제거
```

## 6. 검증 절차

1. `python3 model/finance_model.py` 실행 → EXIT 0 · CSV 생성 확인
2. `python3` 로 `OSVX_model.xlsx` 재오픈 → 시트 8개 · 살아있는 수식 ≥20개 카운트
3. 금지표현 grep 스캔
4. `evidence_S.jsonl` ID 범위·중복·`verified_by=""`·`access_date` 검증
5. DoD 11항목 셀프체크 표 작성
