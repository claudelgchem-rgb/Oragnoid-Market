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
