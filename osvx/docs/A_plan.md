# Agent A — 수요·시장규모 작업계획 (A_plan.md)

작성일 2026-08-11 / 근거 ID 범위 **E-300 ~ E-399** / evidence: `evidence/evidence_A.jsonl`
산출물: `docs/A_plan.md`, `docs/A_market_sizing.md`, `model/market_model.py`, `evidence/evidence_A.jsonl`, `data/market_model_output.csv`

---

## 0. 선행 Wave 1 산출물 Read 완료 (입력 확정)

| 파일 | 사용할 입력값 |
|---|---|
| `docs/B_regulatory.md` | `nam_ramp` (cons 4/12/25 · base 8/25/45 · aggr 12/40/65 %), `clinical_timing_year=2033`, `grade_verdict` RUO 우선, `gmp_premium_multiple=1.85` |
| `docs/premise_audit.md` | P1 수요 +4년 지연, P4 이식 +6년 지연, P5 규제는 defined matrix 미강제 → **램프 함수의 상한 억제** |
| `docs/C_competition.md`, `data/price_table.csv` | `asp_bme=48.24`, `asp_defined=60.47`, `asp_gmp=117.43`, `top3_share=0.78`, `distributor_markup=35.9%`, 중국 로컬 21.30, Corning LS 2025 972 MUSD |
| `docs/D_voc_barriers.md` | `segment_switch_propensity` 학술 6.0 / 제약 8.3 / CRO 2.7 / 임상 3.2 / GMP 25.0 %/년, `switching_cost=56,810 USD`, **"증분 지출 수용률"로 SAM 모델링 강제**, 라미닌 효능 격차 |

---

## 1. 조사 쿼리 목록 (실행 예정)

### 1.1 경로1 Bottom-up — 랩 수 프록시
| # | 쿼리/URL | 목적 |
|---|---|---|
| Q01 | `eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=organoid&mindate=YYYY&maxdate=YYYY` (1990~2025 전 연도) | 연도별 논문 수 → CAGR 직접 계산 |
| Q02 | 동일 API `term=organoid AND (patient-derived)` / `term=organoid AND matrigel` | 세그먼트 프록시 분해 |
| Q03 | Europe PMC REST `search?query=organoid&resultType=idlist` | 교차검증 |
| Q04 | "organoid core facility" 대학 리스트 검색 | 코어시설 수 |
| Q05 | HUB Organoids licensing / 라이선스 기관 수 | 상용 라이선스 모집단 |
| Q06 | 논문당 고유 기관(affiliation) 수 비율 | 논문→랩 환산 계수 |
| Q07 | NIH RePORTER organoid 과제 수 | 미국 랩 수 하한 |

### 1.2 경로1 Bottom-up — 소모량 프록시
| # | 쿼리 | 목적 |
|---|---|---|
| Q08 | Nature Protocols intestinal organoid dome 50 µL/well 프로토콜 | 실험당 mL |
| Q09 | PDO(환자유래 오가노이드) 배양 프로토콜 매트릭스 사용량 | 임상진단 세그먼트 |
| Q10 | 뇌 오가노이드 embedding Matrigel 사용량 | 세그먼트 분해 |
| Q11 | passage 주기(주 1회/2주 1회), 유지 라인 수 | 랩당 연간 mL |
| Q12 | 384/1536-well HTS 오가노이드 스크리닝 매트릭스 소모량 | 제약 세그먼트 |

### 1.3 경로2 Top-down — 시장보고서 (최소 5개 교차, 정의 확인 필수)
Grand View Research / MarketsandMarkets / Mordor Intelligence / Fortune Business Insights / Precedence Research / Research and Markets / Global Market Insights
- 대상 카테고리: `organoid market`, `3D cell culture market`, `extracellular matrix market`, `basement membrane extract market`, `organoids and spheroids market`
- **각 보고서의 포함/제외 정의를 확인**. 정의 불명 → T3 강등 + 사유 기록. **금액만 있고 물량 환산 불가한 보고서는 부적합 처리.**

### 1.4 경로3 Proxy / 역산
| # | 소스 | 목적 |
|---|---|---|
| Q13 | SEC EDGAR Corning 10-K Life Sciences (Agent C [E-127][E-128] 재사용 + 추가 확인) | 역산 기준 |
| Q14 | Bio-Techne 10-K Protein Sciences ([E-129] 재사용) | 역산 |
| Q15 | Thermo Fisher 10-K Life Sciences Solutions | 역산 |
| Q16 | BME 3사 점유율 0.78 [E-165] 로 전체 매트릭스 시장 역산 | 경로3 산출 |
| Q17 | 논문 수 CAGR 역산 교차검증 | 경로3 보조 |

### 1.5 GMP/이식 별도 트랙
| # | 쿼리 | 목적 |
|---|---|---|
| Q18 | ClinicalTrials.gov API v2 `organoid`, `organoid-derived`, `PDO` 등록 건수 (검색 URL 기록) | 임상 모집단 |
| Q19 | 세포치료제 임상시험 배치당 매트릭스 소요량 | GMP 물량 |

### 1.6 지역 가중 프록시
| # | 쿼리 | 목적 |
|---|---|---|
| Q20 | 국가별 organoid 논문 수 (PubMed affiliation 검색) | 지역 가중 1 |
| Q21 | OECD/UNESCO 국가별 R&D 지출(GERD) | 지역 가중 2 |
| Q22 | 국가별 제약사·바이오텍 수 | 지역 가중 3 |

---

## 2. 산출 방법론

### 2.1 경로1 기본식
```
연간시장_세그먼트,지역 = 랩수 × 랩당연간실험수 × 실험당매트릭스mL × ASP(USD/mL)
물량_L/년 = 랩수 × 랩당연간실험수 × 실험당매트릭스mL / 1000
```

### 2.2 Addressable subset (기술적 대체가능 비율)
Agent D 의 효능 격차(2024년까지 모든 합성 매트릭스가 외인성 라미닌 필수 [E-231]) 및 장기별 편중(성공 5/7이 소장·위·간)에 근거해 **세그먼트·장기별 기술적 대체가능 비율**을 별도 산정한다. BME 전량이 defined 로 대체 가능하다고 가정하지 않는다.

### 2.3 SAM = 증분 지출 수용률 (Agent D 경고 준수)
```
SAM_naive     = TAM_addressable × (전환확률 미반영)     ← 참고용으로만 병기
SAM_adjusted  = Σ_t TAM_addressable,t × [1-(1-P_switch)^(t-t0)] × incremental_spend_ratio
```
전환확률 반영 전/후를 **반드시 둘 다 제시**하여 배수 차이를 보인다.

### 2.4 NAM 램프 함수 (스텝 금지)
B 의 nam_ramp 3점(2026/2030/2035)을 **구간별 CAGR 보간(기하 램프)** 으로 연속화한다.
```
ramp(t) = ramp(t0) × ((ramp(t1)/ramp(t0))^(1/(t1-t0)))^(t-t0)
```

### 2.5 CAGR
```
CAGR = (End/Start)^(1/n) - 1     ← 인용 금지, 전건 직접 계산
```

### 2.6 3경로 편차 판정
경로 간 최대/최소 > 2.0 → `docs/gaps.md` 에 원인 분석 append + 채택 경로와 근거 명시.

---

## 3. 산출 순서
1. PubMed 연도별 논문 수 수집 → 랩 수 프록시 확정
2. 프로토콜 소모량 수집 → 랩당 연간 mL 확정
3. price_table.csv 단가 결합 → 경로1 산출
4. 시장보고서 5개 이상 교차 → 경로2 산출
5. 10-K 역산 → 경로3 산출
6. 삼각측량 → 채택
7. `model/market_model.py` 작성 → `python3` 실행 검증 → 출력 문서 반영
8. `evidence_A.jsonl` 적재 (E-300~E-399), `assumptions.md`·`gaps.md` append
9. DoD 셀프체크 표 + HANDOFF

---

## 4. 준수 선언
- R1 No-Deferral: 금지표현 0건, 미확인 값은 가정+계산 완료 후 `assumptions.md` append
- R2 Evidence: E-300~E-399 만 생성, 선행 [E-###] 는 인용만, `verified_by=""`, access_date 2026-08-11
- R4 Show-Your-Math: 전 파생값에 계산식
- 실제 WebSearch/WebFetch ≥ 40회
