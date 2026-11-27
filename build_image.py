#!/usr/bin/env python3
"""news-image-20261127 round 3 — fresh broadsheet renderer.

Draws a 1024x1024 JPEG front page summing up Friday 27 November 2026:
50 stories, every one first reported on Friday 27 November 2026 (any time
zone), verified in-session against live sources. Fixed data, fixed geometry,
no randomness, no network, no clock reads — two runs are byte-identical.

Layout (broadsheet, burgundy masthead, cream paper):
  masthead -> giant dateline -> subline -> 10 region chips -> 8 key numbers
  -> UTC timeline (00:30-09:33) -> 3 big scenes -> 12 small scenes
  -> 35 listed rows -> TOMORROW + DATE CHECK -> footer.
Every string is measured before it is drawn; the script raises instead of
shipping clipped or overflowing text.
"""

import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 14
PAPER = (247, 243, 234)
INK = (26, 26, 26)
MUTED = (90, 84, 74)
BURGUNDY = (123, 30, 38)
GOLD = (201, 162, 39)
LINE = (180, 172, 156)
NAVY = (31, 58, 95)
OCHRE = (122, 74, 0)
GREEN = (20, 83, 45)
TINT = (238, 232, 218)
WHITE = (255, 255, 255)
RED = (178, 34, 34)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines, each fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, fnt, x, y, max_w, max_lines, fill=INK,
                  leading=None, align="left"):
    """Draw wrapped text; raise if it needs more than max_lines."""
    if leading is None:
        leading = fnt.size + 3
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) > max_lines:
        raise ValueError(
            "text overflows %d lines: %r -> %r" % (max_lines, text, lines))
    for i, line in enumerate(lines):
        lx = x
        if align == "center":
            lx = x + (max_w - draw.textlength(line, font=fnt)) / 2
        draw.text((lx, y + i * leading), line, font=fnt, fill=fill)
    return y + len(lines) * leading


def fit_check(draw, text, fnt, max_w, label):
    if draw.textlength(text, font=fnt) > max_w:
        raise ValueError("%s too wide: %r" % (label, text))


# ---------------------------------------------------------------- pictograms
# Each takes (draw, x, y, s, ink) and draws inside an s x s box.

def pic_stars(d, x, y, s, ink):
    cx, cy, r = x + s / 2, y + s / 2, s * 0.36
    for k in range(12):
        import math
        a = math.pi * 2 * k / 12 - math.pi / 2
        px, py = cx + r * math.cos(a), cy + r * math.sin(a)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=GOLD)
    d.text((cx - 6, cy - 8), "EU", font=font(SANS_B, int(s * 0.28)),
           fill=NAVY)


def pic_bank(d, x, y, s, ink):
    d.polygon([(x + 2, y + s * 0.38), (x + s / 2, y + 2),
               (x + s - 2, y + s * 0.38)], fill=ink)
    for i in range(3):
        cx = x + s * (0.22 + 0.28 * i)
        d.rectangle([cx - 3, y + s * 0.42, cx + 3, y + s * 0.82], fill=ink)
    d.rectangle([x + 2, y + s * 0.84, x + s - 2, y + s * 0.92], fill=ink)


def pic_bars(d, x, y, s, ink):
    hs = [0.35, 0.55, 0.8]
    for i, h in enumerate(hs):
        bx = x + s * (0.12 + 0.30 * i)
        d.rectangle([bx, y + s * (1 - h), bx + s * 0.20, y + s * 0.95],
                    fill=ink)
    d.line([(x + 2, y + s * 0.55), (x + s * 0.55, y + s * 0.28),
            (x + s - 2, y + s * 0.12)], fill=RED, width=3)
    d.polygon([(x + s - 8, y + s * 0.05), (x + s - 2, y + s * 0.12),
               (x + s - 9, y + s * 0.20)], fill=RED)


def pic_drone(d, x, y, s, ink):
    for cx, cy in [(x + s * 0.14, y + s * 0.2), (x + s * 0.86, y + s * 0.2),
                   (x + s * 0.14, y + s * 0.8), (x + s * 0.86, y + s * 0.8)]:
        d.ellipse([cx - 7, cy - 4, cx + 7, cy + 4], outline=ink, width=2)
    d.line([(x + s * 0.14, y + s * 0.2), (x + s * 0.5, y + s * 0.5)], fill=ink,
           width=2)
    d.line([(x + s * 0.86, y + s * 0.2), (x + s * 0.5, y + s * 0.5)], fill=ink,
           width=2)
    d.line([(x + s * 0.14, y + s * 0.8), (x + s * 0.5, y + s * 0.5)], fill=ink,
           width=2)
    d.line([(x + s * 0.86, y + s * 0.8), (x + s * 0.5, y + s * 0.5)], fill=ink,
           width=2)
    d.ellipse([x + s * 0.36, y + s * 0.36, x + s * 0.64, y + s * 0.64],
              fill=ink)


def pic_skyline(d, x, y, s, ink):
    hs = [0.55, 0.8, 0.45, 0.7, 0.6]
    for i, h in enumerate(hs):
        bx = x + s * (0.04 + 0.19 * i)
        d.rectangle([bx, y + s * (1 - h), bx + s * 0.15, y + s * 0.95],
                    fill=ink)
    d.ellipse([x + s * 0.62, y + s * 0.06, x + s * 0.78, y + s * 0.22],
              fill=GOLD)
    d.ellipse([x + s * 0.30, y + s * 0.10, x + s * 0.44, y + s * 0.24],
              fill=(200, 200, 200))


def pic_shield(d, x, y, s, ink):
    d.polygon([(x + s * 0.5, y + 2), (x + s - 2, y + s * 0.25),
               (x + s - 2, y + s * 0.6), (x + s * 0.5, y + s - 2),
               (x + 2, y + s * 0.6), (x + 2, y + s * 0.25)], fill=ink)
    d.line([(x + s * 0.28, y + s * 0.52), (x + s * 0.45, y + s * 0.68),
            (x + s * 0.74, y + s * 0.32)], fill=WHITE, width=3)


def pic_mic(d, x, y, s, ink):
    d.rounded_rectangle([x + s * 0.38, y + 2, x + s * 0.62, y + s * 0.5],
                        radius=8, fill=ink)
    d.line([(x + s * 0.5, y + s * 0.5), (x + s * 0.5, y + s * 0.78)],
           fill=ink, width=3)
    d.line([(x + s * 0.3, y + s * 0.78), (x + s * 0.7, y + s * 0.78)],
           fill=ink, width=3)
    d.rectangle([x + s * 0.32, y + s * 0.86, x + s * 0.68, y + s * 0.92],
                fill=ink)


def pic_bag(d, x, y, s, ink):
    d.polygon([(x + s * 0.15, y + s * 0.3), (x + s * 0.85, y + s * 0.3),
               (x + s * 0.78, y + s * 0.95), (x + s * 0.22, y + s * 0.95)],
              fill=ink)
    d.arc([x + s * 0.3, y + s * 0.02, x + s * 0.7, y + s * 0.45],
          start=180, end=360, fill=ink, width=3)
    d.text((x + s * 0.38, y + s * 0.5), "%", font=font(SANS_B, int(s * 0.3)),
           fill=WHITE)


def pic_split(d, x, y, s, ink):
    d.rectangle([x + 2, y + s * 0.3, x + s / 2, y + s * 0.7], fill=GREEN)
    d.rectangle([x + s / 2, y + s * 0.3, x + s - 2, y + s * 0.7],
                fill=(120, 120, 120))
    d.text((x + s * 0.08, y + s * 0.42), "65", font=font(SANS_B, int(s * 0.24)),
           fill=WHITE)
    d.text((x + s * 0.62, y + s * 0.42), "65", font=font(SANS_B, int(s * 0.24)),
           fill=WHITE)


def pic_factory(d, x, y, s, ink):
    d.polygon([(x + 2, y + s * 0.5), (x + s * 0.3, y + s * 0.5),
               (x + s * 0.3, y + s * 0.3), (x + s * 0.42, y + s * 0.3),
               (x + s * 0.42, y + s * 0.5), (x + s * 0.55, y + s * 0.35),
               (x + s * 0.68, y + s * 0.5), (x + s - 2, y + s * 0.5),
               (x + s - 2, y + s * 0.95), (x + 2, y + s * 0.95)], fill=ink)
    d.rectangle([x + s * 0.78, y + s * 0.12, x + s * 0.88, y + s * 0.5],
                fill=ink)
    d.ellipse([x + s * 0.74, y + s * 0.02, x + s * 0.86, y + s * 0.14],
              fill=(200, 200, 200))


def pic_barrel(d, x, y, s, ink):
    d.rounded_rectangle([x + s * 0.25, y + s * 0.08, x + s * 0.75,
                         y + s * 0.92], radius=6, fill=ink)
    d.rectangle([x + s * 0.25, y + s * 0.3, x + s * 0.75, y + s * 0.36],
                fill=GOLD)
    d.rectangle([x + s * 0.25, y + s * 0.62, x + s * 0.75, y + s * 0.68],
                fill=GOLD)
    d.text((x + s * 0.40, y + s * 0.42), "$", font=font(SANS_B, int(s * 0.28)),
           fill=WHITE)


def pic_chart(d, x, y, s, ink):
    d.line([(x + 4, y + s * 0.9), (x + s - 4, y + s * 0.9)], fill=ink, width=2)
    d.line([(x + 4, y + s * 0.9), (x + 4, y + 4)], fill=ink, width=2)
    d.line([(x + 6, y + s * 0.7), (x + s * 0.4, y + s * 0.5),
            (x + s * 0.65, y + s * 0.55), (x + s - 4, y + s * 0.15)],
           fill=RED, width=3)
    d.ellipse([x + s - 8, y + s * 0.11, x + s - 1, y + s * 0.19], fill=RED)


def pic_flags(d, x, y, s, ink):
    d.rectangle([x + 2, y + s * 0.2, x + s * 0.48, y + s * 0.8], fill=(255, 153, 51))
    d.rectangle([x + 2, y + s * 0.4, x + s * 0.48, y + s * 0.6], fill=WHITE)
    d.rectangle([x + 2, y + s * 0.6, x + s * 0.48, y + s * 0.8], fill=(19, 136, 8))
    d.rectangle([x + s * 0.52, y + s * 0.2, x + s - 2, y + s * 0.8],
                fill=(60, 59, 110))
    for i in range(3):
        yy = y + s * (0.28 + 0.18 * i)
        d.rectangle([x + s * 0.52, yy, x + s - 2, yy + s * 0.08], fill=WHITE)
    d.ellipse([x + s * 0.56, y + s * 0.24, x + s * 0.68, y + s * 0.38],
              fill=WHITE)


def pic_boat(d, x, y, s, ink):
    d.polygon([(x + s * 0.1, y + s * 0.55), (x + s * 0.9, y + s * 0.55),
               (x + s * 0.75, y + s * 0.85), (x + s * 0.25, y + s * 0.85)],
              fill=ink)
    d.line([(x + s * 0.5, y + s * 0.55), (x + s * 0.5, y + s * 0.1)],
           fill=ink, width=3)
    d.polygon([(x + s * 0.5, y + s * 0.12), (x + s * 0.85, y + s * 0.4),
               (x + s * 0.5, y + s * 0.4)], fill=RED)


def pic_rocket(d, x, y, s, ink):
    d.line([(x + s * 0.2, y + s * 0.9), (x + s * 0.8, y + s * 0.15)],
           fill=ink, width=3)
    d.polygon([(x + s * 0.72, y + s * 0.05), (x + s * 0.95, y + s * 0.12),
               (x + s * 0.8, y + s * 0.3)], fill=RED)
    d.text((x + s * 0.1, y + s * 0.55), "+12%",
           font=font(SANS_B, int(s * 0.22)), fill=RED)


PICS = {
    "stars": pic_stars, "bank": pic_bank, "bars": pic_bars,
    "drone": pic_drone, "skyline": pic_skyline, "shield": pic_shield,
    "mic": pic_mic, "bag": pic_bag, "split": pic_split,
    "factory": pic_factory, "barrel": pic_barrel, "chart": pic_chart,
    "flags": pic_flags, "boat": pic_boat, "rocket": pic_rocket,
}


# ---------------------------------------------------------------- the 50 stories
# Fields: id, headline, detail, region, field, source, pic (pictogram key).
# All 50 first reported Friday 27 November 2026 (any time zone); see
# STRATEGY.md / README.md for per-story verification and the DATE CHECK.

BIG = [
    dict(id="P1", tag="EU SUMMIT · NO DEAL", color=NAVY, pic="stars",
         head="EU leaders leave Brussels with no budget deal",
         detail="€1.58tn budget and €45bn Ukraine loan blocked; 24 states "
                "back the loan. Talks resume 17–18 Dec.",
         region="Europe", field="Politics", source="Consilium/Reuters"),
    dict(id="P5", tag="GAZA · THE TOLL RISES", color=OCHRE, pic="skyline",
         head="Strikes wound children in Gaza City on Friday",
         detail="11 killed in 24 hours; 19 in 48 hours. Toll since the "
                "ceasefire: 1,705. Total since Oct 2023: 74,772.",
         region="Middle East", field="Conflict", source="WAFA/QNA/Al Jazeera"),
    dict(id="P9", tag="NEW ZEALAND · 65–65", color=GREEN, pic="split",
         head="Final count leaves coalition one seat short",
         detail="Coalition 65 of 130 seats; the Opportunity Party is "
                "kingmaker. Result released Friday, 2pm NZ time.",
         region="Oceania", field="Elections", source="NZ Herald/Reuters"),
]

SMALL = [
    dict(id="P2", pic="bank", head="De Cos picked to lead the ECB",
         detail="Ex-Bank of Spain chief succeeds Lagarde in Feb 2027.",
         region="Europe", field="Politics", source="Consilium/Reuters"),
    dict(id="P3", pic="bars", head="Asia shares steady on Friday",
         detail="Kospi +2%, Nikkei +0.7% in the morning wrap.",
         region="East Asia", field="Markets", source="Reuters"),
    dict(id="P4", pic="drone", head="Drone violates Latvia's airspace",
         detail="Unidentified drone crossed in early on Friday.",
         region="Europe", field="Conflict", source="Reuters"),
    dict(id="P6", pic="shield", head="155 drones fired at Ukraine overnight",
         detail="110 shot down; 1 killed, 9 hurt; rail and power hit.",
         region="Europe", field="Conflict", source="Ukrainian AF/h.ua"),
    dict(id="P7", pic="mic", head="Zelensky: US 'too focused' on Mideast",
         detail="BBC interview: Patriot delays are costing lives.",
         region="Europe", field="Politics", source="BBC"),
    dict(id="P8", pic="bag", head="Black Friday: $12.9bn online expected",
         detail="AI steers spending; Adobe sees $12.9bn in one day.",
         region="N. America", field="Retail", source="Adobe/AP"),
    dict(id="P10", pic="factory", head="China factory profits jump 20.1%",
         detail="October industrial profits beat a year earlier.",
         region="East Asia", field="Economy", source="NBS/Reuters"),
    dict(id="P11", pic="barrel", head="Brent crude $96.14 a barrel",
         detail="Down 0.4% on the day, up 3.9% on the week.",
         region="Europe", field="Energy", source="Reuters"),
    dict(id="P12", pic="chart", head="Tokyo inflation hits 16-month high",
         detail="Core CPI 2.9%; the case for a BOJ hike grows.",
         region="East Asia", field="Economy", source="Reuters"),
    dict(id="P13", pic="flags", head="India–US trade deal 'nearing completion'",
         detail="Minister Goyal says the deal is almost done.",
         region="South Asia", field="Diplomacy", source="Reuters"),
    dict(id="P14", pic="boat", head="Seoul sends six North Koreans home",
         detail="Rescued crew repatriated by sea; one chose to stay.",
         region="East Asia", field="Diplomacy", source="Reuters"),
    dict(id="P15", pic="rocket", head="China stocks surge on Beijing's vow",
         detail="Shanghai +3.3%; STAR 50 +12% in afternoon trade.",
         region="East Asia", field="Markets", source="Reuters"),
]

LISTED = [
    ("L1", "Erdogan ratifies Turkey's Mecca defence pact", "Middle East", "Diplomacy", "Reuters"),
    ("L2", "Iran warns over Gulf as Seoul grows naval role", "Middle East", "Diplomacy", "Reuters"),
    ("L3", "Dollar heads for 3rd monthly gain, +1.8%", "N. America", "Markets", "Reuters"),
    ("L4", "S&P futures +1.7%, Nasdaq +2.5% pre-open", "N. America", "Markets", "InvestingLive"),
    ("L5", "Gold $3,662 (+2.7%); silver $43.27 (+4.92%)", "N. America", "Markets", "CoinMarketCap"),
    ("L6", "Brands shift $254m of orders out of Bangladesh", "South Asia", "Trade", "Reuters"),
    ("L7", "Bitcoin ~$61,600 as $7bn of options expire today", "N. America", "Crypto", "CryptoNews"),
    ("L8", "Zelensky: major Russian grid attack imminent", "Europe", "Conflict", "AP"),
    ("L9", "Trump 'a little concerned' by Wednesday market dip", "N. America", "Politics", "Reuters"),
    ("L10", "Bears 39–35 Lions on a TD with 3 seconds left", "N. America", "Sport", "AP"),
    ("L11", "Marseille fan violence condemned; 11 injured", "Europe", "Sport", "Reuters"),
    ("L12", "Macron: €204bn cuts a 'strategic mistake'", "Europe", "Politics", "Reuters/ANI"),
    ("L13", "Merz: no new debt; praises Trump's peace efforts", "Europe", "Politics", "Reuters/ANI"),
    ("L14", "China cabinet vows new steps to steady markets", "East Asia", "Economy", "Xinhua/Reuters"),
    ("L15", "France CPI 3.2%; Spain 4.1%; France GDP −0.2%", "Europe", "Economy", "Reuters/WSJ"),
    ("L16", "Europe opens higher: Stoxx +0.9%, DAX +0.7%", "Europe", "Markets", "WSJ"),
    ("L17", "Gaza: 37 killed in a week; a baby dies of cold", "Middle East", "Health", "Al Jazeera"),
    ("L18", "Russia hits 2 grain ships near Odesa; 100,000+ t", "Europe", "Conflict", "Reuters"),
    ("L19", "Rand +~1% to 17.37; platinum +5%; Top-40 +2.2%", "S. Africa", "Markets", "Reuters"),
    ("L20", "Quake M5.3 off Japan's Bonin Islands; no tsunami", "East Asia", "Disaster", "EMSC/GFZ"),
    ("L21", "Rupee: foreign buyers put $600m+ in on Thursday", "South Asia", "Markets", "Reuters"),
    ("L22", "India frees 164 in Delhi cyber-fraud racket", "South Asia", "Crime", "Reuters"),
    ("L23", "Spain's Vox nears power as election kingmaker", "Europe", "Elections", "Reuters"),
    ("L24", "Strobe Talbott, ex-deputy secretary, dies at 80", "N. America", "Obituary", "AP/NPR"),
    ("L25", "China: ex-Guangxi chief gets death, reprieved", "East Asia", "Law", "Xinhua/Reuters"),
    ("L26", "CPTPP to open talks: UAE, Indonesia, Philippines", "East Asia", "Trade", "Reuters"),
    ("L27", "China drills Taiwan landing on floating bridge", "East Asia", "Conflict", "Reuters"),
    ("L28", "Google AI Pro Black Friday deals open to all", "N. America", "Tech", "Android Central"),
    ("L29", "Duterte: resignation 'out of the question'", "SE Asia", "Politics", "Reuters"),
    ("L30", "Egypt mosques pray for Ring Road fire victims", "N. Africa", "Religion", "CairoScene"),
    ("L31", "Russia lost 55,629 troops in November so far", "Europe", "Conflict", "Ukr. General Staff"),
    ("L32", "Nigeria's envoy presents credentials in Mexico", "Latin America", "Diplomacy", "Thenigeriannews"),
    ("L33", "Indonesia arrests 3 over share manipulation", "SE Asia", "Law", "Reuters"),
    ("L34", "Serbia still has no PM as deadlines loom", "Europe", "Politics", "Reuters"),
    ("L35", "Australia sanctions 2 over antisemitic attacks", "Oceania", "Diplomacy", "Reuters"),
]

KEY_NUMBERS = [
    ("€45bn", "UKRAINE LOAN BLOCKED"),
    ("74,772", "GAZA DEATH TOLL"),
    ("65–65", "NZ COALITION 1 SHORT"),
    ("+12%", "CHINA STAR 50"),
    ("$3,662", "GOLD, +2.7%"),
    ("$61,600", "BITCOIN, $7BN EXPIRY"),
    ("+0.9%", "STOXX 600 FRIDAY"),
    ("155", "DRONES AT UKRAINE"),
]

TIMELINE = [
    ("00:30", "EU: no deal"),
    ("02:33", "Asia steady"),
    ("04:44", "Korea: 6 home"),
    ("06:12", "Talbott dies"),
    ("07:51", "Marseille condemned"),
    ("08:06", "155 drones"),
    ("08:26", "Europe opens up"),
    ("09:33", "India fraud rescue"),
]

REGIONS = [
    ("EUROPE", 16), ("MIDDLE EAST", 4), ("EAST ASIA", 10),
    ("SOUTH ASIA", 4), ("SE ASIA", 2), ("OCEANIA", 2),
    ("N. AMERICA", 9), ("N. AFRICA", 1), ("S. AFRICA", 1),
    ("LATIN AMERICA", 1),
]


def check_counts():
    stories = BIG + SMALL + [dict(id=i, region=r, field=f) for i, _, r, f, _ in LISTED]
    assert len(stories) == 50, len(stories)
    from collections import Counter
    rc, fc = Counter(s["region"] for s in stories), Counter(s["field"] for s in stories)
    assert sum(rc.values()) == 50 and sum(fc.values()) == 50
    assert len(rc) == 10, rc
    assert len(fc) == 18, fc
    assert sum(n for _, n in REGIONS) == 50
    assert {k.upper(): v for k, v in dict(REGIONS).items()} == \
        {k.upper(): v for k, v in dict(rc).items()}, (dict(REGIONS), dict(rc))
    return rc, fc


# ---------------------------------------------------------------- drawing

def draw_page():
    check_counts()
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN
    cw = x1 - x0

    # Masthead
    d.rectangle([0, 0, W, 58], fill=BURGUNDY)
    d.text((MARGIN, 12), "THE WORLD IN ONE PAGE",
           font=font(SANS_B, 30), fill=WHITE)
    d.text((W - MARGIN - d.textlength("50 STORIES · 1 DAY",
           font=font(SANS_B, 15)), 20), "50 STORIES · 1 DAY",
           font=font(SANS_B, 15), fill=(232, 205, 160))

    # Dateline
    d.text((MARGIN, 66), "FRIDAY 27 NOVEMBER 2026",
           font=font(SERIF_B, 38), fill=INK)
    right = "ALL FIRST REPORTED TODAY"
    d.text((W - MARGIN - d.textlength(right, font=font(SANS_B, 13)), 82),
           right, font=font(SANS_B, 13), fill=BURGUNDY)

    # Subline
    sub = ("EVERY STORY FIRST REPORTED FRIDAY 27 NOVEMBER 2026  ·  "
           "AS OF 11:00 UTC — THE DAY CONTINUES AFTER THIS IMAGE")
    fit_check(d, sub, font(SANS, 12), cw, "subline")
    d.text((MARGIN, 110), sub, font=font(SANS, 12), fill=MUTED)

    # Region chips
    y = 130
    cx = MARGIN
    chip_f = font(SANS_B, 11)
    for name, n in REGIONS:
        label = "%s %d" % (name, n)
        wch = d.textlength(label, font=chip_f) + 14
        d.rounded_rectangle([cx, y, cx + wch, y + 20], radius=10,
                            fill=TINT, outline=LINE)
        d.text((cx + 7, y + 4), label, font=chip_f, fill=INK)
        cx += wch + 6
    assert cx <= x1 + 6, "region chips overflow: %d" % cx

    # Key numbers
    y = 156
    bw = (cw - 7 * 6) / 8
    for i, (num, label) in enumerate(KEY_NUMBERS):
        bx = MARGIN + i * (bw + 6)
        d.rectangle([bx, y, bx + bw, y + 50], outline=LINE, fill=WHITE)
        d.text((bx + bw / 2 - d.textlength(num, font=font(SANS_B, 17)) / 2,
                y + 5), num, font=font(SANS_B, 17), fill=BURGUNDY)
        lab_f = font(SANS_B, 8)
        lines = wrap(d, label, lab_f, bw - 8)
        assert len(lines) <= 2, label
        for j, ln in enumerate(lines):
            d.text((bx + bw / 2 - d.textlength(ln, font=lab_f) / 2,
                    y + 27 + j * 10), ln, font=lab_f, fill=INK)

    # Timeline
    y = 212
    d.text((MARGIN, y), "THE DAY IN UTC",
           font=font(SANS_B, 11), fill=BURGUNDY)
    d.line([(MARGIN, y + 31), (x1, y + 31)], fill=INK, width=2)
    def clamp_cx(cx, text, fnt):
        w = d.textlength(text, font=fnt)
        return min(max(cx - w / 2, MARGIN), x1 - w)
    n = len(TIMELINE)
    for i, (t, label) in enumerate(TIMELINE):
        tx = MARGIN + i * (cw - 40) / (n - 1)
        d.ellipse([tx - 3, y + 28, tx + 3, y + 34], fill=BURGUNDY)
        tf = font(SANS_B, 10)
        d.text((clamp_cx(tx, t, tf), y + 14), t, font=tf, fill=INK)
        lf = font(SANS, 9)
        lines = wrap(d, label, lf, 110)
        assert len(lines) <= 2, label
        for j, ln in enumerate(lines):
            d.text((clamp_cx(tx, ln, lf), y + 38 + j * 11), ln, font=lf,
                   fill=MUTED)

    # Big scenes
    y = 276
    bh = 200
    colw = (cw - 2 * 8) / 3
    for i, s in enumerate(BIG):
        bx = MARGIN + i * (colw + 8)
        d.rectangle([bx, y, bx + colw, y + bh], outline=LINE, fill=WHITE)
        d.rectangle([bx, y, bx + colw, y + 24], fill=s["color"])
        tf = font(SANS_B, 11)
        fit_check(d, s["tag"], tf, colw - 12, "big tag")
        d.text((bx + 8, y + 5), s["tag"], font=tf, fill=WHITE)
        pic = PICS[s["pic"]]
        pic(d, bx + colw / 2 - 40, y + 32, 80, s["color"])
        draw_wrapped(d, s["head"], font(SANS_B, 15), bx + 10, y + 118,
                     colw - 20, 2, leading=18)
        draw_wrapped(d, s["detail"], font(SANS, 11), bx + 10, y + 156,
                     colw - 20, 3, leading=14, fill=MUTED)

    # Small scenes: 4 cols x 3 rows
    y = 484
    sh = 72
    scw = (cw - 3 * 8) / 4
    for i, s in enumerate(SMALL):
        r, c = divmod(i, 4)
        bx = MARGIN + c * (scw + 8)
        by = y + r * (sh + 6)
        d.rectangle([bx, by, bx + scw, by + sh], outline=LINE, fill=WHITE)
        d.rectangle([bx, by, bx + 46, by + sh], fill=TINT)
        PICS[s["pic"]](d, bx + 3, by + sh / 2 - 20, 40, INK)
        tx = bx + 52
        tw = scw - 58
        draw_wrapped(d, s["head"], font(SANS_B, 11), tx, by + 6, tw, 2,
                     leading=13)
        draw_wrapped(d, s["detail"], font(SANS, 9.5), tx, by + 34, tw, 2,
                     leading=12, fill=MUTED)

    # Listed rows
    y = 718
    d.text((MARGIN, y), "ALSO LISTED — 35 MORE STORIES, ALL FIRST REPORTED TODAY",
           font=font(SANS_B, 12), fill=BURGUNDY)
    d.line([(MARGIN, y + 18), (x1, y + 18)], fill=INK, width=1)
    cols = [LISTED[i::3] for i in range(3)]
    colw2 = (cw - 2 * 16) / 3
    lf = font(SANS, 10)
    for ci, col in enumerate(cols):
        cx = MARGIN + ci * (colw2 + 16)
        for ri, (lid, head, _r, _f, _s) in enumerate(col):
            ry = y + 24 + ri * 17
            line = "%s · %s" % (lid, head)
            fit_check(d, line, lf, colw2, "listed " + lid)
            d.text((cx, ry), line, font=lf, fill=INK)

    # Bottom boxes
    y = 950
    bw2 = (cw - 8) / 2
    d.rectangle([MARGIN, y, MARGIN + bw2, y + 50], outline=LINE, fill=TINT)
    d.text((MARGIN + 8, y + 5), "TOMORROW",
           font=font(SANS_B, 11), fill=BURGUNDY)
    draw_wrapped(d, "Spain votes Sunday — Vox tipped kingmaker. OPEC+ "
                    "meets Sunday on output. NZ kingmaker talks begin.",
                 font(SANS, 10), MARGIN + 8, y + 21, bw2 - 16, 2,
                 leading=13, fill=INK)
    d.rectangle([MARGIN + bw2 + 8, y, x1, y + 50], outline=LINE, fill=TINT)
    d.text((MARGIN + bw2 + 16, y + 5), "DATE CHECK — NOT TODAY'S NEWS",
           font=font(SANS_B, 11), fill=BURGUNDY)
    draw_wrapped(d, "Bangkok oil blast (Thu) · UK migration 77,000 (Thu) · "
                    "N. Korea aid pause (Thu) · Trump 'pull back' (Thu) · "
                    "Wright biathlon (Thu) · Quantum drone record (Thu).",
                 font(SANS, 10), MARGIN + bw2 + 16, y + 21, bw2 - 16, 2,
                 leading=13, fill=INK)

    # Footer
    foot = ("Sources: Reuters · AP · Al Jazeera · BBC · Consilium · Xinhua · "
            "WSJ · NBS · NZ Herald · WAFA/QNA · Ukrainian Air Force — "
            "drawn by an AI agent for make.fun · news-image-20261127")
    fit_check(d, foot, font(SANS, 9), cw, "footer")
    d.text((MARGIN, 1006), foot, font=font(SANS, 9), fill=MUTED)
    return img


def main():
    img = draw_page()
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img.save(out, "JPEG", quality=88, optimize=True)
    data = open(out, "rb").read()
    assert data[:2] == b"\xff\xd8", "not a JPEG"
    assert data[-2:] == b"\xff\xd9", "JPEG missing end marker"
    assert len(data) <= 1048576, len(data)
    im = Image.open(out)
    assert im.size == (1024, 1024), im.size
    print("%s %d bytes sha256=%s" % (out, len(data),
                                     hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
