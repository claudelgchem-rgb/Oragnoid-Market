# Agent F — IP / FTO / 진입장벽 : 작업 계획

작성 2026-08-11 / 근거 ID 범위 **E-500 ~ E-599** / evidence 파일 `evidence/evidence_F.jsonl`
산출물: `docs/F_plan.md`(본 문서), `data/patent_table.csv`, `docs/F_ip_fto.md`, `evidence/evidence_F.jsonl`

---

## 0. 선행 Wave 1 입력 (Read 완료)

| 출처 | 본 조사에 쓰는 입력값 |
|---|---|
| `docs/C_competition.md` §7 | **101Bio Col-Tgel** = 콜라겐/젤라틴 + 트랜스글루타미나제 2액형, $38.90/mL, Fisher/AMSBIO 유통, PLOS One(PMC4136878)로 조성 확증 [E-120][E-164]. → **최우선 선행기술** |
| `docs/C_competition.md` HANDOFF | `mtg_prior_commercial_exists = true` — "Agent F 는 이를 선행기술로 반드시 반영할 것" |
| `docs/C_competition.md` §4 | QGel(EPFL 스핀오프) 정체, Ectica 초기고착, CollPlant 구조조정, denovoMATRIX 제품 단종 → 특허 유지료 포기(abandonment) 가능성 점검 대상 |
| `docs/B_regulatory.md` §6.6 | **Type II DMF 등재 = 영업 자산**(규제 의무 아님). 비특허 진입장벽 분석의 핵심 축 [E-058][E-047] |
| `docs/B_regulatory.md` H2 | 등급 로드맵 RUO(2026) → GMP/DMF(2029) → ATMP(2033). 특허 존속기간과 이 타임라인을 겹쳐 판정 |
| `docs/C_competition.md` §6.2 | defined 대체재 PubMed 침투율 1.95% → citation lock-in 이 비특허 장벽의 최대 항목 |

---

## 1. 조사 7축과 검색 쿼리 목록

### 축 1. mTG 가교 젤라틴/콜라겐 하이드로겔 (**최우선 — 직접 충돌 축**)
- `microbial transglutaminase crosslinked gelatin hydrogel patent`
- `transglutaminase collagen hydrogel cell culture patent Ajinomoto`
- `101Bio Col-Tgel patent transglutaminase collagen 3D culture`
- `Ajinomoto Activa transglutaminase enzyme preparation patent Streptoverticillium`
- `tissue adhesive transglutaminase gelatin patent US`
- Google Patents 검색 URL 직접 fetch: `q=(transglutaminase)+(collagen)+(hydrogel)+(cell+culture)`

### 축 2. 효소 가교 하이드로겔 세포배양 매트릭스 (FXIIIa / PEG)
- `Factor XIIIa crosslinked PEG hydrogel patent Lutolf Hubbell`
- `QGel SA patent hydrogel cell culture`
- `enzymatically crosslinked PEG hydrogel matrix metalloproteinase degradable patent`

### 축 3. Defined organoid culture matrix 조성물
- `defined synthetic organoid culture matrix patent Lutolf EPFL`
- `Cellendes Manchester BIOGEL Ectica TheWell VitroGel patent`
- `Advanced BioMatrix patent collagen`

### 축 4. 재조합 콜라겐 조성물·생산
- `CollPlant recombinant human collagen tobacco plant patent`
- `Fibrogen recombinant collagen patent` / `Evonik recombinant collagen`
- `Geltor Modern Meadow Jellagen recombinant collagen patent`
- `recombinant collagen China patent 江苏 三 collagen`

### 축 5. 오가노이드 배양 배지·프로토콜 (Clevers/Hubrecht) — **만료 계산 축**
- `Clevers Lgr5 stem cell culture medium patent Hubrecht organoid`
- `R-spondin Wnt surrogate patent Surrozen`
- 우선일 → 만료 = 우선일 + 20년(+ PTA/SPC 별도 명시)

### 축 6. Matrigel / BME 및 Corning 방어 포트폴리오
- `Corning Matrigel patent basement membrane matrix`
- `Corning Synthegel patent self-assembling peptide hydrogel`
- `Trevigen Cultrex BME patent` / `Bio-Techne`

### 축 7. LG화학 자체 보유 현황
- Google Patents `q=transglutaminase&assignee=LG+Chem`
- `q=collagen&assignee=LG+Chem` / `q=cell+culture&assignee=LG+Chem`
- LG Household/LG생활건강, LG화학 KR 출원 확인

---

## 2. 검증 원칙 (R2 강화 적용)

1. **특허번호는 반드시 patents.google.com 개별 페이지를 WebFetch 하여 존재를 확인**한 것만 기록한다.
   확인 항목: 권리자(assignee), 우선일(priority date), 등록일(grant date), 만료예상(expiry), 상태(status), 청구항 1.
2. 검색결과 스니펫만 있고 개별 페이지 확인이 안 된 번호는 **테이블에 올리지 않는다.**
3. 만료 추정: `expiry_estimate = priority_date + 20년`을 기본으로 하고,
   Google Patents 가 표시하는 `Anticipated expiration` 이 있으면 그 값을 우선한다(term adjustment 반영값이므로).
4. 접근 실패 URL 은 `access_status:"failed"` 로 남기고 다른 소스로 대체한다.
5. `verified_by` 는 전건 `""`.

---

## 3. 산출 스펙

### `data/patent_table.csv` 컬럼(고정 순서)
```
patent_number,jurisdiction,assignee,priority_date,grant_date,expiry_estimate,status,
claim_gist,relevance_to_us,infringement_risk,design_around_note,url,evidence_id
```
- jurisdiction: US/EP/CN/JP/KR/WO
- status: 등록/출원중/만료/포기
- relevance_to_us: 직접충돌/인접/배경
- infringement_risk: 상/중/하
- 목표 30건 이상

### `docs/F_ip_fto.md` 필수 섹션
0) 결론 요약 + FTO 종합판정
1) Col-Tgel 선행기술 심층분석 (특허 + 문헌)
2) 보유자별 포트폴리오 규모·존속기간·지역 커버리지
3) 만료/만료임박 핵심특허 = 기회 목록
4) 침해 위험 시나리오 3개 (특허–청구항–제품구성 매핑)
5) 회피 설계안 3개
6) 확보 가능한 신규 특허 포지션 (또는 불가 판정)
7) 비특허 진입장벽 (GMP·DMF·citation·유통·브랜드)
8) DoD 셀프체크 + HANDOFF

---

## 4. 판정 기준 (DECISION_GATE 연동)

`AGENT_RULES §0` : `FTO_리스크_허용: "중 이하 (상 = 즉시 No-Go 사유)"`

본 에이전트의 판정 룰(사전 선언 — 결과에 맞춰 사후 조정하지 않는다):

| 판정 | 조건 |
|---|---|
| **상** | 유효·존속 중인 등록특허의 **독립항이 우리 제품의 필수 구성요소 전부를 문언적으로 읽고**, 주요 시장(US 또는 EP) 중 하나 이상에서 회피 설계가 제품 정체성을 훼손하지 않고는 불가능 |
| **중** | 문언 침해 가능 청구항이 존재하나 (a) 조성비/공정조건 한정으로 회피 가능하거나 (b) 만료가 5년 내이거나 (c) 특정 지역만 커버 |
| **하** | 직접충돌 등록특허 없음. 인접·배경 특허만 존재 |

R1 준수: 판정을 유보하지 않는다. 조사 결과가 어느 쪽이든 그대로 쓴다.
