# -*- coding: utf-8 -*-
"""
伊朗-以色列冲突专题报道 PDF生成器
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

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

def create_styles():
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

def build_pdf():
    doc = SimpleDocTemplate(
        "E:/claude/iran_conflict_report.pdf",
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm
    )

    styles = create_styles()
    story = []

    # ===== 头版 =====
    story.append(Paragraph("GUAN CHA JIA", styles['ChineseTitle']))
    story.append(Paragraph("THE OBSERVER", ParagraphStyle(
        name='Subtitle', fontName=FONT_NAME, fontSize=12, alignment=TA_CENTER, textColor=white
    )))
    story.append(HRFlowable(width="100%", thickness=2, color=RED, spaceAfter=10))
    story.append(Paragraph("2026-3-1 | Stage1st | Page 120-133", styles['ChineseSmall']))
    story.append(Spacer(1, 20))

    story.append(Paragraph("<font color='#e94560'>[BREAKING NEWS]</font>", ParagraphStyle(
        name='Tag', fontName=FONT_NAME, fontSize=12, alignment=TA_CENTER, textColor=RED
    )))
    story.append(Paragraph("Middle East After Khamenei's Death", styles['ChineseH1']))
    story.append(Paragraph("Iran's Headless Knight Fights Back", styles['ChineseH1']))
    story.append(Spacer(1, 15))

    story.append(Paragraph(
        "US-Israel decapitation strike killed Iran's Supreme Leader Khamenei, former President Ahmadinejad and other top officials, "
        "but unexpectedly released the Revolutionary Guard from their 'seal'. "
        "Missile launch authority decentralized, asymmetric warfare unleashed, Jihad decree issued - Middle East situation deteriorates rapidly.",
        ParagraphStyle(name='Lead', fontName=FONT_NAME, fontSize=11, leading=18, alignment=TA_JUSTIFY, textColor=DARK_GRAY)
    ))
    story.append(Spacer(1, 20))

    # 统计数据
    stats_data = [
        ['544', '167', '14', '3h+'],
        ['Posts', 'Users', 'Pages', 'Duration']
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
    story.append(Spacer(1, 25))

    # 关键事件
    story.append(HRFlowable(width="100%", thickness=1, color=DARK_BLUE, spaceAfter=15))
    story.append(Paragraph("<font color='#e94560'>KEY EVENTS</font>", styles['ChineseH2']))

    events = [
        "Khamenei killed in US-Israel airstrike",
        "Ahmadinejad also killed in the attack",
        "Alireza Arafi appointed as interim Supreme Leader",
        "Iran fires missiles at USS Abraham Lincoln",
        "Strait of Hormuz shipping disrupted",
        "Brent crude oil up 10%"
    ]
    for event in events:
        story.append(Paragraph(f"- {event}", styles['ChineseSmall']))

    story.append(PageBreak())

    # ===== 时间线 =====
    story.append(Paragraph("<font color='#e94560'>TIMELINE</font>", styles['ChineseH1']))
    story.append(HRFlowable(width="100%", thickness=1, color=RED, spaceAfter=15))

    timeline = [
        ("21:26", "Iranian F-4 jets bomb US base in Iraqi Kurdistan"),
        ("21:27", "Maersk suspends Hormuz transit, Brent crude +10%"),
        ("21:28", "250+ ships anchored in Hormuz, insurance rates soar"),
        ("21:31", "President Pezeshkian delivers first post-war speech"),
        ("21:40", "Confirmed: Ahmadinejad killed in attack"),
        ("21:43", "Grand Ayatollah Makarem issues Jihad decree"),
        ("21:47", "Alireza Arafi named interim Supreme Leader"),
        ("21:55", "IRGC: 4 ballistic missiles fired at USS Lincoln"),
        ("22:05", "FM: Military operating independently, authority decentralized"),
        ("22:09", "Iranian missile hits French naval base in Abu Dhabi"),
        ("22:11", "Reports: 4 US B-2 bombers participated in Iran strike"),
        ("22:29", "Iran attacks UAE oil platform"),
    ]

    for time, event in timeline:
        story.append(Paragraph(f"<font color='#e94560'><b>{time}</b></font>  {event}", styles['ChineseSmall']))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 15))

    # 引用
    story.append(Paragraph(
        "\"We cannot strike the US mainland, so we have no choice but to attack their bases in the region. "
        "Our military forces are now operating independently, isolated from outside contact.\"",
        styles['ChineseQuote']
    ))
    story.append(Paragraph("- Iranian FM Abbas Araghchi", ParagraphStyle(
        name='QuoteAuthor', fontName=FONT_NAME, fontSize=10, alignment=TA_CENTER, textColor=RED
    )))

    story.append(Spacer(1, 20))

    # 观点分析
    story.append(Paragraph("<font color='#e94560'>VIEWPOINTS</font>", styles['ChineseH1']))
    story.append(HRFlowable(width="100%", thickness=1, color=RED, spaceAfter=15))

    story.append(Paragraph("<b>Core Theme: Hardliners Eliminated, Young Hawks Rise</b>", styles['ChineseH2']))
    story.append(Paragraph(
        "Forum users generally believe the US-Israel decapitation strike accidentally removed Iran's 'moderate' faction, "
        "allowing the Revolutionary Guard's younger generation to take control. As one user noted: "
        "\"From the 12-Day War we can see the mid-low level guards have clear-headed brave fighters, it's the top that's compromiser.\"",
        styles['ChineseBody']
    ))

    viewpoints = [
        ("Military Strategy: Decentralized Counterattack", "Delegating missile launch authority to mid-level commanders makes this uncontrollable.", "hululuxiu"),
        ("Tech Gap: Not Decisive", "US can't even intercept small drones now. Iran can fire missiles easily.", "ycjiang1337"),
        ("Regional Impact: GCC Biggest Loser", "Investors won't put money near an unstable Iran.", "pointer243"),
        ("Decapitation Effect: Backfired", "As long as Iran targets military bases, they hold moral high ground.", "yijiyongcun"),
    ]

    for title, content, author in viewpoints:
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

    quotes = [
        ("The US is Hydra, Iran is Headless Knight.", "zhutumengjinR"),
        ("Dark tactics - Prince offers his own head. Khamenei played the Eight Wonders.", "xingbujizhenkeai"),
        ("Never thought Iran would fight like this. Solved the small rocket problem from 12-Day War.", "sofing"),
        ("Now it's turn-based. Daytime is Israel-US turn, nighttime is Iran turn.", "longqishiyinzhiping"),
        ("After Old Ha's death, the limiter is released.", "xuecongxinsheng"),
        ("Top wiped out, suppressed factions rise. Is this the new Godzilla?", "scikirbypoke"),
        ("Sometimes the dead are more useful than the living.", "yijiyongcun"),
    ]

    for text, author in quotes:
        story.append(Paragraph(f"<font color='#e94560'>\"</font>{text}<font color='#e94560'>\"</font>", styles['ChineseQuote']))
        story.append(Paragraph(f"- {author}", ParagraphStyle(
            name='QA', fontName=FONT_NAME, fontSize=10, alignment=TA_CENTER, textColor=RED, spaceAfter=15
        )))

    story.append(Spacer(1, 20))

    # 用户榜
    story.append(Paragraph("<font color='#e94560'>TOP USERS</font>", styles['ChineseH1']))
    story.append(HRFlowable(width="100%", thickness=1, color=RED, spaceAfter=15))

    users_data = [
        ['Rank', 'User', 'Posts', 'Role'],
        ['1', 'Ny', '50', 'News Aggregator'],
        ['2', 'iantsai', '29', 'Military Analysis'],
        ['3', 'Longqi', '28', 'Commentary'],
        ['4', 'Lokad', '23', 'Strategy Analysis'],
        ['5', 'zeroboss4', '22', 'Multi-angle View'],
        ['6', 'Dongjingrelei', '18', 'Opinion'],
        ['7', 'Pinulu', '17', 'Tech Analysis'],
        ['8', 'ycjiang1337', '16', 'Deep Analysis'],
    ]

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

    story.append(Paragraph("<font color='#e94560'>KEYWORDS</font>", styles['ChineseH2']))
    story.append(Paragraph(
        "Iran  Missile  Israel  US Military  Base  Hormuz  Oil Price  Khamenei  GCC  Liberals  Conservatives  Young Hawks  USS Lincoln  Jihad",
        styles['ChineseBody']
    ))

    story.append(PageBreak())

    # ===== 总结 =====
    story.append(Paragraph("<font color='#e94560'>CONCLUSION</font>", styles['ChineseH1']))
    story.append(HRFlowable(width="100%", thickness=1, color=RED, spaceAfter=15))

    story.append(Paragraph(
        "This discussion reflects S1 forum users' deep interest and analytical capabilities regarding Middle East affairs. "
        "From military technology to geopolitics, from weapons gap to international games, users demonstrated multi-dimensional thinking.",
        styles['ChineseBody']
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "The core consensus: The US-Israel decapitation strike may have backfired, removing Iran's 'brakes' at the top "
        "and unleashing the Revolutionary Guard's young hawks. The decentralized counterattack model makes the situation more unpredictable.",
        styles['ChineseBody']
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "As one user said: The 'Headless Knight's' rampage may be harder to deal with than the 'Hydra'.",
        styles['ChineseBody']
    ))

    story.append(Spacer(1, 30))

    # 页脚
    story.append(HRFlowable(width="100%", thickness=1, color=DARK_BLUE, spaceAfter=15))
    story.append(Paragraph("THE OBSERVER", ParagraphStyle(
        name='F1', fontName=FONT_NAME, fontSize=14, alignment=TA_CENTER, textColor=DARK_BLUE
    )))
    story.append(Paragraph("Source: Stage1st Forum thread-2271232 | Date: 2026-03-01", styles['ChineseSmall']))
    story.append(Paragraph("Report generated by Claude Code for research purposes only", styles['ChineseSmall']))

    # 构建PDF
    doc.build(story)
    print("PDF generated: E:/claude/iran_conflict_report.pdf")

if __name__ == "__main__":
    build_pdf()
