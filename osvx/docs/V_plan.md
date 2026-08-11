# Agent V — 내부 정합성·완결성 감사 작업계획

작업 루트: `/home/user/Oragnoid-Market/osvx`
작성일: 2026-08-11
역할: 내부 논리·수치 정합성 감사 (외부 근거 신뢰도는 감사 대상 아님 — Agent R 소관)

---

## 0. 격리 선언 (R3 준수)

본 감사는 다음 파일을 **읽지 않는다**:

| 파일 | 소유 | 사유 |
|---|---|---|
| `docs/R_credibility.md` | Agent R | R3 상호 독립 검증 |
| `docs/X_redteam.md` | Agent X | R3 상호 독립 검증 |
| `evidence/evidence_verified.jsonl` | Agent R | R3 |
| `evidence/evidence_rejected.jsonl` | Agent R | R3 |

또한 본 감사는 **새 근거 ID(`E-###`)를 생성하지 않는다.** 기존 문서에 기재된 `[E-###]`는 인용만 한다.
근거의 **외부 신뢰도(tier/confidence/URL 실재성)는 판정 대상에서 제외**한다. 오직 **문서 간 수치 일치·계산 재현성·논리 연결**만 본다.

또한 본 감사는 **타 에이전트 문서를 수정하지 않는다.** 산출물은 수정 **지시서**(`docs/V_audit.md` §7)뿐이며, 반영은 Agent S / W 가 수행한다.

---

## 1. 감사 대상

### 문서
`docs/A_market_sizing.md`, `docs/B_regulatory.md`, `docs/C_competition.md`, `docs/D_voc_barriers.md`, `docs/E_cogs.md`, `docs/F_ip_fto.md`, `docs/G_gtm.md`, `docs/premise_audit.md`, `docs/assumptions.md`, `docs/gaps.md`

### 데이터
`data/price_table.csv`, `data/patent_table.csv`, `data/market_model_output.csv`, `data/cogs_output.csv`

### 코드
`model/market_model.py`, `model/cogs_model.py`

---

## 2. 감사 절차 (7단계)

### 단계 V-1. 수치 정합성 크로스체크
- **방법**: 각 문서의 핵심 수치를 추출 → 동일 개념 수치를 문서 간 대조 → **직접 재계산(bash/python3)으로 검산**
- 검산 항목:
  - (a) A 의 시장규모 단가 vs `price_table.csv` 실측 단가 (평균·중앙값 직접 계산)
  - (b) A 의 물량(L/년) × 단가 = 금액 (직접 곱셈)
  - (c) E 의 COGS + C 의 ASP → GM% 재계산 vs E 문서 GM%
  - (d) G 의 제안 ASP vs E 의 COGS 대비 목표 GM 충족 여부
  - (e) TAM/SAM/SOM 포함관계, addressable subset 이중곱 여부
  - (f) 연도 기준·통화·환율·단위 정합성

### 단계 V-2. 교차충돌 3건 판정 (최우선)
`run_state.json` `critical_collisions` 참조.
- **COL-01**: E `min_volume_L_for_GM60 = 191.8 L/년` vs A `SOM_2030_L = 21.6 L` / SOM_2035_L vs G `volume_192L_year = 2042`
  → 세 수치 각각의 **가정 스택을 추출**하여 표로 비교, 정합/비정합 판정 + 원인 귀속
- **COL-02**: D "모든 합성 매트릭스가 외인성 라미닌 필수" vs E "라미닌 시 COGS +110.96 USD/mL"
  → A/G 의 매출 추정이 라미닌 무첨가를 **명시적으로 전제**하는지 문서 grep 으로 확인
- **COL-03**: C `Col-Tgel 38.90 USD/mL 상용` vs G `ASP 32.00 USD/mL` vs F `광의 특허 불가`
  → 3자 정합성 판정 + GM/신규성 연쇄 영향 계산

### 단계 V-3. 모델 코드 실행 검증
```bash
python3 model/market_model.py
python3 model/cogs_model.py
```
- 실행 성공 여부, 출력 수치 vs 문서 기재 수치 대조
- 출력 CSV(`market_model_output.csv`, `cogs_output.csv`) 재생성분과 커밋본 diff
- 불일치 전건 기록

### 단계 V-4. 과신 언어 탐지 (최소 10건)
- 단정형 어미(`~이다`, `~한다`, `확실히`, `반드시`, `명백히`, `필연적`, `불가능하다`) 중
  근거가 `T3` / `source_type:"추정"` / `assumptions.md` 가정인 것을 추출
- **원문 → 수정안** 쌍으로 제시 (확률/조건/범위 표현으로 하향)
- **역방향도 동일 적용**: 근거 없는 비관("사업 붕괴", "성립 불가")도 조건부로 교정

### 단계 V-5. 금지 표현 스캔
AGENT_RULES.md §1 금지 목록을 `grep -n` 으로 **실제 실행**:
`추후 검토`, `향후 과제`, `범위를 벗어남`, `데이터 부족으로 생략`, `일반적으로 알려진 바에 따르면`, `업계에서는`, `TBD`, 사유 미기재 `N/A`, 근거 미기재 `추정됨`, `압도적`, `혁신적`, `획기적`
- `파일:줄번호:문장` 전건 리스트업 + 수정안
- 본인 문서 `V_audit.md` / `V_plan.md` 는 위반 인용이 불가피하므로 **스캔 제외** (명시)

### 단계 V-6. DoD 누락 스캔 (선언 vs 실제 카운트)
| 선언 | 검증 방법 |
|---|---|
| F "특허 N건" | `data/patent_table.csv` 실제 행 수 카운트 |
| C "제품 N개" | `data/price_table.csv` 실제 행 수 카운트 |
| D "VOC N건" | 문서 내 실제 인용 수 카운트 |
| A "3경로 병기" | Bottom-up/Top-down/Proxy 3개 존재 확인 |
| 각 문서 evidence_count | `evidence_<AGENT>.jsonl` 행 수 카운트 |
- **웹호출 횟수(`web_calls`)는 사후 검증 불가 → 검증 대상에서 제외하고 그 사실을 문서에 명시**

### 단계 V-7. 논리 비약 탐지 (최소 6건)
탐색 패턴:
- "TAM 이 크다 → 우리가 먹는다" (점유율 근거 결손)
- "규제가 바뀐다 → 수요가 생긴다" (규제-구매 연결 결손)
- "기술적으로 가능하다 → 고객이 산다" (전환의사 결손)
- "부실기업이 싸다 → 인수하면 이득" (자산 잔존가치 결손)
- "특허 만료 → 시장 개방" (실시 역량 결손)
- "COGS 낮다 → 이익 난다" (물량 도달 결손)
각 건에 대해 **빠진 전제(missing premise)를 명시적 문장으로 복원**

---

## 3. 산출물

| 파일 | 내용 |
|---|---|
| `docs/V_plan.md` | 본 문서 |
| `docs/V_audit.md` | 감사 결과 + `## 필수 수정 항목` 수정 지시서 |

`docs/V_audit.md` 말미에 필수 수록:
- `## 필수 수정 항목` 표: `| # | 파일 | 위치(줄/절) | 현재 서술 | 수정 요구 | 심각도(상/중/하) |`
- 심각도 '상' 항목은 **무엇을 어떻게 고칠지 구체적 대체 문장까지** 기재
- DoD 셀프체크 표 (7항목)

---

## 4. 감사 원칙 (사용자 선호 반영)

1. **과장된 확신은 하향 교정한다.** 듣기 좋은 결론이 아니라 틀린 전제를 잡는 것이 목적.
2. **근거 없는 비관도 동일하게 교정 대상이다.** "붕괴", "불가능"도 조건·확률로 환원한다.
3. **검산은 직접 한다.** 문서에 적힌 계산식을 그대로 믿지 않고 `python3` 로 재계산한다.
4. **판정은 유보하지 않는다.** 정합/비정합 중 하나를 반드시 선택하고 근거를 남긴다.
5. **타 문서를 고치지 않는다.** 지시서만 만든다.

---

## 5. DoD 예정 항목

1. 모순 항목 전건 목록 + 수정 요구
2. 과신 표현 수정 로그 10건 이상 (원문→수정안)
3. 금지표현 grep 결과 (0건이면 증빙 명령·출력 첨부)
4. 모델 코드 2종 실행 검증 결과
5. DoD 주장 vs 실제 카운트 대조표
6. 논리 비약 6건 이상 + 빠진 전제 복원
7. 교차충돌 3건(COL-01/02/03) 판정
