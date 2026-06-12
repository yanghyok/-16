---
name: ops-data-analysis
description: 로얄앤컴퍼니 운영 데이터(매출·AS·입고·영업사원 실적·위탁정산·카드결제·거래처) 분석. Node.js로 CSV/Excel을 읽어 주차별·영업사원별·카테고리별·채널별 집계, 달성률, 입금 지연, AS 현황을 리포트. "운영 데이터 분석", "매출 분석", "영업 실적", "주차별 실적", "AS 현황", "입고 집계", "생산량", "거래처 채권", "카드 입금 지연", "영업사원 순위", "정산 현황" 등을 언급하면 자동 실행.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# 운영 데이터 분석 스킬

로얄앤컴퍼니 Q1 운영 데이터를 분석하는 스킬. Python 미설치 환경이므로 **Node.js 인라인 스크립트**로 모든 분석 실행.

## 데이터 경로

```
50-resources/sample-data/royalco-q1-operational/
├── royalco_2026Q1_운영데이터.xlsx          # Excel 원본
├── royalco_2026Q1_운영데이터_sales_daily.csv
├── royalco_2026Q1_운영데이터_as_received.csv
├── royalco_2026Q1_운영데이터_customers.csv
├── royalco_2026Q1_운영데이터_products.csv
├── royalco_2026Q1_운영데이터_dealer_settlement.csv
├── royalco_2026Q1_운영데이터_card_payment.csv
├── royalco_2026Q1_운영데이터_sales_rep_targets.csv
└── royalco_2026Q1_운영데이터_inbound_inventory.csv
```

## 시트 구조

| 시트 | 행수 | 주요 컬럼 |
|------|------|-----------|
| sales_daily | 9,011 | 일자, 매장, 품번, 시리즈, 수량, 매출, 채널, 영업사원, 거래처 |
| as_received | 2,101 | 접수일, 품번, 현장, 유형, 완료여부, 완료일, 정체일수, 대응유형 |
| customers | 90 | 거래처코드, 거래처명, 약정금액, 환원유예여부, 결제조건, 매출채권_90일초과 |
| products | 150 | 품번, 구품번, 시리즈, 제품명, 카테고리, 단가 (**원가 컬럼 분석 제외**) |
| dealer_settlement | 624 | 정산일, 위탁업체, 품번, 정산수량, 적용단가, 정산금액, 기안번호, 승인여부 |
| card_payment | 790 | 일자, 매장, 카드사, 승인액, 입금예정일, 실입금일, 지연일수 |
| sales_rep_targets | 130 | 주차, 영업사원, 약정금액, 달성액, 환원유예신청, 특별출고승인_건수, 특별가요청_건수 |
| inbound_inventory | 824 | 입고일, 품번, 수량, 외주처, 계정 |

## 실행 환경

- **Python 미설치** — `python` 명령어 사용 금지
- **Node.js v24** 사용 (`node -e "..."` 인라인 실행)
- xlsx 패키지 위치: `node_modules/xlsx` (이미 설치됨)
- 모든 Bash 명령은 워크스페이스 루트(`C:\Users\HRD1\do-better-workspace-v2`)에서 실행

## 워크플로우

### 1단계: CSV 파일 확인

Glob으로 `50-resources/sample-data/royalco-q1-operational/*.csv` 확인.
없으면 Excel → CSV 변환 먼저 실행:

```javascript
// Excel 전체 시트 → UTF-8 BOM CSV
const XLSX = require('xlsx');
const fs = require('fs'), path = require('path');
const wb = XLSX.readFile('50-resources/sample-data/royalco-q1-operational/royalco_2026Q1_운영데이터.xlsx');
const outDir = '50-resources/sample-data/royalco-q1-operational';
wb.SheetNames.forEach(name => {
  const csv = XLSX.utils.sheet_to_csv(wb.Sheets[name]);
  fs.writeFileSync(path.join(outDir, `royalco_2026Q1_운영데이터_${name}.csv`), '﻿' + csv, 'utf8');
});
```

### 2단계: 분석 유형 결정

| 키워드 | 사용할 시트 |
|--------|------------|
| 영업 실적, 주차별 매출, 영업사원 순위, 채널별 | sales_daily |
| AS 현황, AS 유형, 정체일수, 완료율 | as_received |
| 입고, 생산량, 카테고리별 입고 | inbound_inventory + products |
| 거래처 현황, 채권, 환원유예 | customers |
| 정산, 위탁 정산, 승인 현황 | dealer_settlement |
| 카드 결제, 입금 지연 | card_payment |
| 목표 달성, 달성률 | sales_rep_targets |
| 전체 현황, 종합 | 복수 시트 조합 |

### 3단계: 공통 유틸 (모든 스크립트에 포함)

```javascript
const fs = require('fs');
const BASE = '50-resources/sample-data/royalco-q1-operational/royalco_2026Q1_운영데이터_';

function readCsv(sheet) {
  const raw = fs.readFileSync(BASE + sheet + '.csv', 'utf8').replace(/^﻿/, '');
  const lines = raw.split('\n').filter(l => l.trim());
  const headers = lines[0].split(',');
  return lines.slice(1).map(l => {
    const cols = l.split(',');
    const obj = {};
    headers.forEach((h, i) => obj[h] = cols[i] || '');
    return obj;
  });
}

// ISO 주차 계산 (월요일 시작)
function getWeek(dateStr) {
  const d = new Date(dateStr);
  if (isNaN(d)) return null;
  const day = d.getDay() || 7;
  d.setDate(d.getDate() + 4 - day);
  const yearStart = new Date(d.getFullYear(), 0, 1);
  return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
}
```

## 분석 유형별 스크립트

### A. 영업사원별 주차 실적 (sales_daily, B2B 채널)

```javascript
const sd = readCsv('sales_daily');
const agg = {};
sd.filter(r => r['채널'] === 'B2B' && r['영업사원']).forEach(r => {
  const wk = getWeek(r['일자']);
  const rep = r['영업사원'];
  if (!agg[wk]) agg[wk] = {};
  if (!agg[wk][rep]) agg[wk][rep] = { 매출: 0, 수량: 0, 건수: 0 };
  agg[wk][rep].매출 += parseInt(r['매출']) || 0;
  agg[wk][rep].수량 += parseInt(r['수량']) || 0;
  agg[wk][rep].건수++;
});
// 주차별 출력
Object.keys(agg).map(Number).sort((a,b)=>a-b).forEach(wk => {
  const total = Object.values(agg[wk]).reduce((s,d)=>s+d.매출,0);
  console.log(`\n▶ ${wk}주차 (합계: ${total.toLocaleString()}원)`);
  Object.entries(agg[wk]).sort((a,b)=>b[1].매출-a[1].매출).forEach(([rep,d]) => {
    const pct = (d.매출/total*100).toFixed(1);
    console.log(`  ${rep.padEnd(12)} ${d.매출.toLocaleString().padStart(14)}원  ${d.수량}개  ${d.건수}건  (${pct}%)`);
  });
});
```

### B. AS 현황 분석 (as_received)

```javascript
const as = readCsv('as_received');
const statusCnt = {}, typeCnt = {}, resCnt = {};
let totalDays = 0, completedCount = 0;
as.forEach(r => {
  statusCnt[r['완료여부']] = (statusCnt[r['완료여부']] || 0) + 1;
  typeCnt[r['유형']] = (typeCnt[r['유형']] || 0) + 1;
  resCnt[r['대응유형']] = (resCnt[r['대응유형']] || 0) + 1;
  if (r['완료여부'] === '완료') { totalDays += parseInt(r['정체일수']) || 0; completedCount++; }
});
console.log('완료여부:', JSON.stringify(statusCnt));
console.log('AS 유형:', JSON.stringify(typeCnt));
console.log('대응유형:', JSON.stringify(resCnt));
console.log('평균 처리일수(완료건):', (totalDays/completedCount).toFixed(1), '일');
```

### C. 입고/생산량 집계 (inbound_inventory + products)

```javascript
const inv = readCsv('inbound_inventory');
const pr = readCsv('products');
// 카테고리 정규화: 정수기류/정수기/정수 → 정수기(CW1)
const catMap = {};
pr.forEach(r => {
  let cat = r['카테고리'];
  if (cat.startsWith('정수기') || cat === '정수') cat = '정수기(CW1)';
  catMap[r['품번']] = cat;
  if (r['구품번']) catMap[r['구품번']] = cat;
});
const agg = {};
inv.forEach(r => {
  const wk = getWeek(r['입고일']);
  const cat = catMap[r['품번']] || '미분류';
  const qty = parseInt(r['수량']) || 0;
  if (!agg[wk]) agg[wk] = {};
  agg[wk][cat] = (agg[wk][cat] || 0) + qty;
});
// 크로스탭 출력
const cats = [...new Set(Object.values(agg).flatMap(w=>Object.keys(w)))].sort();
const weeks = Object.keys(agg).map(Number).sort((a,b)=>a-b);
console.log(['카테고리', ...weeks.map(w=>w+'주')].join('\t'));
cats.forEach(c => console.log([c, ...weeks.map(w=>agg[w]?.[c]||0)].join('\t')));
```

### D. 카드 결제 지연 분석 (card_payment)

```javascript
const cp = readCsv('card_payment');
const delayed = cp.filter(r => parseInt(r['지연일수']) > 0);
const cardAgg = {};
delayed.forEach(r => {
  cardAgg[r['카드사']] = cardAgg[r['카드사']] || { 건수: 0, 총지연일: 0 };
  cardAgg[r['카드사']].건수++;
  cardAgg[r['카드사']].총지연일 += parseInt(r['지연일수']) || 0;
});
console.log(`지연 건수: ${delayed.length}/${cp.length} (${(delayed.length/cp.length*100).toFixed(1)}%)`);
Object.entries(cardAgg).sort((a,b)=>b[1].건수-a[1].건수).forEach(([card,d]) => {
  console.log(`  ${card}: ${d.건수}건, 평균 ${(d.총지연일/d.건수).toFixed(1)}일 지연`);
});
```

### E. 영업사원 목표 달성률 (sales_rep_targets)

```javascript
const st = readCsv('sales_rep_targets');
const reps = {};
st.forEach(r => {
  const rep = r['영업사원'];
  if (!reps[rep]) reps[rep] = { 약정: 0, 달성: 0 };
  reps[rep].약정 += parseInt(r['약정금액']) || 0;
  reps[rep].달성 += parseInt(r['달성액']) || 0;
});
Object.entries(reps).sort((a,b)=>b[1].달성-a[1].달성).forEach(([rep,d]) => {
  const pct = (d.달성/d.약정*100).toFixed(1);
  const flag = pct < 80 ? ' ⚠' : pct >= 100 ? ' ✓' : '';
  console.log(`${rep.padEnd(12)} 달성률 ${pct}% (달성 ${d.달성.toLocaleString()} / 약정 ${d.약정.toLocaleString()})${flag}`);
});
```

## 데이터 품질 주의사항

| 이슈 | 내용 | 처리 |
|------|------|------|
| 거래처명 오염 | 특수문자(｜ ` \ { \x80) 혼입 | 정규표현식으로 필터링 |
| 카테고리 비일관 | 정수기류/정수기/정수 혼재 | 정규화 로직 적용 |
| 채널 누락 | sales_daily 3건 채널="" | 해당 건 제외 처리 |
| 14주차 부분 집계 | Q1 마지막 잔여 주 | 결과에 주석 표기 |
| **원가 컬럼** | products 시트 포함 | **분석 대상에서 반드시 제외** |

## 출력 형식

- 숫자: 천 단위 구분(`.toLocaleString()`) 또는 원화 표기
- 테이블: 마크다운 파이프 테이블
- 이상값: ⚠ 아이콘 강조
- 분기 요약: 항상 최하단에 합계·평균 행 추가

## 보안 안내

products 시트의 원가 컬럼은 회사 보안 정책상 분석 대상에서 제외. 관련 질문 시:
> "※ 원가 정보는 회사 보안 정책상 제공이 제한됩니다."
