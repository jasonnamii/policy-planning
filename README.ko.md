# 정책기획 풀 파이프라인

> 🇺🇸 [English README](./README.md)

**리서치에서 제출까지 풀 정책기획 파이프라인 — 6개 실제 정부 및 캠프 프로젝트 기반**

## 사전 요구사항

- **Obsidian Vault** — 기획 문서는 기본으로 Obsidian 호환 `.md`로 출력
- **Claude Cowork 또는 Claude Code** 환경

## 목적

정책 업무는 리서치, 이해관계자 매핑, 법적 제약, 정치 전략 전반에 걸친 엄밀함을 요구합니다. Policy-Planning은 정부 및 캠프 프로젝트로부터의 실제 패턴을 기반으로 전체 파이프라인을 간소화합니다. 다양한 정책 맥락을 위한 캠프 전략 템플릿 (8개)을 통합합니다.

## 사용 시점 및 방법

정책 리서치 개시, 정책 제안 작성, 정책 캠프 기획 시 이 스킬을 사용하세요. 스킬은 완전한 파이프라인을 실행합니다: 다축 조사를 위한 research-frame 통합 → 축별 리서치 → 핵심 주장을 위한 스파인 추출 → 제안 작성 → 제출 청소. 정책 질문 입력 → 제출 준비 완료된 제안.

## 사용 예시

| 상황 | 프롬프트 | 결과 |
|---|---|---|
| 환경 규제 | `"policy-planning: draft proposal for carbon pricing"` | 선례 리서치→이해관계자 매핑→스파인 추출→제안 초안→제출 준비 |
| 기관 규칙 제정 | `"Policy-planning: data privacy rule for healthcare IoT"` | 법적/기술 리서치→축 분석→핵심 주장→공식 규칙 제안 |
| 투표 안건 전략 | `"Campaign plan for housing zoning reform"` | 캠프 템플릿: 리서치→메시징→이해관계자 연합→승인 경로 |

## 핵심 기능

- 완전한 파이프라인: research-frame → 이해관계자/영향/선례 축 → 스파인 추출 → 제안 작성 → 제출 청소
- 다양한 정책 맥락을 위한 8개 캠프 전략 템플릿
- 6개 실제 정부 및 캠프 프로젝트로부터의 패턴 기반
- 다중 이해관계자 영향 분석 통합
- 법적 및 정치 제약 매핑


## 연관 스킬

- **[research-frame](https://github.com/jasonnamii/research-frame)** — policy-planning은 research-frame을 기반 단계로 활용합니다
- **[deliverable-engine](https://github.com/jasonnamii/deliverable-engine)** — deliverable-engine은 제안 및 정책 브리프 포맷
- **[trigger-dictionary](https://github.com/jasonnamii/trigger-dictionary)** — trigger-dictionary 도구는 의사결정 게이트 정보 제공

## 설치

```bash
git clone https://github.com/jasonnamii/policy-planning.git ~/.claude/skills/policy-planning
```

## 업데이트

```bash
cd ~/.claude/skills/policy-planning && git pull
```

`~/.claude/skills/`에 배치된 스킬은 Claude Code 및 Cowork 세션에서 자동으로 사용할 수 있습니다.

## Cowork 스킬 생태계

25개 이상의 커스텀 스킬 중 하나입니다. 전체 카탈로그: [github.com/jasonnamii/cowork-skills](https://github.com/jasonnamii/cowork-skills)

## 라이선스

MIT 라이선스 — 자유롭게 사용, 수정, 공유하세요.
