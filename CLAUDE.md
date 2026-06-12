바# Do Better Workspace 가이드

> Claude Code + Johnny Decimal 기반 PKM 워크스페이스. 업무 자동화 및 데이터 분석.

## 폴더 구조 (Johnny Decimal)

```
00-inbox/      # 임시 캡처 (20개 미만 유지, 주간 처리)
00-system/     # 시스템 설정, 템플릿, 가이드
10-projects/   # 활성 프로젝트 (시한부)
20-operations/ # 지속적 운영 (종료일 없음)
30-knowledge/  # 지식 (00-wiki + 도메인 아카이브)
40-personal/   # 개인 노트 (daily, weekly, ideas, reflections, todos)
50-resources/  # 외부 자료, 첨부파일
90-archive/    # 완료/중단 항목
```

### 주요 하위 폴더

| 번호 | 폴더 | 용도 |
|------|------|------|
| **00-wiki** | 30-knowledge/ | **지식 위키 (복리 축적). 아래 Wiki Schema 참조** |
| 41-daily | 40-personal/ | Daily Notes (월별: 41-daily/YYYY-MM/) |
| 42-weekly | 40-personal/ | Weekly Review |
| 43-ideas | 40-personal/ | 아이디어 캡처 |
| 44-reflections | 40-personal/ | 회고 및 학습 |
| 46-todos | 40-personal/ | active-todos.md |
| 37-claude-code | 30-knowledge/ | Claude Code 관련 지식 |

## Wiki (30-knowledge/00-wiki/)

지식이 복리로 축적되는 위키. 주제에 대해 물으면 **00-wiki/index.md를 먼저 확인**.

@30-knowledge/00-wiki/SCHEMA.md

## 파일 명명 규칙

| 유형 | 형식 | 예시 |
|------|------|------|
| Daily Note | `YYYY-MM-DD.md` | 2026-04-24.md |
| 주제 노트 | `주제명.md` | thinking-partner.md |
| JD 폴더 | `XX-name` 또는 `XX.YY-name` | 37-claude-code, 37.01-learning |
| 중복 파일명 | JD prefix 필수 | 18-progress-tracker.md |

## Inbox 관리 (00-inbox)

- **목적**: 임시 캡처, 영구 저장소 아님
- **규칙**: 20개 미만 유지
- **주기**: 주간 처리 (Capture → Process → Organize)

## 첨부파일 (50-resources/attachments/)

- 모든 비텍스트 파일 저장
- 명명: `[관련노트]_[설명].[ext]`

## 도구 시스템

### Skills (`.claude/skills/`)

키워드 기반 **자동 트리거** — 수동 슬래시 커맨드 아님.

| 카테고리 | 스킬 | 트리거 예시 |
|---------|------|-----------|
| 일상 | `daily-note` | "오늘 daily note", "하루 기록" |
| 일상 | `todo` / `todos` | "할 일 추가", "오늘 할 일 보여줘" |
| 일상 | `weekly-synthesis` | "주간 정리", "이번 주 회고" |
| 데이터 | `ops-data-analysis` | "매출 분석", "영업 실적", "운영 데이터" |
| 데이터 | `excel-to-csv` | "엑셀 변환", "xlsx 변환" |
| 데이터 | `pdf-to-md` | "PDF 변환", "PDF 마크다운으로" |
| 지식 | `wiki-ingest` | "위키 업데이트", "wiki-ingest" |
| 지식 | `thinking-partner` | "같이 생각해보자", "브레인스토밍" |
| 기획 | `dashboard-prd` | "대시보드 PRD", "대시보드 기획" |
| 협업 | `notion-handler` | "노션", "DB 만들어" |

### Agents (`.claude/agents/`)

복잡한 작업을 Claude가 자동 위임. 명시적 호출: "research-worker로 조사해줘"

### MCP 서버 (`.mcp.json`)

| 서버명 | 엔드포인트 | 비고 |
|--------|-----------|------|
| `royal-mcp` | `http://192.168.7.77:8080/mcp` | 로얄앤컴퍼니 사내 서버, Bearer 토큰 인증 |

- 연결 확인: `/mcp` 명령 · Claude Code 재시작 시 자동 활성화

---

## 내 프로필

**이름**: 양혁
**역할**: 로얄앤컴퍼니 정보관리팀 부장
**관심사**: AI 활용
**이 워크스페이스 용도**: 업무 자동화 및 데이터 분석

_작성일: 2026-05-13_

---

**Last Updated**: 2026-05-20
