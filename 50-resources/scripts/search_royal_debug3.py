# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

def debug():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://search.naver.com/search.naver?where=news&query=로얄앤컴퍼니&sort=1")
        page.wait_for_load_state("networkidle", timeout=15000)

        # 뉴스 기사 링크만 추출
        all_links = page.query_selector_all("a")
        print("=== 뉴스 기사로 보이는 링크 ===")
        for a in all_links:
            href = a.get_attribute("href") or ""
            txt = a.inner_text().strip()
            if ("news.naver.com" in href or "n.news.naver.com" in href or
                ("naver" not in href and href.startswith("http") and len(txt) > 10)):
                print(f"  [{txt[:60]}]\n  {href[:100]}\n")

        browser.close()

debug()
