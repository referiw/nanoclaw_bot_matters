# -*- coding: utf-8 -*-
"""
临时脚本：爬取指定页码范围
"""

import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import jieba.analyse
import time
import random
import json

# Cookies
COOKIES = {
    "B7Y9_2f85_saltkey": "C1vaaVPg",
    "B7Y9_2f85_lastvisit": "1772446170",
    "B7Y9_2f85_auth": "de5dUmWyZUGIQcqvonLv9PLL4zMJZ%2B2q%2FOPvLHmm4n3tHsSqAvKi8eRJdRX8gjqMGC3W%2Bf6JbkEit0hNQIqEpaOcPTw",
    "B7Y9_2f85_lastcheckfeed": "569825%7C1772449786",
    "B7Y9_2f85_smile": "3D1",
    "B7Y9_2f85_nofavfid": "1",
    "_gid": "GA1.2.2032329666.1772634497",
    "B7Y9_2f85_sid": "YCjT5y",
    "B7Y9_2f85_lip": "42.234.95.125%2C1772741896",
    "B7Y9_2f85_ulastactivity": "7b30sz9K0FP3vYUVVJ4tK%2B%2BCV8oK9m8mrNdqZOZylcMFFifoQXIZ",
    "B7Y9_2f85_sendmail": "1",
    "B7Y9_2f85_checkpm": "1",
    "_gat_gtag_UA_141266582_1": "1",
    "B7Y9_2f85_st_t": "569825%7C1772772243%7Cba73df6432d307aef33fb489bdc0fecd",
    "B7Y9_2f85_forum_lastvisit": "D_6_1772772237D_157_1772772243",
    "B7Y9_2f85_visitedfid": "157D6",
    "B7Y9_2f85_lastact": "1772772245%09forum.php%09viewthread",
    "B7Y9_2f85_st_p": "569825%7C1772772245%7C33a16ce0a4534802363880e88e034d77",
    "B7Y9_2f85_viewid": "tid_2275908",
    "_ga_BYLFGNMRD4": "GS2.1.s1772772240$o136$g1$t1772772248$j52$l0$h0",
    "_ga": "GA1.1.1057216128.1759553388",
}

THREAD_ID = "2275908"
START_PAGE = 135
END_PAGE = 175

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://stage1st.com/2b/",
}


def fetch_page(thread_id, page, cookies):
    url = f"https://stage1st.com/2b/thread-{thread_id}-{page}-1.html"
    session = requests.Session()
    session.headers.update(HEADERS)
    session.cookies.update(cookies)
    response = session.get(url, timeout=30)
    response.encoding = "utf-8"
    return response.text, url


def parse_posts(html):
    soup = BeautifulSoup(html, "html.parser")
    posts = []
    post_items = soup.select("div[id^='post_']")

    for post in post_items:
        try:
            author_elem = post.select_one(".authi .xw1")
            author = author_elem.get_text(strip=True) if author_elem else "未知用户"

            floor_elem = post.select_one("a[id^='postnum'] em")
            floor = floor_elem.get_text(strip=True) if floor_elem else ""

            content_elem = post.select_one("td.t_f")
            if content_elem:
                for quote in content_elem.select(".quote, blockquote, .pstatus"):
                    quote.decompose()
                for img in content_elem.select("img"):
                    alt_text = img.get("alt", "") or img.get("file", "")
                    if alt_text:
                        img.replace_with(f"[图片:{alt_text}]")
                    else:
                        img.decompose()
                for smiley in content_elem.select("img[src*='smiley']"):
                    smiley.replace_with("")
                content = content_elem.get_text(strip=True, separator=" ")
                content = re.sub(r'\s+', ' ', content).strip()
            else:
                content = ""

            time_elem = post.select_one("em[id^='authorposton']")
            post_time = time_elem.get_text(strip=True) if time_elem else ""
            post_time = post_time.replace("发表于", "").strip()

            if content and author != "未知用户":
                posts.append({
                    "author": author,
                    "content": content,
                    "floor": floor,
                    "time": post_time
                })
        except Exception as e:
            continue

    return posts


def main():
    print("=" * 60)
    print(f"[START] 爬取第 {START_PAGE}-{END_PAGE} 页")
    print("=" * 60)

    all_posts = []

    for page in range(START_PAGE, END_PAGE + 1):
        print(f"\n[GET] 正在获取第 {page}/{END_PAGE} 页...")

        try:
            html, url = fetch_page(THREAD_ID, page, COOKIES)

            if "指定主题不存在" in html:
                print(f"[ERR] 第 {page} 页不存在")
                continue

            print(f"[OK] 页面获取成功")
            posts = parse_posts(html)

            if posts:
                for p in posts:
                    p["page"] = page
                all_posts.extend(posts)
                print(f"[OK] 解析到 {len(posts)} 条回复")

            if page < END_PAGE:
                delay = random.uniform(1.5, 3.0)
                print(f"[WAIT] 等待 {delay:.1f} 秒...")
                time.sleep(delay)

        except Exception as e:
            print(f"[ERR] 第 {page} 页处理出错: {e}")
            continue

    if all_posts:
        # 保存
        with open("posts_mar7.json", "w", encoding="utf-8") as f:
            json.dump(all_posts, f, ensure_ascii=False, indent=2)

        with open("posts_mar7.txt", "w", encoding="utf-8") as f:
            for p in all_posts:
                f.write(f"【{p['floor']}】{p['author']} ({p['time']}):\n")
                f.write(f"{p['content']}\n")
                f.write("-" * 40 + "\n")

        print(f"\n[DONE] 共获取 {len(all_posts)} 条回复")
        print(f"保存到 posts_mar7.json 和 posts_mar7.txt")

        # 分析
        all_text = " ".join(p["content"] for p in all_posts)
        keywords = jieba.analyse.extract_tags(all_text, topK=20, withWeight=True)
        print("\n关键词 TOP 20:")
        for word, weight in keywords:
            print(f"  {word}: {weight:.3f}")

        authors = Counter(p["author"] for p in all_posts)
        print("\n活跃用户 TOP 10:")
        for author, count in authors.most_common(10):
            print(f"  {author}: {count} 条")


if __name__ == "__main__":
    main()
