# -*- coding: utf-8 -*-
import sys
import json
sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

def search_royal_news():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://search.naver.com/search.naver?where=news&query=로얄앤컴퍼니&sort=1")
        page.wait_for_load_state("networkidle", timeout=15000)

        articles = []
        items = page.query_selector_all("li.bx")

        for item in items:
            try:
                title_el = item.query_selector("a.news_tit")
                if not title_el:
                    continue

                title = title_el.inner_text().strip()
                link = title_el.get_attribute("href") or ""

                press_el = item.query_selector("a.info.press")
                press = press_el.inner_text().strip() if press_el else ""

                desc_el = item.query_selector(".dsc_txt_wrap, .dsc_txt")
                desc = desc_el.inner_text().strip() if desc_el else ""

                date_els = item.query_selector_all("span.info")
                date = date_els[-1].inner_text().strip() if date_els else ""

                if title:
                    articles.append({
                        "title": title,
                        "press": press,
                        "date": date,
                        "desc": desc[:200],
                        "link": link
                    })
            except Exception as e:
                continue

        browser.close()
        return articles

if __name__ == "__main__":
    results = search_royal_news()
    if results:
        art = results[0]
        print(f"제목: {art['title']}")
        print(f"언론사: {art['press']}")
        print(f"날짜: {art['date']}")
        print(f"내용: {art['desc']}")
        print(f"링크: {art['link']}")
    else:
        print("검색 결과가 없습니다.")
