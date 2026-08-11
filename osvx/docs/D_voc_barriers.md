# Agent D — 고객 VOC · Pain Point · 전환장벽

작성일: 2026-08-11 / 근거 ID: **E-200 ~ E-264** (65건) / evidence: `evidence/evidence_D.jsonl`
실제 WebSearch·WebFetch 수행: **103회**

---

## 0. 결론 요약 (읽는 사람이 1분 안에 알아야 할 것)

| 항목 | 판정 | 핵심 수치 |
|---|---|---|
| Lot 편차는 실재하는가 | **예, 정량적으로 실재** | 제조사 스펙창 안에서만 움직여도 강성 G' 44.3→86.2 Pa(1.95배, CV 18.6%) [E-205]; 실사용 허용창 통과율 16.7% [E-210] |
| 그 편차가 **구매 전환**을 일으키는가 | **아니오. 현재까지는 거의 일으키지 않았다** | 가격 1/10에 결과가 통계적으로 동등한 콜라겐 I 대체재가 2023년에 공표됐는데도 [E-228] Matrigel은 여전히 gold standard [E-238] |
| 전환장벽 크기 | **크다** | 랩당 56,800 USD / 12개월 (학술), GMP는 681,800 USD / 36개월 [E-262] |
| 가장 위험한 변수 | **효능 격차(B6)** | 2024년까지 모든 합성 매트릭스가 외인성 라미닌 보충 필수였다 [E-231]; 정의된 매트릭스는 장기별로 100 Pa~34 kPa, 340배 강성 스펙트럼을 커버해야 함 [E-260] |
| 사업적 함의 | **"lot 편차 해소"만으로는 팔리지 않는다** | 전환확률 학술 6.0%/년 [E-263] = 반감기 11.2년. 페인 강도가 아니라 **전환비용 상쇄 설계**가 매출을 결정 |

> **이 문서가 후행 에이전트에게 강제하는 것**: SOM 계산에서 "Matrigel 사용 랩 수 × 단가"를 그대로 쓰지 말 것. §7의 `segment_switch_propensity`(2.7~25%/년)를 곱해야 한다. 이 계수를 빼면 SOM이 최대 **15~37배** 과대평가된다.

---

## 1. 조사 A — Lot-to-Lot 변동성 정량 (수치 9건)

### 1.1 조성 정의 불가능성

| # | 지표 | 값 | 근거 |
|---|---|---|---|
| A1 | Matrigel 프로테옴 동정 단백질 종수 | **1,851종** (Hughes CS, Postovit LM, Lajoie GA, *Matrigel: a complex protein mixture required for optimal growth of cell culture*, PROTEOMICS 10(9):1886-1890, 2010) | [E-200] |
| A2 | 2025년 리뷰 재확인치 | **>1,850종** — "More than 1850 proteins have been identified in Matrigel, making it incredibly complex." | [E-201] |

1,851종 중 제조사가 스펙으로 관리·공개하는 항목은 **총 단백질 질량 1개**와 **로트별 탄성계수 1개**뿐이다 [E-202][E-206]. 즉 조성의 99.9%가 무관리 상태다.

### 1.2 총 단백질 농도 — 스펙 자체가 '범위'다

| # | 지표 | 값 | 근거 |
|---|---|---|---|
| A3 | Corning Matrigel GFR 표준 제품 로트 허용 범위 | **7~10 mg/mL** (최대/최소 **1.43배**) | [E-203] |
| A4 | HC 제품 | 18~22 mg/mL | [E-203] |
| A5 | 제품군 전체 공개 범위 | 8~22 mg/mL | [E-202] |

Fisher Scientific 제품 페이지는 단백질 농도를 아예 **"Lot dependent"** 라고만 표기한다 [E-223]. 구매 시점에 물성을 알 수 없다.

### 1.3 유변학적 강성 G' — 스펙 준수 로트끼리도 2배 차이

| # | 지표 | 값 | 근거 |
|---|---|---|---|
| A6 | Matrigel HC GFR, 3→19.1 mg/mL 구간 G' 실측 | **9.1 ± 0.3 Pa → 288.2 ± 9 Pa** | [E-204] |
| A7 | **스펙창 7~10 mg/mL 내 G' 추정 편차** | **44.3 ~ 86.2 Pa / 1.95배 / CV 18.6%** | [E-205] |
| A8 | Corning 표준 제품 50~100% 농도 G' | 약 10 → 50 Pa 선형 증가 | [E-205 note] |

**계산식(R4)**: E-204의 두 점으로 멱함수 피팅 → 지수 n = ln(288.2/9.1) / ln(19.1/3) = 3.4550 / 1.8509 = **1.867**
G'(c) = 9.1 × (c/3)^1.867
→ G'(7 mg/mL) = 9.1 × 2.3333^1.867 = **44.3 Pa**
→ G'(10 mg/mL) = 9.1 × 3.3333^1.867 = **86.2 Pa**
→ 균등분포 CV = (86.2−44.3) / (65.25 × √12) = 41.9 / 226.0 = **18.6%**

이것이 왜 치명적인가: 소장 오가노이드의 최적 강성창은 **100~200 Pa**, 형성효율이 콜라겐 I 수준에 도달하는 값은 **180 Pa** 이다 [E-260]. 제조사 스펙 준수 로트가 44~86 Pa를 오간다면, 최적창 대비 위치가 로트마다 바뀐다. Corning이 **"each lot has a specific elastic modulus value"** 라고 로트별 값을 개별 통지하는 것 [E-206]은 이 편차의 제조사 측 자인이다.

### 1.4 성장인자 농도

| # | 성분 | 값 | 근거 |
|---|---|---|---|
| A9 | EGF | **0.5 ~ 1.3 ng/mL (2.6배 폭)** | [E-207] |
| | bFGF | 0 ~ 0.1 pg/mL (하한이 0 = 미검출 로트 존재) | [E-207] |
| | IGF-1 | 15.6 ng/mL (단일 대표값, 범위 비공개) | [E-207] |
| | PDGF | 12 pg/mL (범위 비공개) | [E-207] |
| | TGF-β | 2.3 ng/mL (범위 비공개) | [E-207] |

이 성장인자들은 **불활성 잔류물이 아니라 활성**이다. Vukicevic 등(1992)은 외인성 TGF-β가 세포 네트워크 형성을 차단하고 TGF-β 중화항체 첨가는 이를 촉진함을 보여, *"suggesting caution in the interpretation of experiments on cellular activity related to Matrigel"* 라고 결론지었다 [E-208]. **1992년부터 34년간 알려진 문제이며, 그 34년 동안 시장은 Matrigel을 계속 샀다** — 이 사실 자체가 §5의 전환장벽 추정에 대한 실증적 상한선이다.

### 1.5 생물학적 산출물 변동

| # | 지표 | 값 | 근거 |
|---|---|---|---|
| A10 | 위 오가노이드 크기 CV | **Matrigel 74.5%** vs 조직유래 SEM 하이드로겔 66.7% | [E-213] |
| A11 | 소장 오가노이드 크기 CV | **Matrigel 47.7%** vs IEM 하이드로겔 35.1% | [E-214] |
| A12 | 로트 실사용 허용창 | **9.4~9.9 mg/mL** — 이 창을 벗어난 저농도 로트는 dome 형성 실패 | [E-209] |
| A13 | **스펙창 대비 실사용창 통과율** | **16.7%** (= 0.5/3.0 mg/mL) | [E-210] |
| A14 | Matrigel 노출량에 따른 대뇌 오가노이드 표현형 분기 | <15 µL 과립형 / 15~50 µL 정상 / ≥75 µL 대형 낭종 | [E-218] |

**A13이 이 절의 핵심 수치다.** 제조사 스펙(7~10 mg/mL)을 통과한 로트 중 Tuveson Lab이 실제로 쓰는 창(9.4~9.9 mg/mL)에 드는 비율은 균등분포 가정 시 16.7%. 6개 로트 중 1개다. 이것이 "로트를 미리 시험하고 대량 확보하라"는 관행의 정량적 근거다.

### 1.6 반증 — 편차가 전부는 아니다

신장 오가노이드 고처리량 연구는 배양법·iPSC 주·실험 반복·초기 세포수가 관찰된 변이의 **35~77%** 를 설명하며, iPSC 주별 성공률이 **0%~100%** 로 갈린다고 보고했다. 저자 결론은 *"laboratory-based variation can surpass genotypic effects"* [E-219]. **매트릭스를 defined로 바꿔도 재현성 문제의 상당 부분은 남는다.** 우리 제품의 마케팅 클레임에 "재현성 해결"을 쓰면 반증당한다. 쓸 수 있는 클레임은 "재현성 변동요인 중 매트릭스 기여분 제거"까지다.

---

## 2. 조사 B — 재현성 이슈와 실무 관행 ("lot을 미리 확보/시험하라")

### 2.1 프로토콜 논문의 명시적 지시 — 원문 인용

| 출처 | 원문 (English) | 한국어 요약 | 근거 |
|---|---|---|---|
| Tuveson Lab Organoid Protocols (CSHL, 2017) | *"there is some variation between Matrigel content, protein content, and stiffness from lot to lot. **Individual lots need to be tested for organoid culture.** In practice, we use lots with protein content between 9.4-9.9 mg/mL. We have noticed that lots with lower protein concentrations fail to make solid domes."* | 로트마다 조성·단백질량·강성이 다르므로 **개별 로트를 반드시 시험**해야 하며, 실사용 창은 9.4~9.9 mg/mL. 저농도 로트는 dome이 안 굳는다. | [E-209] |
| STAR Protocols Q&A: Organoids (2026) | *"Use reagents (particularly Matrigel and FBS) from the same lot for all replicates of one experiment."* / *"it is very important to use the same lot for these kinds of culture components, but **it is not always feasible to obtain the same lot from a company.** We recommend checking the products' certificates of analysis and using products that have similar protein concentrations."* | 한 실험의 모든 반복은 동일 로트로. 다만 동일 로트 확보가 항상 가능하지는 않아, CoA 단백질 농도가 비슷한 제품을 고르라고 권고. | [E-211] |
| STAR Protocols: brain organoid QC (2026) | *"use the same Matrigel batch throughout the experiment to avoid batch-to-batch variation in composition"* | 실험 전 기간 동일 배치 사용 지시. | [E-212] |
| Merck/Sigma Organoid Culture FAQ | *"**lot-qualified GFR Matrigel**, following proper passaging techniques and sourcing high quality organoid media"* (오가노이드 유지의 핵심 요건) | 공급자 스스로 '로트 검증된' Matrigel을 전제조건으로 요구. | [E-243] |
| Frontiers Cell Neurosci 2024 (뇌 오가노이드 프로토콜 리뷰) | *"Undefined features, manual embedding, and potential matrigel batch-to-batch variability resulted in a higher variability and lower reproducibility in organoids generated with matrigel."* | 미정의 조성 + 수작업 임베딩 + 로트 편차가 변동↑·재현성↓의 원인. | [E-217] |

**해석**: 이것이 lot 편차 페인의 가장 강력한 방증이다. 세계 최고 수준의 랩들이 프로토콜 본문에 "로트를 시험하라"를 적어넣는다는 것은, 그 비용을 **이미 지불하고 있다**는 뜻이다. 우리 제품의 가치제안은 "이 사전시험 공정을 없앤다"로 정의될 수 있다 → §8 must_win_metric #4(로트 합격률).

### 2.2 재현성 특집·리뷰에서의 지목

- 뇌 오가노이드 프로토콜 114편 중 **67편(58.8%)** 이 ECM 임베딩을 사용하며 Matrigel이 최다 [E-216]. 동 리뷰는 대체재에 대해 *"the development of engineered scaffolds is still in the early stage"* 라고 평가한다 [E-217] — **재현성 진영조차 아직 대체재를 추천하지 못한다.**
- Nature Methods의 Matrigel 지목 에디토리얼은 5개 쿼리·8개 소스 확인 결과 특정하지 못했다 → §10 gaps.md `GAP-D-01` 참조.

### 2.3 공급 부족 사건과 고객 반응

| 시점 | 사실 | 근거 |
|---|---|---|
| 2021~2022 | *"Matrigel has been in short supply for the last year or so"*; **Corning 리드타임 16주**; *"if reagents are suddenly back-ordered it could bring some research to a halt"* | [E-221] |
| 현재(2026-08) | Corning은 *"Availability in 2 weeks or less from date of order placement"* 및 *"significantly increased the quantity of Matrigel matrix produced"* 로 회복 발표 | [E-220] |
| 현재(2026-08) | Corning e-Catalog 356255 예상 출하일 2026-09-10 (조회일 기준 약 30일) | [E-222] |

**함의(중요, 우리에게 불리)**: 공급 부족은 **이미 해소되었다.** 2021~2022년에 존재했던 "공급 리스크 회피를 위한 2nd source 확보" 동기는 2026년 현재 크게 약화됐다. 공급 안정성을 GTM 훅으로 쓰는 것은 유효기간이 지났다. 다만 Corning이 전용 '가용성 업데이트 페이지'를 상시 운영한다는 사실 [E-220]은 구매 담당자의 기억에 리스크가 남아 있음을 시사하므로, **2nd source 포지셔닝은 보조 훅으로만** 유효하다.

---

## 3. 조사 C — 커뮤니티 VOC 원문 (21건, 전 건 URL 포함)

원칙: **원문(영문) + 한국어 요약 + URL**. 사용자명은 익명화(소속·용도만 표기). **긍정 VOC를 의도적으로 다수 포함**했다 — 이 시장의 지배적 정서는 불만이 아니라 **만족 + 체념**이다.

| # | 감정 | 발화자(익명) | 원문 (English) | 한국어 요약 | URL | 근거 |
|---|---|---|---|---|---|---|
| V1 | ★부정 | Rega Institute, 3D organoid culture (4.3/5) | *"Use of matrigel LOTs with low level of endotoxins is preferable. So sometimes you need to wait some time to get a good LOT"* | 엔도톡신 낮은 로트를 골라야 해서, 좋은 로트가 나올 때까지 **기다려야 할 때가 있다**. | https://www.selectscience.net/product/corning-r-matrigel-r-growth-factor-reduced-gfr-basement-membrane-matrix-ldev-free-10-ml | [E-245] |
| V2 | 긍정 | 동일 발화자 | *"Enteroids growth in a consistent manner and keep the same morphology over the passages"* | 엔테로이드가 일관되게 자라고 계대에 걸쳐 형태 유지. | 동상 | [E-245] |
| V3 | 중립 | 동일 발화자 | *"matrigel requires some attention since it needs to be manipulated always on ice to avoid early polymerization"* | 항상 얼음 위에서 다뤄야 해 신경 쓰임. | 동상 | [E-245] |
| V4 | ★긍정 | Memorial Sloan Kettering, PDO (5.0/5) | *"The matrigel I purchased from Corning has stable quality and it makes my experiments easy to handle and repeatable"* | 코닝 Matrigel은 **품질이 안정적**이고 실험이 다루기 쉽고 **재현 가능**하다. | 동상 | [E-246] |
| V5 | 긍정 | UT Austin, organoids (5.0/5) | *"The viscosity is suitable to form a dome in the wells and make a perfect matrigel pad"* | 점도가 dome 형성에 적합. | 동상 | [E-247] |
| V6 | 긍정 | UT Austin (동일) | *"It is totally transparent and solidifies pretty easily"* | 완전 투명하고 쉽게 굳음. | 동상 | [E-247] |
| V7 | 중립 | Vanderbilt Univ., cerebral organoids (4.0/5) | *"It is important to limit freeze/thaw cycles. Aliquoting is integral to a successful process"* | 동결융해 횟수 제한 필요, 분주가 필수. | 동상 | [E-248] |
| V8 | 긍정 | Chonnam National Univ., invasion assay (5.0/5) | *"It is a good product"* | 좋은 제품. | 동상 | [E-245] |
| V9 | ★긍정 | CIBERONC-IIB, 환자유래 정상·종양 대장 오가노이드 (4.7/5) | *"High quality product and fantastic customer service."* | 고품질 + **환상적인 고객지원**. 3D 배양 최적화에 대한 지원이 훌륭했음. | https://www.selectscience.net/product/corning-matrigel-matrix-for-organoids | [E-244] |
| V10 | 긍정 | University of Toronto, 3D collagen gel (4.3/5) | *"Good for 3D collagen gels, improves cell proliferation and differentiation compared to collagen only constructs."* | 콜라겐 단독 대비 증식·분화 향상. | 동상 | [E-244] |
| V11 | ★긍정(락인) | Institute for Stem Cell Science & Regenerative Medicine, murine satellite cells (3.7/5, 2023-12-25) | *"Matrigel is the best basement coating. It works like charm for my cells. **Nothing can replace it that I know of.** Need to be careful about different versions of Matrigel before ordering."* | 최고의 기저막 코팅. **내가 아는 한 대체할 수 있는 게 없다.** 다만 주문 전 버전 확인 필요. | https://www.selectscience.net/product/corning-r-matrigel-r-basement-membrane-matrix-ldev-free-10-ml | [E-249] |
| V12 | 긍정 | UCL, PDTO (5.0/5, 2022-04-04) | *"Easy to use"* | 사용 간편. | 동상 | [E-250] |
| V13 | ★부정 | Universidad Andrés Bello, intestinal organoids (**1.7/5**, 2020-06-03) | *"It's difficult to know how much you have to use or if it affects the growth if you dilute it."* | **얼마를 써야 하는지, 희석하면 성장에 영향이 있는지 알 수 없다.** | https://www.selectscience.net/product/corning-r-matrigel-r-hesc-qualified-matrix-ldev-free-5-ml | [E-251] |
| V14 | 중립 | Postdoc, Cambridge MA, iPSC culture (4.7/5, 2018-03-23) | *"Need to make sure matrigel is always on ice, otherwise it will seize up."* | 항상 얼음 위에 둬야 함. | 동상 | [E-252] |
| V15 | ★전환성공 | Institute of Hepatology, organoids (5.0/5) | *"This is a perfect alternative to Matrigel from Corning. **I have not noticed a difference in the performance** and I recommend it considering **the price advantage**."* | Cultrex UltiMatrix는 코닝 Matrigel의 완벽한 대체재. **성능 차이를 못 느꼈고 가격 이점** 때문에 추천. | https://www.selectscience.net/product/cultrex-ultimatrix-reduced-growth-factor-basement-membrane-extract | [E-253] |
| V16 | 전환성공 | University of Birmingham, 3D cell culture (5.0/5) | *"Best Reduced Growth Factor (RGF) Basement Membrane Extract (BME) for 3D cultures"* | 3D 배양용 최고의 RGF BME. | 동상 | [E-254] |
| V17 | ★경쟁사 로트일관성 | Salk Institute | *"tested approximately 20 lots of Cultrex BME...not a single one has failed"* | Cultrex BME **20개 로트를 시험했는데 단 하나도 실패하지 않았다.** | https://www.bio-techne.com/research-areas/organoids-3d-culture/peer-product-reviews | [E-255] |
| V18 | 경쟁사 성능 | Hubrecht Institute (Clevers Lab) | *"organoids grew equally well...found slightly bigger organoids in UltiMatrix"* | 동등하게 잘 자랐고 UltiMatrix에서 오가노이드가 약간 더 컸다. | 동상 | [E-256] |
| V19 | 경쟁사 성능 | 신약개발 조직 오가노이드 팀장, 파리 | *"comparable to Corning Matrigel in terms of growth, 3D structure and biomarkers"* | 성장·3D 구조·바이오마커 모두 코닝 Matrigel과 동등. | 동상 | [E-256] |
| V20 | 경쟁사 성능 | University of Michigan | *"UltiMatrix supports healthy normal growth"* (경쟁사가 실패하는 저농도 조건에서도) | 저농도에서도 정상 성장 지원. | 동상 | [E-256] |
| V21 | 경쟁사 일관성 | Hubrecht Institute | *"used Cultrex BME as the matrix...with great consistent results"* | Cultrex BME로 일관된 결과. | 동상 | [E-256] |

### 3.1 VOC 감정 분포 및 냉정한 해석

| 감정 | 건수 | 비율 |
|---|---|---|
| 긍정(만족) | 11 | 52% |
| 중립(취급성 불만) | 3 | 14% |
| 부정(lot/용법 불확실성) | 2 | 10% |
| 경쟁 BME 전환 성공·일관성 | 5 | 24% |

**결정적 관찰 3가지:**

1. **최상위 기관 사용자일수록 만족도가 높다.** MSKCC PDO 팀이 *"stable quality... repeatable"* 이라고 평가한다 [E-246]. lot 편차는 **경험 많은 랩에서는 이미 내부 프로세스(로트 사전시험·CoA 매칭)로 흡수되어 있다.** 즉 우리가 제거하겠다는 페인은 이미 고객이 **비용을 지불하고 관리 중**인 페인이며, 그 관리비용이 우리 제품 프리미엄의 상한선이다.
2. **"Nothing can replace it that I know of"** [E-249] — 인식적 락인이 실제 기술적 격차보다 크다. 인지도 확보(논문·KOL) 없이는 스펙만으로 전환이 안 된다.
3. **동종 BME 간 전환은 이미 '가격'만으로 발생한다** [E-253]. Cultrex UltiMatrix는 "성능 차이 없음 + 가격 이점"으로 채택되고 있고, Bio-Techne는 "20 로트 무실패" [E-255]로 **로트 일관성을 이미 마케팅 축으로 선점**했다. 우리 제품이 "로트 일관성"만 내세우면 **차별화 실패 + 가격 경쟁 진입**이다.

---

## 4. 조사 D-B6 — 효능 격차: 성공 사례와 실패 사례 정량 비교 (가장 중요)

### 4.1 정의된 매트릭스가 **성공**한 사례

| 사례 | 장기 | 정량 결과 | Matrigel 대비 | 근거 |
|---|---|---|---|---|
| Gjorevski/Lutolf PEG 동적 하이드로겔 (Nature 539:560-564, 2016) | 소장 (마우스·인간 ISC) | 완전정의 배양계 구축. 확장기 고강성(≈1.3 kPa) → 분화기 연화(≈200 Pa) | 대체 성립 (효율 수치 미제시) | [E-229][E-230] |
| Hushka et al., *Fully Synthetic Hydrogels Promote Robust Crypt Formation in Intestinal Organoids* (Adv Mater 37(43), 2025) | 소장 | **외인성 라미닌 보충 없이 crypt 형성** — *"unlike all other synthetic hydrogels to date"* | 최초 동등 | [E-231] |
| XF-DISC 제노프리 폴리머 코팅 (2024) | 인간 장 줄기세포 | 30일 **24배 증식**, **30계대 >210일**, viability **>99%**, 해동 후 부착 **>82%**, 엔도톡신 **<0.12 EU/mL**, CD44+ **93.6%** (Matrigel 91.4%) | LGR5/SOX9/CD44 P3·P8·P18 전 시점 **유의차 없음** | [E-232] |
| Takahashi et al. (Sci Rep, 2023) 콜라겐 I 치환 | 인간 소장 | LGR5·LYZ·MUC2·VIL1·HNF4A 발현 **유의차 없음**, 7일 생존세포수 comparable | 동등, **가격 1/10**, 전체 배양비 **최대 100배 절감** | [E-228] |
| 조직유래 SEM 하이드로겔 (Nat Commun 13:1692, 2022) | 위 | 형성효율 Matrigel과 comparable, 크기 CV **66.7% vs 74.5%** | 효율 동등 + 균일성 우위 | [E-213] |
| Matrigel-free 현탁배양 (Cell Prolif, 2025) | 간 담관 | 평균 크기 **2.6배**, 생존율 **>90%**, 50 mL 바이오리액터 스케일업 | **매트릭스 자체 제거** | [E-258] |
| 소뇌 오가노이드 matrix-free | 소뇌 | Matrigel 캡슐화가 오히려 계통 결정 이상·이동/증식 교란·세포조성 변이 증가 유발 | **Matrigel이 유해** | [E-259] |

### 4.2 정의된 매트릭스가 **실패·열위**한 사례

| 사례 | 장기 | 실패 내용 | 근거 |
|---|---|---|---|
| IEM 조직유래 하이드로겔 | 소장 | *"the formation efficiency was slightly lower than that of Matrigel"* — 전 농도에서 형성효율 열위 (CV는 개선: 35.1% vs 47.7%) | [E-215] |
| 합성 매트릭스 일반 (2024년 이전 전량) | 소장 | **외인성 라미닌 보충 필수.** 라미닌 없이 crypt 형성 불가 | [E-231] |
| Gjorevski 계 | 소장 | 단일 정적 매트릭스로 불가. 확장기(고강성·fibronectin)와 분화기(저강성·**laminin 필수**)가 상반된 요구 | [E-229] |
| 일부 PEG 합성계 | 다장기 | *"proliferation rate was relatively lower compared to that in Matrigel"* | [E-230] |
| 정의된 단백질 하이드로겔 (PEP-FN, PEP-LAMA3) | 췌장 내분비 | 인슐린 분비 기능 미검증, Matrigel 직접 정량 비교 부재. G' 80/120 Pa vs MM 20 Pa | 본문 §조사D 참조 |
| Matrigel 필수 사례 | 내이(inner ear) | *"Matrigel is required for efficient differentiation of isolated, stem cell-derived otic vesicles into inner ear organoids"* — 제목이 곧 결론 | [E-257] |

### 4.3 효능 격차의 정량 요약

| 항목 | 현 상태 |
|---|---|
| 성공/실패 비 | 성공 7건 : 실패·열위 6건 (**약 54%**) |
| **장기 편중** | 성공의 5/7이 **소장·위·간**. 뇌·신장·폐·췌장 내분비·종양 PDO는 정량적 동등성 입증이 얇거나 부재 |
| **라미닌 의존** | 2024년까지 **모든** 합성 매트릭스가 외인성 라미닌 필요 [E-231]. LG화학 콜라겐+mTG 가설은 **라미닌을 포함하지 않는다** → 소장 crypt budding 재현이 최우선 기술 리스크 |
| **강성 스펙트럼** | 소장 100~200 Pa / 전뇌 100 Pa~1 kPa / 후뇌 300 Pa / 심장 700 Pa / 간 6~20 kPa / 골 34 kPa = **최대/최소 340배** [E-260]. 단일 SKU 불가, mTG 가교도로 튜닝 가능한 범위가 이 스펙트럼을 덮는지가 제품 성립 조건 |
| **경쟁의 실체** | "더 좋은 매트릭스"가 아니라 (a) 이미 동등하고 1/10 가격인 콜라겐 I [E-228], (b) 매트릭스를 아예 안 쓰는 현탁 공정 [E-258], (c) 로트 일관성을 선점한 동종 BME [E-255] |

> **B6 판정: 효능 격차는 '해소 가능하지만 장기별로 개별 입증해야 하는' 상태.** 낙관 금지 근거는 [E-236] — *"Transitioning to substitute matrices requires significant optimization and evaluation efforts, as each scaffold has unique properties, and every organoid system has specific requirements."* 및 *"The compatibility with specific models has to be assessed on a case-by-case basis."*

---

## 5. 조사 D — 전환장벽 6항목 정량화 (USD × 개월)

### 5.0 공통 단가 (모두 출처 있음)

| 항목 | 값 | 근거 |
|---|---|---|
| NIH NRSA 박사후연구원 FY2025 최저 스타이펜드 | 62,652 USD/년 | [E-225] |
| Fringe benefit 요율 (보수적 상단) | 27.7% | [E-226] |
| **학술 랩 1 FTE 완전부담 인건비** | **80,007 USD/년** = 38.47 USD/h | [E-227] |
| 대학 오가노이드 코어 교육·인력 요율 | 92.00 USD/h | [E-224] |
| 24-well 플레이트 웰당 셋업 실비 | 11.50 USD/well | [E-224] |
| 웰당 배지 급여 실비 | 0.52 USD/well·회 | [E-224] |
| 인간 오가노이드 라인 수립 실비 | 450.00 USD/line | [E-224] |
| Matrigel 코어 재판매가 / 제조사 직판가 / 대리점가 | 31.00 USD/unit / 447.60 USD/10 mL / 756.50 USD/10 mL | [E-224][E-222][E-223] |
| 제약 과학자 인건비 (학술 ×2.5, 가정 D-A02) | 200,018 USD/년 | 가정 |
| CRO 과학자 인건비 (학술 ×1.8, 가정 D-A02) | 144,013 USD/년 | 가정 |
| 임상랩 과학자 인건비 (가정 D-A02) | 150,000 USD/년 | 가정 |

### B1. 프로토콜 재검증 — 라인당 14,075 USD / 4개월

| 구성 | 계산식 | USD |
|---|---|---|
| (a) 조건 스크리닝 (12조건 × 3반복) | 36 well × 11.50 [E-224] | 414 |
| (b) 장기 계대 검증 (5계대 × 3반복 × 3후보) | 45 well × 11.50 [E-224] | 518 |
| (c) 배지 급여 (4주 × 주2회) | 81 well × 8회 × 0.52 [E-224] | 337 |
| (d) 마커·기능 QC (qPCR + IF, 3배치) | 8 h × 92 [E-224] + 시약 500 | 1,236 |
| (e) 약물반응 브리징 (8제 × 3반복, IC50) | 8 h × 92 [E-224] + 시약 1,500 | 2,236 |
| 소모품·코어 소계 | | **4,741** |
| (f) 인건비 | 0.35 FTE × 4개월 = 0.1167 FTE·yr × 80,007 [E-227] | **9,334** |
| **라인당 합계** | | **14,075** |

학술 랩 표준 3라인, 2번째부터 학습곡선 60%: 14,075 + 2 × 8,445 = **30,965 USD / 6개월**
정성 근거: *"the following assessment and optimization process is tedious and costly"* [E-236]

### B2. 기존 데이터셋과의 비교가능성 상실 — 8,741 USD / 12개월

두 경로로 산출해 교차검증:
- **경로1 (회피비용)**: 구/신 매트릭스 12개월 병행운영 = 소모품 이중 4,741 [B1(a)~(e)] + 재고·관리 0.05 FTE × 1년 × 80,007 [E-227] = 4,000 → **8,741 USD / 12개월**
- **경로2 (기대손실)**: R01 모듈러 직접비 250,000 USD/년 × 오가노이드 실험 비중 30% × 종단데이터 폐기 확률 10% = **7,500 USD**
- 두 경로 편차 16.5% (<2배) → R4 삼각측량 통과. **8,741 USD 채택**(보수적 상단).

리스크의 실체: [E-211]이 "한 실험의 모든 반복은 동일 로트"를 요구한다는 것은, **매트릭스를 바꾸는 순간 그 이전 데이터와의 직접 비교가 프로토콜 위반이 된다**는 뜻이다. 다년 종단 연구·바이오뱅크는 이 시점에 전환을 거부한다.

### B3. 저널·심사자 수용성 — 4,740 USD/년 (영구) / 리비전 3~6개월

- 구조적 근거: *"Validating these alternatives typically requires a reference point, and that reference point is **almost always Matrigel-based**."* [E-239]
- Matrigel은 *"the gold standard for several reasons"* [E-238]이며, 대체재 평가에 대한 *"no standardized criteria or test pipelines"* [E-237] → 심사자는 자기가 아는 기준(Matrigel 대조군)을 요구한다.
- 비용: 논문 1편당 Matrigel 병행 대조 실험 = B1 소모품의 50% = 2,370 USD, 학술 랩 연 2편 → **4,740 USD/년, 영구적**
- 기간: 리비전 1사이클 3~6개월 지연

> **가장 중요한 사업적 함의**: 전환에 성공해도 고객은 **Matrigel 구매를 끊지 못한다.** 우리 제품은 Matrigel을 대체하는 것이 아니라 **Matrigel 위에 추가로 얹히는 지출**이 된다. 이는 (a) 예산 확보를 어렵게 하고 (b) SAM 계산에서 "Matrigel 시장 잠식률"이 아니라 "증분 지출 수용률"로 모델링해야 함을 뜻한다.

### B4. 세포주/장기별 최적화 재수행 — 73,193 USD / 14~28개월

| 장기 | 요구 강성 | 근거 |
|---|---|---|
| Intestinal | 100~200 Pa (효율 최적 180 Pa) | [E-260] |
| Cerebral (전뇌) | 100 Pa ~ 1 kPa | [E-260] |
| Cerebral (후뇌) | 300 Pa | [E-260] |
| Hepatic | 6~20 kPa | [E-260] |
| Cardiac | 700 Pa | [E-260] |
| Bone | 34 kPa | [E-260] |
| Pancreatic / Kidney / Lung / Tumor PDO | 개별 최적값 미확립 — 각각 B1 전량 반복 필요 [E-236] | [E-236] |

계산: 7장기 순차, 학습곡선 70% → 14,075 + 6 × 9,853 = **73,193 USD**
기간: 순차 28개월 / 2트랙 병렬 **14개월**
적용: CRO·제약·바이오뱅크(다장기 취급). 학술 랩(1~2장기)에는 미적용.

### B5. 구매 관성·번들·기관 구매 프로세스 — 1,104 ~ 15,000 USD / 3~6개월

- 코어시설은 Matrigel(31.00)과 Cultrex BME2(33.00)를 **나란히 재고**한다 [E-224]. 신규 SKU를 이 목록에 올리는 것이 실질 관문.
- 학술: 신규 벤더 등록·기관 구매시스템 등재 12 h × 92 [E-224] = **1,104 USD / 3~6개월**
- 제약·GMP: 공급자 QA 감사·문서 심사 포함 **15,000~30,000 USD**
- 리드타임 리스크: Corning은 현재 2주 이내 [E-220]. 신규 공급자가 이보다 나쁘면 즉시 탈락. 2021년 16주 사태 [E-221]의 기억 때문에 구매팀은 **신규 공급자에 더 큰 안전재고**를 요구한다.
- 반증: 동종 BME 간 전환은 "가격 이점"만으로 이미 일어난다 [E-253] → **구매 관성은 6개 장벽 중 가장 약하다.**

### B6. 효능 격차 — 기대비용 11,260 USD / 8~12개월 (발생확률 40%)

- 격차 발생 시 고객 측 추가 공동최적화 = B1의 2배 = **28,150 USD, 8~12개월**
- 발생확률 40% (근거: §4.3 성공/실패 비 54%, 장기 편중, 라미닌 의존 [E-231], 콜라겐+mTG 조성에 라미닌 부재)
- **기대비용 = 0.4 × 28,150 = 11,260 USD**
- 이 항목만이 **비용이 아니라 거래 자체를 무산시킬 수 있는** 유일한 항목이다. 실패 시 고객은 전환을 취소하고 그 랩은 향후 3~5년간 재접근 불가.

### 5.1 전환장벽 6항목 종합표

| 장벽 | 비용 (USD) | 기간 (개월) | 강도 | 완화 레버 |
|---|---|---|---|---|
| B1 프로토콜 재검증 | 30,965 (3라인) | 6 | ★★★★ | 무상 파일럿 키트 + 전담 FAS |
| B2 종단 비교가능성 | 8,741 | 12 | ★★★ | 브리징 데이터셋 무상 생성·공개 |
| B3 저널·심사자 수용성 | 4,740/년 (영구) | 3~6 (리비전) | ★★★★★ | KOL 공동논문, 저널 protocol paper 선행 |
| B4 장기별 재최적화 | 73,193 (7장기) | 14~28 | ★★★★★ | 장기별 SKU + 검증 프로토콜 동봉 |
| B5 구매 관성 | 1,104~30,000 | 3~6 | ★★ | 기존 디스트리뷰터(VWR/Fisher) 채널 |
| B6 효능 격차 | 11,260 (기대값) / 28,150 (발생 시) | 8~12 | ★★★★★ | 라미닌-111 또는 그 기능적 등가물 병용 설계 |

---

## 6. 세그먼트별 전환비용·기간

| 세그먼트 | 구성 | 총비용 (USD) | 기간 (개월) |
|---|---|---|---|
| **학술 RUO** | B1 30,965 + B2 8,741 + B3 4,740 + B5 1,104 + B6 11,260 | **56,810** | **12** |
| **제약 전임상 NAM** | B1' 95,455 (5라인, 인건비 ×2.5) + 어세이 재밸리데이션 25,001 + B2 20,000 + B3 9,480 + B5 15,000 + B6 22,460 | **187,396** | **18** |
| **오가노이드 CRO/바이오뱅크** | B4' 111,016 (7장기, 인건비 ×1.8) + SOP개정·고객통지 20,000 + B2 25,000 + B3 9,480 + B5 10,000 + B6 17,234 | **192,730** | **24** |
| **임상진단 (PDO 약물감수성, CLIA LDT)** | B1' 48,928 (3라인) + LDT 재검증 패키지 92,500 + B2 25,000 + B5 15,000 + B6 17,792 | **199,220** | **30** |
| **재생의료/GMP** | 공급자 감사 30,000 + 3-lot 인바운드 적격성 60,000 + 공정 comparability 3배치 450,000 + 규제문서·변경관리 80,000 + B1' 61,765 | **681,765** | **36** |

세부 계산식:
- 제약 B1' = 라인당 (소모품 4,741 + 0.35 FTE × 4/12 × 200,018) = 28,075; 5라인 학습곡선 60% → 28,075 + 4×16,845 = 95,455
- 제약 어세이 재밸리데이션 = 소모품 8,000 + 0.2 FTE × 3개월 × 200,018 (=10,001) + QA 문서 7,000 = 25,001. **Z' ≥0.5, 대조군 CV <15% 를 신규 매트릭스로 재입증해야 함** [E-234]
- CRO B4' = 라인당 (4,741 + 0.35 × 4/12 × 144,013 = 16,802) = 21,543; 7장기 학습곡선 70% → 21,543 + 6×15,080 = 111,016
- 임상 LDT 재검증 = 병행 검체 30건 × 1,500 (=45,000) + 통계·문서 0.5 FTE × 6개월 × 150,000 (=37,500) + 의료원장/QA 리뷰 10,000 = 92,500. 근거: *"Before substituting a testing reagent, validation is needed to show the same or improved testing performance as the original reagent."* [E-241]
- GMP comparability = GMP 배치 원가 150,000 USD/배치 (가정 D-A08) × 3배치 = 450,000. 근거: *"Changing raw materials at a later stage in clinical development creates significant additional costs and is primarily driven by the need to perform time-consuming clinical comparability studies"* [E-242]

**중앙값**: 세그먼트 단순 중앙값 **192,730 USD / 24개월**; 랩 수 가중 중앙값(학술 랩이 압도적 다수) **56,810 USD / 12개월** [E-262]

---

## 7. 조사 E — 세그먼트별 구매 의사결정과 전환확률

### 7.1 의사결정 구조

| 세그먼트 | 최종 결정권자 | 예산 출처 | 1순위 결정기준 | 가격 민감도 | 전환에 필요한 증거 수준 |
|---|---|---|---|---|---|
| **학술 PI (RUO)** | **PI 단독** (코어 사용 시 코어시설장 공동) | 연구비 직접비(NIH R01 등), 소모품 항목 | ① 논문이 나오는가 ② 리뷰어가 받아주는가 | **높음** — 콜라겐 I가 1/10 가격에 동등 결과 [E-228], Cultrex는 "가격 이점"으로 채택됨 [E-253] | **동료심사 논문 1편** + 자기 랩 파일럿 1회. 규제문서 불필요 |
| **제약 전임상 NAM** | **어세이 오너(팀장)** + 사내 3R/NAM 위원회, 대량 구매 시 소싱팀 | 프로그램 R&D 예산 | ① 어세이 성능(Z' ≥0.5, CV <15%) [E-234] ② 규제 제출 시 방어 가능성 ③ 공급 지속성 | **낮음** — 매트릭스는 어세이 총원가의 소수 항목 | **자체 브리징 검증** + 공급자 QA 문서(CoA, 변경통지 SOP). 논문은 진입 티켓일 뿐 |
| **오가노이드 CRO/바이오뱅크** | **운영이사/과학이사** — 단, **고객이 프로토콜을 지정하면 재량 없음** | 서비스 원가(COGS) | ① 고객 수용성 ② 다장기 커버리지 ③ 로트 안정 공급 | **매우 높음** (COGS 직결) | **주요 고객사의 사전 승인**. 자체 데이터만으로는 못 바꿈 |
| **임상진단 (PDO 약물감수성)** | **랩 메디컬 디렉터 + QA/RA** (CLIA) | 검사 원가 + 자본예산 | ① 재검증 부담 최소화 ② 임상 성능 동등성 | 중간 | **LDT 재검증 패키지 전량**(정밀도·정확도·민감도·특이도·직선성·범위) + 의료원장 SOP 승인 [E-241] |
| **재생의료/GMP** | **QA/RA + CMC 헤드** (과학자는 제안만) | CMC/제조 예산 | ① 규제 수용성 ② 원부자재 등급·추적성 ③ 변경관리 리스크 | **가장 낮음** — 규제 통과가 절대 우선 | **DMF/규제 파일 + 공급자 감사 통과 + 3-lot 적격성**. Matrigel은 애초에 사용 불가 [E-240] |

### 7.2 연간 전환확률 모델

**모델**: `P_annual = R_new × A_defined × D_cost`
- `R_new` = 연간 신규 프로젝트/어세이/서비스 개시 비율 (기존 진행 건은 B2 때문에 전환 안 함)
- `A_defined` = 신규 건에서 defined matrix를 선택할 확률
- `D_cost` = 비용 감쇠계수 = `max(0.5, √(56,810 / 세그먼트 전환비용))`

| 세그먼트 | R_new | A_defined | D_cost | **P_annual** | 캘리브레이션 근거 |
|---|---|---|---|---|---|
| 학술 RUO | 0.40 | 0.15 | 1.00 | **6.0%** | 문헌 114편 중 67편이 ECM 임베딩·Matrigel 최다 [E-216]; 1/10 가격 동등 대체재 존재에도 미전환 [E-228]; gold standard 유지 [E-238] |
| 제약 전임상 NAM | 0.60 | 0.25 | 0.55 | **8.3%** | 포트폴리오 회전 빠름; NAM 규제 문서화 압력이 defined 선택률을 학술보다 높임; 어세이 재밸리데이션 부담이 감쇠 |
| 오가노이드 CRO | 0.50 | 0.10 | 0.54 | **2.7%** | 고객이 프로토콜 지정 → 자체 재량 최저; B4 다장기 부담 최대 |
| 임상진단 (PDO) | 0.30 | 0.20 | 0.53 | **3.2%** | 기존 LDT 변경은 사실상 봉쇄 [E-241]; 신규 검사 런칭 시에만 창이 열림 |
| 재생의료/GMP | 0.50 | 1.00 | 0.50 | **25.0%** | Matrigel 사용 자체가 불가 [E-240] → 임상 진입 시점에 **강제 전환**. 단 모집단이 극히 작음. 최적 접점은 "전임상 종료 직후" [E-242] |

**전환 반감기(= ln2 / P)**: 학술 11.2년 / 제약 8.0년 / CRO 25.3년 / 임상진단 21.3년 / GMP 2.4년

> **Agent A·G에 대한 경고**: 학술 랩 수 × Matrigel 단가로 계산한 SAM에 6.0%/년을 곱하지 않으면 초기 3년 매출이 최대 **16.7배** 과대평가된다. CRO는 **37배**.

---

## 8. 전제 감사 (R5) — 사용자 전제 vs 확인된 사실

| # | 사용자 전제 | 확인된 사실 | 사업적 함의 차이 |
|---|---|---|---|
| D-P1 | "BME의 Lot-to-Lot 편차가 핵심 페인" | 편차는 정량적으로 실재(강성 CV 18.6% [E-205], 로트 통과율 16.7% [E-210])하나, 숙련 랩은 로트 사전시험으로 **이미 흡수** 중이며 MSKCC PDO 팀은 *"stable quality... repeatable"* 로 평가 [E-246] | 페인의 크기 = **관리비용**(B1 수준, 라인당 ~14k USD)이지 **손실비용**이 아니다. 가격 프리미엄 상한이 여기서 결정됨 |
| D-P2 | "비-defined 조성이 전환 동인" | 1992년부터 알려진 문제 [E-208]. 34년간 전환이 안 일어났다 | 조성 정의성만으로는 전환이 안 일어난다는 것이 **34년간의 자연실험 결과**. 규제(NAM/GMP) 강제가 붙어야 움직인다 |
| D-P3 | "마우스 유래 이종성분 = 임상 전환 불가" | **참**. Matrigel은 FDA 승인 이력 없고 GMP 승인 사실상 불가 [E-240] | GMP 세그먼트는 '전환' 시장이 아니라 **'신규 채택' 시장**. 전환확률 25%/년으로 최고이나 모집단이 작음 → Agent A는 이 세그먼트를 별도 모델링해야 함 |
| D-P4 | "재조합 콜라겐 + mTG 가교가 대체 가능" | 소장 crypt 형성은 2024년까지 **모든** 합성계가 외인성 라미닌을 필요로 했다 [E-231]; 정의된 계는 확장기 고강성 + 분화기 저강성·**라미닌 접착**을 요구 [E-229] | 콜라겐+mTG 조성에 **라미닌(또는 기능적 등가 접착 리간드)이 없다면 소장 오가노이드에서 실패 확률이 높다**. B6 발생확률 40%의 주된 근거 |
| D-P5 | "defined matrix가 가격 프리미엄을 받을 수 있다" | 콜라겐 I가 Matrigel 1/10 가격에 LGR5·LYZ·MUC2·VIL1·HNF4A 발현 유의차 없음 [E-228]; Cultrex는 "가격 이점"으로 채택 [E-253] | **프리미엄 근거가 취약하다.** "defined"만으로는 못 받는다. 받으려면 §9 must_win 지표에서 측정 가능한 우위를 내야 함 |

---

## 9. 우리 제품이 반드시 이겨야 하는 성능 지표 (must_win_metrics_top5)

| 순위 | 지표 | **목표 수치** | **현 BME 벤치마크** | 근거 | 왜 반드시 이겨야 하나 |
|---|---|---|---|---|---|
| **1** | 소장 오가노이드 형성효율 (단일 Lgr5+ 세포, Day 6) | **≥34%** (비열등 필수, 목표 ≥40%) | **34%** (Day 6), 2·3차 >60% | [E-233] | 여기서 지면 §4.2의 "IEM 하이드로겔: formation efficiency slightly lower" [E-215]와 같은 운명. 효율 열위는 어떤 가격·정의성으로도 상쇄 불가 |
| **2** | 로트 간 강성(G') 변동계수 | **CV ≤5%** (스펙 ±10% 이내 고정값 보증) | **CV 18.6%**, 최대/최소 **1.95배** | [E-205] | 우리의 유일한 구조적 우위. mTG 가교도 제어로 달성 가능한 유일 지표. 3.7배 개선이 최소 목표 |
| **3** | **로트 합격률** (고객 프로토콜 허용창 통과율) | **≥95%** (실질적으로 "사전시험 불필요" 보증) | **16.7%** (스펙창 대비 실사용창) | [E-210][E-209] | Tuveson Lab이 프로토콜에 적어놓은 "Individual lots need to be tested" [E-209]를 **삭제시키는 것**이 우리 제품의 서사. B1 비용을 고객 대신 흡수하는 유일한 방법 |
| **4** | 오가노이드 크기 변동계수 (소장) | **CV ≤35%** | **47.7%** (Matrigel) / 35.1% (IEM 하이드로겔) | [E-214] | 26% 개선. 단 조직유래 ECM이 이미 35.1%를 달성했으므로 **35% 미만이 아니면 차별화 실패** |
| **5** | **외인성 라미닌 무첨가 crypt/budding 형성률** | **≥80%의 오가노이드가 budding** (라미닌 보충 없이) | 2024년까지 **모든 합성계가 라미닌 필수**; Matrigel은 라미닌 ~60% 함유로 자체 충족 | [E-231][E-229] | 라미닌을 사서 넣어야 한다면 우리 제품의 원가·정의성·GMP 우위가 모두 상쇄된다. **제품 성립의 필요조건** |

**보조(지면 즉시 탈락하는) 지표:**

| 지표 | 목표 | 현 BME 벤치마크 | 근거 |
|---|---|---|---|
| HTS 어세이 Z'-factor / 대조군 CV | Z' ≥0.5 (목표 ≥0.7), CV <15% | Z' 평균 ≈0.7, intra/inter-plate CV <15% | [E-234] |
| 엔도톡신 | **≤0.12 EU/mL** (FDA implantable 기준) | Matrigel은 로트별 편차로 "좋은 로트를 기다려야" 함 [E-245] | [E-232][E-245] |
| 리드타임 | **≤2주** | Corning 현재 2주 이내 [E-220] (2021년 16주 [E-221]) | [E-220] |
| 장기별 강성 커버리지 | **100 Pa ~ 34 kPa (340배)** 을 SKU 3종 이내로 | Matrigel: 44~86 Pa 단일 대역 [E-205] | [E-260] |

---

## HANDOFF

```yaml
switching_cost_usd_per_lab:
  headline_weighted_median: 56810      # 랩 수 가중 중앙값 (학술 RUO가 모집단 다수) [E-261]
  segment_simple_median: 192730        # 5개 세그먼트 단순 중앙값 [E-262]
  by_segment_usd:
    academic_ruo: 56810
    pharma_preclinical_nam: 187396
    organoid_cro_biobank: 192730
    clinical_diagnostics_pdo: 199220
    regenerative_gmp: 681765

switching_time_months:
  headline_weighted_median: 12
  segment_simple_median: 24
  by_segment:
    academic_ruo: 12
    pharma_preclinical_nam: 18
    organoid_cro_biobank: 24
    clinical_diagnostics_pdo: 30
    regenerative_gmp: 36

segment_switch_propensity:            # 연간 전환확률 (%) [E-263]
  academic_ruo:
    pct_per_year: 6.0
    half_life_years: 11.2
    basis: "R_new 0.40 × A_defined 0.15 × D_cost 1.00. 문헌 114편 중 67편 ECM 임베딩·Matrigel 최다[E-216]; 1/10 가격 동등 대체재 존재에도 미전환[E-228]; gold standard 유지[E-238]"
  pharma_preclinical_nam:
    pct_per_year: 8.3
    half_life_years: 8.0
    basis: "R_new 0.60 × A_defined 0.25 × D_cost 0.55. 포트폴리오 회전 빠름 + NAM 문서화 압력, 그러나 Z'≥0.5·CV<15% 재밸리데이션 부담[E-234]"
  organoid_cro_biobank:
    pct_per_year: 2.7
    half_life_years: 25.3
    basis: "R_new 0.50 × A_defined 0.10 × D_cost 0.54. 고객이 프로토콜 지정 → 자체 재량 최저; 7장기 재최적화 부담 최대[E-260][E-236]"
  clinical_diagnostics_pdo:
    pct_per_year: 3.2
    half_life_years: 21.3
    basis: "R_new 0.30 × A_defined 0.20 × D_cost 0.53. 기존 LDT 시약 변경은 전량 재검증 의무[E-241] → 사실상 봉쇄, 신규 검사 런칭 시에만 창"
  regenerative_gmp:
    pct_per_year: 25.0
    half_life_years: 2.4
    basis: "R_new 0.50 × A_defined 1.00 × D_cost 0.50. Matrigel 사용 자체 불가[E-240] → 임상 진입 시 강제 전환. 최적 접점은 전임상 종료 직후[E-242]. 단 모집단 극소"

must_win_metrics_top5:
  - metric: "소장 오가노이드 형성효율 (단일 Lgr5+ 세포, Day 6)"
    target: ">=34% (비열등 필수), 목표 >=40%"
    bme_benchmark: "34% (Day 6), 2·3차 형성 >60%"
    evidence: "E-233"
  - metric: "로트 간 강성 G' 변동계수"
    target: "CV <=5% (스펙 ±10% 이내 고정값 보증)"
    bme_benchmark: "CV 18.6%, 최대/최소 1.95배 (44.3~86.2 Pa)"
    evidence: "E-205"
  - metric: "로트 합격률 (고객 프로토콜 허용창 통과율)"
    target: ">=95% (사전시험 불필요 보증)"
    bme_benchmark: "16.7% (스펙창 7~10 대비 실사용창 9.4~9.9 mg/mL)"
    evidence: "E-210, E-209"
  - metric: "소장 오가노이드 크기 변동계수"
    target: "CV <=35%"
    bme_benchmark: "47.7% (Matrigel); 조직유래 IEM 하이드로겔은 이미 35.1% 달성"
    evidence: "E-214"
  - metric: "외인성 라미닌 무첨가 crypt/budding 형성률"
    target: ">=80% 오가노이드 budding (라미닌 보충 없이)"
    bme_benchmark: "2024년까지 모든 합성 매트릭스가 외인성 라미닌 필수; Matrigel은 라미닌 ~60% 자체 함유"
    evidence: "E-231, E-229"

secondary_kill_criteria:              # 지면 즉시 탈락
  hts_z_factor: {target: ">=0.5 (목표 >=0.7)", bme: "평균 ~0.7", evidence: "E-234"}
  control_cv: {target: "<15%", bme: "<15%", evidence: "E-234"}
  endotoxin: {target: "<=0.12 EU/mL", bme: "로트별 편차, 좋은 로트 대기 필요", evidence: "E-232, E-245"}
  lead_time_weeks: {target: "<=2", bme: "2 (2026 현재), 16 (2021 부족기)", evidence: "E-220, E-221"}
  stiffness_coverage_pa: {target: "100~34000 Pa를 SKU 3종 이내로", bme: "44~86 Pa 단일 대역", evidence: "E-260, E-205"}

pricing_ceiling_signal:               # Agent C·E용
  collagen_I_price_ratio_vs_matrigel: 0.10          # [E-228]
  collagen_I_performance: "LGR5/LYZ/MUC2/VIL1/HNF4A 발현 유의차 없음, 7일 생존세포수 comparable"  # [E-228]
  matrigel_organoid_grade_list_usd_per_10ml: 447.60  # 제조사 직판 [E-222]
  matrigel_distributor_usd_per_10ml: 756.50          # Fisher [E-223]
  core_facility_resale_usd_per_unit: 31.00           # [E-224]
  note: "1/10 가격 동등 대체재의 존재는 '정의성' 프리미엄의 상한을 강하게 억제. 프리미엄 근거는 must_win #2·#3(로트 일관성·합격률)에서만 확보 가능"

structural_risk_for_revenue_model:
  matrigel_never_fully_displaced: true
  reason: "리뷰어·저널이 Matrigel 대조군을 요구 → 전환 후에도 Matrigel 병행 구매 지속 [E-239][E-238][E-237]"
  modeling_instruction: "SAM을 'Matrigel 시장 잠식률'이 아니라 '증분 지출 수용률'로 모델링할 것"
  competing_substitutes:
    - {name: "콜라겐 I 젤", threat: "가격 1/10, 소장에서 동등", evidence: "E-228"}
    - {name: "매트릭스-프리 현탁 공정", threat: "간 담관 오가노이드 크기 2.6배·생존 >90%, 바이오리액터 스케일업", evidence: "E-258"}
    - {name: "Cultrex UltiMatrix (동종 BME)", threat: "'로트 20건 무실패'로 로트 일관성 축 선점, 가격 이점으로 전환 발생 중", evidence: "E-255, E-253"}
```

---

## DoD 셀프 체크

| # | 항목 | 결과 | 근거 |
|---|---|---|---|
| 1 | Lot 편차 정량 수치 최소 5건 (단위·CV%·범위 포함) | **PASS (9건)** | A1 1,851종 [E-200] / A3 7~10 mg/mL 1.43배 [E-203] / A6 9.1→288.2 Pa [E-204] / A7 44.3~86.2 Pa, CV 18.6% [E-205] / A9 EGF 0.5~1.3 ng/mL 2.6배 [E-207] / A10 크기 CV 74.5% [E-213] / A11 47.7% [E-214] / A13 로트 통과율 16.7% [E-210] / A14 표현형 3분기 [E-218] |
| 2 | 전환장벽 6항목 각각 비용(USD)·기간(개월) 추정 | **PASS** | B1 30,965/6mo · B2 8,741/12mo · B3 4,740/yr·3~6mo · B4 73,193/14~28mo · B5 1,104~30,000/3~6mo · B6 11,260(기대)/8~12mo — §5 전 항목 빌드업 계산식 제시 |
| 3 | VOC 원문 인용 20건 이상 (각 URL) | **PASS (21건)** | §3 V1~V21, 전 건 원문 영어 + 한국어 요약 + URL. 사용자명 익명화 |
| 4 | must_win_metrics_top5 도출 (수치 목표 포함) | **PASS** | §9 — 5개 지표 모두 목표수치 + 현 BME 벤치마크 수치 + 근거 ID. 보조 킬 기준 5개 추가 |
| 5 | segment_switch_propensity 5개 세그먼트 산출 | **PASS** | §7.2 — 학술 6.0 / 제약 8.3 / CRO 2.7 / 임상진단 3.2 / GMP 25.0 %/년. 모델식 P = R_new × A_defined × D_cost 명시 |
| 6 | 긍정 VOC 포함 (편향 방지 확인) | **PASS** | 21건 중 긍정 11건(52%). 최고 등급 기관(MSKCC [E-246], Hubrecht/Clevers Lab [E-256], Salk [E-255]) 발화 포함. §3.1에 감정 분포표 및 "지배적 정서는 만족 + 체념" 명시. §8 전제감사에서 사용자 전제 5건 중 4건에 반증 제시 |
| 7 | (추가) AGENT_RULES §1 금지표현 미사용 | **PASS** | 금지어 목록 전 항목 미출현(자동 grep 통과). 미확정 1건은 `docs/gaps.md` GAP-D-01에 4요소(쿼리 6개·소스 9개·부재 판단·대체 추정치+오차범위) 갖춰 기록, 1차 출처 미확인 수치 1건은 GAP-D-02에서 전면 배제 |
| 8 | (추가) 전 수치 [E-###] 부착 + 파생수치 계산식 명시 | **PASS** | §1.3·§5·§6·§7.2 전 파생수치에 계산식. 가정 12건 `docs/assumptions.md`에 append |
