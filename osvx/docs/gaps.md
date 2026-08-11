# OSVX 미해결 갭 (gaps.md)

"확정 불가" 선언은 4요소(① 검색 쿼리 5개+ ② 확인 소스 8개+ ③ 부재 판단 ④ 대체 추정치+오차범위)를 모두 갖춰야 유효하다.


## [D] 미해결 갭 (Agent D, 2026-08-11)

### GAP-D-01 — "Nature / Nature Methods 재현성 특집 중 Matrigel을 명시 지목한 에디토리얼"의 특정 실패

① **시도한 검색 쿼리 (6개)**
1. `Nature Methods editorial organoid reproducibility Matrigel standardization "batch-to-batch" 2023 2024`
2. `Nature Protocols organoid protocol "test several batches" OR "pre-test" OR "same batch of Matrigel" troubleshooting`
3. `Matrigel batch-to-batch variability proteomic analysis lot`
4. `Matrigel lot-to-lot variation organoid forming efficiency coefficient of variation`
5. `"use the same Matrigel batch throughout the experiment to avoid batch-to-batch variation" brain organoid protocol`
6. `ISSCR 2025 abstract Matrigel-free defined matrix organoid adoption survey researchers percentage using Matrigel`

② **확인한 소스 (9개)**
`nature.com/articles/s41578-020-0199-8` (IdP 리다이렉트로 접근 실패) · `nature.com/articles/s43586-022-00174-y` · `nature.com/articles/s44385-025-00054-6` · `stemcell.com/nature-research-roundtable-organoid-applications` · `sciencedirect.com/science/article/pii/S2213671124001140` (403) · `frontiersin.org/.../fncel.2024.1351734/full` (접근 성공) · `pmc.ncbi.nlm.nih.gov/articles/PMC12713094/` (접근 성공) · `cell.com/star-protocols/fulltext/S2666-1667(26)00299-6` (403) · `academic.oup.com/rb/article/doi/10.1093/rb/rbaf038/8131465`

③ **왜 존재하지 않는다고 판단하는가**
Matrigel 로트 편차는 **에디토리얼 수준의 논쟁 사안이 아니라 방법론 논문 본문에서 상시 언급되는 기정사실**로 취급되고 있다. Nature Reviews Materials의 *Synthetic alternatives to Matrigel* (2020, s41578-020-0199-8)이 이 주제의 사실상 표준 참조 문헌이나, 이는 리뷰 논문이지 재현성 특집 에디토리얼이 아니다. 검색 인덱스에서 Nature 계열 재현성 특집이 Matrigel을 **표제로 지목한** 사례는 확인되지 않았다.

④ **대체 추정치 + 오차범위**
'권위 있는 저널의 Matrigel 지목'이라는 정성적 자산은 다음 3건으로 **충분히 대체 가능**하며 오히려 실무 구속력이 더 강하다:
- STAR Protocols(Cell Press) 2편의 동일 로트/배치 사용 **명령형 지시** [E-211][E-212]
- Tuveson Lab(CSHL) 공식 프로토콜의 *"Individual lots need to be tested"* + 9.4~9.9 mg/mL 창 [E-209]
- Frontiers Cell Neurosci 2024 리뷰의 *"...resulted in a higher variability and lower reproducibility"* [E-217]
이 대체 근거군의 정성적 설득력은 에디토리얼 1건 대비 **동등 이상**(오차범위: 마케팅 인용가치 −20% ~ +10%)으로 평가한다. **후속 조사 불필요 — 본 갭은 산출물에 영향을 주지 않는다.**

### GAP-D-02 — Matrigel 2개 로트 MS 비교 "배치 간 단백질 동정 유사도 53%"의 1차 출처 미확인
검색 요약 단계에서 제시된 수치이나, 지목된 후보 문헌(Wolff & Hendrix 2025, PMC12713094)을 직접 fetch하여 확인한 결과 **해당 수치가 본문에 없음**을 검증했다(별도 쿼리 `"53%" batch-to-batch similarity Matrigel protein identification mass spectrometry two lots` 재검색에서도 1차 출처 미발견). **URL 날조를 피하기 위해 본 수치는 evidence 및 본문에서 전면 배제**했다. 대체 근거: 조성 편차는 프로테옴 종수 [E-200][E-201], 단백질 농도 스펙 폭 [E-203], 강성 편차 [E-205]로 정량화했으며 결론에 영향 없음.

## [B] 미해결 갭 (Agent B, 2026-08-11)

### GAP-B-01. 중국 NMPA의 오가노이드 전용 기술지도원칙 부재 확인
- ① 시도 검색 쿼리(5개 이상): `NMPA China organoid guideline 2024 2025 技术指导原则 类器官 drug evaluation CDE` / `China CDE organoid technical guideline` / `NMPA 类器官 指导原则` / `China cell therapy products guidance 2025 NMPA` / `NMPA stem cell products CMC guidance 2024`
- ② 확인 소스(8개 이상): CCFDIE(중국식품약품국제교류중심) 영문 공고 [E-044], Pacific Bridge Medical China Pharma Regulation Update 2024-2025, Cisema NMPA 세포치료제 변경관리 draft, Cisema NMPA 임상평가 가이드라인, ClinRegs(NIH) China country page, IntuitionLabs China NMPA Drug Approval Pathways, Vision Life Sciences NMPA 가이드, NMPA/CDE 관련 2차보도 다수
- ③ 부재 판단: NMPA/CDE는 2024-12 인간줄기세포제품 CMC 지침(Trial), 2025-07 세포치료제 변경관리 draft를 공표했으나 **오가노이드를 대상으로 하는 별도 기술지도원칙은 영문·중문 검색 모두에서 확인되지 않았다.** 중국은 오가노이드를 세포치료·줄기세포 지침의 하위로 다루고 있을 가능성이 높다.
- ④ 대체 추정치 + 오차범위: 중국의 오가노이드 전용 지침 공표 시점을 **2028년 ± 2년**으로 추정. 근거: 중국은 통상 FDA/EMA 프레임워크를 2~4년 시차로 추종하며, FDA의 NAM 검증 프레임워크 확정이 2026-03 [E-014]이므로 +2~4년. 사업 영향: 중국 시장 진입 논리는 규제 pull이 아니라 연구비·CRO 수요 pull로 설계해야 한다(Agent G).

### GAP-B-02. NIH ORIVA 전용 예산 규모 미공개
- ① 시도 검색 쿼리: `NIH Office of Research Innovation Validation and Application ORIVA 2025 budget non-animal methods` / `ORIVA budget appropriation` / `NIH non-animal methods funding FY2026` / `NIH ODSPI budget NAM` / `NIH animal research reduction initiative funding amount`
- ② 확인 소스: FASEB Washington Update [E-027], Americans for Medical Progress, FierceBiotech, Science(AAAS), Reprocell blog, UVA Office of Sponsored Programs, Latham & Watkins client alert, NIH 보도자료(403으로 직접 접근 실패)
- ③ 부재 판단: 복수 소스가 **"NIH did not share how much money the ORIVA will receive"** 로 일치 기술. 예산 미공개는 사실이며, 이는 조직 신설의 실행력 불확실성을 의미한다.
- ④ 대체 추정치 + 오차범위: ORIVA 직접 예산을 **연 2,000만 ~ 1억 USD**로 추정(오차 5배). 근거: 확인 가능한 인접 지출인 SOM Center 8,700만 USD/3년 = 연 2,900만 USD [E-026]가 단일 센터 규모이므로, 조정 사무국 예산은 그 이하~수배 범위. 사업 영향: nam_ramp conservative 시나리오는 ORIVA 예산 미확보를 전제로 한다.

### GAP-B-03. USP `<1043>` 현행판(2026) 원문 미확보
- ① 시도 검색 쿼리: `USP General Chapter <1043> Ancillary Materials tier 1 2 3 4 qualification` / `USP 1043 current version text` / `USP-NF 1043 ancillary materials 2026` / `USP 1043 tier definitions endotoxin` / `USP standards cell gene therapy ancillary material`
- ② 확인 소스: doi.usp.org 공식 페이지(프리뷰만, 구독 필요), drugfuture USP32-NF27 아카이브 [E-046][E-047], pharmacopeia.cn USP29 아카이브, USP 공식 발표자료 PDF 2건, ASGCT 포스터, STEMCELL 기술보고서 [E-061], BioProcess International 기사, Burger SR 자료
- ③ 부재 판단: 현행 USP-NF는 유료 구독 전용이며 무료 접근 가능한 것은 USP29/USP32 아카이브판이다. Tier 1~4 체계와 5개 qualification 영역은 아카이브판과 복수 2차 문헌이 일치하므로 **구조는 변경되지 않은 것으로 판단**되나, 현행판의 세부 수치 규격은 확인하지 못했다.
- ④ 대체 추정치 + 오차범위: Tier 체계·qualification 5영역은 아카이브판 그대로 사용(신뢰도 상). 현행판에서 추가되었을 가능성이 있는 구체 수치 규격(엔도톡신·잔류물 한도)은 **미확인**이며, 대신 Ph. Eur. 5.2.12 [E-053][E-054]와 시장 실측 벤치마크 [E-070][E-073]로 대체했다. 사업 영향: 제품 규격 확정 전 USP-NF 구독 확보 필요(실행 액션, Agent G).

### GAP-B-04. BioLamina 등 매트릭스형 원부자재의 RUO vs 임상등급 공개 가격 부재
- ① 시도 검색 쿼리: `"Biolaminin 521 CTG" price OR "CT521" price catalog` / `BioLamina laminin-521 GMP grade price LN521 comparison` / `Advanced BioMatrix collagen GMP grade price vs research grade` / `recombinant human albumin GMP grade price Recombumin vs research grade` / `Miltenyi MACS GMP cytokine price vs premium grade`
- ② 확인 소스: biolamina.com 제품 페이지 [E-075], Fisher Scientific BioLamina 리스팅, Alpha Labs, Bio-Connect, Sartorius shop(Recombumin Elite/Prime, 가격 로그인 필요), Advanced BioMatrix PureCol 페이지, Corning eCatalog, Sigma-Aldrich, R&D Systems(가격 동적 로딩)
- ③ 부재 판단: **매트릭스·ECM 카테고리의 임상등급 가격은 업계 관행상 문의(quote) 기준이며 공개되지 않는다.** 반면 재조합 사이토카인은 공개된다. 이 비대칭 자체가 매트릭스 카테고리의 가격 불투명성을 시사한다.
- ④ 대체 추정치 + 오차범위: 재조합 단백질 매칭 4쌍의 중앙값 **1.75×** [E-077]를 매트릭스 카테고리에도 1차 앵커로 적용하되, 오차범위를 **1.3~3.0×** 로 확대한다(상방 확대 이유: 매트릭스는 RUO 기준선이 BME=Tier 4[E-046]이므로 등급 격차가 더 크고, 가격 불투명성이 공급자 가격결정력을 높인다). Agent C가 BME 대비 실판매가로 재검증할 것.

## [A] 미해결 갭 (Agent A, 2026-08-11)

### GAP-A-01 — 경로1(Bottom-up) 대 경로2(Top-down) 편차 5.35배 (R4 삼각측량 2배 초과 → 원인 분석 의무)

**편차 실측**: 경로1 = 42.97 M USD [E-334] / 경로2 = 230.1 M USD [E-336] → **5.35배**
(bear 6.00배 / bull 4.85배 — 시나리오 무관하게 2배를 초과)

① **시도한 검색 쿼리 (7개)**
1. `Grand View Research organoids market size 2024 2030 CAGR report`
2. `"3D cell culture market" size 2025 2030 MarketsandMarkets scaffold based hydrogel segment`
3. `Mordor Intelligence organoids market size 2025 2030 report scope segmentation`
4. `Precedence Research organoids market size 2025 2034 USD billion`
5. `"basement membrane extract" market size report 2024 2032 Matrigel market USD million`
6. `Matrigel market "K Units" OR "volume" sales quantity global 2024 QYResearch consumption`
7. `"organoid culture medium market" 2024 USD billion size report scope reagents`

② **확인한 소스 (9개 보고서)**
Grand View Research Human Organoids [E-312] · Grand View Research Organoids & Spheroids [E-313] · Mordor Intelligence Organoids [E-314] · Fortune Business Insights Human Organoids [E-315] · MarketsandMarkets 3D Cell Culture [E-316] · Precedence Research 3D Cell Culture [E-317] · QYResearch Matrigel [E-318] · MarketsandMarkets Human Organoids [E-319] · WiseGuy Organoid Culture Medium [E-337]
(추가 접근 실패 5건: GVR 제품페이지 2건 403, statsmarketresearch 403, openpr 403, Tracxn 403 — 전건 검색 인덱스 요약으로 교차 확인)

③ **편차의 원인 판단 — 4가지, 전부 정량 확인됨**

**(원인 1) 스코프 오염 — 지배적 원인.** 오가노이드 시장 보고서는 (i) 오가노이드 모델·세포주 판매, (ii) CRO 서비스 매출, (iii) 배지·보충제, (iv) 장비·이미징, (v) 매트릭스를 모두 합산한다. Grand View 는 2024년 organoid models 세그먼트가 단독 **51.21%** 라고 명시한다 [E-312]. 즉 절반 이상이 매트릭스와 무관한 항목이다. 매트릭스 비중을 0.195 로 가정(A-A22)해도 남는 오염이 크다.

**(원인 2) 논리적 불가능 — 결정적.** 경로2 결과 230.1 M USD 는 **모든 용도를 합친 3D 매트릭스 시장 총액 117.2 M USD** [E-335]의 **1.96배**다. 오가노이드용 매트릭스 지출이 오가노이드 + invasion assay + xenograft 동시주입 + 2D 코팅을 전부 합친 매트릭스 지출보다 클 수 없다. 이는 가정 조정으로 해소되지 않는 **구조적 모순**이며, 경로2 기각의 단독 충분 사유다.

**(원인 3) 보고서 상호 비정합.** 동일 카테고리·동일 연도에 대해 벤더 간 값이 갈린다.
- `3D cell culture market` 2025: MarketsandMarkets 1.29 B USD [E-316] vs Precedence 2.12 B USD [E-317] → **1.64배**
- `human organoids market` 2025: Grand View 987 M(역산) [E-312] vs MarketsandMarkets 1,352 M(역산) [E-319] → **1.37배**
- 배지 시장 660 M USD [E-337] vs 매트릭스 카테고리 97 M USD [E-318] → 6.8배라는 주장인데, 랩 단위 실측(배지 약 5,000 USD/년 vs 매트릭스 6,271 USD/년 = 0.80배)과 정면 배치.
서로를 검증하지 못하는 소스군이므로 중앙값을 취해도 신뢰도가 회복되지 않는다.

**(원인 4) 물량 지표 부재 → 검증 불가.** 9개 보고서 중 물량 단위(L 또는 K Units)를 명시한 것은 QYResearch Matrigel **1개뿐**이다 [E-318]. 나머지 8개는 금액 단독이므로 `금액 = 물량 × 단가` 항등식으로 자기 검증할 수 없다. 본 임무 규정("금액만 있는 시장보고서 인용은 부적합 처리")을 그대로 적용한다.

**대조 — 편차가 없는 쪽**: 동일 스코프(학술 세그먼트)로 맞추면 경로1 25.34 M USD vs 경로3 32.82 M USD 로 **1.30배**이며 2배 이내다 [E-341]. 즉 문제는 방법론이 아니라 **경로2 소스의 정의 문제**다.

④ **채택 결정 + 대체 추정치 + 오차범위**
- **채택: 경로1 (Bottom-up) 을 주 경로로, 경로3 (Proxy) 을 검증용으로 사용한다. 경로2 는 기각한다.**
- 채택값 TAM 2025 = **42.97 M USD / 1,178.7 L** [E-334]
- 오차범위: 시나리오 밴드 **38.37 ~ 47.40 M USD** (±10.5%), 최대 민감 인자(소모량 계수 A-A10/A-A11) ±50% 반영 시 **21.5 ~ 64.5 M USD**
- 경로2 를 굳이 상한으로 쓴다면 그 값은 "오가노이드 매트릭스"가 아니라 **"오가노이드 관련 소모품·서비스 전체"** 로 재라벨해야 하며, 그 경우 매트릭스 사업의 TAM 이 아니라 **제품 확장 시의 잠재 TAM** 으로만 유효하다. → Agent S(통합)·Agent G(GTM) 에 이관: 제품 정의를 매트릭스 단품에서 "매트릭스 + 배지 + 오가노이드 키트"로 확장할 경우의 TAM 상한 참조값.

---

### GAP-A-02 — Agent B `clinical_timing_year` 의 매출 임계 정의(연 5 M USD)와 본 모델 GMP 매출의 불일치

**불일치 실측**: Agent B 는 clinical_timing_year 를 "이식용/재생의료 원부자재 매출이 **단일 공급자 기준 연 5 M USD 이상**이 되는 최초 연도 = 2033" 로 정의했다 [E-079]. 본 모델의 GMP 세그먼트 TAM 은 **시장 전체** 기준으로 2033년 **1.44 M USD**, 2035년 **2.51 M USD** 다. 단일 공급자 기준으로는 base LG 점유율 25% 적용 시 2035년 **0.63 M USD** — B 의 임계값의 **12.6%**.

① **시도한 검색 쿼리 (6개)**
1. `cell and gene therapy clinical trials number active 2025 ATMP ongoing worldwide ARM sector report`
2. `organoid transplantation clinical trial 2026 phase 2 number of patients`
3. `HUB Organoids license academic institutions number worldwide organoid technology license Hubrecht`
4. `Human Cancer Models Initiative HCMI number of organoid models 2025 biobank patient-derived cancer models count`
5. ClinicalTrials.gov API `query.term=organoid transplantation` / `query.intr=organoid` / `AREA[StudyType]INTERVENTIONAL`
6. `patient-derived organoid drug sensitivity testing clinical laboratory CLIA commercial test 2025`

② **확인한 소스 (8개)**
ClinicalTrials.gov API v2 [E-308] · ASGCT/Citeline Landscape Report 2025 Q3 [E-328] · NCI HCMI / Nature compendium [E-327] · SEngine PARIS CLIA (JCO abstract) [E-333] · Agent B 의 [E-066][E-067][E-079] · Agent B `docs/premise_audit.md` P4 · CGT Catapult UK 2025 데이터 · Fortune/Mordor 재생의료 세그먼트 기술

③ **불일치의 원인 판단**
Agent B 의 5 M USD 는 **임계값(threshold)이지 추정치(estimate)가 아니다.** B 문서 H4 는 산출식을 "Phase 2 개시 2026-01 + Phase2 3년 + Phase3 3년 + 심사 1년 = 2033" 으로 제시하며, **연도는 도출하되 금액은 도출하지 않았다.** 즉 5 M USD 는 "유의미"의 정성 기준으로 설정된 값이다. 반면 본 모델은 임상시험 건수 × 시험당 소모량 × 단가로 상향식 산출했다. 두 값은 같은 종류의 수치가 아니므로 **모순이 아니라 정의 차이**다. 다만 후행 에이전트가 5 M USD 를 매출 예측으로 오독할 위험이 있어 여기에 명시적으로 기록한다.

④ **대체 추정치 + 오차범위 (본 에이전트 채택값)**
- **GMP 세그먼트 시장 전체 TAM**: 2030 **0.50 M USD / 5.1 L**, 2033 **1.44 M USD**, 2035 **2.51 M USD / 28.5 L**
- 오차범위: bear 2035 **0.53 M USD** ~ bull 2035 **8.82 M USD** (16.6배 폭 — 시험 수 성장률 가정 A-A17 이 지배)
- LG 단일 공급자 기준 2035 = 2.51 × 0.25 = **0.63 M USD** (bull 8.82 × 0.40 = 3.53 M USD)
- **판정: GMP 트랙은 2035년까지도 단일 공급자 연 5 M USD 에 도달하지 않는다.** 근거의 강도: CGT/ATMP 진행 임상 1,905건 중 오가노이드 이식은 4건(0.21%) [E-328][E-067]이며, 2035년까지 143건(35.7배 증가)을 가정해도 매트릭스 매출은 2.51 M USD 다. clinical_timing_year 2033 이라는 **연도**는 그대로 채택하되, **금액 임계 5 M USD 는 채택하지 않는다.**
- Agent E(원가)·Agent S(통합)에 대한 지시: GMP 라인 CAPEX 의 회수 근거를 **GMP 제품 매출**에 두면 payback 이 성립하지 않는다. 정당화 근거는 (i) RUO 제품의 품질 서사, (ii) Type II DMF 라는 영업 자산 (Agent B [E-058]), (iii) 고객 qualification 부담 이전 이어야 한다.

---

### GAP-A-03 — Matrigel/BME 카테고리의 절대 물량(리터) 공표치 미확보

**미확보 대상**: QYResearch Matrigel 보고서는 물량 단위를 `Unit: Liters (L)`, 가격 단위를 `US$/ml` 로 명시하지만 [E-318], **집계 물량 절대값은 유료 구간**이라 확보하지 못했다.

① **시도한 검색 쿼리 (5개)**
1. `Matrigel market "K Units" OR "volume" sales quantity global 2024 QYResearch consumption`
2. `Corning Matrigel production capacity liters per year manufacturing mice EHS tumor supply expansion`
3. `"basement membrane extract" market size report 2024 2032 Matrigel market USD million`
4. `organoid laboratory annual Matrigel consumption cost per year budget "10 mL" bottles reagent spending`
5. `Matrigel Gel Cell Culture Medium Market volume` (marketreportanalytics 경유)

② **확인한 소스 (9개)**
QYResearch/GII Matrigel 보고서 [E-318] · QYResearch 원 페이지(본문 미노출) · statsmarketresearch Matrigel(403) · openpr QYResearch 요약(403) · GlobalInfoResearch Basement Membrane Matrigel · IMR Market Reports Basement Membrane Matrigel · Corning Matrigel Availability Update 페이지 · Corning CLS-DL-CC-101 제품 문헌 · Wolff & Hendrix 2025 Advanced Science 리뷰 [E-332]

③ **부재 판단**
Corning 은 Matrigel 생산량을 공개하지 않는다 — 가용성 업데이트 페이지에서 "significantly increased the quantity of Matrigel matrix produced" 라는 **정성 표현만** 사용한다. 마우스 EHS 육종 유래라는 원료 특성상 생산능력이 경쟁 민감 정보이기 때문으로 판단한다. 학술 리뷰(Wolff & Hendrix 2025)도 시장 규모·물량·단가를 전혀 제시하지 않는다 [E-332] — 이 주제에 대한 1차 물량 통계는 **존재하지 않는다**고 판단한다.

④ **대체 추정치 + 오차범위**
```
전 용도 3D 매트릭스 물량 = 117.2 M USD [E-335] ÷ 블렌디드 ASP 36.46 USD/mL [E-334] = 3,215.8 L
  ASP 를 Corning 일반 Matrigel 직판가 30.29 USD/mL [E-100, Agent C] 로 쓰면  3,869 L
  ASP 를 Matrigel 오가노이드 SKU 44.76 USD/mL [E-102, Agent C] 로 쓰면       2,618 L
→ 대체 추정치 3,216 L, 오차범위 2,618 ~ 3,869 L (±19%)
오가노이드 스코프 물량(경로1 실측) 1,178.7 L 은 이 범위의 30.5 ~ 45.0%
  — 인용 기준 오가노이드 점유율 하한 28.8% [E-331]와 정합
```
**본 갭은 결론에 영향을 주지 않는다.** 경로1 이 물량을 독립적으로 상향 산출하므로 경로3 물량은 검증용이며, ±19% 오차 내에서 경로1(1,178.7 L)과 경로3(3,215.8 L)의 스코프 차이 해석(오가노이드 = 전 용도의 36.7%)은 변하지 않는다.
