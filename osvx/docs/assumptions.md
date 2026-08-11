# OSVX 가정 목록 (assumptions.md)

각 에이전트가 append 한다. 형식: `| 가정ID | 가정값 | 근거 | 민감도 영향 |`


## [C] 경쟁·가격 (Agent C) — 가격표 산출 가정

기준: `data/price_table.csv` / 근거 `evidence/evidence_C.jsonl` (E-100~E-199) / access_date 2026-08-11

### C-A0. 환율 (전 통화 공통)
| 가정ID | 가정값 | 근거 | 민감도 영향 |
|---|---|---|---|
| C-A0 | USD/EUR 1.1559 (USD per EUR), USD/GBP 1.3498 (USD per GBP), CNY 6.7474/USD, JPY 157.54/USD, KRW 1,409.94/USD — 모두 주간 평균, week ending 2026-08-07 | Federal Reserve H.10 Foreign Exchange Rates, https://www.federalreserve.gov/releases/h10/current/ [E-146] | EUR 표시 제품 3건(GrowDex, VitroGel ORGANOID 2mL, Cellendes 원가) · CNY 1건(Beyotime). 환율 ±5% → 해당 제품 USD/mL ±5%, 전체 중앙값 영향 <1% (표본 4/33) |

### C-A1. USD/mL 정규화 기준
| 가정ID | 가정값 | 근거 | 민감도 영향 |
|---|---|---|---|
| C-A1 | `usd_per_mL = list_price_usd / size_mL`, 여기서 size_mL 은 **구매 시 공급되는 원액/키트 최종 겔 부피**(as-supplied basis)로 통일. 사용 시 희석배수는 반영하지 않음 | 제품별 희석 프로토콜이 세포주·용도별로 달라 정규화 불가. as-supplied 기준이 카탈로그에서 직접 검증 가능한 유일한 공통 분모 | BME 는 원액을 그대로 쓰므로 영향 없음. 합성 겔 중 일부(VitroGel)는 1:1 희석 후 사용 → 실사용 기준 USD/mL 은 표 값의 약 1/2. 정의성 프리미엄 비율은 이 효과가 defined 쪽에만 작용하므로 **프리미엄을 과대평가하는 방향**. 본문에서 3D 겔 한정 분석으로 보정 |
| C-A1b | 코팅 전용 시약(라미닌, 비트로넥틴)은 3D 매트릭스가 아니므로 정의성 프리미엄 통계 본 계산에서 **제외**하고 별도 표기 | 2D 코팅(µg/cm² 기준)과 3D 포매(mL 기준)는 단위 경제가 다름 | 미제외 시 fully-defined 중앙값이 라미닌 고가($81~840/mL)에 끌려 상향 왜곡됨. 제외가 보수적(가설에 불리한) 처리 |

### C-A2. 질량 표기 제품의 부피 환산
| 가정ID | 가정값 | 근거 | 민감도 영향 |
|---|---|---|---|
| C-A2a | Corning Collagen I rat tail 354249 (100 mg): 농도 8-11 mg/mL 의 중간값 9.5 mg/mL 적용 → 10.53 mL | Corning 제품 페이지 명기 농도 범위 [E-110] | 하한 8 mg/mL 적용 시 12.5 mL($16.42/mL), 상한 11 적용 시 9.09 mL($22.58/mL). ±16% |
| C-A2b | Laminin-521 계열 원액 농도는 업계 표준 **0.1 mg/mL** 로 통일 적용 (Gibco A29248 제품 슬러그 'fg-rh-laminin-521-0-1-mg-ml' 로 직접 확인, BioLamina LN521 제품 개요도 0.1 mg/mL 명기) | Fisher Scientific A29248 URL 및 Bio-Connect LN521 페이지 [E-147] | Gibco A29249 1 mg → 10 mL. Corning 354221 100 µg → 1 mL. 농도 2배 오차 시 해당 2행 USD/mL 2배 변동, 단 코팅시약이라 본 통계에서 제외되므로 결론 영향 0 |
| C-A2c | iMatrix-511 350 µg = 175 µg × 2 vial, 0.5 mg/mL → 0.7 mL | Reprocell 제품 카탈로그의 '175 μg x 2 vials, 0.5 mg/mL in PBS' 표기 [E-117] | 코팅시약으로 본 통계 제외 |

### C-A3. 키트형 제품의 최종 겔 부피
| 가정ID | 가정값 | 근거 | 민감도 영향 |
|---|---|---|---|
| C-A3a | Cellendes 3-D Life 하이드로겔 키트 1개 = 최종 겔 **2.0 mL** (soft 기준) | Cellendes 제품 데이터시트/브로슈어: 'A standard kit allows formation of up to 2 ml 3-D Life Hydrogel depending on the stiffness of the gel (2 ml at soft, 1 ml at medium)' [E-148] | medium stiffness(1 mL) 적용 시 해당 3행 USD/mL 2배. fully-defined 중앙값 상향 → 정의성 프리미엄 **과대** 방향이므로 2.0 mL(보수적) 채택 |
| C-A3b | Sigma TrueGel3D 키트 1개 = 최종 겔 **2.0 mL** (추정) | 제조사가 겔 수율을 공개하지 않음(제품페이지·기술문서·TRUE1 프로토콜 3개 소스 확인, 모두 미기재). 동급 PEG/덱스트란 2액형 연구용 키트인 Cellendes(2.0 mL, C-A3a)로부터 유추 | ±50% 오차 시 해당 1행 USD/mL $115.69~$347.08. 표본 33개 중 1개로 중앙값 영향 미미 |
| C-A3c | Gelomics LunaGel Ultrapure GelMA High Stiffness 키트 = 최종 겔 **7.5 mL** | Gelomics 제품 사양: 'high stiffness kit contains enough LunaGel to create a total volume of 7.5mL hydrogel' [E-143] | 실측값이므로 가정 아님(기록 목적) |
| C-A3d | denovoMATRIX screenMATRIX (5 × 96-well 프리코팅 플레이트) 의 매트릭스 등가 부피 = 5 × 96 × 50 µL = **24.0 mL** (수동 코팅 시 96-well 당 표준 코팅액 50 µL 기준) | 96-well 코팅 표준 작업량. 프리코팅 제품이라 실제 겔 부피는 존재하지 않으므로 '수동 코팅 대체 시 필요한 작업용액 부피'로 등가 환산 | 코팅액 30~100 µL/well 범위 적용 시 $12.50~$41.67/mL. fully-defined 하위값이라 중앙값 영향 제한적 |
| C-A3e | Ectica 3DProSeed 96-well 플레이트 1매의 프리캐스트 하이드로겔 부피 = 96 × 10 µL = **0.96 mL** | 96-well 글래스바텀 이미징 플레이트의 프리캐스트 3D 겔은 통상 well 당 10 µL 수준. 제조사가 well 당 겔 부피를 비공개(제품페이지 확인, 'Contact us' 안내) | 5~20 µL/well 범위 시 0.48~1.92 mL/plate → USD/mL 2배 변동 |

### C-A4. 가격 미공개(Request a quote) 제품의 회귀 추정
공통 규칙: 동일 카테고리·동일 제품 아키텍처의 실측 USD/mL 을 기준선으로 삼고, 제품 포지셔닝 배수를 적용. 해당 셀에 `추정:` 접두사 표기.

| 가정ID | 대상 | 추정값 | 회귀 근거 | 민감도 영향 |
|---|---|---|---|---|
| C-A4a | Manchester BIOGEL PeptiGel Alpha 5 mL | 추정 $275.00 (= $55.00/mL × 5 mL) | 자가조립 펩타이드 하이드로겔 실측 comparable 2건의 평균: Corning PuraMatrix $62.72/mL [E-122], Corning Synthegel 3D hiPSC $37.08/mL + Spheroid $43.26/mL [E-130][E-131] → 평균 $47.69/mL. 영국 소규모 제조사 프리미엄 +15% 적용 → $54.84 ≈ $55.00/mL | ±40% 시 $33~$77/mL. fully-defined 중앙값 부근이라 중앙값 이동 거의 없음 |
| C-A4b | Biogelx-S (펩타이드, 동결건조 분말, 5 mL 겔 환산) | 추정 $275.00 (= $55.00/mL × 5 mL) | C-A4a 와 동일 아키텍처(합성 펩타이드 하이드로겔)로 동일 기준선 적용 | 동상 |
| C-A4c | QGel CN99 (5 mL) | 추정 $335.70 (= $67.14/mL × 5 mL) | Corning Matrigel for Organoid Culture $44.76/mL [E-102] 대비 1.5배. 근거: QGel 은 pharma 대상 fully-defined 오가노이드 전용 매트릭스로 BME 오가노이드 전용 라인 상위 포지셔닝. 1.5배는 Corning 자사 내 일반 Matrigel($30.29) → 오가노이드 전용($44.76) 상승폭 1.478배를 그대로 한 단계 더 적용한 것 | ±50% 시 $33.6~$100.7/mL |
| C-A4d | Jellagen JellaGel 10 mL 키트 | 추정 $389.00 (= $38.90/mL × 10 mL) | 동일 제품 아키텍처(콜라겐 용액 + 버퍼 + 가교제 2~3액형 키트)의 유일한 실측 comparable 인 101Bio Col-Tgel 10 mL $389.00 [E-120] 을 1:1 적용 | ±40% 시 $23~$54/mL |
| C-A4e | BioLamina Biolaminin 521 LN (LN521-02, 0.1 mg = 1 mL) | 추정 $118.00 (= $118.00/mL × 1 mL) | 동일 단백(재조합 인간 laminin-521) 실측 2건: Gibco A29249 $114.97/mL [E-116], Corning 354221 $81.01/mL [E-144]. 평균 $97.99 × 1.2 (BioLamina 는 laminin-521 원천 개발사·프리미엄 포지션) = $117.59 ≈ $118.00 | 코팅시약으로 본 통계 제외 → 결론 영향 0 |
| C-A4f | Ectica 3DProSeed ECT-PS1 플레이트 1매 정가 | 추정 $204.00/plate (= $212.50/mL × 0.96 mL) | 실측 eBay 2차유통가 $273.80/9매($30.42/매) [E-113] 는 재고처분가로 정가 대용 불가. 대신 동일 포맷 comparable 인 denovoMATRIX screenMATRIX $600/5매 = $120/매 [E-124] 에, Ectica 가 추가로 갖는 (i) 프리캐스트 3D 합성 하이드로겔 (ii) 180 µm 글래스바텀 이미징 사양 프리미엄 1.7배 적용 → $204/매 | ±50% 시 $106~$319/mL. fully-defined 최상위 구간이라 중앙값 영향 없음(Q3 이상) |

### C-A5. 시장 점유율 추정 (top3_share_estimate)
| 가정ID | 가정값 | 근거 | 민감도 영향 |
|---|---|---|---|
| C-A5 | BME 3사(Corning Matrigel / Bio-Techne Cultrex / Thermo Geltrex)의 오가노이드·3D배양 매트릭스 시장 합산 점유율 = **78%** (Corning 58% / Bio-Techne 12% / Thermo 8%) | PubMed 인용 실측 [E-149~E-152]: Matrigel 15,004건 vs Geltrex 104건 vs Cultrex 53건 → 인용 점유율 Matrigel 98.97%. 인용은 신제품에 후행하고 Matrigel 이 총칭어로 오용되므로 인용 점유율을 그대로 쓰면 과대. 매출 기반 보정: Corning Life Sciences 2025 매출 $972M [E-127], Bio-Techne Protein Sciences $870.2M [E-129] 중 BME 비중 차이를 반영해 Corning 58%로 하향, Cultrex 는 UltiMatrix 출시 후 조직적 프로모션 반영해 12%로 상향 | 3사 합산 70~85% 범위. 하한 70% 적용 시에도 '과점' 결론 불변. Corning 단독 점유율은 50~65% 범위 |
