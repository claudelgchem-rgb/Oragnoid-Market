# Agent D 작업계획 — 고객 VOC · Pain Point · 전환장벽

작성일: 2026-08-11 / 근거 ID 범위: **E-200 ~ E-299** / evidence 파일: `evidence/evidence_D.jsonl`

## 0. 목적과 관점

두 가지를 동시에 한다. 그리고 **두 번째가 더 중요하다.**

1. (Pull) "Matrigel Lot 편차가 문제다"라는 정성적 통념을 **정량 증거**(CV%, Pa, 단백질 종수, 성장인자 ng/mL)로 치환한다.
2. (Friction) **그럼에도 왜 시장이 Matrigel을 계속 쓰는가** — 전환장벽을 비용(USD)·기간(개월)으로 정량화한다.

의사결정 상 함의: pain의 크기만으로는 매출이 생기지 않는다. `전환확률 = f(pain − 전환비용 − 효능격차)` 이므로,
전환장벽을 낙관적으로 추정하면 SOM 전체가 과대평가된다. **본 에이전트는 의도적으로 전환장벽 쪽에 보수적 편향을 건다.**

## 1. 조사 블록 및 쿼리 목록

### 조사 A — Lot-to-Lot 변동성 정량 (목표: 수치 5건 이상)
- QA1 `Matrigel batch-to-batch variability proteomic analysis`
- QA2 `Hughes 2010 Matrigel proteomic 1851 proteins Proteomics journal`
- QA3 `Matrigel lot variation organoid forming efficiency CV`
- QA4 `basement membrane extract mechanical variability stiffness storage modulus Pa`
- QA5 `Matrigel growth factor concentration variability TGF-beta EGF IGF ELISA lot`
- QA6 `Matrigel proteomics 2021 2022 lot comparison mass spectrometry`
- QA7 `Corning Matrigel certificate of analysis growth factor range specification`
- 소스: PubMed / Europe PMC / bioRxiv / Nature Methods / Nature Protocols / Acta Biomaterialia / Biomaterials / Sci Rep

### 조사 B — 재현성 이슈 + 실무 관행("lot 확보/사전시험" 권고 원문)
- QB1 `Nature Methods reproducibility Matrigel organoid variability editorial`
- QB2 `protocol "same lot" Matrigel "pre-test" recommend organoid`
- QB3 `Matrigel supply shortage Corning backorder 2020 2021 organoid`
- QB4 `"reserve" OR "batch test" Matrigel lot protocol Nature Protocols organoid`
- QB5 `Matrigel lot testing recommendation stem cell protocol STEMCELL Technologies`

### 조사 C — 커뮤니티 VOC 원문 20건+ (URL 필수, 긍정 VOC 포함)
- QC1 `ResearchGate Matrigel lot to lot variation question`
- QC2 `reddit labrats Matrigel lot variability organoid`
- QC3 `reddit cellculture Matrigel expensive alternative`
- QC4 `Biocompare Matrigel review` / `SelectScience Corning Matrigel review`
- QC5 `protocols.io Matrigel lot note` / `Bio-protocol Matrigel comment`
- QC6 `PubPeer Matrigel`
- QC7 `Matrigel "works great" OR "gold standard" researcher blog` ← **긍정 VOC 확보용(편향 방지)**
- QC8 `X/Twitter thread Matrigel organoid frustration`
- QC9 학회 초록: ISSCR / AACR / SLAS / EACR / ESACT

### 조사 D — 전환장벽 정량화 (B1~B6) ← **최우선**
- B1 프로토콜 재검증 비용: `organoid culture optimization time cost per line`, 인건비 단가(BLS/Glassdoor/NIH salary cap), BME 카탈로그가(Agent C 참조)
- B2 종단 비교가능성 상실: `biobank longitudinal organoid drug screening consistency matrix change`
- B3 저널·리뷰어 수용성: `reviewer requested Matrigel control comparison synthetic hydrogel`
- B4 장기별 재최적화: intestinal / hepatic / pancreatic / cerebral / kidney / lung / tumor PDO 각각 별도 논문
- B5 구매 관성: `institutional supply agreement Corning life sciences distributor VWR standing order`
- B6 **효능 격차(가장 위험한 변수)**:
  - `Gjorevski Lutolf 2016 designer matrices intestinal stem cell organoid Nature`
  - `PEG hydrogel intestinal organoid crypt budding efficiency vs Matrigel`
  - `defined matrix organoid failure did not form`
  - `laminin-111 entactin requirement organoid`
  - **성공 사례와 실패 사례를 모두 수집**하여 형성효율(%)로 직접 비교

### 조사 E — 세그먼트별 구매 의사결정
- QE1 `core facility manager purchasing decision cell culture reagent`
- QE2 `pharma preclinical reagent qualification vendor change process`
- QE3 `CRO assay validation reagent lot change client notification`
- QE4 `clinical diagnostic LDT reagent change CLIA validation`
- QE5 `GMP ancillary material change control cell therapy comparability`

## 2. 산출물
| 파일 | 내용 |
|---|---|
| `docs/D_plan.md` | 본 파일 |
| `docs/D_voc_barriers.md` | 본문 + VOC 원문표 + 전환장벽 정량표 + HANDOFF + DoD |
| `evidence/evidence_D.jsonl` | 근거 레코드 (E-200~E-299) |
| `docs/assumptions.md` | append (D-A## 가정) |
| `docs/gaps.md` | append (해당 시) |

## 3. HANDOFF 산출 목표
- `switching_cost_usd_per_lab` (중앙값)
- `switching_time_months`
- `segment_switch_propensity` — 5세그먼트 연간 전환확률(%)
- `must_win_metrics_top5` — 목표수치 + 현 BME 벤치마크

## 4. DoD
1) Lot 편차 정량 5건+ 2) 전환장벽 6항목 USD·개월 3) VOC 원문 20건+ URL 4) must_win_metrics_top5 5) segment_switch_propensity 5개 6) 긍정 VOC 포함
