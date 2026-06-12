param([string]$Url)

# 설정 로드
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$config = Get-Content "$scriptDir\config.json" -Encoding UTF8 | ConvertFrom-Json
$token = $config.notion_token
$dbId = $config.db_id

# video_id 추출
if ($Url -match "(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})") {
    $videoId = $Matches[1]
} else {
    Write-Host "ERROR: 유효한 유튜브 URL이 아닙니다."
    exit 1
}

# YouTube oEmbed로 제목·채널명 가져오기
try {
    $oembed = Invoke-RestMethod -Uri "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=$videoId&format=json"
    $title   = $oembed.title
    $channel = $oembed.author_name
} catch {
    $title   = "(제목 없음)"
    $channel = ""
}

$thumbnailUrl = "https://img.youtube.com/vi/$videoId/maxresdefault.jpg"
$today = (Get-Date).ToString("yyyy-MM-dd")

# JSON 이스케이프
$titleEsc   = $title   -replace '"', '\"' -replace '\\', '\\'
$channelEsc = $channel -replace '"', '\"' -replace '\\', '\\'
$urlEsc     = $Url     -replace '"', '\"'

# Notion 페이지 생성 payload
$pageJson = @"
{
  "parent": { "database_id": "$dbId" },
  "cover": { "type": "external", "external": { "url": "$thumbnailUrl" } },
  "properties": {
    "영상 제목": { "title": [{ "text": { "content": "$titleEsc" } }] },
    "유튜브 URL": { "url": "$urlEsc" },
    "채널명": { "rich_text": [{ "text": { "content": "$channelEsc" } }] },
    "썸네일": { "files": [{ "name": "thumbnail", "type": "external", "external": { "url": "$thumbnailUrl" } }] },
    "시청일": { "date": { "start": "$today" } }
  }
}
"@

# 임시 파일로 저장 후 전송 (한글 인코딩 보장)
$tmpFile = "$env:TEMP\notion_yt_$(Get-Random).json"
$pageJson | Out-File -FilePath $tmpFile -Encoding utf8NoBOM

$result = curl.exe -s -X POST "https://api.notion.com/v1/pages" `
    -H "Authorization: Bearer $token" `
    -H "Content-Type: application/json; charset=utf-8" `
    -H "Notion-Version: 2022-06-28" `
    --data-binary "@$tmpFile"

Remove-Item $tmpFile -Force

$json = $result | ConvertFrom-Json
if ($json.id) {
    Write-Host "SUCCESS"
    Write-Host "TITLE:$title"
    Write-Host "CHANNEL:$channel"
    Write-Host "NOTION_URL:$($json.url)"
} else {
    Write-Host "ERROR:$($json.message)"
}
