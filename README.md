# explain_me

**개념부터 사건, 문서, 시스템까지. 이해가 필요한 주제를 근거 있는 시각 설명으로 바꾸는 Agent Skill.**

<picture>
  <source media="(max-width: 600px)" srcset="docs/overview-mobile.svg">
  <img src="docs/overview.svg" alt="explain_me: 질문과 자료를 받아 독자와 목적을 파악하고, 근거를 확인한 뒤, 개념은 관계도·사건은 시간선·비교는 같은 기준·절차는 단계도·시스템은 구조도로 설명합니다. 사실, 해석, 가정, 불확실성을 구분하며 SVG 중심의 요약과 필요한 세부 설명을 제공합니다." width="960">
</picture>

[크게 보기](docs/overview.svg) · [모바일 그림](docs/overview-mobile.svg) · [스킬 지침](SKILL.md)

## 이렇게 요청하세요

```text
Use $explain-me to explain this topic.
```

뒤에 주제와 원하는 독자 수준을 붙이면 됩니다.

| 알고 싶은 것 | 요청 예시 | 설명의 중심 |
| --- | --- | --- |
| 개념·원리 | “캐시가 왜 빠른지 비전공자에게 설명해줘.” | 관계도 + 예시 + 한계 |
| 사건·역사 | “이 기사에 나온 사건의 배경과 전개를 설명해줘.” | 시간선 + 확인된 사실과 해석 |
| 비교·선택 | “이 두 방식의 차이를 같은 기준으로 비교해줘.” | 차이 + 조건별 장단점 |
| 절차·과정 | “이 업무가 어떤 순서로 진행되는지 설명해줘.” | 입력 + 단계 + 분기 + 결과 |
| 문서·주장 | “이 보고서가 무슨 주장을 하는지 설명해줘.” | 주장 + 근거 + 가정 |
| 저장소·시스템 | “이 저장소에서 요청과 데이터가 흐르는 길을 보여줘.” | 구성 + 흐름 + 책임 + 운영 |

## 설명 방식

질문, 텍스트, 링크, 문서, 이미지, 데이터, 저장소를 출발점으로 삼습니다. 지원되는 입력과 실제 자료 접근은 사용하는 호스트의 기능에 따릅니다.

- **독자에 맞게:** 기본은 배경지식이 적은 성인. 언어·목적·깊이를 요청에 맞춥니다.
- **주제에 맞게:** 모든 것을 아키텍처나 장단점 목록에 끼워 맞추지 않습니다.
- **근거를 구분해:** 사실·해석·가정·불확실성과 출처·시점을 따로 다룹니다. 사건의 순서를 인과관계로 단정하지 않습니다.
- **비유는 필요할 때:** 쉽게 설명하되 실제 원리와 비유의 차이를 밝힙니다.
- **읽을 수 있는 결과로:** 핵심 SVG와 필요한 세부 설명을 제공합니다. 복잡하면 나누고, 텍스트만 요청하면 그 형식을 따릅니다.

미리보기 기능이 없는 환경에서는 독립 SVG 파일로 전달합니다. 그림에는 외부 스크립트나 폰트 서비스가 필요하지 않습니다. 위 그림은 이 스킬의 동작 방식을 설명하는 정적 예제입니다.

## 설치와 호출

저장소와 표시 이름은 **`explain_me`**입니다. Agent Skills의 이름 규칙에 맞춘 **호출 ID와 설치 폴더 이름은 `explain-me`**입니다. 기존 `svg-eli5-archify`를 설치했다면 해당 폴더를 `explain-me`로 이름을 바꾸고 업데이트하거나, 새 위치에 설치한 뒤 기존 항목을 비활성화해 중복을 피하세요. 직접 수정한 파일은 먼저 보존하세요.

아래는 개인용 설치 예시입니다. `~`는 홈 디렉터리입니다.

### Codex

```sh
git clone https://github.com/kcc920926-droid/explain_me.git ~/.agents/skills/explain-me
```

```text
Use $explain-me to explain why caching helps, with a simple example.
```

### Claude Code

```sh
git clone https://github.com/kcc920926-droid/explain_me.git ~/.claude/skills/explain-me
```

```text
/explain-me 이 문서의 핵심 주장과 근거를 설명해줘.
```

### Gemini CLI

```sh
gemini skills install https://github.com/kcc920926-droid/explain_me
```

```text
Use explain-me to explain the sequence of events in this article.
```

프로젝트에만 설치하려면 Codex는 `.agents/skills/explain-me`, Claude Code는 `.claude/skills/explain-me`를 사용합니다. Gemini CLI는 설치 명령에 `--scope workspace`를 추가합니다.

설치와 호출은 [Codex 문서](https://developers.openai.com/codex/skills/), [Claude Code 문서](https://code.claude.com/docs/en/skills), [Gemini CLI 문서](https://geminicli.com/docs/cli/using-agent-skills/)를 기준으로 안내합니다. 공통 지침은 이식 가능하도록 작성했으며, 세 호스트에서의 실제 실행을 모두 검증한 것은 아닙니다.

## 구성

| 파일 | 역할 |
| --- | --- |
| [SKILL.md](SKILL.md) | 독자 파악, 설명 구조 선택, 근거 관리, 시각화, 검증의 공통 지침 |
| [references/repository-analysis.md](references/repository-analysis.md) | 저장소·인프라를 설명할 때만 읽는 전문 지침 |
| [agents/openai.yaml](agents/openai.yaml) | 선택 사항인 Codex 표시 이름·설명·기본 프롬프트 |
| [docs/overview.svg](docs/overview.svg) | README의 데스크톱 시각 설명 |
| [docs/overview-mobile.svg](docs/overview-mobile.svg) | 작은 화면에서도 읽을 수 있는 별도 구성 |

저장소 분석에서는 `declared`(설정), `intended`(의도), `recorded`(과거 기록), `observed`(이번 분석 중 실시간 관측)를 계속 구분합니다. 관측 시점을 모르면 모른다고 표시하고, 저장된 기록을 현재 실행 상태처럼 설명하지 않습니다.
