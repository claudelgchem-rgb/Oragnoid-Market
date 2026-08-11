# Agent X — 반증 레드팀(Bear Case) 작업계획

작성일 **2026-08-11** / 근거 ID 범위 **E-700 ~ E-799** / evidence: `evidence/evidence_X.jsonl`
읽지 않은 문서: `docs/R_credibility.md`, `docs/V_audit.md` (AGENT_RULES R3 — R·V·X 상호 비열람)

---

## 0. 임무 정의

이 사업(LG화학 — 재조합 콜라겐 + mTG 가교 Defined Organoid Matrix)을 **죽이는 논리**를 증거와 숫자로 최대한 강하게 만든다. 균형 서술을 하지 않는다. 다만 **증거 없는 비관도 실패**이므로 모든 반증에 (i) 실제 접근한 URL, (ii) SOM(2030) 삭감액·삭감률 계산식, (iii) 참일 확률과 근거를 붙인다.

### 0.1 baseline (선행 확정값 — 이 값을 깎는다)

| 항목 | 값 |
|---|---:|
| SOM_2030 | 747,000 USD / 21.6 L |
| SOM_2035 | 2,024,000 USD / 61.9 L |
| SAM_adjusted_2030 | 10,080,000 USD |
| bull_SOM_2030 | 3,920,000 USD |
| GM60 임계물량 | 191.8 L/년 |
| BEP | 61.8 L/년 |
| CAPEX | 13,731,000 USD |
| G 옵션(b) 채택 시 | SOM_2030 = 8,670,000 USD / 467.2 L, 192 L 를 2028년 통과 |

### 0.2 두 갈래 공격

- **(i) base case 추가 삭감** — H1~H10
- **(ii) G 의 구제책 정면 공격** — H11(재정의 옵션 b), H12(서비스 상쇄). **여기가 승부처**: base 는 이미 게이트를 크게 미달하므로, 사업의 생사는 구제책의 성립 여부가 결정한다.

---

## 1. 반증 가설 12개와 조사 쿼리

| # | 가설 | 핵심 조사 쿼리 |
|---|---|---|
| H1 | NAM 수요가 오가노이드가 아니라 organ-on-chip/MPS/in silico 로 흡수 | `FDA ISTAND accepted submissions 2026`, `Simulations Plus revenue FY2025`, `Certara revenue growth 2025`, `Emulate Organ-Chip FDA qualification`, `MPS funding 2025` |
| H2 | Defined matrix 가 BME 대비 효능 미달 (실증 문헌) | `synthetic hydrogel organoid forming efficiency versus Matrigel`, `PEG hydrogel intestinal organoid efficiency %`, `defined matrix organoid inferior` |
| H3 | 학계 관성 — Matrigel 인용 lock-in, 리뷰어 수용성 | `Matrigel publications trend 2020 2025`, `why researchers keep using Matrigel`, PubMed esearch 카운트 |
| H4 | Corning/Thermo/Bio-Techne 즉시 가격 대응 여력 (10-K GM%) | `Corning 10-K gross margin 2025`, `Thermo Fisher gross margin 2025`, `Bio-Techne gross margin FY2025`, `Corning Synthegel price` |
| H5 | 중국 저가 진입 확대 | `Yeasen Ceturegel price`, `中国 类器官 基质胶 价格`, `Bioperfectus / Abwell / OrganoidSciences China matrix` |
| H6 | 재조합 콜라겐 GMP 실단가 — E 의 "ASP 의 0.50%" 검증 | `GMP recombinant collagen price per gram`, `medical grade recombinant collagen cost`, `Evonik/Jellagen/Geltor GMP collagen pricing` |
| H7 | mTG 가교의 기술적 한계 (문헌) | `transglutaminase crosslinking laminin LG domain`, `mTG cytotoxicity cell viability crosslink density`, `collagen triple helix glutamine lysine accessibility transglutaminase`, `mTG residual removal immunogenicity` |
| H8 | ATMP 원부자재 등재 기간 과소평가 | `Type II DMF review time FDA`, `ancillary material qualification timeline cell therapy`, `USP <1043> ancillary materials` |
| H9 | 시장보고서 편차 배수 (양방향 — A 의 bottom-up 과소추정 가능성도) | `organoid market size 2025 report`, `3D cell culture market size`, `Matrigel market size` |
| H10 | LG화학 내부 요인 — 최소 사업규모 미달 | `LG화학 생명과학본부 매출 영업이익 2025`, `LG Chem Life Sciences division revenue`, `LG화학 사업 철수 기준` |
| H11 | ★ G 재정의 옵션(b) 공격 — 바이오잉크·비오가노이드 확장 | `bioink market size 2025`, `CELLINK BICO revenue 2025`, `Advanced BioMatrix bioink`, `Rousselot X-Pure GelMA`, `collagen bioink printability limitation` |
| H12 | ★ G 서비스 상쇄 전략 공격 — 서비스 인력비의 SG&A 회귀 | `field application scientist salary 2025`, `technical support cost per customer life science`, `SG&A % life science tools company` |

---

## 2. 산출물

1. `docs/X_plan.md` (본 문서)
2. `docs/X_redteam.md` — 반증 12건 + Kill Criteria 5개 + Bear-case SOM + 실패확률 + 최강 반증 지목 + DoD 표
3. `evidence/evidence_X.jsonl` — E-700~E-799, `verified_by:""`, `access_date:"2026-08-11"`

## 3. 정량 임팩트 계산 규약 (R4)

```
각 반증 Hk 에 대해
  삭감계수 f_k ∈ (0,1]  = 반증이 참일 때 SOM_2030 에 곱해지는 잔존 비율
  삭감액   = 747,000 × (1 − f_k)   [USD]
  삭감률   = (1 − f_k) × 100        [%]
  참일확률 p_k = 주관 확률(근거 명시)

Bear-case SOM(2030)
  독립 가정 : SOM_bear = 747,000 × Π_k [ 1 − p_k × (1 − f_k) ]
  상관 보정 : 동일 메커니즘을 두 번 세지 않도록 클러스터별 최대값만 반영 (근거 명시)
```

## 4. Kill Criteria 형식

`[측정 대상 / 측정 방법 / 임계값 / 확인 시점(개월) / 담당]` — 모호 서술 금지.

## 5. DoD

1) 반증 10건 이상 각각 실제 URL 2) 각 반증 정량 임팩트(삭감액·률·계산식) 3) 각 반증 참일 확률 4) Kill Criteria 5개 5) Bear-case SOM(2030) 6) G 구제책 2건 정면 공격 7) 웹호출 40회 이상
