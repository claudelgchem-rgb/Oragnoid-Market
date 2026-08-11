# Agent E — 원가·단위경제·수익성 작업계획

작성일: 2026-08-11 / 근거 ID 범위: **E-400 ~ E-499** / evidence 파일: `evidence/evidence_E.jsonl`

---

## 0. 이 작업의 판정 대상

LG화학 "재조합/정제 콜라겐 + mTG 효소가교 Defined Organoid Matrix"가
DECISION_GATE 의 **Gross Margin ≥ 0.60** 과 **Payback ≤ 5년**을 통과하는가.

선행 Wave 1 이 이미 확정한 제약조건(내가 임의로 바꾸지 않는다):

| 제약 | 값 | 출처 |
|---|---:|---|
| 동일 아키텍처 선행 상용품 가격 앵커 (101Bio Col-Tgel) | 38.90 USD/mL | C [E-120] |
| 중국 로컬 가격 하한 (Yeasen Ceturegel) | 21.30 USD/mL | C [E-125] |
| Matrigel 오가노이드 전용 SKU 직판 | 44.76 USD/mL | C [E-102] |
| defined 중앙값 | 60.47 USD/mL | C [E-161] |
| 정의성 프리미엄 통계적 유의성 | **없음 (p=0.168)** | C [E-161] |
| 유통 마크업 | 35.9% | C [E-162] |
| GMP 배수 (B·C 통합 권고) | 1.85× | B [E-077]+C [E-159] |
| 1차 등급 판정 | RUO (GMP 2029~) | B H2 |
| 라미닌 필수 문제 | 2024년까지 전 합성계가 외인성 라미닌 필요 | D [E-231] |
| 엔도톡신 목표 | ≤ 0.12 EU/mL | D [E-232] |
| 강성 커버리지 | 100 Pa ~ 34 kPa 을 SKU 3종 내 | D [E-260] |

**따라서 나의 ASP 설정 원칙**: "defined 라서 비싸게" 금지. Col-Tgel 38.90 을 RUO 상한 참조로 두고
그 아래에서 GM 60% 가 나오는지를 검증한다. 나오지 않으면 나오지 않는다고 쓴다.

---

## 1. 조사 쿼리 목록 (실제 WebSearch/WebFetch ≥ 40회)

### 1-A. 콜라겐 원료 단가 (동물유래 정제)
1. `Advanced BioMatrix PureCol bovine collagen 100 mL price catalog 5005`
2. `TeloCol-6 telocollagen 6 mg/mL price Advanced BioMatrix`
3. `Nippi collagen type I bulk price per gram medical grade`
4. `Collagen Solutions / Symatese / Kensey Nash bulk collagen USD per gram`
5. `pharmaceutical grade collagen powder bulk price USD/kg supplier`

### 1-B. 재조합 인간 콜라겐 단가
6. `CollPlant rhCollagen price per gram plant-derived recombinant collagen`
7. `Evonik VERAMER recombinant collagen price`
8. `Humabiologics human collagen type I price per mg`
9. `recombinant humanized collagen type III China supplier price USD/g (巨子生物 Giant Biogene / 锦波生物 Jinbo)`
10. `Jellagen jellyfish collagen price per mg`
11. `recombinant collagen single chain vs triple helix price difference`
12. `Sigma-Aldrich recombinant human collagen type I C7624 price`

### 1-C. mTG / 트랜스글루타미나제
13. `Ajinomoto Activa TG transglutaminase price USD per kg food grade`
14. `microbial transglutaminase bulk price per kg supplier alibaba/chemical`
15. `pharmaceutical grade transglutaminase GMP price per gram`
16. `Zedira / Sigma T5398 transglutaminase Streptomyces mobaraensis price unit`
17. `transglutaminase specific activity U/g collagen crosslinking concentration`

### 1-D. 재조합 라미닌 (COGS 결정 인자)
18. `BioLamina Biolaminin 521 LN521 price per 100 µg`
19. `Nippi iMatrix-511 price 350 µg catalog`
20. `Thermo rhLaminin-521 A29249 price`
21. `laminin-111 concentration µg/mL organoid crypt formation requirement literature`
22. `laminin 111 100 µg/mL PEG hydrogel intestinal organoid Gjorevski Lutolf`
23. `recombinant laminin production cost CHO expression yield`

### 1-E. 공정·발효·정제 원가
24. `recombinant protein E. coli / Pichia titer g/L fermentation cost of goods`
25. `downstream processing cost percentage total biomanufacturing 50-80%`
26. `CDMO microbial fermentation cost per batch 1000 L USD`
27. `recombinant collagen Pichia pastoris yield g/L literature`
28. `cost of goods recombinant protein USD per gram microbial fermentation`

### 1-F. QC 시험 단가 (실제 CRO 가격표)
29. `sterility testing USP 71 price per sample CRO`
30. `bacterial endotoxin test LAL USP 85 price per sample`
31. `mycoplasma testing PCR price per sample USP 63`
32. `SDS-PAGE purity HPLC assay price per sample contract lab`
33. `LC-MS protein identification service price per sample`
34. `rheology testing service price per sample G' G''`
35. `ICH stability study cost per timepoint USD`

### 1-G. 포장·콜드체인·충전
36. `2R/5 mL glass vial price per unit bulk pharmaceutical`
37. `sterile filtration 0.22 µm capsule filter price Millipore Sartorius`
38. `dry ice shipping cost per package biological reagent US`
39. `aseptic fill finish cost per vial CDMO small batch`

### 1-H. CAPEX / GMP 인증
40. `GMP cleanroom construction cost per square meter USD ISO 7`
41. `ISO 20399 / GMP certification cost timeline months biologics facility`
42. `pilot scale bioprocessing facility CAPEX USD 100 L`
43. `single-use bioreactor 200 L price USD`

### 1-I. Matrigel 원가 구조 (비교군)
44. `Matrigel EHS sarcoma mouse production cost per mL yield`
45. `Engelbreth-Holm-Swarm tumor mouse yield mL Matrigel per mouse`
46. `laboratory mouse cost per animal per diem housing USD`

---

## 2. 산출 순서

1. 원료 단가 실측 → BOM 표 (≥10 항목, 각 [E-4##])
2. 배합 설계 2안: **BOM-A (라미닌 무첨가)** / **BOM-B (라미닌 첨가)** — D [E-231] 리스크 대응
3. 공정원가(발효·정제·가교·충전) + QC 시험 단가 → 단위 변환(배치당 → mL당)
4. RUO vs GMP 원가 배수 산출
5. CAPEX (파일럿/상업) + FTE
6. 단위경제표 1/5/10 mL × ASP 시나리오
7. 규모의 경제 곡선 1/10/100/1000 L·년
8. `model/cogs_model.py` 작성 → **실행 검증** → `data/cogs_output.csv`
9. 민감도 6종
10. DoD 표 + HANDOFF

## 3. 산출물
- `docs/E_plan.md` (본 문서)
- `docs/E_cogs.md`
- `model/cogs_model.py`, `data/cogs_output.csv`
- `evidence/evidence_E.jsonl` (E-400~E-499)
- `docs/assumptions.md` **append** `## [E] ...` 섹션
