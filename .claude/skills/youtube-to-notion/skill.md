---
name: youtube-to-notion
description: 유튜브 URL을 Notion 유튜브 콘텐츠 정리 DB에 저장. "유튜브 저장", "노션에 저장", "유튜브 노션", youtube.com 또는 youtu.be URL과 함께 "저장" 언급 시 자동 실행.
context: fork
allowed-tools:
  - PowerShell
  - Bash
---

# YouTube → Notion 저장 스킬

유튜브 URL을 받아 **유튜브 콘텐츠 정리** Notion DB에 자동 저장합니다.
저장 항목: 영상 제목, 채널명, 유튜브 URL, 썸네일(cover + files), 시청일(오늘)

## 실행 순서

### 1. URL 추출

ARGUMENTS 또는 대화에서 유튜브 URL을 찾습니다.
- `https://www.youtube.com/watch?v=XXXXXXXXXXX`
- `https://youtu.be/XXXXXXXXXXX`

URL이 없으면 사용자에게 요청합니다.

### 2. 스크립트 실행

```powershell
& "C:\Users\HRD1\do-better-workspace-v2\.claude\skills\youtube-to-notion\save_youtube.ps1" -Url "추출한_URL"
```

### 3. 결과 파싱 및 보고

출력에서 각 줄을 파싱합니다:
- `SUCCESS` → 저장 성공
- `TITLE:...` → 영상 제목
- `CHANNEL:...` → 채널명
- `NOTION_URL:...` → 저장된 Notion 페이지 URL
- `ERROR:...` → 오류 메시지

### 4. 사용자에게 안내

저장 완료 시:
```
✅ Notion 저장 완료
제목  : [영상 제목]
채널  : [채널명]
페이지: [Notion URL]
```

오류 시 원인과 해결 방법 안내.

## 참고

- DB ID: `35f317e3-87b1-8172-8f91-d86f656c9230`
- 카테고리, 키워드, 요약, 평점은 저장 후 Notion에서 직접 입력
- 썸네일은 유튜브 maxresdefault.jpg를 자동 사용
