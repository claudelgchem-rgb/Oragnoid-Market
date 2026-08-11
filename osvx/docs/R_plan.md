# Agent R — 근거 신뢰도 독립 검증 작업계획

작업 루트: `/home/user/Oragnoid-Market/osvx`
작성일: 2026-08-11
담당: Agent R (Independent Verification, AGENT_RULES.md §R3)

---

## 0. 독립성 선언 (R3 준수 기록)

| 항목 | 조치 |
|---|---|
| 타 에이전트 결론문서 본문 열람 | **하지 않음.** `docs/A_market_sizing.md`, `B_regulatory.md`, `C_competition.md`, `D_voc_barriers.md`, `E_cogs.md`, `F_ip_fto.md`, `G_gtm.md` 의 서술·판단 부분을 근거로 사용하지 않았다. |
| Agent V / Agent X 산출물 | 열람하지 않음. |
| 문서 grep | `[E-###]` 인용 위치 추출용 grep 1회만 수행. 그 결과도 최종 버킷 배정에는 사용하지 않고, **레코드 자체의 claim/value/ID 대역으로 결정론적 배정**하는 방식으로 대체했다(문서 서술 의존 제거). |
| 출발점 | `evidence/evidence_A~G.jsonl` 원본 438건의 **레코드와 URL 원자료**. |
| 읽기전용 준수 | `evidence/evidence.jsonl`, `evidence/evidence_A~G.jsonl` 는 읽기만 하고 수정하지 않았다. |

**병합본 결함 발견**: `evidence/evidence.jsonl` 은 373건으로, Agent G 의 65건(E-600~E-664)이 누락되어 있다. 본 검증은 병합본이 아니라 **원본 7개 파일의 합집합 438건**을 모집단으로 삼았다.

---

## 1. 목표

1. 438건 전 레코드의 tier·confidence 를 **원 소유자의 판정과 무관하게** 재판정한다.
2. 최소 70건을 실제 WebFetch 로 원자료까지 열어 **접근성 + 원문 일치 여부**를 확인한다.
3. 핵심 수치 최소 15건은 원문에서 숫자 자체를 눈으로 확인한다.
4. 통과/격리를 분리하고, 6개 핵심 결론별 근거품질 스코어카드와 게이트 판정을 낸다.
5. 게이트 FAIL 영역에 대해 R 이 직접 더 나은 T1 근거를 찾아 보강한다.

---

## 2. 표본 선정 기준 (실검증 대상)

우선순위대로 선정. 미선정 레코드는 결과 JSONL 에 `"sampled": false` 로 표기하고, 출처유형·발행주체 기준의 서면 재판정만 적용한다.

| 우선순위 | 기준 | 대상 |
|---|---|---|
| P1 | 6개 핵심 결론(시장규모·단가·COGS/GM·규제 타이밍·FTO·전환장벽)을 직접 지탱하는 수치 근거 | 가격 정가 전량, 10-K·IR 공시 전량, FDA/EU/OECD 1차 규제문서, FTO 판정의 근거가 되는 특허·검색건수, 로트편차 CV 실측 |
| P2 | 원 소유자가 `tier:"T1"` 이라고 주장한 레코드 | 특히 URL 호스트가 유통사·시장보고서·블로그인데 T1 로 기재된 건 |
| P3 | 값이 사업판단을 크게 움직이는 큰 수치 | TAM/SAM 원천, titer·발효원가, 유통마진율, GMP 프리미엄 배수 |
| P4 | 무작위/교차 표본 | 각 에이전트 대역에서 고르게 추출, 동일 URL을 두 에이전트가 다르게 기록한 충돌 후보 |

**미선정 사유 명시**: (a) 동일 URL·동일 출처를 이미 다른 ID 로 실검증하여 한계효용이 낮은 건, (b) 특허 원문 52건 중 Google Patents 서버가 반복 503 을 반환하여 대표 4건만 실검증한 건, (c) 값이 파생계산(추정)이어서 원자료 검증 대상이 아닌 건.

---

## 3. Tier 재판정 규칙 (사전 고정 — 사후 조정 금지)

| Tier | 정의 | 판정 규칙 |
|---|---|---|
| **T1** | 1차 원자료 | 규제기관·정부 원문/공식 API(fda.gov, congress.gov, govinfo, eCFR, EUR-Lex, ec.europa.eu, OECD, MFDS, ISO, USP, ClinicalTrials.gov, Federal Reserve) · 상장사 공시/IR 원자료(SEC EDGAR, investor.corning.com, ir.collplant.com, lgcorp.com) · 공적 등기(North Data/Handelsregister) · 대학 공식 요율표 · 특허 원문 및 특허DB 검색결과(Google Patents, FreePatentsOnline) · **제조사 본인** 공식 카탈로그·앱노트·CoA(ecatalog.corning.com, corning.com, thermofisher.com, stemcell.com, qkine.com, biolamina.com, zedira.com, 101bio.com, yeasenbio.com 등) · 피어리뷰 논문 및 1차 문헌DB(PMC, PubMed, NCBI eutils, Europe PMC, Nature, Cell, Frontiers, Wiley, ScienceDirect) |
| **T2** | 2차 | **유통사 판매가**(Fisher, VWR/Avantor, Krackeler, Alkali, BioCat, AMSBIO, Ilex Life, store.reprocell, Modernist Pantry, Amerigo) · 업계지·뉴스(FierceBiotech, BioWorld, BusinessWire, PR Newswire, 국내 매체) · 사용자 리뷰 플랫폼(SelectScience) · 애널리스트 요약 |
| **T3** | 3차 | **시장보고서 전량**(Grand View, Mordor, MarketsandMarkets, Precedence, Fortune BI, QYResearch/GII, Stats Market Research, WiseGuy, Straits, GMI, 世展网, YH Research 등) · 블로그·개인사이트(owlposting, ipscell, grokipedia, bioprocesstools, terrapincg, wolf-packing, excedr, parcelpath, sofpromed) · 집계DB(Tracxn, Crunchbase, PitchBook, MacroTrends, PharmaCompass) · 재판매 리스팅(eBay, Made-in-China, Accio) · **`source_type:"추정"` 전량** |

**강제 규칙 3가지** (과제 지시 항목 3 대응)
1. 유통사 가격을 제조사 공식 카탈로그로 기재한 건은 **무조건 T2 로 강등**한다. 예: `publisher:"Fisher Scientific (Advanced BioMatrix)"` 는 제조사가 아니라 대리점이다.
2. 시장보고서는 발행주체가 규제기관·상장사가 아닌 한 **T1/T2 로 승격 불가**, 전량 T3.
3. `source_type:"추정"` / `url:"internal:calc"` 는 입력이 아무리 좋아도 **T3**. 자기 산출물은 1차 원자료가 아니다.

---

## 4. 신뢰도 5축 재부여 규칙

각 축 0/1 채점 후 합산: **4~5점 = 상 / 2~3점 = 중 / 0~1점 = 하**. 모든 레코드에 `r_reason` 1줄 사유를 필수 기재한다.

| 축 | 1점 조건 | 0점 조건 |
|---|---|---|
| 출처 독립성 | 이해당사자가 아닌 제3자·1차 기관 산출 | 자기 산출(추정), 방법론 비공개 벤더 보고서 |
| 방법론 공개 | 측정조건·표본·산식이 원문에 기재(T1 기본 충족) | 시장보고서(유료구간에 방법론 은폐), 산식 미기재 추정 |
| 최신성 | 2016년 이후 자료 또는 상시 갱신 카탈로그/API | 2015년 이전 원자료를 현재값처럼 사용 |
| 재현가능성 | R 이 실제로 재현 성공(num/ok/urlfix) 또는 결정론적 재현 가능 출처(규제기관·특허DB·NCBI API·SEC·Corning e-catalog) | 실검증에서 부분확인·접근불가·불일치, 또는 프로모션가·비공개DB 등 비결정론적 출처 |
| 이해상충 | 없음 | 제조사가 자사 제품 우위를 주장, 벤더 리뷰 플랫폼, 자기 결론을 지지하는 자기 추정 |

---

## 5. 격리(rejection) 기준

`evidence/evidence_rejected.jsonl` 로 이동시키고 `rejection_reason` 을 기재한다.

1. **접근불가**: R 의 실호출에서 404 / 410 Gone / 페이월·봇차단으로 본문 미확인 + 대체경로 교차확인 실패
2. **원문불일치**: claim/value 가 그 URL 원문에 존재하지 않거나 다른 값
3. **원본 access_status = failed** 인데 R 도 재확인하지 못한 건
4. **URL 날조 의심**: 문법상 유효하나 실재하지 않는 경로

**격리하지 않는 경우** (구분 원칙): 기재 URL 이 죽었으나 R 이 **동일 발행주체의 정정 URL 에서 내용을 확인**한 건은 통과시키고 `r_reason` 에 `urlfix` 사유와 정정 URL 을 남긴다. 잘못된 링크는 결함이지만 사실 자체가 거짓인 것과는 다르기 때문이다.

---

## 6. 실검증 쿼리·호출 목록 (계획)

### 6-1. 가격·ASP (제조사 직판 vs 유통사)
- ecatalog.corning.com 354234 / 356255 / 354230 / 354249 / 354789 / 354221
- thermofisher.com A1413202 / A1413201 / A29249 / 23017015
- stemcell.com 200-0960, yeasenbio 40192, 101bio P720, qkine Qk025
- fishersci.com 08774406(356255) / cb40234(354234) / BME00105 / NC2107418 / 50360230 — **동일 제품의 제조사가 vs 유통가 마진 실측**

### 6-2. 공시
- SEC EDGAR glw-20251231.htm (Corning 10-K), tech-20250630x10k.htm (Bio-Techne 10-K)
- investor.corning.com 2025 실적발표, ir.collplant.com Q1 2026, lgcorp.com 2025 실적

### 6-3. 규제 타이밍
- congress.gov S.5002 원문 / govinfo BILLSTATUS H.R.2821
- fda.gov/media/191986/download (Year One), fda.gov newsroom Roadmap PDF
- EU 집행위 C(2026) 3497 PDF, OECD TGP work plan PDF, MFDS 보도자료
- health.ec.europa.eu ATMP GMP 가이드라인 PDF (7.13/7.15/7.16 조문)
- eCFR 21 CFR 1271.10

### 6-4. COGS
- zedira.com Andracon T300 정가표, PMC10540378 (Pichia 500 L), bioprocesstools 발효원가
- 보강 탐색: Pichia 재조합 콜라겐 titer 피어리뷰 논문

### 6-5. FTO
- patents.google.com US8642339B2 / US4829000A / US20230034857A1 / US8455717B2
- freepatentsonline 기재 URL 5건 **원문 그대로 재실행** (검색결과 건수 재현성 확인)

### 6-6. 전환장벽
- PMC8967832 (CV 실측), PMC12713094 (Adv Sci 리뷰), frontiersin fncel.2024.1351734
- tuvesonlab 프로토콜 PDF (9.4~9.9 mg/mL), PMC10070462 (콜라겐 1/10 가격)
- ddrcc.wustl.edu 코어 요율표 PDF, selectscience VOC

### 6-7. 시장규모
- NCBI eutils / Europe PMC REST / ClinicalTrials.gov API — 건수 직접 재현
- mordorintelligence, giiresearch(QYResearch), citeline

### 6-8. 보강 탐색 쿼리 (게이트 FAIL 대응)
1. `techno-economic analysis recombinant collagen Pichia pastoris production cost per kg`
2. `Matrigel lot-to-lot stiffness variability quantified rheology coefficient of variation organoid`
3. `European Commission Roadmap phasing out animal testing C(2026) 3497`
4. `OECD Test Guidelines work plan project 4.176 Korea organoid`
5. Corning 공식 앱노트 CLS-AC-AN-449 (탄성계수 원자료)

---

## 7. 산출물

| 파일 | 내용 |
|---|---|
| `docs/R_plan.md` | 본 문서 |
| `evidence/evidence_verified.jsonl` | 통과 레코드. 원본 필드 전량 보존 + `verified_by:"R"`, 재판정 `tier`/`confidence`, `r_reason`, `r_score`, `r_axes`, `r_buckets`, `sampled`, `orig_tier`, `orig_confidence` |
| `evidence/evidence_rejected.jsonl` | 격리 레코드 + `rejection_reason` |
| `docs/R_credibility.md` | 분포 통계, 6항목 스코어카드, 게이트 판정, 재조사 지시, 보강근거, DoD |

보강 레코드는 `id = 원본ID + "-R"`, `owner_agent:"R"` 로 `evidence_verified.jsonl` 에 추가한다.

---

## 8. 실행 결과 요약 (본 계획 대비)

| 계획 | 목표 | 실적 |
|---|---|---|
| 전 레코드 재평가 | 438건 | **438건** (통과 417 + 격리 21) |
| 실검증 | ≥70건 | **118건** (원본 레코드 기준) |
| 원문 숫자 직접 확인 | ≥15건 | **32건** |
| 웹 호출 | ≥70회 | **93회** (WebFetch 87 + WebSearch 6) |
| 보강 근거 | ≥5건 | **8건** |
