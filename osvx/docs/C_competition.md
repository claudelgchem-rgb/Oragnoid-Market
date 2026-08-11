# Agent C — 경쟁·공급자 랜드스케이프 & 가격 구조

작업 루트: `/home/user/Oragnoid-Market/osvx` / 근거 ID: **E-100 ~ E-170** (71건)
데이터: `data/price_table.csv` (42개 제품) / access_date: **2026-08-11**
환율: Federal Reserve H.10, week ending 2026-08-07 — USD/EUR 1.1559, USD/GBP 1.3498, CNY 6.7474/USD, JPY 157.54/USD, KRW 1,409.94/USD [E-146]

---

## 0. 요약 — 이 조사가 사업가설에 던지는 3가지 불리한 사실

본 보고서는 LG화학 제품가설(재조합/정제 콜라겐 + mTG 효소 가교 기반 Defined Organoid Matrix)에
유리한 근거와 불리한 근거를 동일한 기준으로 기술한다. 먼저 **불리한 사실 3가지**를 앞에 둔다.

1. **"정의성 프리미엄"은 통계적으로 입증되지 않는다.** fully-defined 중앙값 $60.47/mL 대 
   undefined-BME 중앙값 $48.24/mL 로 명목상 1.25배지만, Mann-Whitney U 검정 **p=0.168** 로
   유의수준 0.05 에서 두 분포가 다르다고 말할 수 없다. BME 의 3사분위($72.45)가
   fully-defined 의 중앙값($60.47)보다 높다 [E-161]. **defined 라는 이유만으로 가격을 더 받을 수 있다는
   전제는 현재 시장 데이터로 지지되지 않는다.**
2. **콜라겐 + mTG(트랜스글루타미나제) 가교 3D 배양 매트릭스는 이미 상용 판매 중이다.**
   101Bio 의 **Col-Tgel** 이 Component A(콜라겐/젤라틴) + Component B(트랜스글루타미나제 가교제)
   2액형으로 2 mL $109 / 10 mL $389 에 판매되며, 3단 강성(0.9–1.5 / 14–20 / 35–47 kPa)까지 제품화되어 있다
   [E-120]. 1차 문헌으로 가교 효소가 트랜스글루타미나제임을 확증했다 [E-164].
   **"mTG 가교"는 신규 차별화 요소가 아니다.**
3. **Corning 이 이미 완전합성 defined 라인(Synthegel)을 출시했고, 자사 BME 오가노이드 SKU보다 싸게 책정했다.**
   Synthegel 3D hiPSC Matrix Kit $37.08/mL 대 Matrigel for Organoid Culture $44.76/mL [E-130][E-102].
   기존 강자가 defined 카테고리를 **프리미엄이 아니라 가격 방어 수단**으로 쓰고 있다 [E-166].

동시에 사업가설에 **유리한 사실**도 명확하다. Matrigel 의 락인은 가격이 아니라 인용·프로토콜 관성에
있으며(PubMed 15,004건 대 defined 대체재 7종 합계 292건 [E-149][E-152]), GMP 등급에서는
**공개 정가를 가진 제품이 42개 중 0개** [E-160] — 즉 임상·재생의료 구간은 아직 비어 있다.

---

## 1. 가격표 개요

`data/price_table.csv` — **42개 제품**, USD/mL 빈칸 0건, 추정 셀 6건(전부 `추정:` 접두사 + assumptions.md 가정ID 기재).

### 1.1 카테고리별 분포 (3D 매트릭스 37개, 2D 코팅시약 5개 제외)

| category | n | 중앙값 USD/mL | 대표 제품 |
|---|---:|---:|---|
| BME | 14 | **48.24** | Corning Matrigel, Cultrex UltiMatrix, Geltrex, Ceturegel |
| synthetic-defined | 15 | **58.21** | Corning Synthegel, PuraMatrix, VitroGel, Cellendes, TrueGel3D |
| purified-animal-protein | 5 | **11.64** | PureCol, TeloCol-6, Nutragen, Corning Collagen I, JellaGel |
| recombinant-protein | 2 | **45.55** | Col-Tgel, HumaDerm |
| plant-or-other | 1 | **72.82** | UPM GrowDex |
| *(별도) 2D 코팅시약* | *5* | *114.97* | *rhLaminin-521, rLaminin-521, Biolaminin, iMatrix-511, Vitronectin XF* |

2D 코팅시약(라미닌·비트로넥틴)은 µg/cm² 기준으로 소비되어 mL 기준 3D 포매 제품과 단위경제가 다르므로
정의성 프리미엄 통계에서 **제외**했다(가정 C-A1b). 포함 시 fully-defined 중앙값이 상향 왜곡되어
사업가설에 유리한 방향으로 기울기 때문에, 제외가 보수적 처리다.

### 1.2 가격 극단값

- **최저** $5.40/mL — Advanced BioMatrix PureCol 소 콜라겐 3 mg/mL 100 mL [E-114].
  **매트릭스 원재료 가격의 실질 하한선**. LG화학이 콜라겐 기반으로 진입할 때 고객이 참조할 수 있는
  "원료는 이 가격인데" 앵커가 된다.
- **최고(3D)** $212.50/mL — Ectica 3DProSeed (추정, 가정 C-A4f).
  실측 최고는 Cellendes ToGro $210.00/mL [E-141].
- **최고(전체)** $840.00/mL — iMatrix-511 재조합 라미닌 원액 [E-117] (코팅시약).

---

## 2. 가격–정의수준 분석 — "정의성 프리미엄"은 실재하는가

### 2.1 분포 통계 (3D 매트릭스 37개, USD/mL)

| definition_level | n | min | Q1 | **median** | Q3 | max | mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| undefined-BME | 14 | 21.30 | 38.36 | **48.24** | 72.45 | 88.30 | 53.91 |
| semi-defined | 9 | 5.40 | 11.64 | **38.90** | 52.77 | 72.82 | 33.81 |
| fully-defined | 14 | 25.00 | 52.06 | **60.47** | 168.26 | 212.50 | 92.53 |

### 2.2 판정 — 프리미엄은 명목상 존재하나 **통계적으로 유의하지 않다**

```
definition_premium_ratio = median(fully-defined) / median(undefined-BME)
                         = 60.47 / 48.24
                         = 1.253   [E-161]
```

그러나 이 1.25배는 **검정을 통과하지 못한다**:

```
Mann-Whitney U (fully-defined n=14 vs undefined-BME n=14)
  U = 128.0 ,  z = 1.379 ,  p = 0.168        → 유의수준 0.05 에서 귀무가설 기각 실패
  CLES (P[defined > BME]) = 0.653            → 우연(0.5)보다 약간 나은 수준
  분포 중첩: BME Q3 = 72.45  >  defined median = 60.47
```

**정직한 결론**: 현재 시장에서 "완전 정의(fully-defined)"라는 속성만으로 확보되는 가격 프리미엄은
**중앙값 기준 +25%, 통계적 유의성 없음**이다. fully-defined 의 평균이 높은 것($92.53)은
Cellendes/TrueGel3D 같은 **소용량 연구용 키트(1–2 mL)**의 소용량 프리미엄이 끌어올린 결과이며,
동일 용량대(10 mL)에서 비교하면 오히려 역전된다:

| 10 mL 급 동일 용량 비교 | USD/mL |
|---|---:|
| Corning Synthegel 3D hiPSC (fully-defined, 10 mL) | **37.08** [E-130] |
| Corning Matrigel for Organoid Culture (BME, 10 mL) | **44.76** [E-102] |
| Corning Matrigel 일반 (BME, 10 mL) | 30.29 [E-100] |
| Cultrex RGF BME Type 2 (BME, 10 mL) | 56.60 [E-138] |
| VitroGel ORGANOID-1 (fully-defined, 10 mL) | 56.96 [E-111] |
| Yeasen Ceturegel Organoid (BME, 10 mL) | 21.30 [E-125] |

**같은 제조사(Corning)가 같은 10 mL 규격으로 파는 defined 제품이 BME 오가노이드 제품보다 17% 싸다.**
이것이 이 시장의 가격 현실이다.

### 2.3 실제로 가격을 움직이는 변수는 "정의수준"이 아니라 "용량"과 "브랜드"

관측된 소용량 프리미엄(동일 제품, 용량만 다름):

| 제품 | 대용량 USD/mL | 소용량 USD/mL | 프리미엄 |
|---|---:|---:|---:|
| Corning Matrigel 354234(10mL) → 356234(5mL) | 30.29 | 39.01 | +28.8% [E-100][E-133] |
| Geltrex A1413202(5mL) → A1413201(1mL) | 71.20 | 85.75 | +20.4% [E-105][E-139] |
| Cultrex UltiMatrix BME001-05(5mL) → -01(1mL) | 76.20 | 88.30 | +15.9% [E-106][E-107] |
| VitroGel ORGANOID-1 10mL → 2mL | 56.96 | 113.86 | **+99.9%** [E-111][E-169] |

**소용량 프리미엄(+16~100%)이 정의성 프리미엄(+25%, 유의하지 않음)보다 크고 확실하다.**
사업 함의: 가격 결정력은 "defined 라고 주장하는 것"이 아니라 **SKU 설계와 채널 장악**에서 나온다.

---

## 3. Grade (RUO vs GMP) 별 가격 배수 — 실측

### 3.1 오가노이드 매트릭스에는 공개 정가를 가진 GMP 제품이 **0개**

조사한 42개 제품 전부가 RUO 등급이다 [E-160]. GMP/임상 라인을 **보유**한다고 확인된 곳은 4곳뿐이며
모두 견적제로 정가를 공개하지 않는다:

| 기업 | GMP/임상 라인 | 상태 |
|---|---|---|
| Thermo Fisher | CTS Vitronectin, CTS 계열 | 견적제. A27940 은 단종, A400457/458 로 이관 |
| BioLamina | **Biolaminin 521 CTG (CT521)** — 세계 최초 cell therapy grade 라미닌 | 견적제 [E-158] |
| Nippi / Matrixome | iMatrix-511MG (임상등급) | 견적제 |
| ACROBiosystems | GMP Human Laminin 521 (LA5H24) | 견적제 |

**BME 계열(Matrigel/Cultrex/Geltrex)은 GMP 라인 자체가 존재하지 않는다** — 마우스 EHS 육종 유래라는
원료 특성상 임상 등급화가 구조적으로 불가능하기 때문이다. 이것이 LG화학 가설의 **가장 큰 열린 공간**이다.

### 3.2 RUO → GMP 배수 실측 = **1.942배 (+94.2%)**

매트릭스에 GMP 가격이 없으므로, **동일 제조사·동일 분자·동일 규격**의 RUO/GMP 쌍을 인접
세포배양 원재료 시장에서 실측해 배수를 도출했다:

```
Human IL-21 100 µg (PeproTech / Thermo Fisher, Fisher Scientific 판매가)
  RUO      200-21     100 µg  =  $1,192.00
  PeproGMP GMP200-21  100 µg  =  $2,315.00
  배수 = 2315.00 / 1192.00 = 1.942  (+94.2%)                          [E-159]
```

이 배수는 **순수 품질보증 프리미엄**으로 해석 가능하다 — 제조사 자신이 "GMP 제품은 RUO 와 동일한
클론·동일한 제조공정을 쓰고 QC 시험만 추가된다"고 명시하기 때문이다.

```
asp_gmp_usd_per_mL = median(fully-defined) x RUO→GMP 배수
                   = 60.47 x 1.942
                   = 117.43 USD/mL          [E-160][E-159][E-161]
```

**사업 함의**: LG화학이 GMP 발효·정제 인프라를 이미 보유했다는 것은, 경쟁사가 견적제 뒤에 숨어 있는
구간에서 **표시가격 $117/mL 수준의 defined GMP 매트릭스**를 정가로 내놓을 수 있다는 뜻이다.
이 구간에는 BME 3사가 구조적으로 진입할 수 없다.

---

## 4. 신규 진입자의 최근 3년 자금조달·M&A — **자본이 마르고 있다**

| 기업 | 국가 | 최근 자금조달/사건 | 판정 |
|---|---|---|---|
| **QGel SA** | 스위스 (EPFL 스핀오프) | 누적 $20.5M. 확인된 최대 라운드는 **2016년 12월 $12M**. 2019년 $60M 라운드 추진 보도가 있었으나 완결 공시 미확인. **2023–2026년 신규 라운드 검색 결과 없음** [E-136] | 정체 |
| **Ectica Technologies** | 스위스 (취리히) | 공개 DB 집계 누적 **$54K** (Seed 1 + Grant 2). 최대는 2018년 4월 $60.6K grant. 투자자 EIC Fund, Merck Accelerator [E-137] | 초기 단계 고착 |
| **denovoMATRIX** | 독일 (드레스덴) | 주력 스크리닝 제품 **screenMATRIX 단종(discontinued)** [E-124][E-170] | 제품 철수 |
| **CollPlant Biotechnologies** | 이스라엘 (나스닥 CLGN) | 2025 매출 **$2.4M** (2024 $515K), 증가분 대부분이 AbbVie 마일스톤 $2M. 이후 **AbbVie 개발계약 종료 + 인력 약 50% 감축**, 현금 런웨이 2026 Q4 [E-135] | 구조조정 |
| **Manchester BIOGEL** | 영국 | 정가 미공개(POA) 유지, 공개 라운드 미확인 [E-153] | 소규모 유지 |
| **Biogelx** | 영국 | 정가 미공개, Sigma-Aldrich 기술 파트너 게재 수준 [E-154] | 소규모 유지 |
| **Gelomics** | 호주 | Rousselot(Darling Ingredients) 원료 파트너십으로 X-Pure GelMA 공급 [E-143] | 원료사 제휴형 |
| **TheWell Bioscience** | 미국 | VitroGel 을 Fisher/BioCat 등 광역 유통망에 안착 [E-111][E-169] | 유통 성공 사례 |
| **Humabiologics** | 미국 | VWR/Fisher/Ourobionics 유통 진입 [E-134] | 유통 진입 |
| **Advanced BioMatrix** | 미국 | **BICO 그룹 편입** (M&A 완료) [E-114][E-115] | 피인수 |

**해석**: 지난 3년간 이 카테고리에서 **의미 있는 대형 라운드나 고평가 M&A가 관측되지 않는다.**
오히려 단종(denovoMATRIX), 계약해지·감원(CollPlant), 라운드 정체(QGel)가 지배적이다.
이는 두 가지로 읽힌다 — (a) defined 매트릭스의 **수요가 벤처 기대만큼 크지 않다**는 부정 신호이자,
(b) 경쟁 강도가 낮아 **자본력 있는 후발주자에게 공간이 남아 있다**는 긍정 신호다.
LG화학처럼 자체 현금흐름·GMP 인프라를 가진 대기업에게는 (b)의 비중이 더 크다.

---

## 5. Corning 의 방어 움직임

### 5.1 이중 방어 라인 [E-166]

Corning 은 defined 전환 압력에 **두 개의 라인**으로 대응하고 있다.

**라인 1 — BME 내부 프리미엄화**: `Corning Matrigel Matrix for Organoid Culture` (356255, 10 mL,
Phenol Red-free, LDEV-free). 마우스·인체 오가노이드 성장/분화 지원을 검증한 로트만 선별 출하.
$447.60 = **$44.76/mL**, 일반 Matrigel($30.29/mL) 대비 **+47.8%** [E-102][E-100].
즉 "오가노이드 전용"이라는 라벨만으로 BME 안에서 48% 프리미엄을 이미 걷고 있다.

**라인 2 — 완전합성 Synthegel 출시**: 합성 펩타이드 나노섬유 용액 + Synthegel X-Link 가교제 2액형.
defined, self-healing, 동물유래 무첨가.

| Cat# | 제품 | 규격 | 정가 | USD/mL |
|---|---|---:|---:|---:|
| 354787 | Synthegel 3D hiPSC Matrix Kit | 10 mL | $370.80 | **37.08** [E-130] |
| 354789 | Synthegel Spheroid Matrix Kit | 10 mL | $432.60 | **43.26** [E-131] |
| 354791 | Synthegel 3D hiPSC Suspension Matrix Kit | 16 mL | (동일 라인) | — |
| 354792 | Synthegel 3D hiPSC Grow Mix | 1 mg 동결건조 | (보조제) | — |

**핵심 관찰**: Corning 은 자사 완전합성 defined 제품을 **자사 BME 오가노이드 제품보다 17% 싸게**
책정했다($37.08 vs $44.76). 이는 defined 를 프리미엄으로 파는 것이 아니라,
**defined 로 이탈하려는 고객을 자사 울타리 안에 묶어두는 가격 방어**다.
신규 진입자가 "defined 니까 비싸게 받겠다"는 전략을 쓰면 Corning 의 $37.08/mL 에 정면으로 부딪힌다.

단, Synthegel 의 시장 침투는 아직 미미하다 — PubMed 인용 **1건** [E-152].

### 5.2 Corning 재무 실체 (SEC EDGAR 및 IR 원문)

| 항목 | 2025 | 2024 | 출처 |
|---|---:|---:|---|
| Life Sciences 세그먼트 순매출 | **$972M** | $979M | [E-127] |
| Life Sciences 세그먼트 순이익 | **$61M** | $63M | [E-127] |
| Life Sciences 순이익률 | **6.28%** | 6.44% | [E-167] (계산 = 61/972) |
| 전사 core sales | $16.41B (+13% YoY) | — | [E-127] |
| 10-K 상 LS 비중 | **전사 세그먼트 순매출의 6%** | — | [E-128] SEC 원문 |

**해석**: Life Sciences 는 Corning 전체에서 6% 비중의 **비주력 세그먼트이며 YoY -0.7% 로 역성장**했다.
전사가 AI/데이터센터 광통신으로 +13% 성장하는 동안 LS 는 정체다. 세그먼트 순이익률 6.28%는
Matrigel 이 고마진 제품임을 감안하면 낮은데, 이는 세그먼트 내 저마진 소모품(플라스틱 플레이트·플라스크)
비중이 크기 때문으로 보인다.
**사업 함의**: Corning 에게 Matrigel 방어는 전사 우선순위가 아니다. 공격받았을 때 전면적 가격전쟁으로
대응할 유인이 약하다.

### 5.3 Bio-Techne (Cultrex) 재무

| 항목 | FY2025 | FY2024 | 출처 |
|---|---:|---:|---|
| Protein Sciences 세그먼트 순매출 | **$870.2M** | $830.9M (+5%) | [E-129] SEC 10-K |

Cultrex BME 는 이 세그먼트에 포함된다. Bio-Techne 는 UltiMatrix 를 Matrigel 대체 캠페인의
주력 SKU 로 밀고 있으나(BME001 시리즈), PubMed 인용은 UltiMatrix 6건 / Cultrex 전체 53건에 그친다 [E-151].

---

## 6. 시장 집중도 — BME 3사 과점

### 6.1 인용 기반 점유율 (실측)

| 제품 | PubMed 논문 수 | 인용 점유율 |
|---|---:|---:|
| **Matrigel** (Corning) | **15,004** | **98.97%** [E-149] |
| Geltrex (Thermo) | 104 | 0.69% [E-150] |
| Cultrex (Bio-Techne) | 53 | 0.35% [E-151] |
| *3사 합계* | *15,161* | *100%* |

### 6.2 defined 대체재의 침투율 — 2% 미만

| 제품 | PubMed 논문 수 |
|---|---:|
| PuraMatrix | 228 |
| VitroGel | 22 |
| GrowDex | 17 |
| iMatrix-511 | 12 |
| Col-Tgel | 11 |
| TrueGel3D | 1 |
| Corning Synthegel | 1 |
| **합계** | **292** |

```
defined 대체재 침투율 = 292 / 15,004 = 1.95%          [E-152]
```

**20년 넘게 시장에 있던 PuraMatrix 조차 228건**이다. 이것은 전환 장벽이 **가격이 아니라
프로토콜·인용 관성**임을 강하게 시사한다. 가격을 낮춰도 전환이 일어나지 않을 수 있다는
경고이자, 동시에 인용을 만들어주는 쪽(레퍼런스 랩·CRO 시딩)에 투자하면 장벽을 넘을 수 있다는 지침이다.

### 6.3 점유율 추정

```
top3_share_estimate = 78%   (Corning 58% / Bio-Techne 12% / Thermo 8%)     [E-165]
```

**도출 근거** (가정 C-A5): 인용 점유율 98.97%를 그대로 쓰면 과대추정이다 —
"Matrigel"이 BME 의 총칭어로 오용되며, 인용은 신제품 채택에 2–4년 후행하기 때문이다.
Corning LS 매출 $972M [E-127] 과 Bio-Techne Protein Sciences $870.2M [E-129] 의 규모 관계,
그리고 중국 로컬(Yeasen, Beyotime, Biofargo)의 실질 판매 존재를 반영해
Corning 을 58%로 하향, Cultrex 를 12%로 상향 보정했다. **범위 70~85%**.
어느 쪽이든 "과점" 결론은 불변이다.

3자 시장보고서는 Matrigel 단독 시장을 2024년 $88M → 2032년 $197M, CAGR 12.2%로 제시하나 [E-168],
방법론 미공개 벤더 보고서이므로 신뢰도 하(T3)로 취급한다.

### 6.4 중국 로컬의 가격 파괴

| 제품 | 제조사 | USD/mL | Corning 356255 대비 |
|---|---|---:|---:|
| Ceturegel Matrix for Organoid (10 mL) | Yeasen | **21.30** [E-125] | **−52.4%** |
| AMMS Organoid-specific Matrigel (5 mL) | Biofargo | 44.00 [E-140] | −1.7% |
| Matrix-Gel 오가노이드용 (50 mL) | Beyotime | 48.69 [E-126] | +8.8% |

Yeasen 은 Corning 오가노이드 SKU 의 **절반 가격**에 동등 소구 제품을 팔고 있고,
Beyotime 은 "Corning Matrigel 완전 대체 가능"을 자사 문구로 명시한다 [E-126].
**중국 시장에서 가격 프리미엄 전략은 이미 무력화되어 있다.**

---

## 7. mTG(microbial transglutaminase) 가교 — **기존 상용 제품이 이미 존재한다**

이 항목은 LG화학 제품가설의 핵심 차별화 주장을 직접 검증하는 것이므로, 결과를 있는 그대로 기술한다.

### 7.1 결론: **존재한다. 차별화 주장은 약화된다.**

**101Bio (101 Biosystem) 의 `Col-Tgel` — 3D Cell Culture Gel**

| 항목 | 내용 | 근거 |
|---|---|---|
| 아키텍처 | **2액형: Component A (콜라겐 기반 젤) + Component B (트랜스글루타미나제 가교제)** | [E-120] |
| 가교 화학 | **효소 가교 — microbial transglutaminase** | [E-120][E-164] |
| 1차 문헌 확증 | "12% gelatin (bovine skin type B 225 bloom)" + "purified transglutaminase (Tg) crosslinker for final concentration of 50 µg/ml", 37℃ 약 30분에 비가역 하이드로겔로 전환해 세포를 in situ 포매 | [E-164] PLOS One / PMC4136878 |
| 제품화 수준 | 강성 3단 제품화 — soft 0.9–1.5 kPa / medium 14–20 kPa / stiff 35–47 kPa | [E-120] |
| 가격 | 2 mL $109.00 / 10 mL $389.00 → **$38.90/mL** | [E-120] |
| 적용 세포 | 종양세포, 줄기세포, 초대배양세포(골·근·신경) | [E-120] |
| 유통 | Fisher Scientific, AMSBIO, Gentaur, MaxAnim 등 다중 채널 | [E-121] |
| 학술 침투 | PubMed 11건 | [E-152] |

즉 **"콜라겐 백본 + 트랜스글루타미나제 효소 가교 + 강성 튜닝"이라는 조합은 이미 상용 제품으로
존재하며, 미국·유럽 주요 유통망에 올라가 있다.**

### 7.2 그럼에도 남아 있는 차별화 공간 (정직한 평가)

Col-Tgel 의 존재가 LG화학 가설을 무효화하지는 않는다. 다음 4가지가 여전히 열려 있다.

1. **원료 등급**: Col-Tgel 은 **소 피부 유래 젤라틴(bovine skin type B)** 기반이다 [E-164].
   LG화학 가설의 **재조합/정제 콜라겐**은 이종(異種) 동물유래 성분을 배제한다는 점에서
   규제·임상 전환 관점의 우위가 실재한다.
2. **GMP 등급**: Col-Tgel 은 RUO 전용이며 GMP 라인이 없다. GMP mTG 를 보유한 LG화학은
   **임상등급 mTG 가교 매트릭스**라는 미점유 포지션을 취할 수 있다(§3.1, §3.2).
3. **오가노이드 적격성**: Col-Tgel 의 소구 대상은 종양·줄기·초대배양세포이며,
   **오가노이드 확립·확장 적격성 데이터가 제품 소구에 없다**. PubMed 11건도 오가노이드 특화가 아니다.
   Corning 356255, Cultrex Type 2 가 "오가노이드 적격성 시험 통과"를 명시하는 것과 대비된다 [E-102][E-138].
4. **triple helix 혼합 설계**: Col-Tgel 은 젤라틴(변성 콜라겐, single chain) 기반인 반면,
   LG화학 가설은 **single + triple helix 혼합**이다. 이는 조성 설계상 실제로 구별되는 지점이다.

### 7.3 사업적 함의 (냉정하게)

- **"mTG 가교"를 단독 차별화 메시지로 쓰면 안 된다.** 이미 $38.90/mL 에 파는 선행 제품이 있고,
  고객·심사역·특허심사관 모두 Col-Tgel 을 선행기술로 지목할 수 있다.
- 차별화 메시지는 **"재조합 콜라겐 + GMP 등급 + 오가노이드 적격성 검증"의 3중 결합**으로 이동해야 한다.
  이 세 가지를 동시에 갖춘 제품은 42개 조사 대상 중 **0개**다.
- Col-Tgel 의 $38.90/mL 은 **동일 아키텍처 제품의 가격 앵커**로 작동한다.
  RUO 시장에서 이보다 크게 높은 가격은 정당화가 어렵다. GMP 배수 1.942 [E-159] 를 적용한
  $75.6/mL 정도가 GMP 라인의 현실적 상한 참조점이다.
- **Agent F(IP/FTO) 로의 경고**: Col-Tgel 및 그 기반 문헌(PMC4136878, PLOS One 2014)은
  콜라겐/젤라틴 + 트랜스글루타미나제 가교 3D 배양의 **선행기술**이다. 신규성 확보 범위를
  이 문헌 대비로 반드시 설정해야 한다.

---

## 8. 유통 마진 역산

동일 Cat# 를 제조사 직판 페이지와 유통사 페이지 양쪽에서 확인한 5쌍:

| 제품 | 제조사 직판 | 유통사 | 마진 |
|---|---:|---:|---:|
| Corning rLaminin-521 354221 | $81.01 | Fisher $142.30 | **+75.7%** [E-144][E-145] |
| Corning Matrigel 354234 | $302.85 | Fisher $438.50 | **+44.8%** [E-100][E-163] |
| Corning Matrigel Organoid 356255 | $447.60 | Fisher $608.50 | **+35.9%** [E-102][E-103] |
| Corning Matrigel 354234 | $302.85 | VWR $386.75 | **+27.7%** [E-100][E-101] |
| Corning Matrigel Organoid 356255 | $447.60 | VWR $482.96 | **+7.9%** [E-102][E-103] |

```
distributor_markup_pct = median(75.7, 44.8, 35.9, 27.7, 7.9) = 35.9%   (평균 38.4%)   [E-162]
```

**대조군**: Geltrex A1413202 는 Thermo 직판 $356.00 = Fisher $356.00 으로 **마진 0%** [E-105].
Thermo 가 Fisher 를 소유한 계열 내재화 구조이기 때문이며, 이 쌍은 표본에서 제외했다.

**사업 함의**:
- 유통사를 통하면 최종 고객가가 **중앙값 35.9% 상승**한다. LG화학이 직판 채널을 확보하면
  같은 고객 지불액에서 36%의 여유를 마진 또는 가격경쟁력으로 전환할 수 있다.
- 반대로 Fisher/VWR 를 통해 미국 시장에 접근하려면 **표시가격의 약 26%(= 35.9/135.9)를
  유통 마진으로 내줘야** 한다. Agent E(원가) 및 Agent G(GTM)의 채널 설계 입력값.
- Thermo–Fisher 의 0% 사례는 **수직통합 채널의 가격 경쟁력**을 보여준다.

---

## 9. 데이터 품질과 한계 (정직 고지)

- 42개 제품 중 **6개(14.3%)가 회귀 추정치**다: Ectica 3DProSeed, Manchester BIOGEL PeptiGel,
  Biogelx-S, QGel CN99, Jellagen JellaGel, BioLamina LN521. 모두 `추정:` 접두사로 표시했고
  회귀 근거와 민감도를 `docs/assumptions.md` 가정 C-A4a~C-A4f 에 기재했다.
  이 6개를 전부 제외하고 재계산해도 `definition_premium_ratio` 는 1.20~1.30 범위에 머물러
  §2 의 결론(유의성 없음)은 변하지 않는다.
- 키트형 제품 4건은 제조사가 겔 수율을 공개하지 않아 부피 가정을 적용했다(C-A3a~C-A3e).
  이 중 Cellendes는 제조사 데이터시트 문구로 확정했고 [E-148], TrueGel3D 만 유추다.
- `access_status:"failed"` 1건: AMSBIO Col-Tgel 페이지(403). 제품 존재는
  101Bio 원본 페이지와 다중 유통 인덱스로 교차확인했다 [E-120][E-121].
- 3자 시장보고서(Matrigel 시장규모)는 방법론 미공개로 T3/신뢰도 하 처리했다 [E-168].
  Agent A 의 시장규모 산정에서는 이 수치를 단독 근거로 쓰지 말 것.

---

## HANDOFF

후행 에이전트(A 시장규모 / E 원가 / F IP / G GTM / S 통합)가 그대로 사용할 정량값.

| 키 | 값 | 산출식 / 근거 |
|---|---:|---|
| `asp_bme_usd_per_mL` | **48.24** | median(undefined-BME, n=14) [E-161] |
| `asp_defined_usd_per_mL` | **60.47** | median(fully-defined, n=14) [E-161] |
| `asp_semidefined_usd_per_mL` | **38.90** | median(semi-defined, n=9) |
| `asp_gmp_usd_per_mL` | **117.43** | = 60.47 × 1.942 [E-160][E-159] — 매트릭스 GMP 공개가 0건이므로 IL-21 매칭쌍 배수 적용 |
| `definition_premium_ratio` | **1.253** | = 60.47 / 48.24 [E-161] |
| `definition_premium_significant` | **false** | Mann-Whitney U=128.0, z=1.379, **p=0.168** [E-161] |
| `gmp_over_ruo_multiple` | **1.942** | Human IL-21 100µg: $2,315.00 / $1,192.00 [E-159] |
| `top3_share_estimate` | **0.78** | Corning 0.58 + Bio-Techne 0.12 + Thermo 0.08. 범위 0.70~0.85 [E-165] |
| `distributor_markup_pct` | **35.9** | 5쌍 중앙값 (평균 38.4) [E-162] |
| `matrigel_organoid_sku_usd_per_mL` | **44.76** | Corning 356255 직판 $447.60/10mL [E-102] — **직접 대체 타깃 가격** |
| `corning_synthegel_usd_per_mL` | **37.08** | 354787 $370.80/10mL [E-130] — **defined 진입 시 부딪히는 가격 바닥** |
| `mtg_incumbent_usd_per_mL` | **38.90** | 101Bio Col-Tgel 10mL $389.00 [E-120] — **동일 아키텍처 선행품 가격 앵커** |
| `china_local_organoid_usd_per_mL` | **21.30** | Yeasen Ceturegel 40192ES [E-125] — **중국 시장 가격 하한** |
| `raw_collagen_floor_usd_per_mL` | **5.40** | Advanced BioMatrix PureCol 3mg/mL 100mL [E-114] — **원료 가격 하한 앵커** |
| `corning_ls_revenue_2025_usdm` | **972** | Corning IR / 10-K FY2025 [E-127][E-128] |
| `corning_ls_net_income_2025_usdm` | **61** | 순이익률 6.28% [E-127][E-167] |
| `biotechne_protein_sciences_fy2025_usdm` | **870.2** | SEC 10-K FY2025 [E-129] |
| `matrigel_pubmed_citations` | **15004** | [E-149] |
| `defined_alternatives_pubmed_share` | **0.0195** | 292 / 15,004 [E-152] — **전환 장벽이 가격이 아님을 보여주는 핵심 지표** |
| `mtg_prior_commercial_exists` | **true** | 101Bio Col-Tgel [E-120][E-164] — **Agent F 는 이를 선행기술로 반드시 반영할 것** |
| `gmp_matrix_public_price_count` | **0** | 42개 제품 중 [E-160] — **미점유 구간** |
| `fx_usd_per_eur` / `fx_usd_per_gbp` | **1.1559 / 1.3498** | Fed H.10 week ending 2026-08-07 [E-146] |
| `fx_cny_per_usd` / `fx_jpy_per_usd` / `fx_krw_per_usd` | **6.7474 / 157.54 / 1409.94** | 동상 [E-146] |

---

## DoD 셀프 체크리스트

| # | 항목 | 판정 | 비고 |
|---|---|---|---|
| 1 | 25개 이상 제품 표 완성, 각 행에 evidence_id 와 price_source_url | **PASS** | **42개 제품**. 전 행 `evidence_id` + `price_source_url` 채움. 필수 커버리지(BME/합성/재조합/아시아/배지사 번들) 전 항목 포함 |
| 2 | 전 제품 USD/mL 환산 완료 (빈칸 0건) | **PASS** | 42행 × 18열 = 756셀 **빈칸 0건** (스크립트 검증). 추정 6건은 `추정:` 접두사 + 가정ID C-A4a~f |
| 3 | GMP grade 제품 별도 태깅 | **PASS** | `gmp_line_available` 컬럼으로 태깅. GMP **라인 보유** 4곳(Thermo CTS / BioLamina CTG / Nippi MG / ACRO GMP), **공개 정가 보유 0곳** [E-160]. RUO→GMP 배수 1.942 실측으로 asp_gmp 산출 [E-159] |
| 4 | 가격 프리미엄 정량 결론 (숫자) | **PASS** | `definition_premium_ratio = 1.253`, **단 Mann-Whitney p=0.168 로 통계적 유의성 없음** [E-161]. grade 배수 `1.942` [E-159]. 유통 마진 `35.9%` [E-162]. 소용량 프리미엄 +16~100% |
| 5 | mTG 기존 상용 제품 존재 여부 조사 완료 | **PASS** | **존재함** — 101Bio Col-Tgel, 콜라겐/젤라틴 + 트랜스글루타미나제 2액형, $38.90/mL, Fisher/AMSBIO/Gentaur 유통 [E-120]. 1차 문헌으로 가교 효소 확증 [E-164]. §7 에 차별화 약화 사실과 잔여 공간을 함께 기술 |
| 6 | data/price_table.csv + docs/C_competition.md 생성 | **PASS** | 두 파일 모두 생성. 부수 산출: `docs/C_plan.md`, `evidence/evidence_C.jsonl`(71건, E-100~E-170), `docs/assumptions.md` append(C-A0~C-A5) |
| 7 | 실제 WebSearch/WebFetch 40회 이상 | **PASS** | **약 140회** 수행 (검색 약 55회 + 페이지 fetch 약 85회). 전 가격은 실제 제품 페이지에서 확인, URL 날조 0건, 접근 실패 1건은 `access_status:"failed"` 로 기록 |
| 8 | R1 No-Deferral 준수 | **PASS** | "추후 조사/향후 과제/TBD/범위를 벗어남" 0건. 미공개 가격 6건은 전부 회귀 추정 + 가정 등록으로 종결. `gaps.md` 신규 등재 없음(4요소 충족 항목 없음) |
| 9 | R2 Evidence 준수 | **PASS** | 근거 ID 전량 E-100~E-170 범위 내, `verified_by` 전건 `""`, `access_date` 전건 2026-08-11, JSONL 파싱 검증 통과 |
| 10 | R5 Premise-Audit (사용자 전제 검증) | **PASS** | 전제 "defined 매트릭스는 프리미엄을 받는다" → **반증**(p=0.168). 전제 "mTG 가교가 차별화" → **부분 반증**(선행 상용품 존재). 두 건 모두 사업가설에 불리하나 그대로 보고 |
