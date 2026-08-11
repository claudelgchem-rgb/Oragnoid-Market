# B. 규제·정책 드라이버 & 제품등급 요구사항

Agent B / 작성일 2026-08-11 / 근거파일 `evidence/evidence_B.jsonl` (E-001 ~ E-079, 79건)
대상 제품가설: 재조합·정제 콜라겐(single + triple 혼합) + 미생물 transglutaminase(mTG) 가교 기반 Defined Organoid Matrix

---

## 0. 결론 요약 (Executive Summary)

| 항목 | 판정 | 핵심 근거 |
|---|---|---|
| 규제가 만드는 수요의 성격 | **"동물시험 의무 삭제(permissive)"이지 "오가노이드 승인(qualification)"이 아니다** | FDAMA 2.0 정의문 `may include animal tests` [E-002]; FDA가 qualify 완료한 오가노이드/MPS 도구 0건 [E-021] |
| 2025-04 FDA 로드맵의 후속 조치 | **실재함.** 2025-12~2026-06 사이 draft guidance 3건 + 상설 qualification 프로그램 1건 + DB 1건 | [E-012][E-013][E-014][E-015][E-017][E-025] |
| 오가노이드 vs organ-on-chip의 규제적 위치 | **organ-on-chip이 명백히 앞선다.** ISTAND 16건 초과 활성 제출물 중 FDA가 organoid로 명명한 건 0건 | [E-018][E-019][E-024] |
| 1차 타깃 제품등급 | **RUO (USP `<1043>` Tier 3) 로 출시하되, ISO 20399:2022 준거 품질시스템 위에서 제조하여 Tier 2 승격 경로를 설계** | [E-046][E-048][E-049][E-061] |
| RUO→GMP 가격 프리미엄 | **중앙값 1.75배** (실측 매칭 4쌍, 범위 1.32~2.45배) | [E-077] |
| 이식용 매출 유의미화 시점 | **2033년** | [E-055][E-067][E-079] |

**한 문장 판정:** 규제는 오가노이드 매트릭스 수요를 *강제*하지 않는다. 규제가 하는 일은 (a) 동물시험을 선택사항으로 만들어 NAM 시장의 상한을 열고 [E-002], (b) 동물유래 원부자재에 TSE·바이러스 문서부담을 강제로 부과하여 [E-050][E-053] 정의된(defined) 무동물 매트릭스를 *상대적으로* 유리하게 만드는 것이다. 따라서 사업은 "규제 강제 수요"가 아니라 "규제가 만든 상대적 원가·리스크 우위"로 설계해야 한다.

---

## 1. FDA Modernization Act 2.0 / 3.0 — 법조문으로 본 실체

### 1.1 두 개념의 분리 (가장 중요한 구분)

| 개념 | 정의 | 현재 상태 |
|---|---|---|
| **동물시험 의무 삭제 (permissive)** | 법령이 "동물시험을 해야 한다"고 요구하지 않게 됨. 스폰서가 대안을 *제안할 수 있음* | **완료 (2022-12-29)** [E-003] |
| **오가노이드 승인 (qualification)** | 특정 오가노이드 도구가 특정 context of use에 대해 FDA에 의해 공식 자격을 인정받아, 어떤 스폰서든 그 데이터를 제출하면 수용됨 | **오가노이드 0건** [E-021] |

이 둘은 완전히 다르다. (a)는 "제출해도 된다"이고 (b)는 "제출하면 받아준다"이다. 매트릭스 수요를 만드는 것은 (b)이며, (b)는 2026-08-11 현재 오가노이드에 대해 존재하지 않는다.

### 1.2 FDAMA 2.0 법조문 원문

S.5002는 FD&C Act §505(i)(1)(A)의 `preclinical tests (including tests on animals)`를 `nonclinical tests`로 치환하고, §505(i)(2)(B)의 `animal`도 `nonclinical tests`로 치환했다 [E-001]. 그리고 §505(z)에 다음 정의를 신설했다 [E-002]:

> "A test conducted in vitro, in silico, or in chemico, or a non-human in vivo test that occurs before or during the clinical trial phase of the investigation of the safety and effectiveness of a drug, **and may include animal tests**, or non-animal or human biology-based test methods, such as cell-based assays, **microphysiological systems**, or bioprinted or computer models."

세 가지를 주목해야 한다.
1. `and may include animal tests` — 동물시험은 **삭제되지 않았고 정의 안에 그대로 남아 있다** [E-002].
2. 열거된 대안 중 `microphysiological systems`는 명시되었으나 **`organoid`라는 단어는 법조문에 없다** [E-002].
3. 이 조문은 독립 법률이 아니라 Consolidated Appropriations Act, 2023 (P.L. 117-328) 제3209조 `Animal Testing Alternatives`로 2022-12-29 제정되었다 [E-003].

### 1.3 FDAMA 3.0 (H.R.2821) — 정확한 현재 상태

govinfo Bill Status 원본 데이터 기준 [E-004]:

| 날짜 | 조치 |
|---|---|
| 2025-04-10 | 하원 발의, Energy and Commerce 위원회 회부 |
| 2026-05-13 | 소위원회 구두표결 통과 |
| 2026-05-21 | 전체위원회 44-0 가결 |
| 2026-06-18 | 위원회 보고 (H. Rept. 119-706), Union Calendar No. 614 |
| **2026-07-20** | **하원 구두표결(voice vote) 통과** |
| **2026-07-21** | **상원 접수 (Received in the Senate)** |
| 2026-08-11 | **미제정 (not enacted)** |

그리고 3.0의 실제 요구사항은 동물시험 금지가 아니다 [E-005]:

> "This bill requires the FDA to publish an interim final rule implementing a provision of the Consolidated Appropriations Act of 2023 ... The rule must replace references to animal tests, data, studies, models, and research with **references to nonclinical tests** ... throughout the FDA's regulations governing investigational new drug applications. The rule must be published **within one year of the bill's enactment**."

즉 3.0은 2.0의 법률 변경을 *시행규칙(21 CFR Part 312)에 반영*하라는 절차법이다. 오가노이드 승인과는 무관하다.

**사업적 함의:** 3.0이 2026년 하반기~2027년 상반기에 제정된다고 가정하면, interim final rule은 2027~2028년에 나온다. 이 시점에 IND 규정 문언에서 `animal`이 사라지므로 **스폰서의 심리적 장벽이 제거되는 시점이 2028년**이다. 이것이 NAM ramp의 base 시나리오 변곡점 근거다.

---

## 2. FDA Roadmap (2025-04-10) 과 그 이후 14개월의 실제 경과

### 2.1 Roadmap 원문의 구체 마일스톤

초기 대상 modality는 **monoclonal antibody(mAb)** 로 확정되어 있다 [E-007]:
> "This program is intended to begin with monoclonal antibodies (mAb) as a promising area for reducing animal use in preclinical safety testing, and then will expand to include other biological molecules and eventually new chemical entities and medical countermeasures."

3년 내 구현 항목 6개 [E-007 원문 문서]:
1. 기존 국제 인체 독성 데이터 활용
2. 스폰서에게 NAM 데이터를 동물 데이터와 **병행 제출**하도록 장려 — 원문에 `we welcome organoid or in silico study results in IND/BLA packages as **supportive data**` (보조 데이터로서 환영)
3. 오픈액세스 독성 데이터 저장소 구축
4. mAb의 6개월 영장류 독성시험을 1개월 + NAM으로 3개월로 단축
5. 타 약물군으로 시험기간 단축 확대
6. 반기별 지표 추적

장기 목표는 **3~5년 내 동물시험을 예외로 만드는 것**이다 [E-009] → 2025-04 기준 **2028~2030년**.

경제적 동인의 정량치: mAb 개발비 650~750백만 USD, 최대 9년, 전형적 프로그램에 NHP 144마리, NHP 1마리당 최대 50,000 USD [E-011], 동물시험 통과 신약의 90% 초과가 승인 실패 [E-010].

오가노이드는 `In Vitro Human-Derived Systems (Organoids and Microphysiological Systems)` 절에 명시되었다 [E-008]. 그러나 **로드맵이 인용한 유일한 정량 검증 사례는 Liver-Chip(organ-on-chip)이며 간독성 약물의 87%를 정확 식별했다는 수치다** [E-022]. 오가노이드에 대한 정량 성능 근거는 로드맵 본문에 없다.

### 2.2 2025-04 이후 ~ 2026-08 후속 조치 — **실제로 존재하며, 다음과 같다**

(질문에 대한 직접 답: "없다"가 아니라 "있다". 다만 그 내용이 오가노이드 승인이 아니라는 점이 핵심이다.)

| 날짜 | 조치 | 오가노이드 관련성 |
|---|---|---|
| 2025-04 | CDER NAMs Coordinating Committee 설치 [E-012] | 간접 |
| 2025-07-07 | FDA-NIH 국제 규제기관 워크숍 (EMA, BfR, PMDA, TGA 참가) [E-012] | 간접 |
| **2025-07-31** | **ISTAND를 pilot → 상설 DDT qualification program으로 전환** [E-017] | **직접(경로 개설)** |
| 2025-08-27 | FDA-NIH MOU 225-25-012, Complement-ARIE 연계 [E-028] | 간접 |
| 2025-09 | NIH, FNLCR에 **8,700만 USD / 3년 Standardized Organoid Modeling(SOM) Center** 계약 [E-026] | **직접(공급측)** |
| 2025-10 | CDER `Streamlined Nonclinical Studies and Acceptable NAMs` 검색가능 DB 공개 (7개 독성 범주, 40+ 컨텍스트) [E-025] | **직접(그러나 organoid/MPS 등재 0건)** |
| 2025-11 | FDA NCTR/CDER + Emulate + UNC, liver-on-chip DILI 바이오마커 측정 프로토콜 논문 [E-012] | organ-chip |
| **2025-12-02** | **`Monoclonal Antibodies: Streamlined Nonclinical Safety Studies` draft guidance** (의견마감 2026-02-02) [E-013] | 간접(WoE에 NAM 허용) |
| 2025-12-08 | 최초 qualify된 DDT = **AIM-NASH (AI)**, 오가노이드 아님 [E-021] | 반증 |
| 2025-12 | Dao & Sadrieh, CDER 15년 NAM 제출 분석 발표 [E-023][E-024] | **직접(수요 실측)** |
| **2026-03-18** | **`General Considerations for the Use of NAMs in Drug Development` draft guidance** — 검증 4원칙 [E-014] | **직접(검증 기준 확정)** |
| 2026-03-18 | `Pyrogen and Endotoxins Testing: Q&A` Level 2 업데이트 — 재조합 엔도톡신 시약 전환 [E-016] | 자사 lot release에 직접 |
| 2026-04-20 | Year One 경과보고서 발표 [E-012] | 종합 |
| **2026-06-01** | **`Oncology Pharmaceuticals: Streamlined Nonclinical Safety Studies for Biologics and Conjugated Products` draft guidance** (FDA-2026-D-2839) [E-015] | mAb → 종양 biologics 확대 실증 |

**해석:** 로드맵은 문서상 죽지 않았고 오히려 초과 달성으로 자체평가되었다(8개 목표 중 2개 Exceeded, 6개 Achieved) [E-012]. 그러나 14개월간 나온 산출물의 성격은 전부 **(i) 절차·검증 프레임워크, (ii) 동물시험 기간 단축, (iii) organ-on-chip 지원**이며, **오가노이드를 특정 endpoint에 대해 수용한다는 규제 문서는 단 한 건도 나오지 않았다.**

### 2.3 2026-03-18 NAM 검증 4원칙 — 우리 제품에 대한 직접 요구

`General Considerations for the Use of NAMs` draft guidance의 4원칙 [E-014]:

| 원칙 | 원문 | Defined Matrix 공급자에게 요구되는 것 |
|---|---|---|
| Context of Use | 규제 목적의 명확한 정의 | 매트릭스 자체는 CoU를 가질 수 없음 → **고객(오가노이드 도구 개발자)의 CoU에 종속** |
| Human Biological Relevance | 방법이 독성을 어떻게 평가하는지 입증 | 매트릭스 조성이 인체 ECM을 어떻게 대변하는지 문서화 |
| **Technical Characterization** | **robust protocol에 의한 과학적 신뢰 확립** | **lot-to-lot 재현성 데이터 = 우리 제품의 핵심 판매논거** |
| Fit-for-Purpose | 규제 의사결정 지원 보증 | 고객 검증 패키지에 우리 CoA·안정성 데이터가 삽입되어야 함 |

**사업적 함의:** 이 가이던스는 매트릭스 공급자에게 *직접* 의무를 부과하지 않는다. 대신 **고객이 규제 제출을 하려면 매트릭스의 technical characterization을 자기 dossier에 넣어야 하므로**, 조성이 미정의된 BME를 쓰는 고객은 검증 부담을 스스로 져야 한다. 이것이 우리의 유일한 규제 기반 pull이며, 그 강도는 "강제"가 아니라 "부담 전가"다.

---

## 3. ISTAND / DDT Qualification — 오가노이드의 실제 위치 (정량 비교)

### 3.1 건수

| 지표 | 수치 | 근거 |
|---|---|---|
| ISTAND pilot 기간 수용 건수 | 8건 (AI 3, 무동물 전임상 안전성 도구 2, 조직 관련 신규법 2, 통계 1) | [E-017] |
| 2026년 초 활성(active) 제출물 | **16건 초과** | [E-018] |
| 그중 FDA가 열거한 complex 3D 항목 | liver MPS 1건(최종 qualification 단계), 추가 liver MPS LOI 6건, 임상 DILI MPS, human kidney chip, chorio-decidual organ-on-chip, iPSC-cardiomyocyte | [E-019] |
| 그중 **`organoid`로 명명된 제출물** | **0건** | [E-019] |
| **qualification이 완료된 오가노이드/MPS 도구** | **0건** (최초 qualify 도구는 AI 기반 AIM-NASH, 2025-12-08) | [E-021] |
| ISTAND 수용 = qualification 여부 | **아님. LOI 수용은 3단계 절차의 1단계** | [E-020] |

### 3.2 organ-on-chip 대비 오가노이드 상대 위치 — 정량

FDA가 Year One 보고서에서 이름을 붙여 열거한 complex 3D 제출물을 세면 **MPS/organ-on-chip 계열 ≥5개 프로그램(liver MPS 계열만 7건 이상의 LOI 포함), organoid 계열 0개**다 [E-019].

> **규제 qualification 파이프라인에서 오가노이드의 점유율 = 0 / (5+) = 0%**

이는 우연이 아니라 CDER의 15년 제출 데이터와 정합한다 [E-024]:
> "In vitro NAMs, including stem cell-derived and sandwich culture models, showed higher prevalence compared to **3D models and organ chip or MPS models**."

즉 in vitro NAM 제출(전체 NAM 제출의 44% [E-023]) 안에서도 3D 모델은 2D 줄기세포 유래 모델·sandwich culture보다 **아래**에 있다.

결정적으로, 2025-10 공개된 CDER `Streamlined Nonclinical Studies and Acceptable NAMs` DB(7개 독성 범주, 40개 초과 컨텍스트)에 **organoid / MPS / organ-on-chip은 명시적 수용 NAM으로 등재되어 있지 않다** [E-025]. 등재된 것은 hiPSC-CM(QT), in vitro liver model(DILI), reconstructed human epidermis, in silico secondary pharmacology, weight-of-evidence 등이다.

**왜 organ-on-chip이 앞서는가(구조적 이유):** organ-on-chip은 *디바이스*이므로 단일 제조사가 device + 프로토콜 + 데이터 전체를 통제하여 하나의 CoU로 qualification 패키지를 낼 수 있다. 오가노이드는 *배양 방법론*이므로 세포원·배지·**매트릭스**가 모두 변수이며, 그중 매트릭스가 BME(비정의 조성)인 한 Technical Characterization 원칙[E-014]을 충족할 수 없다.

> **이것이 본 사업의 가장 강력한 규제 논거다: 오가노이드가 규제 qualification 레이스에서 뒤처진 원인의 상당 부분이 매트릭스의 비정의성이며, 그 원인을 제거하는 것이 우리 제품이다.** 단, 이것은 우리 제품이 오가노이드 qualification의 *필요조건*이라는 뜻이지 *충분조건*이 아니며, 수요는 오가노이드 도구 개발자가 qualification에 착수할 때 비로소 발생한다.

---

## 4. NAM 예산·조직 변화

| 주체 | 조치 | 금액/규모 | 근거 |
|---|---|---|---|
| NIH | ORIVA (Office of Research Innovation, Validation and Application) 신설, Office of the Director 산하 | **전용 예산 미공개** | [E-027] |
| NIH / NCI / FNLCR | **Standardized Organoid Modeling (SOM) Center** | **87,000,000 USD / 최초 3년 (2025-09)** | [E-026] |
| FDA CDER | NAMs Coordinating Committee(2025-04), core NAMs workgroup(2026-01), NAMs Integrated Review Team(NAMs-IRT) 2026 파일럿 | 금액 미공개 | [E-012] |
| FDA + NIH | MOU 225-25-012 (2025-08-27), Complement-ARIE 연계 | 금액 미공개 | [E-028] |
| ICCVAM / NICEATM | 18개 연방기관, CAMERA 데이터베이스 베타 2025년 중반 목표 | 금액 미공개 | [E-029] |

**SOM Center가 본 사업에 갖는 의미 (양날의 검):**
- (+) 8,700만 USD가 "재현 가능한 오가노이드 프로토콜"에 투입된다 [E-026]. 표준 프로토콜은 반드시 매트릭스를 지정하게 되며, 정의된 매트릭스가 지정될 확률이 높다 → 사실상의 de facto 표준 진입 기회.
- (−) SOM Center가 특정 상용 매트릭스를 표준으로 채택하면 **경쟁사가 선점할 경우 우리는 구조적으로 배제된다.** 이는 2027~2028년에 결판나는 시간 민감 이슈다. → Agent G(GTM)에 이관: FNLCR/SOM Center 조기 접촉이 최우선 파트너십 액션.

또한 NIH ORIVA는 신설되었으나 **전용 예산이 공개되지 않았다** [E-027]. 예산 없는 조직 신설은 정책 실행력의 불확실성 지표이므로, NAM ramp의 conservative 시나리오는 이 점을 반영한다.

---

## 5. 국제 규제 (EMA/ICH/OECD/EU/중국/일본/한국)

### 5.1 EU — 2026-06-01 로드맵의 실제 범위 (중요한 한계)

유럽집행위원회는 2026-06-01 `Roadmap towards phasing out animal testing for chemical safety assessments` (C(2026) 3497 final)을 채택했다 [E-030]. 15개 법령 도메인, 30개 초과 권고, SWD(2026) 144 동반.

**그러나 각주 20이 결정적이다** [E-031]:
> "Only chemical pharmaceuticals come under the scope; **biologicals, vaccines, gene therapies; advanced therapy medicinal products and novel therapy veterinary medicinal products are excluded.**"

즉 **오가노이드 수요의 최대 원천인 바이오의약품과 ATMP는 EU 로드맵 범위 밖이다.** EU 자체 통계로도 2015-2023년 EU 규제목적 동물사용 1,500만 마리 초과 중 약 40%만 화학물질 안전성 평가이며, 나머지 60%의 대부분이 "화학물질이 아닌" 백신·항체·혈액제제다 [E-034]. 즉 로드맵은 동물사용의 40% 영역만 겨냥한다.

의약품(H) 도메인에서 complex in vitro model 관련 조치는 `Reduction through use of complex in vitro models to predict drug-induced liver injury / pharmacokinetic parameters / cardiotoxicity / immunotoxicity`이며 **Short-/mid-term의 Reduction 목표**로 분류되었다 [E-033]. Replacement가 아니다. 비동물 평가 프레임워크 자체의 확립은 **Long-term**이다 [E-032].

일정: 단기 조치 입법화 **늦어도 2029년말**, 2029년 고위급 콘퍼런스로 점검 [E-032]. Directive 2010/63/EU는 `as soon as scientifically possible`이라는 **기한 없는** 목표를 규정할 뿐이다 [E-036].

EU 문서가 인용한 시장 수치: 세포기반 기술 시장 2028년 265억 EUR, EU 점유 약 30% [E-035] (2차 출처이므로 Agent A의 삼각측량 입력으로만 사용).

### 5.2 ICH

ICH S1B(R1) 부속서(2022-08 공표, FDA 2022-11-01 채택)는 6개 weight-of-evidence 인자로 2년 랫드 발암성시험 생략을 허용한다 [E-037]. **규제 수용의 실제 형태가 "단일 NAM이 단일 동물시험을 대체"가 아니라 "WoE 패키지"임을 보여주는 선례**이며, FDA의 mAb·종양 가이던스도 동일 구조다 [E-013][E-015]. FDA 로드맵은 ICH S6(R1)/S6 개정 제안과 궁극적으로 `ICH guideline on NAMs`를 목표로 명시했으나, 2026-08 현재 그런 ICH 가이드라인은 존재하지 않는다.

### 5.3 OECD — 오가노이드는 아직 Test Guideline이 아니라 DRP 단계

OECD Test Guidelines Programme 작업계획(2025-07 기준) 전체에서 `organoid`는 단 하나의 프로젝트에만 등장한다 [E-038][E-039]:

**Project 4.176** — `Detailed review paper on the use of human iPSCs in regulatory toxicology and on specific target organ toxicity (liver) test method using liver organoid`
- Lead: **Korea / OECD 사무국**
- 작업계획 편입: 2024년
- 국제전문가그룹 구성: 2024-06 / DRP 개발 착수: 2025 Q1 / 초안 제출: 2025 Q2-Q3
- **WNT 승인 최단 시점: 2026-04**

**DRP는 Test Guideline이 아니다.** DRP는 현황 검토 문서이고, 여기서 TG로 가려면 별도 프로젝트·검증 라운드·WNT 채택이 필요하다. 동일 작업계획의 다른 사례(Project 4.188 in vitro Toxicokinetics DRP: 2025 착수 → 2027-04 승인 목표 [E-043])를 보면 DRP 자체에만 2년이 걸린다.

> **따라서 2026-08-11 현재 오가노이드를 채택한 OECD Test Guideline은 0건이며** [E-039], 간 오가노이드 TG의 현실적 최단 시점은 DRP 승인 2026-04 + TG 개발·검증 3~5년 = **2029~2031년**이다.

OECD GIVIMP (Series on Testing and Assessment No.286, 2018)는 in vitro 방법의 10개 영역을 규정하며 영역 4가 `Apparatus, material and reagents`다 [E-040]. 매트릭스 품질 요건의 국제 근거이지만 구체적 매트릭스 규격을 정하지는 않는다.

### 5.4 한국 (MFDS) — 국제표준화의 실질적 리더

식약처는 2025-06-16 `오가노이드 시험법 국제표준화 추진위원회`를 발족했다 [E-041]. 간·장 오가노이드 품질평가 과제가 2024-04 OECD DRP 과제로, 2025-06 ISO 생명공학 총회 공식과제로 채택되었다. 이는 OECD Project 4.176의 Lead가 Korea인 것과 정확히 정합한다 [E-038].

**사업적 함의 (LG화학에 특히 중요):** 간 오가노이드 국제 시험법 표준의 **작성 주체가 한국 규제기관**이다. 표준 문서에 "매트릭스는 조성이 정의된 것을 사용하고 다음 항목을 보고한다"는 문구가 들어가면 그것이 우리 제품의 규격이 된다. → Agent G에 이관: MFDS 독성연구과 및 국제표준화 추진위원회 참여가 규제 기반 GTM의 최고 레버리지.

### 5.5 일본 (PMDA)

AMED-MPS 프로젝트 2017년 개시, PMDA 2020년부터 옵서버 참여, CSAHi-MPS 산업 컨소시엄 활동 중 [E-042]. 여기서도 organoid가 아니라 **MPS/organ-on-chip 중심**이다. OECD Project 4.188(in vitro Toxicokinetics DRP)의 주도국이며 전문가 회의를 2025-06 MPS World Summit에서 개최했다 [E-043].

재생의료 측면: 2025-05 말 기준 재생의료등제품 **22건 승인**, 조건부·기한부 승인 1호 HeartSheet는 시판후 유효성 입증 실패로 **철수** [E-045]. PMD Act 시행(2014) 후 11년간 22건이라는 속도가 재생의료 상용화의 현실적 벤치마크다.

### 5.6 중국 (NMPA)

2024-12 `Guidance for Research and Evaluation on Chemistry, Manufacture and Control of Human Stem Cell Products (Trial)` 공표 [E-044], 2025-07 세포치료제 변경관리 draft guidance. **오가노이드 전용 기술지도원칙은 5개 이상의 검색 쿼리로 탐색했으나 확인되지 않았다** [E-044]. 부재를 사실 그대로 기록한다. 함의: 중국 시장은 규제 pull이 아니라 연구비·CRO 수요 pull로 접근해야 한다.

---

## 6. 원부자재 등급 규제 원문 — 우리 제품이 실제로 받는 요구사항

### 6.1 미국: USP `<1043>` Tier 체계

USP General Chapter `<1043>`는 ancillary material을 4개 tier로 분류한다 [E-046]:

| Tier | 정의(원문 요지) | 우리 제품의 해당 여부 |
|---|---|---|
| Tier 1 | 허가된 biologic / 승인 drug / 승인·허가 medical device, 또는 이식용 biomaterial 의도 | 장기 목표 |
| **Tier 2** | **저위험·well-characterized. 의약품·바이오·의료기기 제조 용도로 생산된 재료** | **GMP 라인 목표** |
| **Tier 3** | 중위험. IVD 용도 등으로 생산된 재료. Tier 1/2보다 많은 qualification 필요 | **RUO 출시 시점 위치** |
| Tier 4 | 최고위험. cGMP 미준수 재료. 사용 전 광범위한 qualification 필요 | Matrigel 등 BME의 위치 |

qualification 프로그램은 5개 영역이다: 식별 / 선정·적합성 / 특성분석 / 공급자 검증 / QA·QC [E-047]. Tier 1·2에는 **DMF cross-reference**가 qualification 활동으로 명시된다 [E-047]. 동물유래 AM은 **원산국(country of origin) 문서화**로 TSE 우려에 대응해야 한다 [E-047].

> **핵심 통찰:** BME는 마우스 육종 유래 + cGMP 미준수 → **Tier 4**. 재조합 콜라겐 + 미생물 mTG로 품질시스템 하에서 생산하면 **Tier 2~3**. 고객 입장에서 Tier 4 → Tier 2 전환은 qualification 활동을 대폭 줄인다. 이것이 프리미엄의 실질 근거다.

### 6.2 ISO 20399:2022

세포·유전자치료제 제조에 사용되는 ancillary material의 공급자·사용자 요구사항 규정. ISO/TS 20399-1/-2/-3:2018을 대체·통합 [E-048]. identity, purity, stability, biosafety, performance의 **lot-to-lot 일관성** 유지를 공급자에게 요구한다. ISO/AWI 20399-4(CoA 및 원산지증명 요건)가 개발 중이다 [E-048].

**실무 함의:** 상용 "GMP grade" 표기의 실질은 대개 "ISO 20399:2022 준거 + ISO 9001:2015 시설 + USP `<1043>` 품질관리"이며 의약품 GMP 인증과 동일하지 않다 [E-070][E-074]. 이는 우리가 GMP 라인에 진입할 때의 **실제 진입비용이 의약품 GMP보다 낮다**는 뜻이다.

### 6.3 EU GMP Annex 2 계열 — ATMP GMP 가이드라인 (2017-11-22)

**7.13항 (결정적 조문)** [E-049]:
> "While raw materials should be of pharmaceutical grade, **it is acknowledged that, in some cases, only materials of research grade are available.** The risks of using research grade materials should be understood ... Additionally, the suitability of such raw materials for the intended use should be ensured, including –where appropriate– by means of testing (e.g. functional test, safety test)."

→ **GMP grade는 법적으로 강제되지 않는다.** 이것이 P5(규제가 defined matrix를 강제한다) 전제를 무너뜨리는 1차 근거다.

**7.16항 (실제로 강제되는 것)** [E-050]:
> "Compliance with the latest version of the Note for Guidance on Minimising the Risk of Transmitting Animal Spongiform Encephalopathy (TSE) Agents via Human and Veterinary Medicinal Products **is required**."
> "the ATMP manufacturer should filter the material prior to use (**0.1 μm** filter), unless the supplier ... has certified that the raw material has been tested and is mycoplasma free."

→ 강제되는 것은 **TSE 준수(EMA/410/01 rev.3)** 와 **마이코플라스마 0.1 µm 여과**다. 둘 다 **동물유래 재료에 붙는 부담**이며, 무동물 재조합 재료는 이 부담에서 자유롭다.

**7.15항** [E-051]: EU에서 의약품으로 허가된 원료(사이토카인, 인혈청알부민, 재조합단백질)는 공급자 CoA조차 요구되지 않으며 허가 의약품 사용이 권장된다. → 등급 사다리를 올라갈수록 고객의 문서 부담이 줄어드는 구조.

**매트릭스가 최종제품에 잔존하는 경우** [E-052]: `matrixes or devices that are a component of the ATMP` 로 취급되며, combined ATMP의 의료기기 구성요소는 EU 의료기기 법규 준수가 요구된다. 즉 **raw material → 구조성분(device)으로 승격되며 요건이 급증한다.** Regulation (EC) No 1394/2007의 tissue engineered product 정의도 `scaffolds or matrices`를 추가 물질로 명시한다 [E-059].

### 6.4 Ph. Eur. 5.2.12 — 우리 제품 포지셔닝의 최적 조문

Ph. Eur. 5.2.12 (01/2017:50212)는 information용(법적 비구속) 챕터이나 규제기관이 사실상 준수를 요구한다. 원문 [E-053]:

> "**From a risk perspective, the use of raw materials free from human or animal substances is preferred.**"

원료 3범주 분류 [E-053]:
1. 인간 또는 동물 유래 원료
2. 인간·동물 유래 물질을 사용하여 생산된 원료
3. **인간·동물 유래 물질이 없는 원료**

> **재조합 콜라겐(비동물 발현계) + 미생물 유래 mTG는 범주 3을 목표로 할 수 있다. Matrigel은 범주 1이다.** 이것이 규제 문서에서 확보 가능한 가장 명시적인 우위 문구다. 단 "preferred"이지 "required"가 아님을 정확히 인식해야 한다.

시험 요구사항 [E-054]:

| 항목 | Ph. Eur. 방법 | 규격 |
|---|---|---|
| 무균 또는 미생물오염도 | 2.6.1 / 2.6.12 | 원료별 정의 |
| **세균내독소** | **2.6.14** | **"less than the limit defined for the particular raw material"** — 절대값을 원료별로 위임 |
| **마이코플라스마** | **2.6.7** | **"Raw materials are free from mycoplasmas"** (절대 요건) |
| 바이러스 오염 | 5.1.7 위험평가 기반 | 인간·동물 유래 시 필수 |
| TSE | 5.2.8 | 인간·동물 유래 시 필수 |
| 원소불순물 / 총단백 / 관련물질 / 수분 | 2.5.33 / 2.5.12 등 | 원료별 정의 |

**엔도톡신 한도의 실무 결정 방법:** 약전은 절대값을 위임했으므로, 실무는 최종 세포치료제의 5 EU/kg 체중 한도에서 역산하여 원부자재 기여분을 배분한다. 시장 실측 벤치마크는 cell therapy grade 재조합 단백질의 **< 0.05 EU/µg protein** [E-070] 및 **≤ 0.1 EU/µg** [E-073]이다. 매트릭스는 단백질 투입량이 사이토카인보다 3~4 자릿수 크므로 µg당 한도를 그대로 적용하면 비현실적이며, **mg당 또는 mL당 규격으로 설정**해야 한다. → 가정 B-A2 참조.

무균시험은 USP `<71>` (14일 배양 후 육안판정) [E-057]. 매트릭스는 세포치료제와 달리 유효기간이 길어 14일 시험이 운영상 제약이 되지 않는다 → **세포치료제 대비 lot release 부담이 낮은 카테고리**다.

FDA는 2026-03-18 `Pyrogen and Endotoxins Testing: Q&A` Level 2 업데이트로 재조합 엔도톡신 시약(rFC 등) 전환 유연성을 제공했다 [E-016] → 자사 lot release 시험 설계에 직접 적용 가능.

### 6.5 21 CFR Part 1271 — 이식 경로의 구조적 결정 요인

21 CFR 1271.10(a) 원문 [E-055]:
> "(3) The manufacture of the HCT/P **does not involve the combination of the cells or tissues with another article, except for water, crystalloids, or a sterilizing, preserving, or storage agent**, provided that the addition ... does not raise new clinical safety concerns with respect to the HCT/P"

> **결정적 함의:** 오가노이드를 매트릭스와 결합하는 순간 (a)(3)을 위배하여 **361 HCT/P 단독 규제 자격을 상실하고 351 biologic(IND/BLA) 경로로 확정된다.** 즉 "이식용 오가노이드 + 매트릭스"는 예외 없이 완전한 임상시험·BLA 경로를 밟아야 하며, 이것이 clinical_timing_year를 구조적으로 늦추는 가장 강한 요인이다.

ISO 13022:2012는 생존 인체세포 함유 의료제품의 위험관리·처리관행 요구사항을 규정하며 동물조직 유래물은 ISO 22442 시리즈를 참조한다 [E-060].

### 6.6 DMF / Master File 제출 경로

FDA DMF 유형 [E-058]:
- **Type II**: `Drug Substance, Drug Substance Intermediate, and Material Used in Their Preparation; or Drug Product`
- **Type IV**: `Excipient, Colorant, Flavor, Essence, or Material Used in Their Preparation`
- Type I은 현재 접수 대상 아님

원부자재 공급자의 표준 경로는 **Type II DMF 등재 → 고객 IND/BLA가 Letter of Authorization으로 참조**하는 구조다. 최종제품에 잔존하지 않는 배양용 매트릭스는 Type II(제조에 사용되는 재료)가, 이식제의 구조성분으로 잔존하면 Type IV(excipient) 또는 결합제품 device 경로가 적합하다. USP `<1043>`도 Tier 1/2 재료의 qualification 활동으로 DMF cross-reference를 명시한다 [E-047].

**전략적 함의:** DMF 등재는 규제 의무가 아니라 **영업 자산**이다. DMF 번호가 있으면 고객이 자사 dossier에 우리 CMC 정보를 넣지 않고 참조만 하면 되므로 전환장벽이 급감한다. RUO 단계에서도 조기 등재 가치가 있다.

---

## 7. Matrigel의 임상 전환 — 규제 근거와 반증 사실

### 7.1 규제상 실제 장애 요인

| 요인 | 규제 근거 | 강도 |
|---|---|---|
| 마우스 육종(EHS) 유래 = Ph. Eur. 5.2.12 범주 1 | "raw materials free from human or animal substances is preferred" [E-053] | 권고 |
| TSE / 동물유래 위험평가 의무 | ATMP GMP 7.16 "Compliance ... **is required**" [E-050]; USP `<1043>` 원산국 문서화 [E-047] | **강제** |
| 마이코플라스마 부재 | Ph. Eur. 5.2.12 "Raw materials are free from mycoplasmas" [E-054]; 0.1 µm 여과 [E-050] — BME는 겔이므로 0.1 µm 여과 불가 | **강제 (기술적 충돌)** |
| 바이러스 오염 (LDEV 등 마우스 바이러스) | Corning이 LDEV/LDHV에 대해 3중 공정중·공정후 검사를 실시한다고 광고 [E-063] → 리스크 실재를 공급자 스스로 인정 | 실질 |
| 조성 미정의 / 로트 편차 | Corning 자사 벤치마킹에서 제네릭 BME 실측 단백질이 CoA 표기 대비 **47% 낮음**(표기 15.56 → 실측 8.37 mg/mL) [E-064]; 문헌은 Matrigel 로트간 편차를 오가노이드 이질성 원인으로 지목 [E-065] | 실질 |
| cGMP 미생산 → USP `<1043>` Tier 4 | [E-046] | 실질 |

**주의:** 위 어느 것도 "Matrigel의 임상 사용을 금지한다"는 조문이 아니다. **강제되는 것은 TSE 준수와 마이코플라스마 부재 입증이며, BME는 이 두 가지를 만족시키는 비용이 매우 높을 뿐이다.**

### 7.2 반증 확인 — ClinicalTrials.gov 실제 검색 (우리 가설에 불리할 수 있는 사실 포함)

ClinicalTrials.gov API v2로 2026-08-11 직접 조회한 결과 [E-062]:

| 쿼리 | 결과 |
|---|---|
| `query.term=Matrigel` (전문검색) | **19건** |
| `query.intr=Matrigel` (intervention 필드) | **2건** |
| 인체에 Matrigel을 투여·이식한 시험 | **0건** |

intervention 필드 2건의 실체:
- **NCT07129330** — RSPO3/SDC-1 Pathway Dysfunction in Alveolar Repair After ARDS. intervention = "Pathway profiling assay" (생체외 분석)
- **NCT05294107** — Intestinal Organoids. intervention = "Additional biopsies" (환자 생검을 받아 실험실에서 오가노이드 배양)

전문검색 19건의 나머지도 모두 혈관신생 assay, 오가노이드 배양, 조직 분석 등 **실험실 용도**이며, Matrigel이 환자에게 투여된 사례는 확인되지 않았다.

> **정직한 기록:** 예외 사례는 발견되지 않았다. 즉 이 항목은 우리 가설에 **유리**하다. 다만 "규제가 금지해서 0건"이 아니라 "0건이라는 사실이 관찰될 뿐"이며, 인과는 (i) 규제 문서 부담, (ii) 조성 미정의로 인한 CMC 불가능, (iii) 애초에 이식용 오가노이드 임상 자체가 극소수라는 세 요인의 혼합이다.

### 7.3 오가노이드 임상의 실제 규모

| 지표 | 수치 | 근거 |
|---|---|---|
| ClinicalTrials.gov `organoid` 전문검색 | 368건 | [E-068] |
| intervention 필드에 `organoid` 포함 | 224건 | [E-068] |
| `organoid transplantation` 검색 | 12건 | [E-067] |
| 실제 오가노이드/세포 전달 개입시험 | **4건 이하** | [E-067] |
| 최고 개발단계 | **Phase 2** (NCT07214649 Organoids for Bile Leaks, 2026-01 개시) | [E-067] |
| Phase 3 | **0건** | [E-067] |
| 승인 제품 | **0건** | [E-067][E-045] |

세계 최초 인체 오가노이드 이식은 2022-07-05 Tokyo Medical and Dental University(TMDU), 난치성 궤양성대장염, jRCTb032190207, 목표 8명 [E-066]. **2022년 최초 이식 후 4년이 지난 2026-08 현재에도 Phase 3 진입 사례가 0건이다.**

> 이식(12건) / 전체(368건) = **3.3%**. 오가노이드 임상 활동의 96.7%는 이식이 아니라 **PDO 약물감수성·모델링**이다 [E-068]. 이는 시장 세그먼트 우선순위를 재정렬해야 함을 의미한다.

---

## 8. RUO vs GMP 가격 프리미엄 — 실측

동일 공급자 · 동일 분자 · 동일 규격으로 매칭한 4쌍(웹 게시가, 2026-08-11 조회):

| # | 제품 | 규격 | RUO 가격 | GMP/CTG 가격 | **배수** | 근거 |
|---|---|---|---|---|---|---|
| 1 | Qkine Recombinant human FGF-2 (145 aa) | 1000 µg | £735.00 (Qk025) | £1,470.00 (Qk025-CTG) | **2.000×** | [E-069][E-070] |
| 1b | 동상 (교차확인) | 500 µg | £500.00 | £1,000.00 | 2.000× | [E-069][E-070] |
| 2 | Qkine Recombinant human activin A | 1000 µg | £3,190.00 (Qk001) | £4,785.00 (Qk001-CTG) | **1.500×** | [E-071] |
| 3 | PeproTech(Gibco) Human IL-3 | 100 µg | $686.00 | $1,678.00 (PeproGMP) | **2.446×** | [E-072] |
| 4 | PeproTech(Gibco) Activin A | 100 µg | $892.00 | $1,176.00 (PeproGMP) | **1.318×** | [E-073] |

**계산 (R4 Show-Your-Math):**
```
배수_i = GMP가격_i / RUO가격_i
배수 = [2.000 [E-070], 1.500 [E-071], 2.446 [E-072], 1.318 [E-073]]
정렬 = [1.318, 1.500, 2.000, 2.446]
중앙값 = (1.500 + 2.000) / 2 = 1.750
평균   = (1.318 + 1.500 + 2.000 + 2.446) / 4 = 1.816
→ gmp_premium_multiple = 1.75× (범위 1.32 ~ 2.45×)   [E-077]
```

**프리미엄이 사는 것(즉 우리가 GMP 라인에서 추가로 제공해야 하는 것)** [E-070][E-073]:
무균시험 · 마이코플라스마 음성 · 엔도톡신 < 0.05 EU/µg · 잔류 HCP < 10 ng/µg · 잔류 HCD < 10 ng/µg · N말단 서열분석 · 질량분석 확인 · 순도 > 98% (SDS-PAGE densitometry) · 바이알 회수율 > 95% · 완전 추적성 문서 · 무동물유래 인증서 · ISO 9001:2015 시설 / ISO 20399:2022 준거.

**중요한 해석상의 경고 (X 레드팀 대비 선제 기록):**
1. 위 4쌍은 모두 **재조합 단백질**이며 RUO 기준선이 이미 AOF·고순도다. 매트릭스 카테고리는 RUO 기준선이 BME(Tier 4)이므로 동일 배수가 그대로 적용된다는 보장이 없다.
2. 1.75×는 **동일 공급자 내부의 등급 간 배수**이지 "BME 대비 재조합 매트릭스의 가격 프리미엄"이 아니다. 후자는 Agent C(경쟁·가격)가 별도 산출해야 한다.
3. BioLamina는 동일 laminin-521에 대해 LN521(연구용) / MX521(임상지향) / CT521(세포치료용) 3단계 사다리를 운영하나 가격을 공개하지 않는다 [E-075]. 매트릭스형 원부자재의 등급 사다리 구조 자체는 업계 표준임을 확인.
4. REPROCELL StemFit bFGF(GMP Compliant) 750 USD vs StemFactor FGF-basic 50 µg 185 USD는 GMP품 용량 미표기로 단위당 배수 산출이 불가하여 **중앙값 계산에서 제외**했다 [E-076].

---

## 9. 규제 타임라인 표 (연도 – 이벤트 – 사업영향)

| 연도 | 이벤트 | 근거 | 우리 사업에 대한 영향 |
|---|---|---|---|
| 2010 | EU Directive 2010/63/EU — 과학적으로 가능해지는 즉시 동물시험 폐지 목표(기한 없음) | [E-036] | 배경. 강제 시한 없음 → 즉각 수요 없음 |
| 2011-03-05 | EMA/410/01 rev.3 TSE 지침 (OJ C 73) | [E-056] | 동물유래 매트릭스에 영구적 문서부담 부과 → 우리의 구조적 우위 |
| 2017 | Ph. Eur. 5.2.12 발효 (01/2017:50212) — "무동물 원료 preferred" | [E-053] | 포지셔닝 문구 확보 |
| 2017-11-22 | EU ATMP GMP 가이드라인 — 7.13 research grade 조건부 허용 | [E-049] | **GMP 강제 부재 확인 → RUO 우선 전략의 근거** |
| 2017 | 일본 AMED-MPS 프로젝트 개시 | [E-042] | 아시아 수요는 MPS 중심 |
| 2018 | OECD GIVIMP (GD No.286) | [E-040] | in vitro 시약 품질 국제 기준 |
| 2022-07-05 | 세계 최초 인체 오가노이드 이식 (TMDU, jRCTb032190207, 8명) | [E-066] | 이식 시장 t=0 |
| 2022-08 / 2022-11-01 | ICH S1B(R1) 부속서 / FDA 채택 | [E-037] | WoE 패키지가 규제 수용의 표준 형태임을 확립 |
| **2022-12-29** | **FDAMA 2.0 제정 (P.L. 117-328 §3209)** | [E-003] | **NAM 시장 상한 개방. 단 permissive** |
| 2024-04 | 한국 주도 간·장 오가노이드 과제, OECD DRP 과제 채택 | [E-041] | MFDS 접점 = 최고 레버리지 |
| 2024-06 | OECD Project 4.176 국제전문가그룹 구성 (Lead: Korea) | [E-038] | 표준 문안 형성기 시작 |
| 2024-09-24 | ISTAND, 최초 organ-on-chip(Liver-Chip) LOI 수용 | [E-020] | organ-chip 선행 확정 |
| 2024-12 | 중국 NMPA 인간줄기세포제품 CMC 지침(Trial) | [E-044] | 중국은 오가노이드 전용 지침 부재 |
| **2025-04-10** | **FDA Roadmap 발표. 초기 대상 = mAb. 3~5년 내 동물시험 예외화 목표** | [E-006][E-007][E-009] | **수요 기대의 기원점. 목표 도달 = 2028~2030** |
| 2025-06-16 | MFDS 오가노이드 시험법 국제표준화 추진위원회 발족 | [E-041] | 한국 기업의 표준 참여 창구 |
| 2025-07-07 | FDA-NIH 국제 규제기관 워크숍 (EMA/BfR/PMDA/TGA) | [E-012] | 국제 정합 신호 |
| **2025-07-31** | **ISTAND 상설화** | [E-017] | qualification 경로 상시 개방 |
| 2025-08-27 | FDA-NIH MOU 225-25-012 (Complement-ARIE) | [E-028] | 공공 검증 인프라 |
| **2025-09** | **NIH SOM Center 8,700만 USD / 3년 (FNLCR)** | [E-026] | **표준 프로토콜에 매트릭스가 지정될 기회 창 (2027~2028 결판)** |
| 2025-10 | CDER Streamlined/Acceptable NAMs DB 공개 (40+ 컨텍스트) | [E-025] | **organoid/MPS 등재 0건 → 수요 상한 확인** |
| **2025-12-02** | **mAb Streamlined Nonclinical draft guidance** | [E-013] | 6개월 NHP → 3개월 + WoE |
| 2025-12-08 | 최초 qualify DDT = AIM-NASH (AI) | [E-021] | 오가노이드 아님 |
| 2025-12 | CDER 15년 NAM 제출 분석 (in silico 49% / in vitro 44%) | [E-023][E-024] | 3D/MPS는 in vitro 내 최하위 |
| **2026-03-18** | **General Considerations for NAMs draft guidance (검증 4원칙)** | [E-014] | **Technical Characterization = 우리 제품 판매논거 확정** |
| 2026-03-18 | Pyrogen/Endotoxin Q&A Level 2 (재조합 시약) | [E-016] | 자사 lot release 시험 유연화 |
| **2026-04** | **OECD Project 4.176 DRP WNT 승인 최단 시점** | [E-038] | DRP ≠ TG. TG는 2029~2031 |
| 2026-04-20 | FDA Year One 경과보고서 | [E-012] | 로드맵 지속 확인 |
| 2026-06-01 | EU 로드맵 채택 C(2026) 3497 final (ATMP·biologicals 제외) | [E-030][E-031] | **EU pull은 제한적** |
| 2026-06-01 | Oncology Streamlined draft guidance (FDA-2026-D-2839) | [E-015] | modality 확대 실증 |
| **2026-07-20 / 07-21** | **FDAMA 3.0 하원 통과 / 상원 접수 (미제정)** | [E-004] | 제정 시 1년 내 IND 규정 개정 → 2028 심리적 장벽 제거 |
| 2027~2028 (예상) | FDAMA 3.0 interim final rule; mAb·종양 가이던스 최종화 | [E-005][E-013][E-015] | NAM 병행 제출 관행화 |
| 2028~2030 (목표) | FDA "동물시험을 예외로" 목표 시점 | [E-009] | base 시나리오 2030 = 25% |
| 2029 | EU 단기 조치 입법화 기한 + 고위급 콘퍼런스 | [E-032] | EU 수요 2차 파동 |
| 2029~2031 (추정) | 간 오가노이드 OECD Test Guideline 채택 가능 시점 | [E-038][E-039] | **오가노이드 규제 수요의 진짜 변곡점** |
| **2033 (추정)** | **이식용 오가노이드 최초 승인 가능 시점** | [E-067][E-079] | GMP/ATMP 라인 매출 유의미화 |

---

## 10. 제품등급 판정

### 10.1 판정

> **1차 타깃 등급 = RUO (USP `<1043>` Tier 3), 단 ISO 20399:2022 준거 품질시스템 위에서 제조하여 Tier 2 승격 및 Type II DMF 등재가 가능한 "GMP-ready RUO"로 설계한다.**
> **2차(2029~) = GMP grade (Tier 2, ISO 20399 준거). 3차(2033~) = ATMP 구조성분/원부자재.**

### 10.2 판정 근거 (6개)

1. **GMP가 법적으로 강제되지 않는다.** EU ATMP GMP 7.13: "While raw materials should be of pharmaceutical grade, it is acknowledged that, in some cases, only materials of research grade are available." [E-049] 업계 기술문헌도 동일: "globally there is no particular grade of raw materials that is required for use in cell therapy manufacturing" [E-061].
2. **현재 매출 가능한 수요가 RUO에 있다.** 오가노이드 임상 활동의 96.7%가 이식이 아닌 PDO 모델링·약물감수성이며 [E-068], 규제 qualification 파이프라인의 오가노이드 점유율은 0%다 [E-019][E-025].
3. **이식 경로는 구조적으로 느리다.** 21 CFR 1271.10(a)(3)에 의해 매트릭스 결합 즉시 351 BLA 경로로 확정되며 [E-055], 실제 개입시험은 4건 이하·최고 Phase 2다 [E-067].
4. **RUO→GMP 프리미엄이 1.75×에 불과하다** [E-077]. GMP 라인 구축비용(설비·QC·문서)이 매출의 1.75배 이내 증분으로 회수되지 않으면 조기 GMP 투자는 파괴적이다. → Agent E(원가)에 이관: GMP 증분 CAPEX/OPEX가 1.75× 프리미엄 안에 들어오는지 검증 필요.
5. **그럼에도 품질시스템은 처음부터 GMP-ready여야 한다.** 이유: (a) ISO 20399:2022는 lot-to-lot 일관성을 공급자 요구사항으로 규정하며 [E-048] 이는 우리 제품의 핵심 판매논거와 동일하다, (b) 2026-03-18 NAM 가이던스의 Technical Characterization 원칙 [E-014]이 RUO 고객에게도 문서를 요구한다, (c) 나중에 소급하여 GMP 문서를 만드는 비용이 처음부터 만드는 비용보다 크다.
6. **Ph. Eur. 5.2.12 범주 3(무동물) 달성이 최고 가치 자산이다** [E-053]. 재조합 콜라겐 + 미생물 mTG는 이를 구조적으로 달성 가능하며, 이는 등급과 무관하게 BME 대비 영구적 우위다.

### 10.3 RUO 단계에서도 반드시 갖춰야 할 규격 (규제 문서에서 역산)

| 항목 | 규격 | 근거 |
|---|---|---|
| 동물유래 성분 | 무함유 (Ph. Eur. 5.2.12 범주 3) + 무동물유래 인증서 | [E-053][E-070] |
| TSE | EMA/410/01 rev.3 준거 선언 (원료 원산국 문서화) | [E-050][E-047][E-056] |
| 무균 | USP `<71>` / Ph. Eur. 2.6.1 | [E-054][E-057] |
| 마이코플라스마 | Ph. Eur. 2.6.7 음성 (절대 요건) — 0.1 µm 여과 불가 시 시험으로 입증 | [E-050][E-054] |
| 엔도톡신 | USP `<85>` / Ph. Eur. 2.6.14, mg 또는 mL 기준 규격 설정 (재조합 시약 사용 가능) | [E-054][E-016] |
| 순도 | SDS-PAGE densitometry > 98% 수준 (업계 CTG 벤치마크) | [E-070] |
| 잔류 HCP / HCD | < 10 ng/µg 수준 (업계 CTG 벤치마크) | [E-070] |
| lot-to-lot 일관성 | ISO 20399:2022 요구, 다중 로트 데이터 공개 | [E-048] |
| 문서 | CoA + CoO + 완전 추적성, ISO/AWI 20399-4 대비 | [E-048][E-047] |
| DMF | Type II 조기 등재 (영업 자산) | [E-058][E-047] |

---

## HANDOFF

후행 에이전트(A 시장규모 / C 가격 / E 원가 / G GTM / S 통합)가 그대로 입력값으로 쓸 수 있는 정량치.

### H1. `nam_ramp`

정의: **제약사 전임상 프로그램 중 complex 3D 인체모델(오가노이드 또는 MPS/organ-on-chip) 데이터를 실제 규제제출(IND/BLA/NDA)에 최소 1개 endpoint에 대해 포함하는 프로그램의 비율(%)**
(광의 NAM — in silico PBPK, Ames, hERG, reconstructed epidermis 등을 포함 — 은 2026년 이미 사실상 보편이므로 매트릭스 수요의 대리변수가 되지 못한다. 따라서 협의 정의를 쓴다.)

| 시나리오 | 2026 | 2030 | 2035 | CAGR 26→30 | CAGR 30→35 |
|---|---|---|---|---|---|
| conservative | **4%** | **12%** | **25%** | 31.6% | 15.8% |
| **base** | **8%** | **25%** | **45%** | **33.0%** | **12.5%** |
| aggressive | **12%** | **40%** | **65%** | 35.1% | 10.2% |

**2026 기준값 산출 근거 (R4)** [E-078]:
동시에 만족해야 하는 세 관측치 —
① CDER 15년 제출 분석에서 3D 모델·organ chip/MPS는 in vitro NAM(전체 NAM 제출의 44%[E-023]) 내에서 stem cell-derived·sandwich culture 모델보다 **낮은** 빈도 [E-024];
② ISTAND 활성 제출물 16건 초과 전체가 *도구 단위*이며 organoid 명명 0건 [E-018][E-019];
③ CDER 수용 NAM DB(40+ 컨텍스트, 2025-10)에 organoid/MPS 명시 항목 0건 [E-025].
→ 세 관측치를 동시에 만족하는 값은 한 자릿수. base = 8%, 불확실성 밴드 ±50% 적용하여 conservative 4% / aggressive 12%.

**CAGR 계산 (base)**
```
CAGR(2026→2030) = (25 / 8)^(1/4) − 1 = 3.125^0.25 − 1 = 0.3296 = 33.0 %/yr
CAGR(2030→2035) = (45 / 25)^(1/5) − 1 = 1.800^0.20 − 1 = 0.1247 = 12.5 %/yr
```

**2030 목표값의 사건 근거:** FDA 로드맵 3~5년 목표 = 2028~2030 [E-009]; FDAMA 3.0 제정 시 1년 내 IND 규정 개정 [E-004][E-005] → 2028; mAb(2025-12)·종양(2026-06) streamlined guidance 최종화 → 2027~2028 [E-013][E-015]; NAM 검증 4원칙 확정(2026-03-18) [E-014].
**2035 목표값의 사건 근거:** 간 오가노이드 OECD TG 2029~2031 [E-038][E-039]; EU 단기 조치 입법화 2029 [E-032]; SOM Center 표준 프로토콜 2028 [E-026].

**시나리오 분기 조건 (S/X가 감도분석에 쓸 것):**
- conservative 조건: MPS/organ-chip이 qualification 슬롯을 계속 독점(현 추세 [E-019] 지속); OECD 간 오가노이드 TG가 2031 이후로 지연; EU 로드맵이 ATMP·biologicals 제외를 유지 [E-031]; NIH ORIVA 예산 미확보 [E-027].
- aggressive 조건: FDAMA 3.0이 2026년 내 제정 [E-004]; SOM Center 표준 프로토콜이 2028년 조기 배포 [E-026]; OECD 간 오가노이드 TG 2029 채택 [E-038].

**⚠ 후행 에이전트 필독 — 이 비율을 매출로 직접 환산하지 말 것:**
nam_ramp의 분자(complex 3D 사용 프로그램)에는 **매트릭스를 대량 소비하는 오가노이드**와 **미량 ECM 코팅만 쓰는 organ-on-chip**이 섞여 있다. 규제 qualification 파이프라인 기준으로는 오가노이드 비중이 0%이지만 [E-019], 연구·스크리닝 볼륨 기준으로는 오가노이드가 다수다. 매트릭스 물량 환산 계수는 Agent A/C가 별도로 산출해야 한다.

### H2. `grade_verdict`

```
1차 타깃 : RUO — USP <1043> Tier 3, 단 ISO 20399:2022 준거 품질시스템 하에서 제조 ("GMP-ready RUO")
2차 (2029~) : GMP grade — USP <1043> Tier 2, Type II DMF 등재 완료
3차 (2033~) : ATMP 원부자재 / 구조성분 (combined ATMP device 요건 포함)
```
근거 요약: EU ATMP GMP 7.13이 research grade를 명시적으로 인정 [E-049]; 세포치료 제조에 강제되는 원료 등급이 전 세계적으로 부재 [E-061]; 오가노이드 임상 활동의 96.7%가 비이식 [E-068]; RUO→GMP 프리미엄이 1.75×에 불과 [E-077]; 21 CFR 1271.10(a)(3)이 이식 경로를 351 BLA로 강제 [E-055]. 전체 근거는 §10.2 참조.

### H3. `gmp_premium_multiple`

```
gmp_premium_multiple = 1.75×   (실측 매칭 4쌍 중앙값)
range                = 1.32× ~ 2.45×
mean                 = 1.82×
n                    = 4 (Qkine FGF-2 2.00× [E-070], Qkine Activin A 1.50× [E-071],
                          PeproTech IL-3 2.446× [E-072], PeproTech Activin A 1.318× [E-073])
적용 주의            : 재조합 단백질 기반 배수. 매트릭스 카테고리는 RUO 기준선이 BME(Tier 4)이므로
                       Agent C가 BME 대비 프리미엄을 별도 산출할 것.
```

**독립 교차검증:** Agent C가 매트릭스·코팅시약 카탈로그 실측(별도 표본, 별도 방법)으로 산출한 GMP 등급 배수는 **1.942×** [E-159, Agent C 범위]이다. 본 에이전트의 재조합 단백질 기반 산출값 1.75×와 **11% 이내로 수렴**한다. 두 값은 표본·카테고리가 서로 겹치지 않으므로 독립 추정치로 취급할 수 있으며, 후행 에이전트는 다음 구간을 사용할 것을 권고한다.
```
gmp_premium_multiple (통합 권고) = 1.75 ~ 1.94×,  점추정 1.85× (두 독립 추정치의 산술평균)
계산: (1.75 [E-077] + 1.942 [E-159, Agent C]) / 2 = 1.846
```

### H4. `clinical_timing_year`

```
clinical_timing_year = 2033   (base)
conservative         = 2036
aggressive           = 2031
정의                 : 이식용/재생의료 원부자재 매출이 단일 공급자 기준 연 5백만 USD 이상이 되는 최초 연도
```

**산출식 (R4)** [E-079]:
```
최초 Phase 2 오가노이드 이식시험 개시 = 2026-01 (NCT07214649) [E-067]
  + Phase 2 소요 3년   (가정 B-A3)
  + Phase 3 소요 3년   (가정 B-A3)
  + BLA 심사 1년       (가정 B-A3)
= 2033년 최초 승인 가능
```
구조적 제약: 매트릭스 결합 시 21 CFR 1271.10(a)(3) 위배로 351 BLA 경로가 불가피하다 [E-055]. 검증 벤치마크: 세계 최초 인체 오가노이드 이식(2022-07-05)[E-066] 후 4년이 지난 2026-08 현재 Phase 3 0건, 승인 0건 [E-067]; 일본은 PMD Act 시행(2014) 후 11년간 재생의료등제품 22건 승인이며 조건부승인 1호는 철수 [E-045].

**⚠ 사업계획 함의:** 2026~2032년의 7년간 매출은 **전액 RUO/NAM 스크리닝·CRO·PDO 세그먼트**에서 나와야 한다. 이식용 GMP 라인은 2029년 이후 착수하는 것이 자본효율적이다.

### H5. 부가 handoff (후행 에이전트가 쓸 수 있는 파생값)

| 키 | 값 | 근거 |
|---|---|---|
| `organoid_share_of_regulatory_qualification_pipeline` | **0%** (ISTAND 활성 제출물 중 organoid 명명 0/16+) | [E-018][E-019] |
| `oecd_organoid_TG_earliest_year` | **2029~2031** (DRP WNT 승인 최단 2026-04 + TG 개발 3~5년) | [E-038][E-039] |
| `fda_animal_exception_target_year` | **2028~2030** (Roadmap 3~5년 목표, 기산일 2025-04-10) | [E-006][E-009] |
| `eu_pull_scope_limitation` | EU 로드맵은 화학의약품만 대상, **ATMP·biologicals·gene therapy 제외** | [E-031] |
| `mandatory_requirements_on_animal_derived_matrix` | TSE(EMA/410/01 rev.3) 준수 **required** + 마이코플라스마 부재 | [E-050][E-054] |
| `matrigel_human_administration_trials` | **0건** (ClinicalTrials.gov 2026-08-11 조회) | [E-062] |
| `organoid_transplant_interventional_trials` | **≤4건**, 최고 Phase 2, Phase 3 0건 | [E-067] |
| `nhp_cost_per_animal` | **50,000 USD**, mAb 프로그램당 144마리 | [E-011] |
| `nih_organoid_public_funding_2025` | **87,000,000 USD / 3년** (SOM Center) | [E-026] |
| `ctg_endotoxin_benchmark` | **< 0.05 EU/µg protein** (Qkine CTG), ≤ 0.1 EU/µg (PeproGMP) | [E-070][E-073] |

---

## DoD 셀프 체크리스트

| # | 항목 | 결과 | 비고 |
|---|---|---|---|
| 1 | 1차 문서(FDA/EMA/USP/ISO/EU/NMPA/PMDA/congress.gov) URL 최소 12건 | **PASS** | 실제 접근 확인 1차 문서 URL **21건**: congress.gov S.5002 [E-001], govinfo BILLSTATUS 119hr2821 [E-004], FDA Roadmap PDF [E-007], FDA Year One PDF [E-012], Federal Register 2025-21864 [E-013], Federal Register 2026-05390 [E-014], Federal Register 2026-10873 [E-015], FDA ISTAND Voices [E-017], FDA Liver-Chip 발표 [E-020], FDA NAMs 페이지 [E-025], FDA DMF Types [E-058], EC Roadmap C(2026)3497 PDF [E-030], EU ATMP GMP PDF [E-049], Ph.Eur. 5.2.12 PDF [E-053], eCFR 21 CFR 1271.10 [E-055], EUR-Lex Reg 1394/2007 [E-059], OECD TGP 작업계획 PDF [E-038], OECD GIVIMP [E-040], ISO 20399:2022 [E-048], ISO 13022:2012 [E-060], MFDS 보도자료 [E-041], NMPA/CCFDIE [E-044], ClinicalTrials.gov API [E-062][E-067] |
| 2 | 규제 타임라인 표 (연도 – 이벤트 – 사업영향) | **PASS** | §9, 33개 행 |
| 3 | 제품등급 판정 결론 1개 + 근거 | **PASS** | §10.1 판정 + §10.2 근거 6개 + §10.3 규격표 |
| 4 | premise_audit.md 5개 전제 전부 검증 | **PASS** | `docs/premise_audit.md` P1~P5, 각각 연 단위 지연 수치 포함 |
| 5 | 모든 수치에 [E-###] | **PASS** | 본문 전 수치에 인라인 근거 ID. 파생값은 §8·HANDOFF에 계산식 명시 |
| 6 | nam_ramp / gmp_premium_multiple / clinical_timing_year 정량값 산출 | **PASS** | HANDOFF H1(3시나리오×3시점+CAGR), H3(1.75×), H4(2033) |
| 7 | 실제 WebSearch/WebFetch 30회 이상 | **PASS** | WebSearch 45회 + WebFetch 54회 + 직접 API 호출 6회 = **105회** |
| 8 | R1 No-Deferral (금지표현 부재) | **PASS** | 미확인 항목(중국 오가노이드 지침 [E-044], NIH ORIVA 예산 [E-027])은 "부재"를 사실로 기록하고 함의를 서술 |
| 9 | R2 근거 ID 범위 준수 (Agent B 배정 범위 내) | **PASS** | E-001 ~ E-079, 79건, 중복 0, 배정범위 이탈 0 |
| 10 | R5 사용자 전제를 참으로 가정하지 않음 | **PASS** | P1·P2 오해 판정, P3·P4·P5 부분과장 판정 |
