export const meta = {
  name: 'osvx-pipeline',
  description: 'OSVX: 콜라겐 기반 Defined Organoid Matrix 사업 Go/No-Go 다중에이전트 분석',
  phases: [
    { title: 'Wave1-전제검증', detail: 'B 규제 / C 경쟁·가격 / D VOC·전환장벽 (병렬)' },
    { title: 'Wave2-정량화', detail: 'A 시장규모 / E 원가 / F IP-FTO (병렬)' },
    { title: 'Wave3-GTM', detail: 'G 채널·앵커고객·로드맵' },
    { title: 'Wave4-검증', detail: 'R 신뢰도 / V 내부감사 / X 레드팀 (독립 병렬)' },
    { title: 'Wave5-통합', detail: 'S 재무모델·시나리오·Go/No-Go 판정' },
  ],
}

const ROOT = '/home/user/Oragnoid-Market/osvx'

const COMMON = `
너는 OSVX 하니스의 서브에이전트다. 작업 루트는 ${ROOT} 이다.

**가장 먼저 ${ROOT}/AGENT_RULES.md 를 Read 하고 그 규칙(R1~R6, 근거 스키마, ID 범위, 금지표현, 반환 스키마)을 전부 준수하라.**

핵심 강제사항 요약:
- R1 No-Deferral: "추후 조사 필요/향후 과제/범위를 벗어남/데이터 부족으로 생략/TBD" 등 책임전가 표현 절대 금지. 모르면 조사하고, 없으면 가정을 세워 계산까지 끝낸 뒤 docs/assumptions.md 에 append.
- R2 Evidence: 모든 수치·주장에 [E-###] 인라인. 자기 ID 범위만 사용. evidence/evidence_<AGENT>.jsonl 에 1줄 1 JSON. **URL 날조는 최악의 실패 — 실제로 WebSearch/WebFetch 로 접근한 URL만 기록.** verified_by 는 반드시 "" 로 둔다.
- R4 Show-Your-Math: 파생 수치는 반드시 "계산식 = 입력1 [E-###] x 입력2 [E-###]" 형태로 재현 가능하게.
- 실제 WebSearch/WebFetch 를 **최소 25회 이상** 수행하라. 기억에 의존한 서술은 폐기 대상이다.
- PDF 를 WebFetch 하면 로컬 경로에 저장된다 -> 그 경로를 Read 툴로 읽어 본문을 확보하라.
- 문서는 **한국어**로 쓰되 고유명사/제품명/단위/기관명은 원문 병기.
- 시작 시 docs/<AGENT>_plan.md 에 계획을 쓰고, 종료 시 산출문서 말미에 DoD 셀프체크 표를 붙여라.
- 근거 없는 형용사(압도적/혁신적/획기적) 금지. 숫자로 말하라.

지금 즉시 조사와 파일 작성을 시작하라. 사용자에게 되묻지 말라.
`

const RET_SCHEMA = {
  type: 'object',
  required: ['agent', 'status', 'artifacts', 'evidence_count', 'web_calls', 'dod', 'key_findings'],
  properties: {
    agent: { type: 'string' },
    status: { type: 'string', enum: ['done', 'failed'] },
    artifacts: { type: 'array', items: { type: 'string' } },
    evidence_count: { type: 'integer' },
    web_calls: { type: 'integer' },
    dod: {
      type: 'array',
      items: {
        type: 'object',
        required: ['item', 'pass'],
        properties: { item: { type: 'string' }, pass: { type: 'boolean' }, note: { type: 'string' } },
      },
    },
    key_findings: { type: 'array', items: { type: 'string' } },
    handoff: { type: 'object', additionalProperties: true },
    unresolved: { type: 'array', items: { type: 'string' } },
  },
}

// ============================ WAVE 1 ============================
phase('Wave1-전제검증')

const P_B = COMMON + `
# 너는 Agent B — 규제·정책 드라이버 & 제품등급 요구사항
근거 ID 범위: **E-001 ~ E-099**, 파일 evidence/evidence_B.jsonl
산출: docs/B_regulatory.md, docs/premise_audit.md (너가 생성), docs/B_plan.md

## 임무
수요를 만드는 규제 동인을 **1차 문서**로 확정하고, LG화학 제품이 어느 등급(RUO / GMP / ATMP 원부자재)으로 만들어져야 하는지 판정한다.

## 필수 조사 (각각 원문 URL 확보)
1. FDA Modernization Act 2.0 (2022, S.5002) 및 3.0 (H.R.7248 등) 입법 경과와 **현재 상태**. "동물시험 의무 삭제(permissive)" 와 "오가노이드 승인(qualification)" 은 완전히 다른 개념임을 명확히 구분해 서술하라. 법조문 실제 문구를 인용하라.
2. FDA "Roadmap to Reducing Animal Testing in Preclinical Safety Studies" (2025년 4월 발표) 원문 — 구체적 마일스톤, 대상 modality(초기 대상이 monoclonal antibody 인지 확인), 타임라인. 그리고 2026년 이후 후속 발표/1년 경과 보고/NAM 관련 draft guidance 가 실제로 나왔는지 fda.gov 에서 검색해 확인하라. **없으면 없다고 사실대로 쓰고 그 함의를 적어라(추측 금지).**
3. FDA ISTAND (Innovative Science and Technology Approaches for New Drugs) 및 DDT (Drug Development Tool) qualification 프로그램에 오가노이드/MPS/organ-on-chip 기반 도구가 몇 건 접수·수용되었는지. FDA 공식 ISTAND 목록 페이지를 실제로 열어 건수와 명칭을 세어라. organ-on-chip 대비 오가노이드의 상대적 위치를 정량 비교.
4. FDA/NIH 의 NAM 관련 예산·조직 변화 (예: NIH ODSPI, FDA CDER NAM 프로그램), ICCVAM, NICEATM.
5. EMA/ICH (ICH S1B(R1), M3(R2) 등), OECD Test Guidelines / GIVIMP, EU Directive 2010/63/EU 및 EU Parliament roadmap for phase-out of animal testing, 중국 NMPA, 일본 PMDA 동향.
6. 원부자재 등급 규제 원문: USP General Chapter <1043> Ancillary Materials for Cell/Gene/Tissue-Engineered Products, ISO 20399 (ancillary materials) / ISO 13022 (animal-derived), EU GMP Annex 2 (ATMP), 21 CFR Part 1271 (HCT/P), EP 5.2.12. 오가노이드가 임상/이식용으로 갈 때 **지지체(scaffold/matrix)가 실제로 받는 요구사항**: 동물유래성분 배제(TSE/BSE — EMA/410/01 rev.3), 무균(USP <71>), 엔도톡신 한도(USP <85>, EU/mL 기준), 마이코플라스마, lot release 규격, DMF/Master File 제출 가능성.
7. Matrigel 등 마우스 육종 유래 BME 가 임상용으로 쓸 수 없는 **구체적 규제 근거**를 원문에서 찾아라 (LDEV, 마우스 바이러스, 조성 미정의). 실제로 Matrigel 을 쓴 임상시험이 존재하는지 ClinicalTrials.gov 에서 검색해 확인하라 (예외 사례가 있으면 정직하게 기록).
8. RUO 시장과 GMP 시장의 규제 요구 격차를 **가격 프리미엄 근거로 정량화** — 실제 시장에서 동일 소재의 RUO vs GMP grade 가격 배수 사례를 최소 3건 찾아라 (예: recombinant laminin, recombinant albumin, GMP cytokine).

## R5 필수 — docs/premise_audit.md 작성 (너가 이 파일의 최초 작성자)
아래 사용자 전제 각각을 1차 문서로 검증하고 표로 정리하라:
| # | 사용자 전제 | 실제 확인 사실 [E-###] | 차이 판정(정확/부분과장/오해) | 사업적 함의 (수요 타이밍 몇 년 지연/가속, 정량) |
전제 목록:
 P1 "FDA가 오가노이드를 전임상 시험에서 허용/인정했다"
 P2 "FDA Modernization Act 로 동물시험이 폐지되었다"
 P3 "마트리겔은 임상 전환이 불가능하다"
 P4 "이식용 오가노이드 시장이 곧 열린다"
 P5 "규제가 defined matrix 수요를 강제한다"
각 전제마다 "이 전제가 실제보다 낙관적이라면 시장 진입 타이밍이 몇 년 밀리는가"를 **연 단위 숫자**로 답하라. 이것은 Agent A 의 수요 램프 함수 입력이 된다.

## 반드시 산출할 정량 handoff (Agent A 가 입력으로 씀)
- nam_ramp: {conservative, base, aggressive} 각각 2026/2030/2035 시점의 "제약사 전임상 프로그램 중 NAM(오가노이드 포함)을 실제 규제제출에 사용하는 비율(%)" 추정치 + 산출 근거
- grade_verdict: RUO/GMP/ATMP 중 1차 타깃 등급 판정과 근거
- gmp_premium_multiple: RUO 대비 GMP grade 가격 배수 (실측 사례 3건 기반 중앙값)
- clinical_timing_year: 이식용/재생의료 원부자재 매출이 유의미해지는 최초 연도 추정 + 근거

## DoD (전부 PASS 해야 status=done)
1) 1차 문서(FDA/EMA/USP/ISO/EU/NMPA/PMDA 원문) URL 최소 12건 확보
2) 규제 타임라인 표 (연도 - 이벤트 - 사업영향) 작성
3) 제품등급 판정 결론 1개 + 근거
4) docs/premise_audit.md 5개 전제 전부 검증 완료
5) docs/B_regulatory.md 생성, 모든 수치에 [E-###]
6) nam_ramp / gmp_premium_multiple / clinical_timing_year 정량값 산출
`

const P_C = COMMON + `
# 너는 Agent C — 경쟁·공급자 랜드스케이프 & 가격 구조
근거 ID 범위: **E-100 ~ E-199**, 파일 evidence/evidence_C.jsonl
산출: docs/C_competition.md, data/price_table.csv, docs/C_plan.md

## 임무
오가노이드 배양 매트릭스 시장의 모든 대안을 훑고 **USD/mL 실측 가격표**를 만든다.

## 필수 커버리지 — 최소 25개 제품 (실제 제품 페이지에서 가격 확인)
- BME 계열: Corning Matrigel (354234 10mL, 356234 5mL, GFR 354230/356231, phenol-red free, Organoid Matrix 356255 등 각 SKU 별로), Cultrex BME (R&D Systems/Bio-Techne, 3432-005-01 등), Cultrex UltiMatrix RGF BME (BME001-05), Geltrex LDEV-Free (Thermo A1413201/A1413202), Sigma ECM Gel (E1270), Corning Matrigel for Organoid Culture
- Defined 합성/펩타이드/PEG: QGel (QGel Bio), Ectica Technologies (3DProSeed), Cellendes (3-D Life PVA hydrogel), Manchester BIOGEL (PeptiGel/PeptiMatrix), 3-D Matrix (PuraMatrix), Gelomics (Lumina), TheWell Bioscience VitroGel (ORGANOID series), Advanced BioMatrix (VitroGel, PhotoCol, HyStem), Denovo Matrix (screenMATRIX), Stem Pharm, AMSBIO (Alvetex 등), UPM Biomedicals GrowDex (nanocellulose), Sigma TrueGel3D, Biogelx, Cellink/BICO
- 재조합/정제 ECM 단백: 재조합 콜라겐 (CollPlant, Evonik VERAMER/rhCollagen, Humabiologics, Fibrogen 계보, Jellagen), 재조합 라미닌 (BioLamina Biolaminin 111/521, Nippi iMatrix-511), 피브린/피브리노겐 기반, Vitronectin (Thermo A14700), 정제 콜라겐 I (Corning 354249, Advanced BioMatrix PureCol/TeloCol, Nutragen)
- 아시아/중국 로컬: 중국 공급자 (예: Yocon Biology, ABW, Bioatla 등 실제 검색으로 확인), 한국 공급자, 일본 (Nippi, Matrixome)
- 오가노이드 전용 배지 회사의 매트릭스 번들: STEMCELL Technologies (IntestiCult 등과 함께 판매하는 매트릭스), Hubrecht Organoid Technology (HUB) 관련

## 각 제품별 수집 필드 (data/price_table.csv 컬럼)
product_id, manufacturer, product_name, catalog_number, category(BME/synthetic-defined/recombinant-protein/purified-animal-protein/plant-or-other), definition_level(undefined-BME / semi-defined / fully-defined), origin(mouse-EHS / human / recombinant / synthetic / marine / plant), grade(RUO / GMP / clinical), size_mL, list_price_usd, price_source_url, usd_per_mL, crosslinking(thermal-gelation/enzymatic/photo/ionic/self-assembly/none), organoid_efficiency_note, pubmed_citation_count, gmp_line_available(Y/N/unknown-사유), key_customers_partnerships, evidence_id

- 가격이 "Request a quote" 인 경우: 유통사(Fisher, VWR, Sigma, Bio-Techne 직판, Biocompare, Labshake, Krackeler, Selleck 등)를 교차 검색해 실가격을 찾아라. 그래도 없으면 동급 제품 회귀로 추정하고 category 를 "추정"으로 표기 + assumptions.md 에 기재. **빈칸 금지.**
- 통화가 EUR/GBP/JPY 면 환율을 명시하고 USD 환산 (환율 출처 URL 필수).
- Matrigel 은 stock 상태 부피 기준 USD/mL 와, **실사용 희석/도밍 기준 유효단가**를 구분해서 계산하라.

## 추가 분석 (docs/C_competition.md)
1. 가격-정의수준 산점도 데이터: definition_level 별 USD/mL 의 중앙값/사분위수 → "정의성 프리미엄"이 실재하는지 통계로 실증. 실재하지 않으면 그렇게 쓰라 (이것은 사업 가설에 불리한 결과일 수 있으나 정직하게).
2. grade(RUO vs GMP) 별 가격 배수 실측.
3. 신규 진입자의 최근 3년 자금조달·M&A: QGel, Ectica, Manchester BIOGEL, Gelomics, Denovo Matrix, CollPlant, Humabiologics 등의 펀딩 라운드 금액·투자자 (Crunchbase, 보도자료, Fierce Biotech, Endpoints).
4. **Corning 의 방어 움직임**: Corning Life Sciences 의 defined/organoid 전용 라인 출시 여부, Matrigel 개량판, 특허, 생산 캐파, Corning 10-K 의 Life Sciences 세그먼트 매출 (SEC EDGAR 원문에서 실제 숫자). Bio-Techne 10-K 의 관련 세그먼트도.
5. 시장 집중도: Matrigel/Cultrex/Geltrex 3사의 추정 점유율과 근거.
6. **mTG(microbial transglutaminase) 가교를 쓰는 기존 상용 세포배양 매트릭스가 이미 있는지** 반드시 검색 (있다면 우리 차별화가 약해진다 — 정직하게 보고).

## 반드시 산출할 정량 handoff
- asp_bme_usd_per_mL: BME 계열 평균/중앙값 USD/mL
- asp_defined_usd_per_mL: fully-defined 계열 중앙값 USD/mL
- asp_gmp_usd_per_mL: GMP grade 중앙값 USD/mL
- definition_premium_ratio: defined / BME 가격비
- top3_share_estimate: BME 3사 점유율 추정 + 근거

## DoD
1) 25개 이상 제품 표 완성, 각 행에 [E-###] 와 price_source_url
2) 전 제품 USD/mL 환산 완료 (빈칸 0건)
3) GMP grade 제품 별도 태깅
4) 가격 프리미엄 정량 결론 (숫자)
5) data/price_table.csv + docs/C_competition.md 생성
`

const P_D = COMMON + `
# 너는 Agent D — 고객 VOC·Pain Point·전환장벽
근거 ID 범위: **E-200 ~ E-299**, 파일 evidence/evidence_D.jsonl
산출: docs/D_voc_barriers.md, docs/D_plan.md

## 임무
"마트리겔 Lot 편차가 문제다"를 **정량 증거**로 바꾸고, 동시에 **왜 아직도 다들 마트리겔을 쓰는지(전환장벽)** 를 냉정하게 파악한다. 후자가 더 중요하다 — 여기서 낙관하면 전체 사업판단이 틀어진다.

## 필수 조사 A — Lot-to-Lot 변동성 정량 (최소 5건 수치)
- 프로테오믹스 조성 편차 논문 (예: Matrigel 의 단백질 수 1,800+ 종 보고, lot 간 단백질 조성 CV%), 성장인자(TGF-beta, EGF, IGF, PDGF) 농도 편차 수치, 유변학적 강성 G' 편차(Pa 단위 범위), 배양 효율/organoid forming efficiency 의 lot 간 CV%.
- 검색어 예: "Matrigel batch-to-batch variability proteomic", "Matrigel lot variation organoid formation efficiency", "basement membrane extract mechanical variability stiffness", "Matrigel composition mass spectrometry 1851 proteins", "Hughes 2010 Matrigel proteomics".
- PubMed / Europe PMC / bioRxiv / Nature Methods / Nature Protocols / Acta Biomaterialia / Biomaterials 에서 실제 논문 확보 후 **수치를 본문에서 인용**.

## 필수 조사 B — 재현성 이슈와 실무 관행
- Nature / Nature Methods 재현성 특집, "reproducibility crisis" 관련 논평 중 Matrigel 을 지목한 것.
- 프로토콜 논문에서 "같은 lot 을 대량 확보해 두라(reserve/pre-test lots)" 는 권고 사례 — 실제 문장 인용. 이것은 lot 편차 페인의 강력한 방증이다.
- Matrigel 공급 부족(supply shortage) 사건이 있었는지 (2020년대 초 보고 여부) 및 그때 고객 반응.

## 필수 조사 C — 커뮤니티 VOC 원문 20건 이상 (URL 필수)
ResearchGate Q&A, Reddit r/labrats / r/biotech / r/cellculture, Bio-protocol 코멘트, protocols.io, X(Twitter) 연구자 스레드, 학회 초록(ISSCR, AACR, SLAS, ESACT, EACR), Biocompare/SelectScience 제품 리뷰, PubPeer.
- 발화를 **원문 그대로(영문) + 한국어 요약** 으로 인용하고 URL 을 붙여라. 익명화(사용자명 제거).
- 긍정 VOC(마트리겔이 좋다는 발화)도 반드시 포함하라 — 편향 금지.

## 필수 조사 D — 전환장벽 정량화 (가장 중요)
아래 각 항목에 **비용(USD)과 기간(개월)** 추정치를 붙여라. 근거가 없으면 구성요소로 빌드업 계산하고 assumptions.md 에 기재:
 B1 프로토콜 재검증: 세포주/오가노이드 라인당 재최적화 실험 횟수 x 인건비 x 소모품
 B2 기존 데이터셋과의 비교가능성 상실 (종단 연구 중단 리스크)
 B3 저널·심사자 수용성 — "Matrigel 로 안 하면 리뷰어가 문제 삼는다" 사례 검색
 B4 세포주/장기별 최적화 재수행 (intestinal, hepatic, pancreatic, cerebral, kidney, lung, tumor PDO 각각)
 B5 구매 관성·번들 계약·기관 구매 프로세스
 B6 **효능 격차**: defined matrix 에서 재현 안 되는 표현형 문헌 — 예: intestinal crypt budding 에 full-length laminin-111 / entactin 필요, Wnt/R-spondin 제시 방식, 세포외 소포·성장인자 잔류 효과. defined matrix 로 성공한 사례와 실패한 사례를 **둘 다** 수집하고 성공률을 정량 비교.
 - 검색어 예: "synthetic hydrogel intestinal organoid crypt formation efficiency comparison Matrigel", "PEG hydrogel organoid Matrigel comparable efficiency", "Gjorevski Lutolf 2016 designer matrices intestinal stem cell".

## 필수 조사 E — 세그먼트별 구매 의사결정
학술 PI / 제약 전임상 / CRO / 임상진단 / GMP 각각의 결정권자(PI vs 코어시설장 vs 구매팀 vs QA/RA), 예산 출처, 결정 기준 우선순위, 가격 민감도, 전환에 필요한 증거 수준(논문? 자체 검증? 규제파일?).

## 반드시 산출할 정량 handoff (Agent A 의 S-curve, Agent G 의 타깃 선정에 쓰임)
- switching_cost_usd_per_lab: 랩 1곳이 defined matrix 로 전환하는 총비용 중앙값
- switching_time_months: 전환 소요 기간
- segment_switch_propensity: 5개 세그먼트별 연간 전환 확률(%) 추정 + 근거
- must_win_metrics_top5: 우리 제품이 반드시 이겨야 하는 성능 지표 5개 (각각 목표 수치 + 현 BME 벤치마크 수치)

## DoD
1) Lot 편차 정량 수치 최소 5건 (단위·CV%·범위 포함)
2) 전환장벽 6항목 각각 비용(USD)·기간(개월) 추정
3) VOC 원문 인용 20건 이상 (각 URL)
4) must_win_metrics_top5 도출 (수치 목표 포함)
5) segment_switch_propensity 5개 세그먼트 산출
6) docs/D_voc_barriers.md 생성
`

const w1 = await parallel([
  () => agent(P_B, { label: 'B:규제·전제검증', phase: 'Wave1-전제검증', schema: RET_SCHEMA }),
  () => agent(P_C, { label: 'C:경쟁·가격', phase: 'Wave1-전제검증', schema: RET_SCHEMA }),
  () => agent(P_D, { label: 'D:VOC·전환장벽', phase: 'Wave1-전제검증', schema: RET_SCHEMA }),
])
log('Wave1 완료: ' + w1.filter(Boolean).map(r => r.agent + '=' + r.status + '(E:' + r.evidence_count + ')').join(' | '))

const w1ctx = `
## 선행 Wave 산출물 (반드시 Read 해서 수치를 입력으로 쓸 것)
- ${ROOT}/docs/B_regulatory.md , ${ROOT}/docs/premise_audit.md
- ${ROOT}/docs/C_competition.md , ${ROOT}/data/price_table.csv
- ${ROOT}/docs/D_voc_barriers.md
- 근거 재사용: ${ROOT}/evidence/evidence_B.jsonl, evidence_C.jsonl, evidence_D.jsonl (기존 [E-###] 인용 권장)

### Wave1 handoff 요약 (원문은 위 파일에서 직접 확인할 것)
B: ` + JSON.stringify(w1[0] && w1[0].handoff || {}) + `
C: ` + JSON.stringify(w1[1] && w1[1].handoff || {}) + `
D: ` + JSON.stringify(w1[2] && w1[2].handoff || {}) + `
`

// ============================ WAVE 2 ============================
phase('Wave2-정량화')

const P_A = COMMON + w1ctx + `
# 너는 Agent A — 수요·시장규모 (TAM/SAM/SOM, 금액 + 물량)
근거 ID 범위: **E-300 ~ E-399**, 파일 evidence/evidence_A.jsonl
산출: docs/A_market_sizing.md, model/market_model.py (실행 가능한 파라메트릭 모델), docs/A_plan.md

## 임무
오가노이드 지지체 시장을 **금액(USD)과 물량(L/년, mL)** 두 축으로 동시에 산출한다. **금액만 있는 시장보고서 인용은 부적합 처리**한다.

## 필수 방법론 — 3경로 삼각측량 (세 경로 모두 수행, 결과를 표로 병기)

### 경로1 Bottom-up (주 경로, 필수)
세그먼트별 연간 시장 = (사용 기관/랩 수) x (기관당 연간 실험/플레이트 수) x (실험당 매트릭스 소모량 mL) x (평균 판매단가 USD/mL)
- **랩 수 프록시**: PubMed / Europe PMC 에서 연도별 "organoid" 논문 수를 실제로 조회하라(1990~2025 추이). 논문당 고유 기관 수 비율, 오가노이드 코어시설 수, HUB/organoid 라이선스 기관 수, ATCC/ECACC 등 세포은행 계정 수. **PubMed 검색 결과 건수를 실제로 확인해서 인용하라** (esearch API 또는 pubmed.ncbi.nlm.nih.gov 검색 URL).
- **소모량 프록시**: 대표 프로토콜에서 추출 — dome culture 50 uL/well (24-well), 96-well 기준, Nature Protocols 의 intestinal organoid 프로토콜, PDO 배양 프로토콜. 주당 passage 횟수, 연간 유지 라인 수. Matrigel 병당 10 mL 규격 기준 랩당 연간 병 수를 역산.
- **단가**: Agent C 의 data/price_table.csv 실측 USD/mL 사용 (반드시 파일을 Read).
- 세그먼트: 학술연구(RUO) / 제약 전임상 NAM / 오가노이드 CRO·바이오뱅크 / 임상진단 PDO / 재생의료·이식용 GMP
- 지역: Global, US, EU, China, Japan, Korea (지역 가중은 논문 수·R&D 지출·제약사 수 등 실제 프록시로)

### 경로2 Top-down
Grand View Research, MarketsandMarkets, Mordor Intelligence, Fortune Business Insights, Precedence, Research and Markets 등의 "organoid market", "3D cell culture market", "extracellular matrix / hydrogel market", "basement membrane extract market" 수치를 무료 요약본에서 실제로 확인. **각 보고서가 무엇을 포함/제외했는지 정의를 반드시 확인**하고, 정의 불명이면 T3 로 강등하고 그 이유를 쓰라. 단일 보고서 의존 금지 — 최소 5개 교차.

### 경로3 Proxy / 역산
- SEC EDGAR 에서 Corning 10-K 의 Life Sciences 세그먼트 매출, Bio-Techne 10-K 의 관련 매출, Thermo Fisher 의 Bioproduction/Cell culture 언급 — 실제 파일링 숫자 인용.
- 어닝콜에서 Matrigel/BME 언급.
- 수입통계 HS 코드(예: 3002.90, 3504.00 등 관련 코드) 활용 가능 여부 확인.
- 오가노이드 논문 수 CAGR 로 역산 교차검증.

**경로 간 편차가 2배를 초과하면 docs/gaps.md 에 원인 분석을 남겨라.** 어느 경로를 채택할지와 그 근거를 명시하라.

## 세부 산출 요구
1. **세그먼트 x 지역 x 연도(2025/2026/2030/2035) 매트릭스** — 금액(USD) & 물량(L/년) 둘 다.
2. **Addressable subset 분리**: BME 전량이 defined 로 대체 가능하다고 가정하지 말 것. 기술적으로 defined matrix 가 현재/미래에 실제 대체 가능한 비율을 Agent D 의 효능 격차 문헌(B6)에 근거해 세그먼트별로 산정하라.
3. **NAM 정책 시나리오 연동**: Agent B 의 nam_ramp (conservative/base/aggressive) 를 입력으로, 제약 전임상 세그먼트 수요를 **램프 함수**로 모델링 (스텝 변화 금지). 수식을 명시.
4. **이식용/재생의료(GMP) 세그먼트는 별도 트랙**: ClinicalTrials.gov 에서 organoid / organoid-derived / PDO 관련 등록 임상시험 건수를 실제 검색해 확인하고(검색 URL 기록), 그 건수 기반 상향식 추정. 임상 1건당 매트릭스 소요량 가정 명시.
5. **CAGR 은 인용하지 말고 직접 계산**하라: CAGR = (End/Start)^(1/n) - 1, 계산식 표기.
6. TAM / SAM / SOM 정의를 명확히: TAM=전체 세포배양 매트릭스, SAM=defined matrix 로 접근 가능한 부분, SOM=LG화학이 5년차에 현실적으로 점유하는 부분(점유율 가정 근거 필수).

## model/market_model.py 요구사항
- 순수 python3 표준 라이브러리만 사용 (외부 의존 금지). 실행하면 세그먼트x지역x연도 표를 stdout 에 출력하고 CSV(data/market_model_output.csv)를 쓴다.
- 모든 입력 파라미터를 파일 상단 딕셔너리로 노출하고 각 값 옆에 # [E-###] 주석.
- scenario 인자(bear/base/bull) 지원.
- **반드시 python3 로 실행해서 에러 없이 도는 것을 확인**하고 출력값을 문서에 옮겨라.

## DoD
1) 3경로 결과가 하나의 표로 병기됨
2) 경로 간 편차와 채택 근거 기술
3) 모든 입력값에 [E-###]
4) 물량(L/년) 산출 존재
5) Addressable subset 분리
6) docs/A_market_sizing.md + model/market_model.py (실행 검증 완료) 생성
7) TAM/SAM/SOM 2025/2026/2030/2035 숫자 확정
`

const P_E = COMMON + w1ctx + `
# 너는 Agent E — 원가·단위경제·수익성
근거 ID 범위: **E-400 ~ E-499**, 파일 evidence/evidence_E.jsonl
산출: docs/E_cogs.md, model/cogs_model.py, docs/E_plan.md

## 임무
mL당 COGS 를 빌드업하고 ASP(Agent C 의 price_table.csv)와 붙여 gross margin 을 낸다. **추정이라도 반드시 숫자를 낸다. 빈칸 금지.**

## 필수 구성

### 1. BOM (원료 단가를 실제 조사)
- **콜라겐**: (a) 동물유래 정제 콜라겐 I (bovine/porcine, 예: Advanced BioMatrix PureCol, Nippi, Collagen Solutions) 의 벌크 단가 USD/g, (b) **재조합 인간 콜라겐** (CollPlant rhCollagen, Evonik VERAMER, Humabiologics, Jellagen, 중국 공급자) 의 단가 USD/g — 카탈로그가와 벌크가를 구분. single-chain(비삼중나선) vs triple-helix 형태별 단가 차이.
- **mTG/eMTG**: microbial transglutaminase 의 산업용 단가 (Ajinomoto Activa 등 식품용 USD/kg) vs GMP/제약급 단가. LG화학 내재 자산이므로 이전가격(transfer price) 가정을 명시.
- 라미닌 등 기능성 성분: 재조합 laminin-511/521 (BioLamina, Nippi iMatrix) 단가 USD/ug 또는 USD/mg. 매트릭스 mL 당 필요 농도(ug/mL)는 문헌 근거로 인용.
- 완충액·첨가제, 무균 여과(0.22 um), 충전, 바이알/캡, 라벨, 콜드체인 포장.

### 2. 공정원가
- 발효·정제: 내재화(LG화학 GMP 발효 인프라) vs 외주 CDMO 의 원가 비교. 재조합 단백 생산 titer(g/L) 가정, 정제 수율(%), downstream 비용 비중 — 바이오공정 문헌의 표준값 인용.
- 가교·제형 공정, 균질화, QC 시험 항목별 단가: 무균(USP <71>), 엔도톡신(USP <85>, LAL), 마이코플라스마, 조성 정량(SDS-PAGE/HPLC/LC-MS), 유변학 G'/G'' 측정, 기능시험(오가노이드 형성 효율 assay), 안정성시험, lot release. **각 시험의 외주 단가를 실제 CRO 가격표에서 조사**.
- 폐기율/수율 손실, 재작업률.

### 3. 등급별 원가 차이
RUO vs GMP 의 원가 배수를 근거와 함께 (환경 등급, 문서화, QP release, 안정성 프로그램, 감사 대응).

### 4. CAPEX
파일럿 규모 → 상업 생산 규모별 설비 투자(USD), GMP 인증 비용·기간(개월), 필요 인력(FTE).

### 5. 단위경제표 (필수 출력)
규격(1 mL / 5 mL / 10 mL) 별: COGS(USD/unit), COGS(USD/mL), 목표 ASP(Agent C 실측 기반), GM%, 손익분기 물량(L/년 및 units/년).

### 6. 규모의 경제 곡선
생산량(L/년: 1, 10, 100, 1000) vs 단위원가 곡선 — 고정비 배분 로직 명시. 경쟁사 추정 원가(Matrigel 은 마우스 EHS 육종 배양 유래 — 그 생산방식의 원가 구조를 추정)와 비교.

## model/cogs_model.py
- python3 표준 라이브러리만. 실행하면 BOM→COGS→GM 표를 출력하고 data/cogs_output.csv 를 쓴다.
- 민감도 함수 포함: 콜라겐 단가 +-50%, 수율 +-30%, ASP +-30%, mTG 단가 +-50%, 생산량 스케일.
- **반드시 실행해서 검증**하고 출력을 문서에 옮겨라.

## 반드시 산출할 정량 handoff
- cogs_usd_per_mL_ruo / cogs_usd_per_mL_gmp (기준 생산량 명시)
- gm_pct_at_target_asp (3규격)
- bep_volume_L_per_year, bep_revenue_usd
- capex_total_usd, gmp_cert_months

## DoD
1) BOM 항목별 단가 [E-###] (최소 10개 항목)
2) COGS 빌드업 표
3) GM% 3규격 산출
4) BEP 물량·매출 산출
5) 민감도 3종(콜라겐 단가/수율/ASP) 수행
6) docs/E_cogs.md + model/cogs_model.py (실행 검증 완료)
`

const P_F = COMMON + w1ctx + `
# 너는 Agent F — IP / FTO / 진입장벽
근거 ID 범위: **E-500 ~ E-599**, 파일 evidence/evidence_F.jsonl
산출: docs/F_ip_fto.md, data/patent_table.csv, docs/F_plan.md

## 임무
이 사업을 막을 수 있는 특허와, LG화학이 세울 수 있는 방어벽을 동시에 본다.

## 필수 조사 — 최소 30건 특허 (Google Patents / Espacenet / KIPRIS / USPTO 에서 실제 특허번호 확인)
검색 축:
1. **효소 가교 하이드로겔 세포배양 매트릭스** — Factor XIIIa(FXIIIa) 가교 PEG 하이드로겔 계보 (EPFL Lutolf / QGel 관련 출원인), transglutaminase 가교 세포배양 지지체.
2. **mTG(microbial transglutaminase) 가교 젤라틴/콜라겐 하이드로겔** — Ajinomoto, 대학 출원, 의료용 접착제/스캐폴드. **우리 핵심 기술과 직접 충돌 가능성이 가장 높은 축이므로 가장 깊게 파라.**
3. **Defined organoid culture matrix** — 합성/화학정의 오가노이드 배양 매트릭스 조성물 특허 (Lutolf, Hubrecht/HUB, Clevers 계보, Cellendes, Manchester BIOGEL, Ectica, TheWell, Advanced BioMatrix).
4. **재조합 콜라겐 조성물·생산** — CollPlant(식물유래 rhCollagen), Evonik, Fibrogen, Modern Meadow, Geltor, Jellagen, 중국 출원인.
5. **오가노이드 배양 배지·프로토콜 특허** — Clevers/Hubrecht 의 기반 특허(예: EP 계열 Lgr5 stem cell culture), R-spondin/Wnt surrogate 특허, 이들의 만료 시점.
6. **Matrigel/BME 관련 특허 및 Corning 의 방어 포트폴리오**.

## data/patent_table.csv 컬럼
patent_number, jurisdiction(US/EP/CN/JP/KR/WO), assignee, priority_date, grant_date, expiry_estimate, status(등록/출원중/만료/포기), claim_gist(청구항 1의 요지 한국어), relevance_to_us(직접충돌/인접/배경), infringement_risk(상/중/하), design_around_note, url, evidence_id

## 필수 분석
- 주요 보유자별 포트폴리오 규모(건수)·존속기간·지역 커버리지 (US/EP/CN/JP/KR 별).
- **만료 임박/이미 만료된 핵심 특허** = 기회. Clevers 오가노이드 기반 특허의 우선일과 만료 예상 시점을 계산해서 제시.
- **침해 위험 시나리오 3개**를 구체적으로 (어느 특허의 어느 청구항이 우리의 어느 제품 구성을 읽는가).
- **회피 설계안 3개** (조성비 변경, 가교 조건 변경, 다른 효소/가교 화학, 지역별 출시 전략).
- **우리가 확보 가능한 신규 특허 포지션**: single+triple helix 콜라겐 혼합비, mTG 가교 조건(농도/시간/온도), 물성 규격(G' 범위), 오가노이드 특이적 용도 청구항. 선행기술 대비 신규성 확보 가능 영역을 구체적으로.
- **비특허 진입장벽**: GMP 이력, 규제 파일(DMF/Master File), 논문 채택 실적(citation lock-in), 유통망, 브랜드.
- LG화학의 기존 관련 특허 보유 현황도 KIPRIS/Google Patents 에서 검색 (transglutaminase, collagen, 세포배양).

## 반드시 산출할 정량 handoff
- fto_verdict: 상/중/하 종합판정 1개 + 3줄 근거
- blocking_patents_count: 직접충돌 등급 특허 건수
- key_expiry_years: 핵심 차단 특허들의 만료 연도 목록

## DoD
1) 특허 30건 이상 테이블 (번호·권리자·만료·청구항 요지·리스크 등급)
2) FTO 종합판정 1개 (상/중/하)
3) 침해 시나리오 3개 + 회피설계 3안
4) 신규 특허 포지션 제안
5) docs/F_ip_fto.md + data/patent_table.csv
`

const w2 = await parallel([
  () => agent(P_A, { label: 'A:시장규모', phase: 'Wave2-정량화', schema: RET_SCHEMA }),
  () => agent(P_E, { label: 'E:원가·단위경제', phase: 'Wave2-정량화', schema: RET_SCHEMA }),
  () => agent(P_F, { label: 'F:IP·FTO', phase: 'Wave2-정량화', schema: RET_SCHEMA }),
])
log('Wave2 완료: ' + w2.filter(Boolean).map(r => r.agent + '=' + r.status + '(E:' + r.evidence_count + ')').join(' | '))

const w2ctx = w1ctx + `
- ${ROOT}/docs/A_market_sizing.md , ${ROOT}/model/market_model.py
- ${ROOT}/docs/E_cogs.md , ${ROOT}/model/cogs_model.py
- ${ROOT}/docs/F_ip_fto.md , ${ROOT}/data/patent_table.csv
### Wave2 handoff
A: ` + JSON.stringify(w2[0] && w2[0].handoff || {}) + `
E: ` + JSON.stringify(w2[1] && w2[1].handoff || {}) + `
F: ` + JSON.stringify(w2[2] && w2[2].handoff || {}) + `
`

// ============================ WAVE 3 ============================
phase('Wave3-GTM')

const P_G = COMMON + w2ctx + `
# 너는 Agent G — 사업모델·GTM·파트너십
근거 ID 범위: **E-600 ~ E-699**, 파일 evidence/evidence_G.jsonl
산출: docs/G_gtm.md, docs/G_plan.md

## 임무
팔 수 있는 경로를 **구체적 기업명과 숫자**로 만든다. 추상적 전략론 금지.

## 필수 산출
### 1. 채널 옵션 정량 비교표 (최소 4개 채널)
직판 / 대형 유통 OEM(Thermo Fisher, Merck-Sigma, Bio-Techne, VWR-Avantor, Fisher) / 오가노이드 기업 번들(배지+매트릭스 세트) / CDMO·CRO 공급 / 학술 얼리어답터 시딩 프로그램
각 채널별: 예상 마진율(%), 유통 마크업 실측(카탈로그가 vs 리스트가 차이로 역산 — Agent C 데이터 활용), 도달 속도(개월), 통제력(상/중/하), 필요 투자(USD), 초기 물량 기대치.

### 2. 초기 앵커 고객 후보 **실명 20곳 이상**
- 글로벌 오가노이드 기업: Hubrecht Organoid Technology(HUB), Crown Bioscience, Xilis, Vivodyne, Cellesce, OcellO, Emulate, CN Bio, Molecular Devices(Cellesce 인수), STEMCELL Technologies, Definigen, Organoid Sciences 등 — 실제 검색으로 현존 여부·규모·최근 뉴스 확인.
- 오가노이드 CRO / NAM 서비스: Charles River, Labcorp, Evotec, Crown Bioscience, Champions Oncology, Certis Oncology, SUN Bioscience 등.
- 국내: 오가노이드사이언스, 넥스트앤바이오, 강스템바이오텍, 티앤알바이오팹, 셀트리온/삼성바이오 관련, 국립암센터·서울아산·삼성서울 오가노이드 뱅크, 한국생명공학연구원(KRIBB) 등 — 실제 존재 확인.
- 대형 코어시설: 미국·유럽 주요 대학 오가노이드 코어, NCI PDMR, Human Cancer Models Initiative.
각 후보별: 기업명 / 근거 URL / 왜 우리 타깃인지 / 접점 가설(누구를 통해 어떻게) / 예상 초기 물량(mL/년) / 우선순위(1~3).

### 3. 진입 전략
어느 세그먼트를 1번으로 칠 것인가 + 그 이유. 판단 기준은 반드시 정량: (전환장벽 낮음: Agent D 의 switching_cost/switch_propensity) x (defined 요구 높음: Agent B 의 규제 요구) x (가격 수용도: Agent C) x (시장 크기: Agent A). **점수표를 만들어 5개 세그먼트를 채점하고 1위를 선언하라.**

### 4. 제품 라인업 로드맵 3단계
RUO → GMP → 이식용 원부자재. 각 단계: 연도, 필요 투자(USD), 필요 기간(개월), 마일스톤, 전제조건, 게이트 판정기준.

### 5. 파트너십/M&A 옵션
기술 도입(예: 재조합 콜라겐 원료사, 라미닌 공급사) / 채널 확보(유통사 OEM) / 인수 후보(소규모 defined matrix 스타트업 — Agent C 가 찾은 기업 중 밸류에이션 추정 가능한 곳). 각 옵션의 논리와 예상 대가.

### 6. 가격 전략
침투가 vs 프리미엄. 근거는 Agent C 가격표(실측 USD/mL)와 Agent D 전환장벽 비용. **"전환장벽 비용을 상쇄하려면 mL당 얼마나 싸야 하는가"를 계산하라**: 필요 할인율 = 전환비용 / (연간 사용량 x 현 단가 x 회수기간). 이 계산이 Agent E 의 GM 과 양립하는지 검증하라 — 양립 불가면 그렇게 보고하라.

## 반드시 산출할 정량 handoff
- target_segment_rank1: 1차 타깃 세그먼트 + 점수
- channel_margin_pct: 채널별 마진율
- price_strategy_usd_per_mL: 제안 출시가
- required_discount_pct: 전환장벽 상쇄에 필요한 할인율
- roadmap_capex_by_phase: 3단계 투자액

## DoD
1) 채널 4개 이상 정량 비교표
2) 앵커 고객 20곳 이상 실명 리스트 (각 URL)
3) 1차 타깃 세그먼트 결론 + 점수표 근거
4) 3단계 로드맵 (연도·투자·마일스톤)
5) 가격 전략 계산식 제시 + Agent E GM 과의 양립성 검증
6) docs/G_gtm.md 생성
`

const wG = await agent(P_G, { label: 'G:GTM·채널', phase: 'Wave3-GTM', schema: RET_SCHEMA })
log('Wave3 완료: G=' + (wG && wG.status))

// ============================ WAVE 4 (독립 병렬) ============================
phase('Wave4-검증')

const P_R = COMMON + `
# 너는 Agent R — 근거 신뢰도 독립 검증
근거 ID 범위: **재판정만 수행, 새 ID 생성 금지**
산출: docs/R_credibility.md, evidence/evidence_verified.jsonl, evidence/evidence_rejected.jsonl, docs/R_plan.md

## 절대 원칙 (R3)
**다른 에이전트의 결론 문서(docs/*_*.md 중 A~G 의 본문 분석·결론 부분)를 읽고 그 판단에 동조하지 말라.** 너는 evidence/evidence_*.jsonl 의 **레코드 자체와 원자료(URL)** 에서만 출발한다. Agent V, X 의 산출물도 읽지 않는다.

## 작업
1. ${ROOT}/evidence/ 의 evidence_A.jsonl ~ evidence_G.jsonl 전부를 Read (bash 로 cat 해도 좋다).
2. **각 레코드의 URL 을 실제로 WebFetch 해서 접근 가능한지, 그리고 claim/value 가 그 원문에 실제로 존재하는지 확인**하라.
   - 레코드 수가 많으면 다음 우선순위로 최소 60건 이상을 실검증하라: (a) 핵심결론(시장규모·가격·COGS·GM·FTO판정)을 지탱하는 근거 전부 (b) tier T1 주장 (c) 무작위 표본.
   - 실검증하지 않은 레코드는 sampled:false 로 표기하고, 표기 기준을 문서에 쓰라.
3. **Tier 재판정** — T1(1차: 규제기관 원문, 상장사 공시/10-K, 특허 원문, 제조사 공식 카탈로그·CoA, 피어리뷰 논문) / T2(2차: 시장보고서, 업계지, 애널리스트, 유통사 가격) / T3(3차: 블로그, 커뮤니티, 위키, 내부 삼각추정)
4. **신뢰도 상/중/하 재부여** — 판정 기준 5축: 출처 독립성 / 방법론 공개 / 최신성 / 재현가능성 / 이해상충. **각 판정에 1줄 사유 필수.**
5. 접근 불가(404, 페이월, 리다이렉트 실패)·원문 불일치(claim 이 원문에 없음)·URL 날조 의심 레코드는 **evidence/evidence_rejected.jsonl 로 격리**하고, 사유를 rejection_reason 필드에 쓴다.
6. 통과 레코드는 verified_by:"R" 와 재판정된 tier/confidence 를 넣어 **evidence/evidence_verified.jsonl** 에 쓴다. (원본 필드 보존)
7. **핵심 결론별 근거품질 스코어카드**: 시장규모(TAM/SAM/SOM) / 가격·ASP / COGS·GM / 규제 타이밍 / FTO / 전환장벽 — 각 결론을 지탱하는 근거의 T1 비중(%)과 '하' 비중(%)을 계산해 표로.
8. **게이트**: 핵심 결론 지지 근거 중 '하' 비중이 30% 를 넘거나 T1 비중이 40% 미만인 항목은 **FAIL** 로 표시하고, 어느 에이전트가 무엇을 재조사해야 하는지 구체적으로 지시하라. 그리고 **너 스스로 그 갭 중 최소 5건을 직접 웹 검색해 더 나은 T1 근거를 찾아 evidence_verified.jsonl 에 보강 레코드(id 는 원본ID + "-R" 접미사)로 추가하라.**

## Tier·신뢰도 분포 통계 (문서에 표로)
전체 / 에이전트별 / 소스타입별 T1:T2:T3 비율, 상:중:하 비율, 격리 건수, URL 접근 성공률.

## DoD
1) 전 레코드 재평가 완료 (실검증 60건 이상 명시)
2) evidence_rejected.jsonl 생성 (0건이면 0건임을 명시)
3) Tier·신뢰도 분포 통계 표
4) 핵심결론 6개 항목 근거품질 스코어카드 + PASS/FAIL
5) 보강 근거 5건 이상 추가
6) docs/R_credibility.md + evidence/evidence_verified.jsonl
`

const P_V = COMMON + `
# 너는 Agent V — 내부 정합성·완결성 감사
산출: docs/V_audit.md, docs/V_plan.md (새 근거 ID 생성 금지)

## 절대 원칙 (R3)
Agent R, X 의 산출물을 읽지 않는다. **외부 근거의 신뢰도는 보지 않는다 — 오직 내부 논리와 수치 정합성만 본다.**

## 작업 (${ROOT}/docs/*.md, data/*.csv, model/*.py 전부를 Read)
### 1. 수치 정합성 크로스체크 (표로 전건 나열)
- Agent A 의 시장규모에 쓰인 단가 vs Agent C 의 price_table.csv 실측 단가가 일치하는가
- Agent A 의 물량(L/년) x 단가 = 금액 이 실제로 맞는가 (직접 계산해서 검산하라)
- Agent E 의 COGS 와 Agent C 의 ASP 로 계산한 GM% 가 Agent E 문서의 GM% 와 일치하는가
- Agent G 의 가격 전략가가 Agent E 의 COGS 대비 목표 GM 을 만족하는가
- 연도 기준(2025 vs 2026), 통화(USD/KRW/EUR), 환율, 단위(mL vs L, USD/mL vs USD/unit)가 문서 간 일치하는가
- **이중계산 탐지**: 같은 수요를 두 세그먼트에서 중복 계상했는가, TAM 안에 SAM 이 포함되는가, addressable subset 이 두 번 곱해졌는가
- **bash 로 python3 model/market_model.py 와 model/cogs_model.py 를 실제 실행**해서 문서에 적힌 숫자와 코드 출력이 일치하는지 확인하라. 불일치는 전부 기록.

### 2. 과신 언어 탐지
단정형 서술("~이다", "~한다", "확실히", "반드시") 중 그 근거의 tier 가 T3 이거나 근거가 추정인 것을 리스트업 → **구체적 수정 문장을 제안**하라 (원문 → 수정안).

### 3. 금지 표현 스캔
AGENT_RULES.md §1 의 금지 표현 목록을 bash grep 으로 전 문서 스캔. 발견된 파일:줄번호:문장 을 전건 리스트업하고 **수정안 제시**. (grep -n 으로 실제 실행할 것)

### 4. DoD 누락 스캔
각 에이전트 문서의 DoD 셀프체크 표를 확인하고, 선언된 PASS 가 실제 문서 내용으로 뒷받침되는지 검증(예: "특허 30건" 이라 했는데 실제 표 행수가 몇 개인지 세어라 — wc/grep 으로).

### 5. 논리 비약 탐지
"TAM 이 크다 → 우리가 먹는다", "규제가 바뀐다 → 수요가 생긴다", "기술적으로 가능하다 → 고객이 산다" 류의 점프 지점을 문서에서 찾아 지점별로 "빠진 전제"를 명시하라.

### 6. 수정 지시서
docs/V_audit.md 말미에 **"필수 수정 항목"** 을 [파일 / 위치 / 현재 서술 / 수정 요구 / 심각도(상중하)] 표로 정리하라. Agent S 와 W 가 이것을 반영한다.

## 사용자 선호 반영
과장된 확신은 **반드시 하향 교정**한다. 듣기 좋은 결론이 아니라 틀린 전제를 잡는 것이 목적이다.

## DoD
1) 모순 항목 전건 목록 + 수정 요구
2) 과신 표현 수정 로그 (원문→수정안)
3) 금지표현 grep 결과 (0건이면 0건 증빙, 발견 시 전건 목록)
4) 모델 코드 실행 검증 결과
5) 논리 비약 지점 목록
6) docs/V_audit.md 생성
`

const P_X = COMMON + `
# 너는 Agent X — 반증 레드팀 (Bear Case)
근거 ID 범위: **E-700 ~ E-799**, 파일 evidence/evidence_X.jsonl
산출: docs/X_redteam.md, docs/X_plan.md

## 절대 원칙
Agent R, V 의 산출물을 읽지 않는다. **균형 잡힌 서술 금지 — 여기서는 이 사업을 죽이는 논리를 최대한 강하게 만든다.** 다만 감정이 아니라 **실제 증거와 숫자**로 죽여라. 증거 없는 비관도 실패다.

## 반증 가설 최소 8개 — 각각 실제 웹 증거 + 정량 임팩트
H1. NAM 전환이 예상보다 느리고, 수요가 오가노이드가 아니라 organ-on-chip / MPS / in silico(QSP, AI 독성예측)로 흡수될 가능성. → 실제 FDA ISTAND 수용 건수, MPS 기업 투자액, AI 독성예측 기업(예: VeriSIM, Simulations Plus) 성장률을 비교 증거로.
H2. Defined matrix 가 오가노이드 효능(배양 효율, crypt formation, 계대 안정성, 장기 유지)에서 BME 를 못 넘는다는 실증 문헌. → 정량 비교 논문을 찾아 효율 격차 %를 제시.
H3. 학계 관성 — Matrigel 인용 lock-in(논문 수 추이), 리뷰어 수용성, "표준 프로토콜" 고착.
H4. Corning / Thermo / Bio-Techne 가 자체 defined 라인으로 즉시 대응할 여력 — R&D 예산, 기존 특허, 유통망, 가격 인하 여력(그들의 GM% 를 10-K 에서 확인해 얼마나 내릴 수 있는지 계산).
H5. 가격 경쟁 격화 + 중국 저가 진입 — 실제 중국 공급자 가격 조사.
H6. **재조합 콜라겐 원료 단가가 COGS 를 무너뜨릴 가능성** — 재조합 콜라겐 g당 단가와 매트릭스 mL 당 필요량(mg/mL, 통상 3~8 mg/mL)을 곱해 원료비만으로 얼마인지 계산. Agent E 의 COGS 가정을 공격하라.
H7. **mTG 가교의 기술적 한계** — 라미닌 LG 도메인 손상, 과가교 시 세포 생존/회수율 저하, 콜라겐 삼중나선 구조에서 Gln/Lys 잔기 접근성 제한, 가교 후 젤 광학투명도/이미징 저하, mTG 잔류 제거 문제, 면역원성. 각각 문헌 증거를 찾아라.
H8. 이식용 시장 도달 시점이 10년 이상일 가능성 / 규제 비용 과소평가 — 실제 ATMP 원부자재로 등재되기까지의 사례 기간.
H9. 시장보고서 수치 자체의 과대추정 구조 — 동일 시장에 대한 서로 다른 보고서 수치의 편차 배수를 실제로 계산해 제시.
H10. LG화학 내부 요인: B2B 소재 대기업이 소량 다품종 연구용 시약 시장(랩당 연 수천 달러)을 운영할 조직 적합성, 최소 사업규모 기준 미달 가능성.

## 각 반증마다 필수
- 증거 URL + [E-###]
- **"이 반증이 참이면 SOM(2030)이 얼마나 깎이는가"를 숫자로**: 기준 SOM 대비 삭감액(USD)과 삭감률(%). 계산식 표기. (docs/A_market_sizing.md 의 SOM 을 Read 해서 기준값으로 쓰라)
- 이 반증이 참일 확률(주관 확률 %) + 그 근거

## Kill Criteria 5개 (검증 가능한 형태)
"어떤 사실이 확인되면 즉시 중단해야 하는가" — 각각 [측정 대상 / 측정 방법 / 임계값 / 확인 시점(개월)] 형태로. 모호한 서술 금지. 예: "내부 파일럿에서 intestinal organoid forming efficiency 가 Matrigel 대비 X% 미만이면 중단".

## 종합
- 전 반증의 결합 효과를 반영한 **Bear-case SOM(2030)** 을 계산하라 (독립 가정 시 곱연산, 상관 가정 시 근거 명시).
- 이 사업이 실패할 종합 확률 추정과 근거.

## DoD
1) 반증 8개 이상, 각각 실제 증거 URL 포함
2) 각 반증의 정량 임팩트 (SOM 삭감액/률, 계산식)
3) Kill Criteria 5개 (측정가능 형태)
4) Bear-case SOM(2030) 산출
5) docs/X_redteam.md + evidence/evidence_X.jsonl
`

const w4 = await parallel([
  () => agent(P_R, { label: 'R:신뢰도검증', phase: 'Wave4-검증', schema: RET_SCHEMA }),
  () => agent(P_V, { label: 'V:내부감사', phase: 'Wave4-검증', schema: RET_SCHEMA }),
  () => agent(P_X, { label: 'X:반증레드팀', phase: 'Wave4-검증', schema: RET_SCHEMA }),
])
log('Wave4 완료: ' + w4.filter(Boolean).map(r => r.agent + '=' + r.status).join(' | '))

// ============================ WAVE 5 ============================
phase('Wave5-통합')

const P_S = COMMON + w2ctx + `
- ${ROOT}/docs/G_gtm.md
- ${ROOT}/docs/R_credibility.md (근거품질 스코어카드)
- ${ROOT}/docs/V_audit.md (**필수 수정 항목을 반드시 반영하라**)
- ${ROOT}/docs/X_redteam.md (Kill Criteria, Bear-case)

# 너는 Agent S — 통합 재무모델 & Go/No-Go 판정
근거 ID 범위: **E-800 ~ E-849**, 파일 evidence/evidence_S.jsonl
산출: docs/S_synthesis.md, model/OSVX_model.xlsx (수식 살아있는 상태), model/finance_model.py, docs/S_plan.md

## 임무
전 에이전트 산출을 하나의 모델로 합치고 **판정한다. 판정을 유보하는 것은 실패다.**

## 필수 작업
### 0. 선행 문서 전부 Read
docs/ 의 A,B,C,D,E,F,G,R,V,X 문서와 data/*.csv, model/*.py 를 모두 읽어라. **Agent V 의 필수 수정 항목과 Agent R 의 FAIL 항목을 반영**하고, 반영 내역을 표로 남겨라. Agent X 의 Kill Criteria 를 모델의 하방 시나리오로 구현하라.

### 1. 시나리오 3종 (Bear / Base / Bull)
구동 변수(각각 3종 값과 근거 출처 [E-###]):
- NAM 램프 속도 (Agent B nam_ramp)
- defined 침투율 S-curve 파라미터 (Agent D 전환장벽 반영 — **선형 점유율 가정 절대 금지**. 로지스틱 S-curve: P(t) = L / (1 + exp(-k(t - t0))) 형태로 L(최종 침투율), k(기울기), t0(변곡점)을 전환장벽 비용·전환확률에서 도출하고 수식을 명시)
- ASP (Agent C/G)
- 우리 점유율 (Agent G 채널·앵커고객 기반, 근거 필수)
- 원가 (Agent E)

### 2. 10년 P&L 추정 (2026~2035)
연도별: 매출(USD), 물량(L), COGS, Gross Profit, GM%, 판관비(SG&A), R&D, EBIT, 누적 투자, FCF.
- 할인율(WACC)을 명시하고 근거를 대라 (LG화학 자본비용 추정 또는 바이오소재 산업 벤치마크, 출처 URL).
- **NPV, IRR, BEP(연도 및 누적물량), Payback(년)** 산출.

### 3. DECISION_GATE 대조 (필수 표)
| 게이트 | 임계값 | Base 시나리오 실적 | 판정 |
- SAM_2030 >= 150,000,000 USD
- SOM_2030 >= 15,000,000 USD
- Gross_Margin >= 0.60
- Payback <= 5년
- FTO 리스크 <= 중
**→ 종합 판정: "Go" / "Conditional-Go" / "No-Go" 중 정확히 하나를 문서에 명시적 문자열로 선언하라.**

### 4. Conditional-Go 인 경우 (또는 어떤 판정이든) 90일 검증 액션 5개
각각 [액션 / 담당 기능(R&D·사업개발·법무·CMC 등) / 비용(USD) / 기간(일) / 판정기준(무엇이 나오면 Go, 무엇이 나오면 Stop)] 표로. 검증 가능한 실험/미팅 형태여야 한다.

### 5. 민감도 (토네이도 차트용 데이터, 상위 8개 변수)
각 변수를 -30%/+30% 흔들었을 때 NPV 변화폭(USD)을 계산해 절대 영향 크기 순으로 정렬한 표.

### 6. Kill Criteria 반영 하방 검증
Agent X 의 Kill Criteria 5개가 각각 발동했을 때의 NPV 를 계산해 표로.

## model/OSVX_model.xlsx 요구사항 (openpyxl 사용, 이미 설치됨)
시트 구성:
 1) README — 모델 설명, 단위, 환율, 작성일
 2) Inputs — 전 파라미터 (셀 참조 가능하게, 각 행에 근거 [E-###] 열)
 3) Market — 세그먼트x지역x연도 시장규모 (금액·물량)
 4) Scenarios — Bear/Base/Bull 3시나리오 P&L (**엑셀 수식으로 살아있게**: Inputs 시트를 참조하는 =B5*C5 형태 수식을 실제로 넣어라. 하드코딩 값만 넣으면 DoD 실패)
 5) PnL_Base — 10년 상세 P&L (수식)
 6) Sensitivity — 상위 8변수 토네이도 데이터 (수식)
 7) Gates — DECISION_GATE 대조표
 8) Evidence_Index — 사용된 [E-###] 목록
- openpyxl 로 생성 후 **다시 열어서 시트 수와 수식 존재를 검증**하라 (bash python3 로 확인).

## model/finance_model.py
python3 표준 라이브러리만으로 동일 계산을 수행하고 3시나리오 P&L·NPV·IRR 을 stdout 과 data/finance_output.csv 로 출력. **실행 검증 필수.**

## DoD
1) 3시나리오 수치표
2) NPV/IRR/BEP/Payback 산출
3) **Go / Conditional-Go / No-Go 명시적 선언 (문서에 그 문자열이 그대로 존재)**
4) 90일 검증 액션 5개 (담당·비용·기간·판정기준 포함)
5) 민감도 상위 8변수
6) model/OSVX_model.xlsx (8시트, 수식 살아있음) + model/finance_model.py (실행 검증)
7) docs/S_synthesis.md 생성
8) V 의 수정 항목 반영 내역 표
`

const wS = await agent(P_S, { label: 'S:통합·판정', phase: 'Wave5-통합', schema: RET_SCHEMA })
log('Wave5 완료: S=' + (wS && wS.status))

return {
  wave1: w1,
  wave2: w2,
  wave3: wG,
  wave4: w4,
  wave5: wS,
}
