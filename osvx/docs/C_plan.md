# Agent C 작업계획 — 경쟁·공급자 랜드스케이프 & 가격 구조

작업 루트: `/home/user/Oragnoid-Market/osvx`
근거 ID 범위: **E-100 ~ E-199** / evidence 파일: `evidence/evidence_C.jsonl`
access_date 기본값: **2026-08-11**

---

## 1. 목적

오가노이드 배양 매트릭스(BME 대체재 포함) 시장의 **모든 상용 대안**을 훑어
실측 **USD/mL 가격표**를 구축하고, "정의성 프리미엄(definition premium)"이
가격에 실재하는지를 통계로 검증한다. 또한 LG화학 제품가설(재조합/정제 콜라겐 +
mTG 가교 defined matrix)의 차별화가 이미 상용화되어 있지 않은지(mTG 선행 상용품)
정직하게 확인한다.

## 2. 산출물

| 파일 | 내용 |
|---|---|
| `docs/C_plan.md` | 본 문서 |
| `data/price_table.csv` | 25개 이상 제품 × 18컬럼 실측 가격표 |
| `docs/C_competition.md` | 경쟁 분석 본문 + HANDOFF + DoD |
| `evidence/evidence_C.jsonl` | 근거 레코드(E-100~E-199) |
| `docs/assumptions.md` (append) | 추정 가격·환율 가정 |
| `docs/gaps.md` (append) | 4요소 충족 시에만 |

## 3. 조사 쿼리 목록 (실행 계획)

### 3.1 BME 계열 가격
1. `Corning Matrigel 354234 price 10 mL`
2. `Corning Matrigel 356234 5 mL price Fisher Scientific`
3. `Corning Matrigel Growth Factor Reduced 354230 / 356231 price`
4. `Corning Matrigel Matrix for Organoid Culture 356255 price`
5. `Cultrex BME Type 2 3532-005-02 / 3432-005-01 price Bio-Techne`
6. `Cultrex UltiMatrix RGF BME BME001-05 price`
7. `Geltrex LDEV-Free A1413201 A1413202 price Thermo Fisher`
8. `Sigma ECM Gel E1270 price Sigma-Aldrich`

### 3.2 Defined 합성/펩타이드/PEG
9. `QGel 3D matrix price organoid`
10. `Ectica Technologies 3DProSeed price`
11. `Cellendes 3-D Life PVA hydrogel price`
12. `Manchester BIOGEL PeptiGel PeptiMatrix price`
13. `3-D Matrix PuraMatrix 354250 price`
14. `Gelomics GelMA price`
15. `TheWell Bioscience VitroGel ORGANOID price`
16. `Advanced BioMatrix VitroGel / HyStem / PhotoCol price`
17. `Denovo Matrix screenMATRIX price`
18. `Stem Pharm hydrogel price`
19. `UPM Biomedicals GrowDex price`
20. `Sigma TrueGel3D price`
21. `Biogelx price`
22. `AMSBIO organoid matrix price`

### 3.3 재조합/정제 ECM 단백
23. `CollPlant rhCollagen price`
24. `Evonik VERAMER rhCollagen`
25. `Humabiologics human collagen price`
26. `Jellagen jellyfish collagen price`
27. `BioLamina Biolaminin 111 / 521 price`
28. `Nippi iMatrix-511 price`
29. `Thermo Vitronectin A14700 price`
30. `Corning Collagen I rat tail 354249 price`
31. `Advanced BioMatrix PureCol / TeloCol / Nutragen price`
32. `fibrin fibrinogen 3D culture matrix price`

### 3.4 아시아/로컬
33. `China organoid matrix gel supplier price` (Bioengine, K2 Oncology, Accegen, Yeasen 등)
34. `Korea organoid matrix supplier` (Cellartgen, Regenmedtech, MEDIFAB 등)
35. `Matrixome Laminin-511 E8 iMatrix price Japan`

### 3.5 배지사 번들 / 시장구조
36. `STEMCELL Technologies IntestiCult / organoid matrix price`
37. `Hubrecht Organoid Technology HUB license matrix`
38. `Corning 10-K Life Sciences segment sales SEC EDGAR`
39. `Bio-Techne 10-K segment revenue`
40. `Matrigel market share Corning`

### 3.6 자금조달·M&A (최근 3년)
41. `QGel funding round`
42. `Ectica Technologies funding Series A`
43. `Manchester BIOGEL investment funding`
44. `Denovo Matrix funding`
45. `CollPlant funding / stock`
46. `Humabiologics funding`
47. `TheWell Bioscience funding acquisition`
48. `Gelomics funding`

### 3.7 mTG 선행 상용품 (차별화 검증 — 최우선 정직성 항목)
49. `microbial transglutaminase crosslinked hydrogel cell culture commercial product`
50. `mTG gelatin hydrogel organoid matrix commercial`
51. `transglutaminase crosslinked collagen 3D culture kit`
52. `Ajinomoto Activa TG cell culture scaffold`

### 3.8 환율
53. `USD EUR exchange rate 2026-08` / `USD GBP` / `USD JPY` (출처 URL 필수)

## 4. 방법론

### 4.1 가격 정규화
- `usd_per_mL = list_price_usd / size_mL`
- 가루/동결건조 제품(펩타이드, 콜라겐 파우더 등)은 **제조사 권장 사용농도로 재구성한
  최종 gel 부피**를 size_mL로 삼고, 그 환산식을 assumptions.md에 기록한다.
- 2-part 키트(예: HyStem, VitroGel + diluent)는 **최종 gel 부피** 기준.
- 통화 환산: EUR/GBP/JPY → USD, 환율 출처 URL 필수 기재.

### 4.2 "Request a quote" 대응 순서
1. 제조사 e-commerce 페이지
2. 유통사 교차검색: Fisher Scientific, VWR/Avantor, Sigma-Aldrich, Bio-Techne 직판,
   Biocompare, Krackeler, Labshake, Stellar Scientific, Cole-Parmer, Genesee
3. 그래도 없으면 **동급 제품 회귀 추정** → 셀에 `추정:` 접두사 + assumptions.md 기재
- **빈칸 0건**이 DoD 조건.

### 4.3 정의성 프리미엄 검증 (통계)
- definition_level(undefined-BME / semi-defined / fully-defined)별로
  USD/mL 의 min / Q1 / median / Q3 / max 산출.
- 중앙값 비 `definition_premium_ratio = median(fully-defined) / median(undefined-BME)`.
- **비율이 1 이하로 나오면 "프리미엄 없음"으로 그대로 보고한다.**
  사업 가설에 불리해도 수치를 왜곡하지 않는다 (R5 Premise-Audit).

### 4.4 grade 배수
- 동일 제조사·동일 소재의 RUO 대 GMP 쌍(paired)을 우선 사용,
  쌍이 부족하면 전체 GMP 중앙값 / 전체 RUO 중앙값.

### 4.5 유통 마진 역산
- `distributor_markup_pct = (유통사가 − 제조사 직판가) / 제조사 직판가 × 100`
- 동일 Cat# 를 제조사·유통사 양쪽에서 확인 가능한 케이스만 사용, 최소 3쌍 이상.

## 5. 자기검증(DoD) 항목

1. 25개 이상 제품 행, 각 행에 `evidence_id` + `price_source_url`
2. `usd_per_mL` 빈칸 0건
3. GMP grade 별도 태깅
4. 가격 프리미엄 정량 결론(숫자)
5. mTG 기존 상용 제품 존재 여부 조사 완료(있으면 있다고 보고)
6. `data/price_table.csv` + `docs/C_competition.md` 생성

## 6. R1 준수 선언

본 작업에서 "추후 조사", "TBD", 사유 없는 "N/A"는 사용하지 않는다.
값이 확보되지 않으면 회귀·유사제품 기반 추정치를 산출하고
`추정:` 접두사와 함께 assumptions.md에 가정ID를 남긴다.
