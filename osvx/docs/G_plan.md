# Agent G — 작업계획 (사업모델 · GTM · 파트너십)

작성일 **2026-08-11** / 근거 ID 범위 **E-600 ~ E-699** / evidence: `evidence/evidence_G.jsonl`
산출물: `docs/G_plan.md`(본 문서), `docs/G_gtm.md`(본편), `evidence/evidence_G.jsonl`

---

## 0. 출발 전제 (선행 Wave 1·2 확정치 — 낙관 금지)

| 축 | 확정치 | 출처 |
|---|---|---|
| A 시장 | TAM 2030 89.20 M USD / 2,708.5 L · SAM_adj 2030 10.08 M / 296.5 L · SOM 2030 0.747 M / **21.6 L** · SOM 2035 2.024 M / **61.9 L** · bull 2035 299.7 L | `docs/A_market_sizing.md` |
| E 원가 | COGS 5.368 USD/mL @500 L · GM 83.2% @ASP 32.00 · **GM60 임계 191.8 L/년** · BEP 61.8 L/년 · CAPEX 13.731 M · 라미닌 첨가 시 +110.96 USD/mL | `docs/E_cogs.md` |
| C 가격 | asp_bme 48.24 · asp_defined 60.47(p=0.168 무의미) · **Col-Tgel 38.90 = 실질 상한** · 중국 21.30 · 유통마크업 35.9% · BME 3사 78% | `docs/C_competition.md` |
| D 고객 | switching_cost 56,810 USD/랩 · 12개월 · 전환확률 학술6.0/제약8.3/CRO2.7/진단3.2/GMP25.0 %/년 · citation lock-in 1.95% | `docs/D_voc_barriers.md` |
| B 규제 | 규제는 defined 수요를 강제하지 않음 · RUO 우선 · GMP 2029~ · ATMP 2033~ · gmp_premium 1.85× | `docs/B_regulatory.md` |
| F IP | FTO '중'(통과) · 광의 조성물 특허 불가, 협의 5포지션 · 라미닌-111 무첨가 필수 · 2030-02 Clevers 만료 | `docs/F_ip_fto.md` |

**구조적 모순 (본 문서가 풀어야 할 문제)**
```
E 의 GM60 게이트 임계물량 = 191.8 L/년
A 의 SOM              2030 = 21.6 L/년  (임계의 11.3%)
                      2035 = 61.9 L/년  (임계의 32.3%)
→ 현 제품정의·현 GTM 으로는 GM 게이트에 영구 미달.
→ G 의 임무는 "어떤 채널·어떤 고객·어떤 제품정의라면 192 L 에 도달하는가" 를 정량으로 답하는 것.
```

---

## 1. 조사 쿼리 목록 (실제 WebSearch/WebFetch ≥ 40회)

### Q군 1 — 채널 (유통 OEM · 계약구조)
1. `Thermo Fisher OEM supplier partnership program life science reagents`
2. `Avantor VWR supplier onboarding distributor agreement margin`
3. `Merck Sigma-Aldrich third party product distribution agreement`
4. `Bio-Techne distribution partnership hydrogel matrix`
5. `Fisher Scientific channel partner program cell culture reagent`
6. `TheWell Bioscience VitroGel distributor Fisher BioCat` (선행 [E-111] 재확인)
7. `contract manufacturing organization organoid media matrix supply agreement`

### Q군 2 — 앵커 고객 실존 확인 (20곳 이상)
8. `Hubrecht Organoid Technology HUB Organoids 2026 news`
9. `Crown Bioscience organoid services 2026`
10. `Xilis Inc 2026 status funding`
11. `Vivodyne funding 2025 2026 lab automation human tissue`
12. `Cellesce acquired Molecular Devices organoid`
13. `Molecular Devices organoid innovation center`
14. `STEMCELL Technologies IntestiCult organoid revenue employees`
15. `Definigen 2026 status`
16. `Emulate Inc organ-on-chip 2026 layoffs funding`
17. `CN Bio Innovations 2026`
18. `SUN bioscience Gri3D 2026`
19. `Certis Oncology Solutions 2026`
20. `Champions Oncology organoid PDX revenue FY2026`
21. `Charles River Laboratories organoid 3D model services`
22. `Labcorp / Evotec organoid panel service`
23. `오가노이드사이언스 2026 매출 투자`
24. `넥스트앤바이오 2026`
25. `강스템바이오텍 2026 실적`
26. `티앤알바이오팹 2026 실적 바이오잉크`
27. `국립암센터 오가노이드 뱅크` / `서울아산병원 오가노이드`
28. `한국생명공학연구원 KRIBB 오가노이드 센터`
29. `NCI Patient-Derived Models Repository PDMR organoid`
30. `Human Cancer Models Initiative HCMI models count`

### Q군 3 — 재정의 옵션 (인접시장 실측)
31. `cultivated meat scaffold market size report`
32. `bioink market size 2025 2030 report`
33. `3D bioprinting market size`
34. `regenerative medicine scaffold market size collagen`
35. `recombinant collagen market size 2025`
36. `cell culture media market size Korea LG Chem`
37. `LG화학 생명과학본부 매출 2025` / `LG Chem Life Sciences segment revenue`
38. `cosmetic ingredient recombinant collagen market China Giant Biogene revenue`

### Q군 4 — 파트너십 / M&A 후보
39. `denovoMATRIX 2026 status acquisition`
40. `CollPlant 2026 restructuring cash runway`
41. `Evonik / Geltor / Jellagen recombinant collagen supplier`
42. `Trautec 巨子生物 recombinant collagen capacity`
43. `laminin alternative peptide E8 fragment supplier Nippi Matrixome`
44. `Humabiologics / Advanced BioMatrix BICO acquisition`

### Q군 5 — 가격/전환 실증
45. `core facility organoid matrix recharge rate price`
46. `Matrigel bulk purchase agreement institutional discount`

---

## 2. 산출 구조 (docs/G_gtm.md)

| 절 | 내용 | DoD 항목 |
|---|---|---|
| §1 | 채널 옵션 5개 정량 비교표 + 각 채널의 192 L 도달 연도 | DoD-1 |
| §2 | 앵커 고객 실명 20+ (URL·실존확인·물량·우선순위) + 물량 합산 vs 192 L | DoD-2 |
| §3 | 5개 세그먼트 점수표 (4인자 정량 가중) + 1위 선언 | DoD-3 |
| §4 | 재정의 옵션 (a)~(e) 5안 정량 평가 + 순위 | DoD-4 |
| §5 | 제품 라인업 3단계 로드맵 (CAPEX 13.731 M 배분) | DoD-5 |
| §6 | 파트너십/M&A 옵션 (기술도입·채널·인수) | — |
| §7 | 가격 전략 — 전환비용 상쇄 할인율 계산 + E GM 양립성 검증 | DoD-6 |
| §8 | HANDOFF + DoD 셀프체크 | DoD-7 |

---

## 3. 계산 규칙 (R4 준수)

```
채널 도달물량(ch, t)  = Σ_고객군 (고객수 × 채널침투율 × 고객당 mL/년) / 1000  [L]
192 L 도달연도        = min{ t : 도달물량(ch,t) ≥ 191.8 }  (미도달 시 "도달불가" 명시)
세그먼트 점수         = w1·정규화(1/switching_cost) + w2·정규화(switch_propensity)
                       + w3·정규화(defined요구도) + w4·정규화(가격수용도) + w5·정규화(TAM2030)
필요 할인율           = 전환비용 56,810 / (연간사용량 mL × 현단가 USD/mL × 회수기간 년)
```

## 4. 준수 사항
- R1: "추후/향후/범위 밖/TBD" 금지. 모르는 값은 조사 → 가정 → 계산 완료 후 `docs/assumptions.md` 에 `## [G]` 섹션으로 **append**.
- R2: 신규 근거는 **E-600~E-699** 만. `verified_by:""`, `access_date:"2026-08-11"`. URL 날조 금지, 실패는 `access_status:"failed"`.
- R4: 전 파생수치 계산식 병기.
- R5: 사용자 전제 검증 결과는 `docs/premise_audit.md` 에 `## [G]` append.
