# -*- coding: utf-8 -*-
"""
Iran Counterattack Special Report PDF Generator - 2026-03-04
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Register Chinese font
font_path = "C:/Windows/Fonts/msyh.ttc"
if os.path.exists(font_path):
    pdfmetrics.registerFont(TTFont('SimHei', font_path))
    FONT_NAME = 'SimHei'
else:
    FONT_NAME = 'Helvetica'

# Colors
DARK_RED = HexColor('#8B0000')
RED = HexColor('#CC0000')
LIGHT_GRAY = HexColor('#F5F5F0')
DARK_GRAY = HexColor('#333333')
HEADER_BG = HexColor('#1A1A1A')

def create_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name='Masthead',
        fontName=FONT_NAME,
        fontSize=42,
        leading=48,
        alignment=TA_CENTER,
        textColor=DARK_RED,
        spaceBefore=0,
        spaceAfter=0
    ))

    styles.add(ParagraphStyle(
        name='Subtitle',
        fontName=FONT_NAME,
        fontSize=14,
        leading=18,
        alignment=TA_CENTER,
        textColor=DARK_GRAY,
        spaceBefore=5,
        spaceAfter=5
    ))

    styles.add(ParagraphStyle(
        name='Headline',
        fontName=FONT_NAME,
        fontSize=28,
        leading=34,
        alignment=TA_CENTER,
        textColor=black,
        spaceBefore=15,
        spaceAfter=10
    ))

    styles.add(ParagraphStyle(
        name='SubHeadline',
        fontName=FONT_NAME,
        fontSize=18,
        leading=24,
        alignment=TA_CENTER,
        textColor=DARK_RED,
        spaceBefore=5,
        spaceAfter=15
    ))

    styles.add(ParagraphStyle(
        name='Lead',
        fontName=FONT_NAME,
        fontSize=12,
        leading=20,
        alignment=TA_JUSTIFY,
        textColor=DARK_GRAY,
        spaceBefore=10,
        spaceAfter=15
    ))

    styles.add(ParagraphStyle(
        name='SectionTitle',
        fontName=FONT_NAME,
        fontSize=16,
        leading=22,
        alignment=TA_LEFT,
        textColor=DARK_RED,
        spaceBefore=15,
        spaceAfter=8
    ))

    styles.add(ParagraphStyle(
        name='Body',
        fontName=FONT_NAME,
        fontSize=11,
        leading=18,
        alignment=TA_JUSTIFY,
        textColor=DARK_GRAY,
        spaceBefore=5,
        spaceAfter=5
    ))

    styles.add(ParagraphStyle(
        name='Quote',
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

    styles.add(ParagraphStyle(
        name='Author',
        fontName=FONT_NAME,
        fontSize=10,
        alignment=TA_RIGHT,
        textColor=RED
    ))

    styles.add(ParagraphStyle(
        name='SmallText',
        fontName=FONT_NAME,
        fontSize=9,
        leading=14,
        alignment=TA_LEFT,
        textColor=DARK_GRAY
    ))

    styles.add(ParagraphStyle(
        name='TimelineItem',
        fontName=FONT_NAME,
        fontSize=10,
        leading=16,
        alignment=TA_LEFT,
        textColor=DARK_GRAY,
        leftIndent=10,
        spaceBefore=3,
        spaceAfter=3
    ))

    return styles

def build_pdf():
    doc = SimpleDocTemplate(
        "E:/claude/stage1st_project/docs/Battle_Report_2026-03-04_Iran_Counterattack.pdf",
        pagesize=A4,
        rightMargin=15*mm,
        leftMargin=15*mm,
        topMargin=15*mm,
        bottomMargin=15*mm
    )

    styles = create_styles()
    story = []

    # Header
    story.append(Paragraph("ZHAN BAO", styles['Masthead']))
    story.append(Paragraph("S1 OBSERVER | STAGE1ST FORUM DAILY", styles['Subtitle']))
    story.append(HRFlowable(width="100%", thickness=3, color=DARK_RED, spaceBefore=5, spaceAfter=5))
    story.append(Paragraph("2026-03-04 | Thread: 2275908 | 74 Pages | 2937 Posts | 550 Users", styles['SmallText']))
    story.append(Spacer(1, 10))

    # Headline
    story.append(Paragraph("<font color='#CC0000'>[HEADLINE]</font> Iran Counterattack Enters Day 4", styles['Headline']))
    story.append(Paragraph("IRGC Distributed Warfare Proves Effective | US Bases Under Sustained Attack", styles['SubHeadline']))

    # Lead
    lead_text = """
    <b>TEHRAN</b> - 72 hours have passed since the US-Israel decapitation strike that killed Supreme Leader Khamenei
    and other top officials on the first day. Contrary to Western expectations, the Islamic Revolutionary Guard Corps (IRGC)
    has not collapsed into chaos. Instead, a pre-designed distributed warfare mechanism was activated - missile launch
    authority has been delegated to mid-level commanders, creating a "Headless Knight" mode of retaliation.
    According to statistics, Iran has launched over 1,300 missiles and drones at US bases across the Gulf region in three days.
    """
    story.append(Paragraph(lead_text, styles['Lead']))

    # Stats
    stats_data = [
        ['2937', '550', '74', '3 Days'],
        ['Posts', 'Users', 'Pages', 'Duration']
    ]
    stats_table = Table(stats_data, colWidths=[100, 100, 100, 100])
    stats_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), FONT_NAME),
        ('FONTSIZE', (0,0), (-1,0), 24),
        ('FONTSIZE', (0,1), (-1,1), 10),
        ('TEXTCOLOR', (0,0), (-1,0), DARK_RED),
        ('TEXTCOLOR', (0,1), (-1,1), DARK_GRAY),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('BOX', (0,0), (-1,-1), 1, DARK_RED),
    ]))
    story.append(stats_table)
    story.append(Spacer(1, 15))

    # Battle Updates
    story.append(HRFlowable(width="100%", thickness=1, color=DARK_GRAY, spaceAfter=10))
    story.append(Paragraph("<font color='#CC0000'>BATTLE UPDATES</font>", styles['SectionTitle']))

    events = [
        "<b>Mar 3, 10:17</b> - New discussion thread opened as previous one reached page limit",
        "<b>Mar 3, 11:00</b> - Iran launches missiles at Bahrain US base, 5th Fleet HQ struck",
        "<b>Mar 3, 11:19</b> - Fars News: 650 US casualties in first two days of fighting",
        "<b>Mar 3, 11:26</b> - Stats: Iran has launched 1300+ missiles and drones at Gulf region",
        "<b>Mar 3, 12:00</b> - Critical 72-hour mark passed, Iran survives first wave",
        "<b>Mar 3, 12:08</b> - Hezbollah launches drones at northern Israel, Golan Heights alert",
        "<b>Mar 3, 18:12</b> - Iran launches new missile wave at Qatar, Bahrain, Oman bases",
        "<b>Mar 3, 19:20</b> - Iranian FM: Military units operating independently, unstoppable",
    ]

    for event in events:
        story.append(Paragraph(f"[{event}]", styles['TimelineItem']))

    story.append(Spacer(1, 10))

    # Missile Data
    story.append(Paragraph("<font color='#CC0000'>MISSILE STRIKE DATA</font>", styles['SectionTitle']))

    missile_data = [
        ['Target', 'Missiles', 'Drones'],
        ['Kuwait', '97', '283'],
        ['UAE', '167', '541'],
        ['Bahrain', '61', '34'],
        ['Qatar', '65', '12'],
        ['Jordan', '1', '49'],
        ['Iraq', 'N/A', 'N/A'],
        ['Saudi Arabia', 'N/A', 'N/A'],
    ]
    missile_table = Table(missile_data, colWidths=[150, 100, 100])
    missile_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), FONT_NAME),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BACKGROUND', (0,0), (-1,0), DARK_RED),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('TEXTCOLOR', (0,1), (-1,-1), DARK_GRAY),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, DARK_GRAY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, LIGHT_GRAY]),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(missile_table)

    story.append(PageBreak())

    # Analysis
    story.append(Paragraph("<font color='#CC0000'>IN-DEPTH ANALYSIS</font>", styles['SectionTitle']))
    story.append(HRFlowable(width="100%", thickness=1, color=DARK_GRAY, spaceAfter=10))

    story.append(Paragraph("<b>Distributed Command: Iran's 'Headless Knight' Strategy</b>", styles['SectionTitle']))
    analysis1 = """
    After Khamenei's death in the US-Israel airstrike, the international community expected Iran to descend into
    power vacuum and chaos. However, the IRGC demonstrated a pre-designed distributed warfare mechanism -
    missile launch authority has been delegated to mid-level commanders, creating a "Headless Knight" retaliation mode.
    As Iranian FM Araghchi stated: "We have instructed our armed forces to be careful in selecting targets.
    In fact, our military units are currently operating independently."

    This mechanism enables Iran's counterattacks to function without central command. Even with the leadership
    decapitated, units at all levels can continue fighting independently. A forum user commented: "From the
    12-Day War we can see that the IRGC mid-low level has clear-headed brave fighters - it's the top that
    had compromisers. Now the top is eliminated, the limiter is released, unleashing true combat power."
    """
    story.append(Paragraph(analysis1, styles['Body']))

    story.append(Paragraph("<b>US-Israel Dilemma: Ammo Depletion and Strategic Passivity</b>", styles['SectionTitle']))
    analysis2 = """
    After three days of intense combat, the US-Israel side faces serious challenges. US air defense ammunition
    reserves are rapidly depleting, forcing redeployment of Patriot missiles from Europe and Asia-Pacific.
    Israeli air defense systems are similarly strained, with analysis suggesting "Iron Dome" interceptors are
    being consumed at alarming rates.

    More critically, US air strike capability is declining. With aerial refueling tanker fleets saturated,
    the Israeli Air Force cannot commit more sorties against Iran and has shifted to bombing Hezbollah targets
    in Lebanon. As one user noted: "Aircraft are essentially consumables too, especially for the aging USAF fleet."

    Iran's "small quantity, multiple waves" strategy - launching dozens of missile and drone waves daily -
    effectively consumes enemy air defense resources while maintaining its own strike capability.
    """
    story.append(Paragraph(analysis2, styles['Body']))

    story.append(Paragraph("<b>Strait of Hormuz: Global Energy Chokepoint</b>", styles['SectionTitle']))
    analysis3 = """
    The risk of a Strait of Hormuz blockade has become a focus of international attention. Data shows multiple
    countries have high dependency on oil transport through this strait: Japan 91%, South Korea 69%,
    Philippines 94%, Sri Lanka 100%. By comparison, China's crude oil through the strait is only 50%,
    and Iran has indicated it will allow Chinese vessels to pass.

    User "C.W.Nimitz" analyzed: "If the blockade exceeds two weeks, Japan and Korea will face energy collapse first.
    Their gas reserves can only last 10 days to three weeks, after which they'll have to compete for resources."
    """
    story.append(Paragraph(analysis3, styles['Body']))

    story.append(Spacer(1, 15))

    # Quotes
    story.append(Paragraph("<font color='#CC0000'>GOLDEN QUOTES FROM FORUM</font>", styles['SectionTitle']))
    story.append(HRFlowable(width="100%", thickness=1, color=DARK_GRAY, spaceAfter=10))

    quotes = [
        ("The US is Hydra, Iran is Headless Knight. The Headless Knight's rampage may be harder to deal with.", "zhutumengjinR"),
        ("Dark tactics - Prince offers his own head. Khamenei played the Eight Wonders.", "xingbujizhenkeai"),
        ("Never thought Iran would fight like this. Solved the small rocket problem from 12-Day War.", "sofing"),
        ("Now it's turn-based. Daytime is Israel-US turn, nighttime is Iran turn.", "longqishiyinzhiping"),
        ("After Old Ha's death, the limiter is released.", "xuecongxinsheng"),
        ("Top wiped out, suppressed factions rise. Is this the new Godzilla?", "scikirbypoke"),
        ("Sometimes the dead are more useful than the living.", "yijiyongcun"),
        ("Fifth Fleet HQ at enemy's doorstep - they want to be hit harder?", "cyberalogo"),
        ("Iran right now is like a mad dog released from its cage.", "ycjiang1337"),
        ("After Soviet collapse, US fought 30 years of policing wars and forgot what great power war means.", "kaluoan"),
    ]

    for quote, author in quotes:
        story.append(Paragraph(f'<font color="#CC0000">"</font>{quote}<font color="#CC0000">"</font>', styles['Quote']))
        story.append(Paragraph(f"-- {author}", styles['Author']))
        story.append(Spacer(1, 5))

    story.append(PageBreak())

    # Viewpoints
    story.append(Paragraph("<font color='#CC0000'>KEY VIEWPOINTS</font>", styles['SectionTitle']))
    story.append(HRFlowable(width="100%", thickness=1, color=DARK_GRAY, spaceAfter=10))

    viewpoints = [
        ("Strategy: Who Benefits from Prolonged War?",
         "Forum analysis suggests Iran's 'little摩托车' (small drones) production is massive, capable of sustained "
         "consumption of enemy air defense resources. Meanwhile, US long-range strike capability is limited, "
         "with tanker fleets saturated. If Iran maintains current strike frequency for two weeks, "
         "US-Israel will face difficult choices. User 'regular' noted: 'At current intensity, the US-Israel side "
         "will run out of attack and defense capability first.'",
         "Multiple Users"),
        ("Bahrain: 5th Fleet's Nightmare",
         "Bahrain, home to the US 5th Fleet headquarters, has become a primary Iranian target. Analysis suggests "
         "the base houses over 10,000 US personnel and cannot be evacuated quickly like Afghanistan. "
         "Sustained missile attacks could cause significant casualties. As one user put it: "
         "'US bases are useless against missiles - countries hosting them need to think twice.'",
         "Water Well and others"),
        ("Gulf States' Dilemma",
         "Saudi Arabia, UAE and other Gulf states face a dilemma: facing Iranian threats while bearing risks "
         "from US bases on their soil. Saudi oil facilities have already been struck, though Iran's FM denied "
         "responsibility. A user observed: 'They thought US forces were guardian angels, but they're actually plagues.'",
         "Various Discussions"),
        ("Hezbollah Opens Second Front",
         "Lebanese Hezbollah has begun launching rockets and drones at northern Israel, opening a second front. "
         "The IDF has issued evacuation orders for southern Lebanon, preparing for ground operations. "
         "However, analysis suggests opening a new front will be more difficult while Israeli air defense "
         "systems are under strain.",
         "scikirbypoke and others"),
    ]

    for title, content, author in viewpoints:
        story.append(Paragraph(f"<b>{title}</b>", styles['SmallText']))
        story.append(Paragraph(content, styles['Body']))
        story.append(Paragraph(f"-- {author}", styles['Author']))
        story.append(Spacer(1, 10))

    # Active Users
    story.append(Paragraph("<font color='#CC0000'>TOP CONTRIBUTORS</font>", styles['SectionTitle']))
    story.append(HRFlowable(width="100%", thickness=1, color=DARK_GRAY, spaceAfter=10))

    users_data = [
        ['Rank', 'User', 'Posts', 'Role'],
        ['1', 'zeroboss4', '143', 'News Updates'],
        ['2', 'Ny', '129', 'News Aggregator'],
        ['3', 'DongfangJiaoShi', '127', 'Deep Analysis'],
        ['4', 'kaluoan', '106', 'Military Analysis'],
        ['5', 'FengXueWuSmile', '92', 'Intel Integration'],
        ['6', 'PiNuLv', '64', 'Tactical Commentary'],
        ['7', 'Promeus', '60', 'Weapons Analysis'],
        ['8', 'BaFangFengYuLai', '57', 'Live Updates'],
        ['9', 'ZheLing', '50', 'Opinion Output'],
        ['10', 'ZhuTuMengJinR', '42', 'Background Context'],
    ]
    users_table = Table(users_data, colWidths=[40, 120, 50, 110])
    users_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), FONT_NAME),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BACKGROUND', (0,0), (-1,0), HEADER_BG),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('TEXTCOLOR', (0,1), (0,-1), DARK_RED),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, DARK_GRAY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, LIGHT_GRAY]),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(users_table)

    story.append(Spacer(1, 20))

    # Keywords
    story.append(Paragraph("<font color='#CC0000'>KEYWORDS</font>", styles['SectionTitle']))
    story.append(Paragraph(
        "Iran | Missile | US Military | Israel | Base | IRGC | Air Defense | Drone | Hormuz | "
        "Bahrain | Saudi | Hezbollah | Ammunition | Tanker | JDAM | Little Moto | 5th Fleet | "
        "Decapitation | Khamenei | Netanyahu | Trump | War of Attrition | Energy | Oil Price",
        styles['Body']
    ))

    story.append(PageBreak())

    # Outlook
    story.append(Paragraph("<font color='#CC0000'>OUTLOOK</font>", styles['SectionTitle']))
    story.append(HRFlowable(width="100%", thickness=1, color=DARK_GRAY, spaceAfter=10))

    conclusion = """
    <b>72 Hours Passed, War Enters New Phase</b>

    Iran has successfully weathered the most dangerous first wave. The effective operation of the distributed
    warfare mechanism means the US-Israel decapitation strategy failed to achieve its intended effect.
    Instead, the IRGC's counterattack intensity exceeded expectations, with US bases across the Gulf region
    continuing to sustain strikes.

    <b>Key Points to Watch</b>

    1. <b>Ammo War of Attrition</b>: Can US-Israel air defense ammunition hold out? Can Iran's missile and drone
       inventories be sustained?

    2. <b>Strait of Hormuz</b>: If Iran decides on full blockade, global energy markets will face shock.
       Japan and Korea will be first affected.

    3. <b>Ground War Risk</b>: Israel has assembled troops at the Lebanon border, but opening a ground front
       will further strain resources.

    4. <b>Political Direction</b>: How will US domestic support for the war evolve? Can Trump sustain
       continued US casualties in the Middle East?

    5. <b>International Response</b>: Gulf states' attitudes are subtly shifting. Saudi Arabia, UAE and others
       are beginning to feel the pressure of "choosing sides."

    <b>Forum Consensus</b>

    This war is rewriting the Middle East landscape. Regardless of final outcome, US deterrence in the region
    has been damaged. As one user noted: "Another nail in the empire's coffin."

    Iran's resistance may become a turning point in Middle Eastern history - proving that even a superpower
    cannot easily suppress a determined, prepared opponent.
    """
    story.append(Paragraph(conclusion, styles['Body']))

    story.append(Spacer(1, 20))

    # Quotes
    story.append(HRFlowable(width="100%", thickness=1, color=DARK_RED, spaceBefore=10, spaceAfter=10))
    story.append(Paragraph(
        '<font color="#CC0000">"</font>We cannot strike the US mainland, so we have no choice but to attack '
        'their bases in the region. Our military forces are now operating independently, isolated from outside contact.<font color="#CC0000">"</font>',
        styles['Quote']
    ))
    story.append(Paragraph("-- Iranian FM Abbas Araghchi", styles['Author']))
    story.append(Spacer(1, 15))

    story.append(Paragraph(
        '<font color="#CC0000">"</font>This is not an endless war, but one that will open an era of peace '
        'we never dreamed of.<font color="#CC0000">"</font>',
        styles['Quote']
    ))
    story.append(Paragraph("-- Israeli PM Netanyahu (Fox News Interview)", styles['Author']))

    story.append(Spacer(1, 30))

    # Footer
    story.append(HRFlowable(width="100%", thickness=2, color=DARK_RED, spaceBefore=20, spaceAfter=10))
    story.append(Paragraph("S1 OBSERVER | Battle Report", ParagraphStyle(
        name='Footer1', fontName=FONT_NAME, fontSize=14, alignment=TA_CENTER, textColor=DARK_RED
    )))
    story.append(Paragraph(
        "Source: Stage1st Forum Thread #2275908 | Period: Mar 3-4, 2026 | Generated: Mar 4, 2026",
        styles['SmallText']
    ))
    story.append(Paragraph(
        "This report is for research reference only and does not represent any political position | Generated by Claude Code",
        styles['SmallText']
    ))

    # Build PDF
    doc.build(story)
    print("PDF Report Generated: E:/claude/stage1st_project/docs/Battle_Report_2026-03-04_Iran_Counterattack.pdf")

if __name__ == "__main__":
    build_pdf()
