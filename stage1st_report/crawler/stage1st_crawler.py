"""
Stage1st论坛帖子爬取与分析脚本
使用方法：
1. 在浏览器中登录 stage1st.com
2. 按F12打开开发者工具 -> Application -> Cookies
3. 复制关键cookie（主要是 bbs_sid 和 bbs_cookietime 等）
4. 在下方COOKIES字典中填入你的cookie值
"""

import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import jieba
import jieba.analyse
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from typing import List, Dict
import time
import random

# ============ 在这里填入你的cookie ============
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

# 帖子ID
THREAD_ID = "2275908"

# 爬取页码范围 (设为0表示只爬最新5页)
START_PAGE = 0  # 0 = 自动获取最新5页

# 请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://stage1st.com/2b/",
}


def fetch_page(thread_id: str, page: int, cookies: Dict[str, str]) -> str:
    """获取指定页码的内容"""
    url = f"https://stage1st.com/2b/thread-{thread_id}-{page}-1.html"
    session = requests.Session()
    session.headers.update(HEADERS)
    session.cookies.update(cookies)

    response = session.get(url, timeout=30)
    response.encoding = "utf-8"
    return response.text, url


def get_total_pages(html: str) -> int:
    """从页面中提取总页数"""
    soup = BeautifulSoup(html, "html.parser")
    # 查找分页信息: <span title="共 126 页">126</span> 或类似结构
    page_info = soup.select_one(".pg .last, .pg label span")
    if page_info:
        text = page_info.get_text()
        # 提取数字
        match = re.search(r'(\d+)', text)
        if match:
            return int(match.group(1))
    return 0


def parse_posts(html: str) -> List[Dict]:
    """
    解析Stage1st(Discuz)论坛帖子内容
    返回：[{"author": "用户名", "content": "回复内容", "floor": "楼层", "time": "时间"}, ...]
    """
    soup = BeautifulSoup(html, "html.parser")
    posts = []

    # Stage1st结构: div[id^='post_'] 包含每个回复
    post_items = soup.select("div[id^='post_']")

    for post in post_items:
        try:
            # 提取用户名: <div class="authi"><a class="xw1">用户名</a>
            author_elem = post.select_one(".authi .xw1")
            author = author_elem.get_text(strip=True) if author_elem else "未知用户"

            # 提取楼层: <a id="postnum..."><em>4961</em>
            floor_elem = post.select_one("a[id^='postnum'] em")
            floor = floor_elem.get_text(strip=True) if floor_elem else ""

            # 提取内容: <td class="t_f" id="postmessage_...">
            content_elem = post.select_one("td.t_f")
            if content_elem:
                # 移除引用块
                for quote in content_elem.select(".quote, blockquote, .pstatus"):
                    quote.decompose()
                # 处理图片 - 提取alt或替换为[图片]
                for img in content_elem.select("img"):
                    alt_text = img.get("alt", "") or img.get("file", "")
                    if alt_text:
                        img.replace_with(f"[图片:{alt_text}]")
                    else:
                        img.decompose()
                # 处理表情
                for smiley in content_elem.select("img[src*='smiley']"):
                    smiley.replace_with("")
                # 获取纯文本
                content = content_elem.get_text(strip=True, separator=" ")
                # 清理多余空白
                content = re.sub(r'\s+', ' ', content).strip()
            else:
                content = ""

            # 提取时间: <em id="authorposton...">发表于 2026-3-1 22:30</em>
            time_elem = post.select_one("em[id^='authorposton']")
            post_time = time_elem.get_text(strip=True) if time_elem else ""
            # 去掉"发表于"前缀
            post_time = post_time.replace("发表于", "").strip()

            if content and author != "未知用户":
                posts.append({
                    "author": author,
                    "content": content,
                    "floor": floor,
                    "time": post_time
                })
        except Exception as e:
            print(f"解析帖子时出错: {e}")
            continue

    return posts


def analyze_posts(posts: List[Dict]) -> Dict:
    """分析帖子内容"""
    analysis = {
        "total_posts": len(posts),
        "unique_authors": len(set(p["author"] for p in posts)),
        "author_post_count": Counter(p["author"] for p in posts),
        "all_text": " ".join(p["content"] for p in posts),
    }

    # 统计关键词
    keywords = jieba.analyse.extract_tags(analysis["all_text"], topK=30, withWeight=True)
    analysis["keywords"] = keywords

    # 分析回复长度
    lengths = [len(p["content"]) for p in posts]
    analysis["avg_length"] = sum(lengths) / len(lengths) if lengths else 0
    analysis["max_length"] = max(lengths) if lengths else 0
    analysis["min_length"] = min(lengths) if lengths else 0

    return analysis


def print_analysis(posts: List[Dict], analysis: Dict):
    """打印分析结果"""
    print("=" * 60)
    print("[STAT] 帖子统计分析")
    print("=" * 60)
    print(f"总回复数: {analysis['total_posts']}")
    print(f"参与人数: {analysis['unique_authors']}")
    print(f"平均回复长度: {analysis['avg_length']:.1f} 字符")
    print(f"最长回复: {analysis['max_length']} 字符")
    print(f"最短回复: {analysis['min_length']} 字符")

    print("\n" + "=" * 60)
    print("[USER] 活跃用户 TOP 10")
    print("=" * 60)
    for author, count in analysis["author_post_count"].most_common(10):
        print(f"  {author}: {count} 条回复")

    print("\n" + "=" * 60)
    print("[TAG] 关键词 TOP 20")
    print("=" * 60)
    for word, weight in analysis["keywords"][:20]:
        print(f"  {word}: {weight:.3f}")


def generate_wordcloud(text: str, output_path: str = "wordcloud.png"):
    """生成词云图"""
    # 停用词
    stopwords = set(['的', '了', '是', '在', '我', '有', '和', '就', '不', '人',
                     '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去',
                     '你', '会', '着', '没有', '看', '好', '自己', '这', '那', '什么'])

    wordcloud = WordCloud(
        font_path="C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
        width=800,
        height=400,
        background_color="white",
        stopwords=stopwords,
        max_words=100
    ).generate(text)

    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"\n词云图已保存: {output_path}")
    plt.close()


def save_posts(posts: List[Dict], output_path: str = "posts.json"):
    """保存帖子数据"""
    import json
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    print(f"帖子数据已保存: {output_path}")


def save_posts_text(posts: List[Dict], output_path: str = "posts.txt"):
    """保存帖子为纯文本格式"""
    with open(output_path, "w", encoding="utf-8") as f:
        for p in posts:
            f.write(f"【{p['floor']}】{p['author']} ({p['time']}):\n")
            f.write(f"{p['content']}\n")
            f.write("-" * 40 + "\n")
    print(f"帖子文本已保存: {output_path}")


def main():
    print("=" * 60)
    print("[START] Stage1st 帖子爬取与分析工具")
    print("=" * 60)

    # 检查cookie是否已配置
    if not COOKIES or all(v == "" for v in COOKIES.values()):
        print("\n[ERR] 错误: 请先在脚本顶部的 COOKIES 字典中填入你的cookie!")
        print("\n获取方法:")
        print("1. 在浏览器中登录 stage1st.com")
        print("2. 按F12打开开发者工具")
        print("3. 切换到 Application/存储 -> Cookies")
        print("4. 找到并复制 bbs_sid, bbs_auth 等关键cookie的值")
        print("5. 粘贴到脚本中的 COOKIES 字典")
        return

    # 先获取第一页确定总页数
    print(f"\n[GET] 正在获取第 {START_PAGE} 页以确定总页数...")
    html, url = fetch_page(THREAD_ID, START_PAGE, COOKIES)

    # 检查是否需要登录
    if "您需要登录" in html or "请先登录" in html:
        print("[ERR] Cookie无效或已过期，请重新获取!")
        return

    total_pages = get_total_pages(html)
    if total_pages > 0:
        print(f"[PAGE] 检测到帖子共 {total_pages} 页")
    else:
        print("[WARN] 未能检测到总页数，将爬取到无内容为止")
        total_pages = START_PAGE + 100  # 设置一个上限

    # 如果START_PAGE为0，则从最新5页开始爬取
    if START_PAGE == 0:
        start_from = max(1, total_pages - 4) if total_pages > 0 else 1
        print(f"[INFO] 将爬取最新5页: 第 {start_from} 页到第 {total_pages} 页")
    else:
        start_from = START_PAGE

    all_posts = []

    # 从start_from开始爬取到最后
    for page in range(start_from, total_pages + 1):
        print(f"\n[GET] 正在获取第 {page}/{total_pages} 页...")

        try:
            if page == START_PAGE:
                # 第一页已经获取过了
                pass
            else:
                html, url = fetch_page(THREAD_ID, page, COOKIES)

            # 检查是否有内容
            if "指定主题不存在" in html:
                print(f"[ERR] 第 {page} 页不存在，停止爬取")
                break

            print(f"[OK] 页面获取成功: {url}")

            # 保存原始HTML（仅第一页用于调试）
            if page == START_PAGE:
                with open("page_sample.html", "w", encoding="utf-8") as f:
                    f.write(html)

            print("[PARSE] 正在解析帖子...")
            posts = parse_posts(html)

            if not posts:
                print(f"[WARN] 第 {page} 页没有解析到帖子内容")
                if page == START_PAGE:
                    print("提示: 可以查看 page_sample.html 文件来调试")
            else:
                # 标记页码
                for p in posts:
                    p["page"] = page
                all_posts.extend(posts)
                print(f"[OK] 解析到 {len(posts)} 条回复")

            # 随机延迟，避免请求过快
            if page < total_pages:
                delay = random.uniform(1.5, 3.5)
                print(f"[WAIT] 等待 {delay:.1f} 秒...")
                time.sleep(delay)

        except requests.exceptions.RequestException as e:
            print(f"[ERR] 第 {page} 页请求失败: {e}")
            continue
        except Exception as e:
            print(f"[ERR] 第 {page} 页处理出错: {e}")
            continue

    if not all_posts:
        print("\n[ERR] 没有获取到任何帖子内容，请检查cookie是否有效")
        return

    print("\n" + "=" * 60)
    print(f"[STAT] 共获取 {len(all_posts)} 条回复")
    print("=" * 60)

    # 分析内容
    print("\n[STAT] 正在分析内容...")
    analysis = analyze_posts(all_posts)

    # 打印分析结果
    print_analysis(all_posts, analysis)

    # 保存数据
    save_posts(all_posts, f"posts_thread_{THREAD_ID}.json")
    save_posts_text(all_posts, f"posts_thread_{THREAD_ID}.txt")

    # 生成词云
    try:
        generate_wordcloud(analysis["all_text"], f"wordcloud_{THREAD_ID}.png")
    except Exception as e:
        print(f"[WARN] 词云生成失败: {e}")

    print("\n" + "=" * 60)
    print("[DONE] 完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
