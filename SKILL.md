---
name: policy-planning
description: "정책기획 풀 파이프라인 (Phase 0~3). 리서치프레임→축별리서치→스파인→기획안→제출청소까지 일관 수행. P1: 정책기획, 리서치, 스파인도출, 기획안, 제출청소. P2: 기획안써줘, 캠프전략. P3: policy planning. P5: 옵시디언, 마크다운. NOT: 사업계획서, 재무모델, PT."
"@uses":
  - references/phase0-setup.md
  - references/phase1-research.md
  - references/phase2-plan.md
  - references/phase3-cleanup.md
  - references/campaign-strategy.md
  - references/cross-validation.md
  - references/why-this-skill.md
  - references/framework-axiom.md
  - references/city-types-diagnosis.md
  - references/scope-scaling.md
  - references/gotchas.md
vault_dependency: SOFT
---

# 정책기획 풀 파이프라인 — 허브 라우터

정부·지자체·선거 후보 측의 정책기획을 리서치부터 기획안 완성까지 체계적으로 수행하는 허브 스킬.

**허브+스포크:** 이 파일은 라우터이자 절차 강제기. 각 Phase의 상세 절차·템플릿·도시유형별 가이드는 `references/`에 분리되어 있다.

---

---

## ⛔ 절대 규칙

| # | 규칙 |
|---|------|
| 1 | 발동 조건 외 임의 실행 금지 |
| 2 | 출력 형식 준수 — 내부 라벨 사용자 노출 금지 |
| 3 | UP 존댓말·호칭 규칙 우선 적용 |

### 자체 점검 (self-check)
SKILL.md ≤10KB · P1 ≥5개 · Gotchas 존재 확인 후 수정 완료.

---

## 절차 강제 (ABSOLUTE RULES)

**순서:** Phase 0 → Phase 1 (research-frame 호출) → Phase 2 → Phase 3 → (선거맥락) 캠프 전략

**게이트:**
- Phase 0→1: 리서치프레임 사용자 확인 필수
- Phase 1→2: 스파인 사용자 확인 필수
- Phase 2 완료→3: 13축 제출청소 필수 (→ references/phase3-cleanup.md)
- 6+ 분야 완료→통합: 교차검증 5축 필수 (→ references/cross-validation.md)

**금지 사항:**
1. 폴더 생성 전 리서치·기획안 착수 금지
2. Phase 1 스킵 금지 (리서치 없이 기획안 쓰지 말 것)
3. 스파인 미확정 상태로 Phase 2 진입 금지
4. research-frame에서 역호출 금지 (리서치 메모는 별도 파일로)
5. 기초자치단체에 ABCD 4축 강제 적용 금지 → 3축 선택 분기

---

## 라우팅 테이블

| Phase | 작업 | 참조 | 담당 주체 |
|-------|------|------|----------|
| **0** | 셋업: 행정단위→도시유형→주체DNA→분야 도출→폴더 생성 | phase0-setup.md | Agent |
| **1** | 리서치프레임→축별리서치→스파인 도출 | phase1-research.md + research-frame 호출 | research-frame 호출 |
| **2** | 기획안 (ABCD 또는 3축) | phase2-plan.md | Agent |
| **3** | 제출청소 13축 | phase3-cleanup.md | Agent |
| **+캠프** | 8대 기획안 (선거맥락에서만) | campaign-strategy.md | 캠프 담당자 |
| **+검증** | 교차검증 5축 (6+ 분야에서만) | cross-validation.md | Agent |

---

## 모드 선택 (행정단위 판별)

```
시작 → "행정단위는?" 질문

├─ 광역(시·도)
│  ├─ 문화예술 단일 분야 → ABCD 4축 기획
│  └─ 다분야 → 분야당 3축 기획 + 교차검증
│
└─ 기초(구·시·군)
   └─ 분야당 3축 기획 + 시-구 협력 레버
```

→ 상세: references/framework-axiom.md
→ 도시유형별 진단 프레임: references/city-types-diagnosis.md

---

## 핵심 개념

**스파인의 필요성:**
- 축 3-4개를 단순 병렬 나열하면 "왜 이 묶음인가"라는 질문에 답 못함
- 스파인 = 축들을 관통하는 핵심 서사 1개
- 스파인 없이는 기획안이 구호 나열로 전락

**도시유형에 따른 진단 프레임:**
- 메가시티: 7대 구조적 공백 → 서울
- 항구2등도시: 3대 병목 → 부산
- 광역지역: 3대 위기 → 경남
- 관문도시: 4대 역설 → 인천
- 기초자치단체: 3대 역차별 → 강남구
- 광역메가도: N대 구조이슈 → 경기도

→ 상세: references/city-types-diagnosis.md

**선거 vs 지자체 vs 광역 vs 기초:**
- 맥락에 따라 스파인·축 구조·제출 대상이 완전히 다름
- → references/scope-scaling.md

---

## 스킬 호출 규칙

```
policy-planning (이 스킬)
  ↓ (Phase 1에서 단방향 호출)
research-frame (리서치 위임)
  → 결과: _research/기획메모_[축명].md로 반환
  (역호출 금지)

policy-planning (계속)
  ↓ (필요시 하위 호출)
ceo-pipeline (내부 조직운영 로드맵)
  (역호출 금지)
```

→ 상세: references/why-this-skill.md

---

## 자주 발생하는 함정 (Gotchas)

| 함정 | 해결 |
|------|------|
| 리서치 스킵 ("바로 기획안 써줘") | Phase 1 필수 + 최소 약식 프레임 설계 |
| 스파인 미확정 → 축 나열만 | 스파인 도출 + 사용자 확인 게이트 |
| 기초자치단체에 ABCD 강제 | 행정단위 판별 → 3축 선택 분기 |
| 선거인데 정책만 쓰기 | 8대 기획안 체계 (판세·브랜딩·위기 필수) |
| 6+ 분야에서 수치·용어 불일치 | 교차검증 5축 (예산정합부터) |
| 제출청소를 뒤에 하기 | 작성 시점부터 제출청소 기반 |

→ 전체 목록: references/gotchas.md

---

## 수정 프로토콜

산출물 수정시 **trigger-dictionary §6 수정4 프로토콜** 적용:
1. 레벨 판정 (L1/L2/L3)
2. 게이트 (범위 확인)
3. 외과적 실행 (grep 기반 검사)
4. POST_VERIFY (전파맵 포함)

특히 Phase 2 버전업·Phase 3 제출청소에서 **old 잔존·중복·과삭제 방지** 필수.

## 예시

발동 후 스킬 프로토콜에 따라 단계별 실행 → 산출물 생성.

---

## Gotchas

| 함정 | 대응 |
|---|---|
| Phase 건너뛰기 | 0→1→2→3 순서 준수. 스파인 없이 기획안 금지 |
| 리서치 과잉 수렴 | Phase 1에서 수렴 기준 명확히. 무한루프 방지 |
| 제출청소 생략 | Phase 3 필수. 내부 용어 노출 시 품질 저하 |
| 볼트 외 저장 | 산출물은 반드시 VAULT 하위 경로에만 |
