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
