from playwright.sync_api import sync_playwright

def debug_search():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://search.naver.com/search.naver?where=news&query=로얄앤컴퍼니&sort=1")
        page.wait_for_load_state("networkidle", timeout=15000)

        # 페이지 HTML 일부 출력
        html = page.content()
        # 뉴스 관련 클래스 탐색
        print("=== 뉴스 컨테이너 탐색 ===")
        for sel in [".news_area", ".list_news", ".group_news", "li.bx", ".news_wrap", "ul.list_news li"]:
            els = page.query_selector_all(sel)
            print(f"  {sel}: {len(els)}개")

        # 첫 번째 li.bx 내부 구조 확인
        first = page.query_selector("li.bx")
        if first:
            print("\n=== 첫 번째 기사 내부 HTML (축약) ===")
            inner = first.inner_html()
            print(inner[:2000])

        browser.close()

debug_search()
