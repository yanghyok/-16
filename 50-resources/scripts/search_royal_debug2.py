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

        items = page.query_selector_all("li.bx")
        print(f"li.bx 개수: {len(items)}")

        for i, item in enumerate(items[:3]):
            print(f"\n=== {i+1}번 기사 ===")
            # a 태그 전체 목록
            links = item.query_selector_all("a")
            for a in links:
                cls = a.get_attribute("class") or ""
                txt = a.inner_text().strip()[:80]
                href = (a.get_attribute("href") or "")[:80]
                print(f"  <a class='{cls}'> {txt} | {href}")

        browser.close()

debug()
