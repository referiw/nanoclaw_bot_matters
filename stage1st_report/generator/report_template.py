# -*- coding: utf-8 -*-
"""
论坛报告生成器模板
使用方法：
1. 修改下方 CONFIG 区域的配置
2. 运行 python report_template.py
"""

import json
import os
from datetime import datetime

# ==================== 配置区域 ====================
CONFIG = {
    # 数据文件路径（爬虫生成的JSON文件）
    "data_file": "posts_thread_2271232.json",

    # 报告标题
    "title": "伊朗-以色列冲突战报",
    "subtitle": "Stage1st论坛精选 | 2026-03-02",

    # 报告主题/事件描述
    "topic": "第130-150页：F-14被毁、内贾德身亡传闻、沙特立场",

    # 时间线事件（手动提取重要事件）
    "timeline": [
        ("23:33", "沙特与巴基斯坦签署共同防御协议，可蹭核保护"),
        ("23:35", "懂王：如果不是我们袭击伊朗核设施，伊朗两周内就会拥有核武器"),
        ("23:37", "伊朗电视台：哈梅内伊14个月大的孙女在袭击中殉难"),
        ("23:39", "内塔尼亚胡：将动用以军全部力量投入战役"),
        ("23:43", "以军称已摧毁所有波斯空军F-14战斗机（含假目标）"),
        ("23:44", "内塔尼亚胡在特拉维夫楼顶发表声明"),
        ("23:48", "新华社快讯：伊朗前总统内贾德遇袭身亡"),
        ("23:54", "CIA评估：哈梅内伊若被击毙，将被强硬派革命卫队成员取代"),
    ],

    # 核心观点（格式：标题, 内容, 作者）
    "viewpoints": [
        ("军事策略", "伊朗打美军基地是战术正确选择，摁住出兵点，不用在乎王爷们说什么", "loli炮"),
        ("无人机产能", "一天3万架产能存疑，1100万/年卖给谁需要这么大产能？", "iantsai"),
        ("王爷立场", "阿联酋：伊朗要决定如何处理传统上对他们公平友好的邻邦", "Lokad"),
        ("武器限制", "沙特若下场，中式武器不会上锁，可随便用", "Lokad"),
    ],

    # 金句（格式：内容, 作者）
    "quotes": [
        ("实力不足，只能用非对称战法，导弹>飞机>航母，东大也是这么一步步走来的", "油条小贩"),
        ("内贾德在复活赛擂台肘赢了另一个牢内", "linchuanwangmou"),
        ("牢哈死后，限制器解除了", "血从心生"),
        ("老美是九头蛇，波斯是无头骑士", "猪突猛进R"),
    ],

    # 输出文件名
    "output_filename": "iran_conflict_report_20260302.pdf",
}

# ==================== PDF生成代码 ====================

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 注册中文字体
font_path = "C:/Windows/Fonts/msyh.ttc"
if os.path.exists(font_path):
    pdfmetrics.registerFont(TTFont('SimHei', font_path))
    FONT_NAME = 'SimHei'
else:
    FONT_NAME = 'Helvetica'

# 颜色定义
DARK_BLUE = HexColor('#1a1a2e')
RED = HexColor('#e94560')
LIGHT_GRAY = HexColor('#f5f5f0')
DARK_GRAY = HexColor('#333333')

def load_data(filepath):
    """加载JSON数据"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_data(data):
    """分析数据"""
    from collections import Counter
    import jieba.analyse

    # 统计用户
    authors = Counter([p['author'] for p in data])
    top_users = authors.most_common(10)

    # 统计时间分布
    times = [p['time'] for p in data if p.get('time')]

    # 提取关键词
    all_text = " ".join([p['content'] for p in data])
    keywords = jieba.analyse.extract_tags(all_text, topK=20)

    return {
        'total_posts': len(data),
        'total_users': len(authors),
        'top_users': top_users,
        'keywords': keywords,
    }

def create_styles():
    """创建样式"""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name='ChineseTitle',
        fontName=FONT_NAME,
        fontSize=36,
        leading=42,
        alignment=TA_CENTER,
        textColor=white
    ))

    styles.add(ParagraphStyle(
        name='ChineseH1',
        fontName=FONT_NAME,
        fontSize=24,
        leading=30,
        alignment=TA_LEFT,
        textColor=DARK_BLUE,
        spaceBefore=20,
        spaceAfter=10
    ))

    styles.add(ParagraphStyle(
        name='ChineseH2',
        fontName=FONT_NAME,
        fontSize=18,
        leading=24,
        alignment=TA_LEFT,
        textColor=DARK_BLUE,
        spaceBefore=15,
        spaceAfter=8
    ))

    styles.add(ParagraphStyle(
        name='ChineseBody',
        fontName=FONT_NAME,
        fontSize=11,
        leading=18,
        alignment=TA_JUSTIFY,
        textColor=DARK_GRAY,
        spaceBefore=5,
        spaceAfter=5
    ))

    styles.add(ParagraphStyle(
        name='ChineseSmall',
        fontName=FONT_NAME,
        fontSize=10,
        leading=16,
        alignment=TA_LEFT,
        textColor=DARK_GRAY
    ))

    styles.add(ParagraphStyle(
        name='ChineseQuote',
        fontName=FONT_NAME,
        fontSize=12,
        leading=20,
        alignment=TA_CENTER,
        textColor=DARK_GRAY,
        leftIndent=20,
        rightIndent=20,
        spaceBefore=10,
        spaceAfter=10
    ))

    return styles

def build_report(config, data, analysis):
    """构建报告"""
    doc = SimpleDocTemplate(
        config['output_filename'],
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm
    )

    styles = create_styles()
    story = []

    # ===== 封面 =====
    story.append(Paragraph("GUAN CHA JIA", styles['ChineseTitle']))
    story.append(Paragraph("THE OBSERVER", ParagraphStyle(
        name='Sub', fontName=FONT_NAME, fontSize=12, alignment=TA_CENTER, textColor=white
    )))
    story.append(HRFlowable(width="100%", thickness=2, color=RED, spaceAfter=10))
    story.append(Paragraph(f"{datetime.now().strftime('%Y-%m-%d')} | {config['subtitle']}", styles['ChineseSmall']))
    story.append(Spacer(1, 20))

    story.append(Paragraph(f"<font color='#e94560'>[SPECIAL REPORT]</font>", ParagraphStyle(
        name='Tag', fontName=FONT_NAME, fontSize=12, alignment=TA_CENTER, textColor=RED
    )))
    story.append(Paragraph(config['title'], styles['ChineseH1']))
    story.append(Paragraph(config['topic'], styles['ChineseH2']))
    story.append(Spacer(1, 20))

    # 统计
    stats_data = [
        [str(analysis['total_posts']), str(analysis['total_users']), '10+', '3h+'],
        ['Posts', 'Users', 'Keywords', 'Duration']
    ]
    stats_table = Table(stats_data, colWidths=[90]*4)
    stats_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), FONT_NAME),
        ('FONTSIZE', (0,0), (-1,0), 28),
        ('FONTSIZE', (0,1), (-1,1), 9),
        ('TEXTCOLOR', (0,0), (-1,0), RED),
        ('TEXTCOLOR', (0,1), (-1,1), DARK_GRAY),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(stats_table)
    story.append(PageBreak())

    # ===== 时间线 =====
    story.append(Paragraph("<font color='#e94560'>TIMELINE</font>", styles['ChineseH1']))
    story.append(HRFlowable(width="100%", thickness=1, color=RED, spaceAfter=15))

    for time, event in config['timeline']:
        story.append(Paragraph(f"<font color='#e94560'><b>{time}</b></font>  {event}", styles['ChineseSmall']))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 20))

    # ===== 观点 =====
    story.append(Paragraph("<font color='#e94560'>VIEWPOINTS</font>", styles['ChineseH1']))
    story.append(HRFlowable(width="100%", thickness=1, color=RED, spaceAfter=15))

    for title, content, author in config['viewpoints']:
        story.append(Paragraph(f"<b>{title}</b>", styles['ChineseSmall']))
        story.append(Paragraph(f"   {content}", styles['ChineseSmall']))
        story.append(Paragraph(f"   - {author}", ParagraphStyle(
            name='VA', fontName=FONT_NAME, fontSize=9, alignment=TA_RIGHT, textColor=RED
        )))
        story.append(Spacer(1, 8))

    story.append(PageBreak())

    # ===== 金句 =====
    story.append(Paragraph("<font color='#e94560'>GOLDEN QUOTES</font>", styles['ChineseH1']))
    story.append(HRFlowable(width="100%", thickness=1, color=RED, spaceAfter=20))

    for text, author in config['quotes']:
        story.append(Paragraph(f"<font color='#e94560'>\"</font>{text}<font color='#e94560'>\"</font>", styles['ChineseQuote']))
        story.append(Paragraph(f"- {author}", ParagraphStyle(
            name='QA', fontName=FONT_NAME, fontSize=10, alignment=TA_CENTER, textColor=RED, spaceAfter=15
        )))

    story.append(Spacer(1, 20))

    # ===== 用户榜 =====
    story.append(Paragraph("<font color='#e94560'>TOP USERS</font>", styles['ChineseH1']))
    story.append(HRFlowable(width="100%", thickness=1, color=RED, spaceAfter=15))

    users_data = [['Rank', 'User', 'Posts', 'Role']]
    for i, (user, count) in enumerate(analysis['top_users'][:8], 1):
        users_data.append([str(i), user, str(count), 'Active'])

    users_table = Table(users_data, colWidths=[40, 100, 50, 110])
    users_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), FONT_NAME),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BACKGROUND', (0,0), (-1,0), DARK_BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('TEXTCOLOR', (0,1), (0,-1), RED),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, DARK_GRAY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, LIGHT_GRAY]),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(users_table)

    story.append(Spacer(1, 25))

    # ===== 关键词 =====
    story.append(Paragraph("<font color='#e94560'>KEYWORDS</font>", styles['ChineseH2']))
    story.append(Paragraph("  ".join(analysis['keywords'][:15]), styles['ChineseBody']))

    # ===== 页脚 =====
    story.append(Spacer(1, 30))
    story.append(HRFlowable(width="100%", thickness=1, color=DARK_BLUE, spaceAfter=15))
    story.append(Paragraph("THE OBSERVER", ParagraphStyle(
        name='F1', fontName=FONT_NAME, fontSize=14, alignment=TA_CENTER, textColor=DARK_BLUE
    )))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d')}", styles['ChineseSmall']))

    doc.build(story)
    print(f"Report generated: {config['output_filename']}")

def main():
    print("=" * 50)
    print("Forum Report Generator Template")
    print("=" * 50)

    # 加载数据
    print(f"\nLoading data from: {CONFIG['data_file']}")
    data = load_data(CONFIG['data_file'])
    print(f"Loaded {len(data)} posts")

    # 分析数据
    print("\nAnalyzing data...")
    analysis = analyze_data(data)
    print(f"Total users: {analysis['total_users']}")
    print(f"Top user: {analysis['top_users'][0][0]} ({analysis['top_users'][0][1]} posts)")

    # 生成报告
    print(f"\nGenerating report: {CONFIG['output_filename']}")
    build_report(CONFIG, data, analysis)

    print("\nDone!")

if __name__ == "__main__":
    main()
