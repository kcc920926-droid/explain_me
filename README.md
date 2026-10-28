# explain_me

**개념부터 사건, 문서, 시스템까지. 이해가 필요한 주제를 근거 있는 시각 설명으로 바꾸는 Agent Skill.**

시각 설명은 **보는 방식과 디자인을 직접 골라** 완성합니다. 호스트 내부 미리보기와 HTML 갤러리 중에서 선택하고, 주제에 맞는 여러 시안을 비교하세요.

<picture>
  <source media="(max-width: 600px)" srcset="docs/overview-mobile.svg">
  <img src="docs/overview.svg" alt="explain_me: 질문과 자료에서 독자·목적·근거를 파악하고 주제에 맞는 설명 구조를 만듭니다. 호스트 내부 미리보기 또는 HTML 갤러리를 선택하고, 개수가 고정되지 않은 시안을 비교한 뒤 디자인을 고릅니다. 사실·해석·가정·불확실성을 구분하며 선택한 구성의 SVG와 필요한 세부 설명을 제공합니다." width="960">
</picture>

[크게 보기](docs/overview.svg) · [모바일 그림](docs/overview-mobile.svg) · [스킬 지침](SKILL.md)

## 이렇게 요청하세요

```text
Use $explain-me to explain this topic.
```

뒤에 주제와 원하는 독자 수준을 붙이면 됩니다.

표시 방식과 시안 수를 미리 지정할 수도 있습니다.

```text
Use $explain-me. 캐시가 왜 빠른지 비전공자에게 설명해줘.
시안은 현재 앱 안에서 보여줘.
```

```text
Use $explain-me. 이 문서의 핵심 주장과 근거를 설명해줘.
서로 다른 시안 3개를 HTML 갤러리로 비교하고 싶어.
```

따로 지정하지 않은 표시 방식은 선택지로 물어봅니다. 시안 수는 요청과 주제에 맞게 조절합니다.

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

미리보기 기능이 없는 환경에서는 독립 SVG 파일로 전달합니다. 선택한 표시 방식을 지원하지 않으면 제약을 설명하고 다른 방식이나 파일 확인을 고르게 합니다. 그림에는 외부 스크립트나 폰트 서비스가 필요하지 않습니다. 위 그림은 이 스킬의 동작 방식을 설명하는 정적 예제입니다.

## 시안 비교와 선택

시각 설명은 다음 순서로 만듭니다. **표시 방식 선택**과 **디자인 선택**은 별도 단계입니다.

| 단계 | 사용자가 하는 일 | 결과 |
| --- | --- | --- |
| 1. 표시 방식 선택 | 호스트 내부 미리보기 또는 HTML 갤러리를 고릅니다. | 비교할 화면을 정합니다. |
| 2. 시안 비교 | 같은 내용을 서로 다르게 구성한 실제 시안을 살펴봅니다. | 배치와 정보의 우선순위를 비교합니다. |
| 3. 디자인 선택 | 내장 선택 도구나 대화에서 시안 번호를 고릅니다. | 선택한 디자인으로 진행합니다. |
| 4. 완성 | 선택한 구성의 최종 설명을 확인합니다. | SVG와 필요한 세부 설명을 받습니다. |

- **표시 방식:** 호스트 내부 미리보기와 HTML 갤러리 중에서 사용자가 고릅니다. 한쪽을 기본값이나 자동 대체 방식으로 강제하지 않습니다.
- **시안 수:** 개수를 고정하지 않습니다. 약 6개는 참고값이며, 요청과 의미 있는 디자인 차이에 따라 조절합니다. 숫자를 채우려고 비슷한 시안을 늘리지 않습니다.
- **디자인 선택:** 실제 시안을 본 뒤 내장 선택 도구나 대화에서 번호로 고릅니다. 이미 정한 방식이나 디자인은 다시 묻지 않습니다.
- **요청 우선:** 텍스트 설명이나 특정 디자인을 요청했다면 그대로 따릅니다. 간단한 사실 답변에 시안 선택을 끼워 넣지 않습니다.

[선택 하네스 안내](references/ui-selection.md)에 표시 방식과 실행 명령이 있습니다. 공통 상태는 SVG 시안, `manifest.json`, `selection.json`이며, `inspect`·`choose`·`status`는 HTML이나 브라우저 없이 동작합니다. 선택은 재개 시에도 유지되며, 시안이나 비교 내용이 바뀌면 다시 선택합니다.

호스트 내부 보기에서는 현재 앱의 이미지·미리보기 기능을 사용하고 대화에서 선택할 수 있습니다. HTML 보기에서는 자체 포함된 비교 파일에서 확대해 볼 수 있습니다. 선택 저장용 로컬 서버와 JSON 다운로드는 선택 사항이며, HTML을 선택해도 대화에서 번호로 답할 수 있습니다.

공통 명령에는 Python 3.9+가 필요하며 외부 패키지는 사용하지 않습니다. 호스트별 미리보기와 내장 선택 도구의 지원 범위는 다를 수 있지만, 같은 시안과 선택 파일을 사용합니다.

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
| [references/ui-selection.md](references/ui-selection.md) | 표시 방식과 디자인을 선택하는 흐름 |
| [scripts/ui_harness.py](scripts/ui_harness.py) | 시안 검사, 선택 저장·재개, HTML 갤러리 명령 |
| [assets/ui-selection.html](assets/ui-selection.html) | 시안 수에 맞춰 표시되는 HTML 비교 화면 |
| [tests/test_ui_harness.py](tests/test_ui_harness.py) | 하네스 동작 검증 |
| [docs/overview.svg](docs/overview.svg) | README의 데스크톱 시각 설명 |
| [docs/overview-mobile.svg](docs/overview-mobile.svg) | 작은 화면에서도 읽을 수 있는 별도 구성 |

저장소 분석에서는 `declared`(설정), `intended`(의도), `recorded`(과거 기록), `observed`(이번 분석 중 실시간 관측)를 계속 구분합니다. 관측 시점을 모르면 모른다고 표시하고, 저장된 기록을 현재 실행 상태처럼 설명하지 않습니다.

## 하네스 검증

```sh
python3 -m unittest discover -s tests -v
```

생성한 시안과 선택 파일은 스킬 패키지 밖의 작업 출력 폴더에 둡니다.
