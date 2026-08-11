# OSVX — 전 에이전트 공통 규칙 (Agent O 발행)

작업 루트: `/home/user/Oragnoid-Market/osvx`
오늘 날짜(access_date 기본값): **2026-08-11**

---

## §0. 프로젝트 파라미터

```yaml
주체: "LG화학 (생명과학/바이오소재)"
제품가설: "재조합/정제 콜라겐(single + triple 혼합) + 효소(mTG) 가교 기반 Defined Organoid Matrix"
보유자산: ["GMP급 microbial transglutaminase (mTG/eMTG)", "콜라겐 소재 접근성", "GMP 발효·정제 인프라"]
대체대상: "Corning Matrigel / Cultrex(UltiMatrix) / Geltrex 등 BME(마우스 EHS 육종 유래)"
핵심가설_고객페인: "BME의 비-defined 조성 + Lot-to-Lot 편차 + 마우스 유래 이종성분 + 임상 전환 불가"
지역: ["Global","US","EU","China","Japan","Korea"]
세그먼트: ["학술연구(RUO)","제약 전임상 NAM 스크리닝","오가노이드 CRO/바이오뱅크","임상진단(PDO 약물감수성)","재생의료/이식용(GMP)"]
기준연도: 2025 / 예측: 2026, 2030, 2035
통화: USD (보조 KRW, 환율 명시 — 2026년 기준 사용 환율을 근거와 함께 명시할 것)
DECISION_GATE:
  SAM_2030_최소: 150,000,000 USD
  SOM_2030_최소: 15,000,000 USD
  Gross_Margin_최소: 0.60
  Payback_최대년: 5
  FTO_리스크_허용: "중 이하 (상 = 즉시 No-Go 사유)"
```

---

## §1. 절대 규칙 (위반 시 산출물 폐기·재실행)

### R1. No-Deferral Rule — 절대 미루지 않는다
- 금지: "추후 조사 필요", "심층 분석 권장", "데이터 확보 시 업데이트", "본 보고서의 범위를 벗어남", "추가 검증이 요구됨"
- 모르는 값 → **조사한다** → 그래도 없으면 → **가정을 세우고 계산까지 완료** 후 `docs/assumptions.md`에 `[가정ID / 가정값 / 근거 / 민감도 영향]` 추가(append).
- 빈칸 금지. 사용자에게 되묻지 않는다.
- "확정 불가" 선언 조건(4요소 전부 필요, `docs/gaps.md`에 append):
  ① 시도한 검색 쿼리 5개 이상 ② 확인한 소스 8개 이상 ③ 왜 존재하지 않는지 판단 ④ 대체 추정치 + 오차범위

### R2. Evidence-Chip Rule — 모든 사실에 근거 ID
- 모든 수치·주장·인용에 `[E-###]` 인라인 표기.
- 자기 전용 파일에만 적재: `evidence/evidence_<AGENT>.jsonl` (1줄 1 JSON 레코드, 아래 스키마 엄수)
```json
{"id":"E-001","claim":"...","value":"...","unit":"...","source_title":"...","publisher":"...","url":"https://...","access_date":"2026-08-11","source_type":"공시|규제문서|학술논문|시장보고서|기업카탈로그|업계인터뷰|추정","tier":"T1|T2|T3","confidence":"상|중|하","verified_by":"","note":"...","access_status":"ok|failed"}
```
- **`verified_by` 필드는 반드시 빈 문자열 `""`로 둔다** (Agent R만 채운다 — R3).
- **URL 날조는 최악의 실패.** 실제 WebSearch/WebFetch로 접근한 URL만 기록. 접근 실패 시 `access_status:"failed"`로 남기고 다른 소스를 찾는다.
- `source_type:"추정"`인 레코드는 url 대신 계산 근거를 note에 쓰되, url 필드에는 그 추정의 입력이 된 대표 URL을 넣는다(없으면 `"internal:calc"`).

### R3. Independent Verification Rule
- 조사 에이전트는 **자기 근거의 신뢰도를 자기가 확정하지 못한다.** `confidence`는 초안값이며 Agent R이 재판정한다.
- R·V·X는 서로의 결론을 읽지 않는다.

### R4. Show-Your-Math Rule
- 모든 파생 수치는 `계산식 = 입력1 [E-###] × 입력2 [E-###] × ...` 형태로 재현 가능하게 기술.
- 출처 없는 "업계 통설 CAGR" 사용 금지. CAGR은 **계산해서 도출**한다.
- 시장규모는 Bottom-up / Top-down / Proxy 3경로 삼각측량 필수, 경로 간 편차 2배 초과 시 `gaps.md`에 원인 분석.

### R5. Premise-Audit Rule
- 사용자 전제를 참으로 가정하지 않는다. 1차 문서로 검증하고 차이를 `docs/premise_audit.md`에 "사용자 전제 → 실제 확인 사실 → 사업적 함의 차이"로 기록.

### R6. 게이트 통과 전 완료 선언 금지

### 금지 표현 (등장 시 자동 실패)
`추후 검토`, `향후 과제`, `범위를 벗어남`, `데이터 부족으로 생략`, `일반적으로 알려진 바에 따르면`, `업계에서는`(출처 없음), `TBD`, 사유 미기재 `N/A`, 근거 미기재 `추정됨`
- 불가피하게 `N/A`를 써야 하면 반드시 `N/A(사유: ...)` 형태로.
- 근거 없는 형용사(`압도적`, `혁신적`, `획기적`) 금지.

---

## §2. 근거 ID 배정 (충돌 방지 — 자기 범위 밖 ID 사용 금지)

| Agent | ID 범위 | evidence 파일 |
|---|---|---|
| B (규제) | E-001 ~ E-099 | `evidence/evidence_B.jsonl` |
| C (경쟁·가격) | E-100 ~ E-199 | `evidence/evidence_C.jsonl` |
| D (VOC·장벽) | E-200 ~ E-299 | `evidence/evidence_D.jsonl` |
| A (시장규모) | E-300 ~ E-399 | `evidence/evidence_A.jsonl` |
| E (원가) | E-400 ~ E-499 | `evidence/evidence_E.jsonl` |
| F (IP/FTO) | E-500 ~ E-599 | `evidence/evidence_F.jsonl` |
| G (GTM) | E-600 ~ E-699 | `evidence/evidence_G.jsonl` |
| X (레드팀) | E-700 ~ E-799 | `evidence/evidence_X.jsonl` |
| S (통합) | E-800 ~ E-849 | `evidence/evidence_S.jsonl` |

선행 에이전트의 `[E-###]`를 **인용**하는 것은 자유(권장). 새로 **생성**할 때만 자기 범위를 쓴다.

---

## §3. 작업 절차 (모든 에이전트 공통)

1. 시작 시 `docs/<AGENT>_plan.md`에 작업계획(조사 쿼리 목록 포함)을 쓴다.
2. **실제 WebSearch / WebFetch를 최소 25회 이상 수행**한다. 기억에 의존한 서술 금지.
   - PDF URL을 WebFetch하면 파일로 저장된다 → `Read` 툴로 그 경로를 읽으면 본문을 볼 수 있다.
3. 선행 Wave 산출물(`docs/*.md`, `data/*.csv`)을 먼저 **Read**하고 그 수치를 입력으로 쓴다.
4. 산출 문서를 쓴다 (한국어, 고유명사·단위 원문 병기).
5. `evidence/evidence_<AGENT>.jsonl` 적재.
6. 필요 시 `docs/assumptions.md`, `docs/gaps.md`에 **append**(기존 내용 삭제 금지 — 파일이 없으면 생성).
7. 문서 말미에 **DoD 셀프 체크리스트**를 표로 붙이고 전 항목 PASS 여부를 적는다.
8. 최종 응답(반환값)은 아래 JSON 스키마를 따른다.

## §4. 파일 동시성 규칙
- 각 에이전트는 **자기 소유 파일만** 생성/수정한다.
- `docs/assumptions.md`, `docs/gaps.md`는 공유 append 파일이다. 반드시 다음 방식으로 **추가만** 한다:
  `bash -c 'cat >> /home/user/Oragnoid-Market/osvx/docs/assumptions.md <<"EOF" ... EOF'`
  섹션 헤더는 `## [<AGENT>] ...`로 시작할 것.
- `evidence/evidence.jsonl`(병합본)은 Agent O가 만든다. 직접 쓰지 말 것.

## §5. 반환 JSON 스키마
```json
{"agent":"B","status":"done|failed","artifacts":["docs/B_regulatory.md","evidence/evidence_B.jsonl"],
 "evidence_count":42,"web_calls":37,"dod":[{"item":"...","pass":true,"note":"..."}],
 "key_findings":["...최대 8개, 각각 수치+[E-###] 포함..."],
 "handoff":{"임의 키":"후행 에이전트가 쓸 핵심 수치"},
 "unresolved":["gaps.md에 기록한 항목 ID"]}
```
