# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

def fetch_article(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=20000)
        page.wait_for_load_state("networkidle", timeout=15000)

        # 제목
        title = ""
        for sel in ["h1", "h2.title", ".article-title", "#articleTitle", ".news_title"]:
            el = page.query_selector(sel)
            if el:
                title = el.inner_text().strip()
                break

        # 날짜
        date = ""
        for sel in [".date", ".info-date", ".article-date", "time", ".txt_info"]:
            el = page.query_selector(sel)
            if el:
                date = el.inner_text().strip()
                break

        # 본문
        body = ""
        for sel in ["#articleBody", ".article-body", ".news-content", "#newsct_article", ".article_body"]:
            el = page.query_selector(sel)
            if el:
                body = el.inner_text().strip()
                break

        if not body:
            # fallback: p 태그 모아서
            paras = page.query_selector_all("article p, .content p, #content p")
            body = "\n".join(p.inner_text().strip() for p in paras if p.inner_text().strip())

        browser.close()
        return title, date, body

if __name__ == "__main__":
    url = "https://www.businesskorea.co.kr/news/articleView.html?idxno=249066"
    title, date, body = fetch_article(url)
    print(f"[제목] {title}")
    print(f"[날짜] {date}")
    print(f"\n[본문]\n{body[:1500]}")
