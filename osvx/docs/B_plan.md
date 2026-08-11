# Agent B 작업계획 — 규제·정책 드라이버 & 제품등급 요구사항

작성일: 2026-08-11 / 근거 ID 범위: E-001 ~ E-099 / evidence 파일: `evidence/evidence_B.jsonl`

## 0. 목적
LG화학의 "재조합 콜라겐 + mTG 가교 Defined Organoid Matrix" 가설에 대해
(a) 수요를 만드는 **규제 동인**을 1차 문서로 확정하고,
(b) 제품이 어느 **등급(RUO / GMP / ATMP 원부자재)** 으로 만들어져야 하는지 판정한다.

## 1. 조사 블록 및 쿼리 목록

### B1. FDA Modernization Act 2.0 / 3.0 (입법 원문)
- Q1 `congress.gov S.5002 FDA Modernization Act 2.0 text`
- Q2 `FDA Modernization Act 3.0 H.R. 7248 status`
- Q3 `21 USC 355(i) animal testing "nonclinical test" definition amendment`
- Q4 `FDA Modernization Act 2.0 "does not mandate" organoid qualification`
- 목표: "동물시험 의무 삭제(permissive)" vs "오가노이드 승인(qualification)" 개념 분리. 법조문 원문 인용.

### B2. FDA Roadmap to Reducing Animal Testing (2025-04)
- Q5 `FDA Roadmap Reducing Animal Testing Preclinical Safety Studies April 2025 PDF`
- Q6 `FDA roadmap monoclonal antibody NAM pilot program`
- Q7 `FDA NAM draft guidance 2026` (2025-04 이후 후속 실제 존재 여부 검증)
- Q8 `FDA New Alternative Methods program progress report 2026`
- 목표: 마일스톤/타임라인/초기 modality 확정 + 후속 발표 실재 여부(없으면 "없다"고 기록)

### B3. FDA ISTAND / DDT qualification
- Q9 `FDA ISTAND pilot program accepted submissions list`
- Q10 `ISTAND organ-on-chip liver-chip acceptance`
- Q11 `FDA DDT qualification microphysiological system organoid`
- 목표: 접수/수용 건수 실제 카운트, organoid vs organ-on-chip 상대 위치 정량

### B4. NAM 예산·조직
- Q12 `NIH ODSPI Office of Research Innovation Validation Application budget`
- Q13 `FDA CDER NAM program 2026`
- Q14 `ICCVAM NICEATM 2026 biennial report`

### B5. 국제 규제
- Q15 `ICH S1B(R1) addendum weight of evidence carcinogenicity`
- Q16 `ICH M3(R2) nonclinical safety studies`
- Q17 `OECD GIVIMP guidance in vitro method`
- Q18 `EU Directive 2010/63/EU animal testing phase-out roadmap European Commission 2025`
- Q19 `NMPA China organoid guideline 2025`
- Q20 `PMDA Japan NAM organoid`
- Q21 `MFDS 식약처 오가노이드 가이드라인`

### B6. 원부자재 등급 규제 원문
- Q22 `USP General Chapter <1043> Ancillary Materials cell therapy tier classification`
- Q23 `ISO 20399 ancillary materials cell therapy`
- Q24 `ISO 13022 animal derived tissue risk management`
- Q25 `EudraLex Volume 4 Annex 2 ATMP GMP`
- Q26 `21 CFR Part 1271 HCT/P`
- Q27 `Ph. Eur. 5.2.12 raw materials cell-based`
- Q28 `EMA/410/01 rev 3 TSE minimising risk note for guidance`
- Q29 `USP <85> bacterial endotoxins limit cell therapy EU/mL`
- Q30 `FDA Drug Master File Type IV / DMF for excipient/ancillary material`

### B7. Matrigel 임상 전환 규제 근거 + 반증
- Q31 `Matrigel lactate dehydrogenase elevating virus LDEV contamination`
- Q32 `Corning Matrigel research use only not for clinical`
- Q33 `ClinicalTrials.gov Matrigel intervention` ← 반증 사례 탐색(불리해도 기록)
- Q34 `Matrigel undefined composition proteomics variability lot`

### B8. RUO vs GMP 가격 프리미엄
- Q35 `BioLamina laminin-521 GMP price`
- Q36 `PeproTech / Miltenyi GMP grade cytokine price vs research grade`
- Q37 `recombinant human albumin GMP catalog price`
- Q38 `collagen GMP grade vs RUO price Advanced BioMatrix / Corning`

## 2. 산출물
| 파일 | 내용 |
|---|---|
| `docs/B_plan.md` | 본 파일 |
| `docs/B_regulatory.md` | 본문 + 규제 타임라인 표 + HANDOFF |
| `docs/premise_audit.md` | P1~P5 전제 감사 (Agent B가 최초 작성자) |
| `evidence/evidence_B.jsonl` | 근거 레코드 |
| `docs/assumptions.md` | append (가정) |
| `docs/gaps.md` | append (확정 불가 항목, 4요소 충족 시) |

## 3. HANDOFF 산출 목표
- `nam_ramp`: {conservative, base, aggressive} × {2026, 2030, 2035} NAM 규제제출 사용 비율(%)
- `grade_verdict`: RUO / GMP / ATMP 원부자재 중 1차 타깃
- `gmp_premium_multiple`: RUO→GMP 가격 배수 (실측 3건 중앙값)
- `clinical_timing_year`: 이식용 원부자재 매출 유의미화 최초 연도

## 4. DoD
1) 1차 문서 URL 12건 이상 2) 규제 타임라인 표 3) 등급 판정 1개 4) 전제 5개 검증 5) 전 수치 [E-###] 6) 정량 HANDOFF 3종
