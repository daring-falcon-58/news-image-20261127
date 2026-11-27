#!/usr/bin/env python3
"""news-image-20261127 round 2 — fresh build.

Draws a 1024x1024 newspaper front page summing up Friday 27 November 2026.
Deterministic: fixed data, fixed geometry, no randomness, no time calls,
no network. Output is a JPEG (written as entry.png, as the brief allows).
Run: python3 build_image.py [out_path]  (default: entry.png)
"""
import sys
from PIL import Image, ImageDraw, ImageFont

BUILD_STAMP = "08:30 UTC"  # build time, fixed string (not read from clock)
W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
NAVY = (20, 38, 74)
NAVY_LT = (36, 59, 102)
GOLD = (201, 162, 39)
RED = (185, 28, 28)
MAROON = (127, 29, 29)
GREEN = (20, 83, 45)
TEAL = (15, 118, 110)
BLUE = (29, 78, 216)
GREY = (100, 100, 100)
LIGHT = (255, 255, 255)
PANEL = (255, 255, 255)
PANEL_BG = (238, 234, 222)

FONT_DIRS = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
FONT_DIRS_B = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def font(size, bold=False):
    for p in (FONT_DIRS_B if bold else FONT_DIRS):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    """Greedy wrap; returns list of lines. Raises if a single word is too wide."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            if draw.textlength(w, font=f) > max_w:
                raise ValueError("word too wide: %r" % w)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, s, f, max_w, max_lines, fill=INK, leading=None):
    lines = wrap(draw, s, f, max_w)
    if len(lines) > max_lines:
        raise ValueError("overflow: %r needs %d lines, max %d" % (s, len(lines), max_lines))
    lh = leading or int(f.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def one_line(draw, x, y, s, f, max_w, fill=INK):
    if draw.textlength(s, font=f) > max_w:
        raise ValueError("one-liner too wide (%d > %d): %r"
                         % (draw.textlength(s, font=f), max_w, s))
    draw.text((x, y), s, font=f, fill=fill)


# ---------------------------------------------------------------- data
# Pictured: (tag, headline, body lines, region, field, source)
PICTURED_BIG = [
    ("EU SUMMIT ENDS IN NO DEAL",
     ["\u20ac1.58tn budget and \u20ac45bn Ukraine loan blocked after ~14 hours in Brussels.",
      "24 states back the loan; Hungary, Slovakia and Czechia oppose.",
      "Leaders try again on Dec 17\u201318."],
     "Europe", "Politics", "Consilium / Reuters"),
    ("GAZA: 19 KILLED IN 48 HOURS",
     ["Toll since the ceasefire: 1,705. Total since Oct 2023: 74,772.",
      "10 more killed on Friday, incl. a Hamas deputy education minister.",
      "37 killed in the past week; a 9-month-old dies of cold."],
     "Middle East", "Conflict", "Al Jazeera / AP"),
    ("NEW ZEALAND: 65\u201365",
     ["Final count: the coalition holds 65 of 130 seats \u2014 one short.",
      "National 40, ACT 13, NZ First 12; Labour 36, Greens 17.",
      "Opportunity, 7 seats, holds the balance of power."],
     "Oceania", "Elections", "NZ Herald / Reuters"),
]

# Pictured small: (headline, fact, region, field, source, icon)
PICTURED_SMALL = [
    ("ECB: DE COS TO LEAD", "Recommended as next president; succeeds Lagarde in Feb 2027",
     "Europe", "Politics", "Consilium", "bank"),
    ("ASIA STEADY", "Kospi +2%, Nikkei +0.7%; MSCI Asia-Pac ex-Japan +0.5%",
     "East Asia", "Markets", "Reuters", "chart"),
    ("LATVIA: DRONE INCURSION", "Unidentified drone briefly violates airspace early Friday",
     "Europe", "Conflict", "Reuters", "drone"),
    ("UKRAINE: 3 KILLED", "Russian drone strikes overnight; at least 10 injured",
     "Europe", "Conflict", "Reuters", "burst"),
    ("ZELENSKY TO BBC", "US \u201ctoo focused on Middle East\u201d; Patriot delays cost lives",
     "Europe", "Conflict", "BBC", "mic"),
    ("BLACK FRIDAY", "Necessities join gifts as AI and higher costs steer spending",
     "N. America", "Retail", "AP", "bag"),
    ("CHINA PROFITS +20.1%", "Industrial profits jump in Oct, fastest in 5 months",
     "East Asia", "Economy", "NBS / Reuters", "factory"),
    ("BRENT $96.14", "Down 0.4% on the day, up 3.9% on the week",
     "Middle East", "Energy", "Reuters", "drop"),
    ("TOKYO CPI 2.9%", "Core inflation at a 16-month high; BOJ hike case grows",
     "East Asia", "Economy", "Reuters", "yen"),
    ("INDIA\u2013US DEAL NEARS", "Trade deal nearing completion, minister Goyal says",
     "South Asia", "Diplomacy", "Reuters", "flags"),
    ("KOREA SENDS 6 HOME", "Six North Koreans repatriated by sea; a 7th chose to stay",
     "East Asia", "Diplomacy", "Reuters", "boat"),
    ("CHINA STOCKS SURGE", "Shanghai +3.3%, STAR 50 +12% as Beijing vows support",
     "East Asia", "Markets", "Reuters", "rocket"),
]

# Listed: (one-liner, region, field, source)
LISTED = [
    ("Erdogan ratifies Mecca defence pact for Turkey", "Middle East", "Diplomacy", "Reuters"),
    ("Iran warns on Gulf presence as Seoul expands naval role", "Middle East", "Diplomacy", "Reuters"),
    ("Dollar heads for 3rd monthly gain: +1.8%, DXY 103.8", "N. America", "Markets", "Reuters"),
    ("US futures rise; Wall St reopens, closes 1pm ET", "N. America", "Markets", "Reuters"),
    ("Gold $3,625.50 (+1.66%), silver $43.27 (+4.92%)", "N. America", "Markets", "IC Markets"),
    ("Sensex drops 400+ pts, Nifty below 25,800; metals gain", "South Asia", "Markets", "Hindu BusinessLine"),
    ("Bitcoin reclaims $60,000: +3.03% to $60,397.69", "N. America", "Crypto", "CoinMarketCap"),
    ("Zelensky: major Russian attack on power grid imminent", "Europe", "Conflict", "AP"),
    ("Trump 'a little concerned' by Wed market dip", "N. America", "Politics", "Reuters"),
    ("Bears 39\u201335 Lions: Williams TD with 3 seconds left", "N. America", "Sport", "AP"),
    ("Louisville 93\u201390 St John's: Wooley buzzer 3-pointer", "N. America", "Sport", "Field Level Media"),
    ("Macron: \u20ac204bn budget cuts a 'strategic mistake'", "Europe", "Politics", "Reuters / ANI"),
    ("Merz: no new debt; praises Trump's peace efforts", "Europe", "Politics", "Reuters / ANI"),
    ("China cabinet vows new steps to steady markets", "East Asia", "Economy", "Xinhua / Reuters"),
    ("France CPI cools to 3.2%; Spain 4.1%; France GDP \u22120.2%", "Europe", "Economy", "Reuters / WSJ"),
    ("Europe stocks rose Thu: DAX +2.08%, FTSE +1.75%", "Europe", "Markets", "Reuters"),
    ("Gaza: 37 killed in a week; baby dies of cold", "Middle East", "Health", "Al Jazeera"),
    ("Russia hits 2 grain ships near Odesa; 100,000+ t", "Europe", "Conflict", "Reuters"),
    ("Rand +~1% to 17.37; platinum +5%; Top-40 +2.2%", "S. Africa", "Markets", "Reuters"),
    ("Quake M5.3 off Bonin Islands, Japan; no tsunami", "East Asia", "Disaster", "EMSC / GFZ / Xinhua"),
    ("Rupee: foreign buyers put $600M+ in Thu; Nov $16B", "South Asia", "Economy", "Reuters"),
    ("2-yr Treasury yield +3bp to 4.6705% on reopen", "N. America", "Markets", "Reuters"),
    ("Euro flat at $1.0964 after de Cos news", "Europe", "Markets", "Reuters"),
    ("Kiwi +0.2% to $0.5482 after the NZ result", "Oceania", "Markets", "Reuters"),
    ("WTI $85.72 (+0.94%)", "N. America", "Energy", "IC Markets"),
    ("Crypto Fear & Greed 12 \u2014 Extreme Fear; market $2.1T", "N. America", "Crypto", "KuCoin"),
    ("China drills Taiwan landing on floating bridge", "East Asia", "Conflict", "Reuters"),
    ("Google AI Pro Black Friday deals open to all", "N. America", "Tech", "Android Central"),
    ("Duterte: resignation 'out of the question'", "SE Asia", "Politics", "Reuters"),
    ("Egypt mosques pray for Ring Road fire victims", "N. Africa", "Religion", "CairoScene"),
    ("MSCI Asia-Pac ex-Japan +0.5% (week +1.9%)", "East Asia", "Markets", "Reuters"),
    ("Shenzhen +1.53%, Hang Seng +0.89% in early trade", "East Asia", "Markets", "Reuters"),
    ("Target opens 6am; first 100 shoppers get gift cards", "N. America", "Retail", "Target"),
    ("Best Buy opens 6am\u201310pm; $100 gift card for $60", "N. America", "Retail", "Best Buy"),
    ("Amazon 'double drops' on Black Friday + Cyber Monday", "N. America", "Retail", "Amazon"),
]

TIMELINE = [
    ("00:30", "EU summit: no deal"),
    ("01:52", "Drones kill 3"),
    ("02:33", "Kospi +2%"),
    ("04:33", "Quake M5.3"),
    ("04:44", "6 Koreans home"),
    ("05:34", "Gaza: 37 dead"),
    ("07:00", "China +3.3%"),
    ("07:45", "France CPI 3.2%"),
]

KEY_NUMBERS = [
    ("\u20ac1.58tn", "EU BUDGET: NO DEAL"),
    ("\u20ac45bn", "UKRAINE LOAN"),
    ("74,772", "GAZA DEATH TOLL"),
    ("65\u201365", "NZ PARLIAMENT"),
    ("+20.1%", "CHINA PROFITS"),
    ("$96.14", "BRENT CRUDE"),
    ("$60,398", "BITCOIN"),
    ("+12%", "CHINA STAR 50"),
]

REGIONS = [
    ("Europe", 12), ("Middle East", 5), ("East Asia", 10), ("South Asia", 3),
    ("SE Asia", 1), ("Oceania", 2), ("N. America", 15), ("N. Africa", 1),
    ("S. Africa", 1),
]


def check_counts():
    n = len(PICTURED_BIG) + len(PICTURED_SMALL) + len(LISTED)
    assert n == 50, "story count %d != 50" % n
    assert sum(c for _, c in REGIONS) == 50, "region counts != 50"
    from collections import Counter
    rc = Counter()
    fc = Counter()
    for _, _, r, f, _ in PICTURED_BIG:
        rc[r] += 1
        fc[f] += 1
    for _, _, r, f, _, _ in PICTURED_SMALL:
        rc[r] += 1
        fc[f] += 1
    for _, r, f, _ in LISTED:
        rc[r] += 1
        fc[f] += 1
    expect_r = dict(REGIONS)
    assert dict(rc) == expect_r, "region mismatch: %s vs %s" % (dict(rc), expect_r)
    assert sum(fc.values()) == 50
    return dict(rc), dict(fc)


# ---------------------------------------------------------------- icons
def draw_icon(d, kind, x, y, s, color):
    """Simple vector pictogram inside an s x s box at (x, y)."""
    if kind == "bank":
        d.polygon([(x + 2, y + 16), (x + s / 2, y + 2), (x + s - 2, y + 16)], fill=color)
        for i in range(3):
            cx = x + 8 + i * 13
            d.rectangle([cx, y + 18, cx + 6, y + s - 8], fill=color)
        d.rectangle([x + 2, y + s - 6, x + s - 2, y + s - 2], fill=color)
    elif kind == "chart":
        bars = [10, 18, 28]
        for i, bh in enumerate(bars):
            bx = x + 5 + i * 13
            d.rectangle([bx, y + s - 6 - bh, bx + 9, y + s - 6], fill=color)
        d.line([(x + 3, y + 12), (x + s - 4, y + 4)], fill=RED, width=3)
    elif kind == "drone":
        d.ellipse([x + s / 2 - 4, y + s / 2 - 4, x + s / 2 + 4, y + s / 2 + 4], fill=color)
        for cx, cy in [(x + 6, y + 6), (x + s - 6, y + 6), (x + 6, y + s - 6), (x + s - 6, y + s - 6)]:
            d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], outline=color, width=2)
            d.line([(x + s / 2, y + s / 2), (cx, cy)], fill=color, width=2)
    elif kind == "burst":
        cx, cy = x + s / 2, y + s / 2
        for k in range(8):
            import math
            a = k * math.pi / 4
            d.line([(cx + 8 * math.cos(a), cy + 8 * math.sin(a)),
                    (cx + 19 * math.cos(a), cy + 19 * math.sin(a))], fill=color, width=3)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)
    elif kind == "mic":
        d.ellipse([x + 9, y + 4, x + s - 9, y + 24], fill=color)
        d.line([(x + s / 2, y + 24), (x + s / 2, y + s - 8)], fill=color, width=3)
        d.line([(x + 10, y + s - 6), (x + s - 10, y + s - 6)], fill=color, width=3)
    elif kind == "bag":
        d.polygon([(x + 7, y + 14), (x + s - 7, y + 14), (x + s - 4, y + s - 4),
                   (x + 4, y + s - 4)], fill=color)
        d.arc([x + 12, y + 4, x + s - 12, y + 20], 180, 360, fill=color, width=3)
    elif kind == "factory":
        d.rectangle([x + 4, y + 18, x + s - 4, y + s - 4], fill=color)
        d.polygon([(x + 4, y + 18), (x + 12, y + 10), (x + 20, y + 18),
                   (x + 28, y + 10), (x + s - 4, y + 18)], fill=PAPER)
        d.rectangle([x + s - 12, y + 4, x + s - 7, y + 16], fill=color)
    elif kind == "drop":
        d.polygon([(x + s / 2, y + 3), (x + s - 6, y + 22), (x + 6, y + 22)], fill=color)
        d.ellipse([x + 8, y + 16, x + s - 8, y + s - 3], fill=color)
    elif kind == "yen":
        d.ellipse([x + 2, y + 2, x + s - 2, y + s - 2], outline=color, width=3)
        d.text((x + s / 2 - 8, y + 6), "\u00a5", font=font(22, True), fill=color)
    elif kind == "flags":
        d.rectangle([x + 4, y + 8, x + s / 2 + 2, y + 24], fill=(255, 153, 51))
        d.rectangle([x + 4, y + 14, x + s / 2 + 2, y + 19], fill=(255, 255, 255))
        d.rectangle([x + s / 2 - 2, y + 14, x + s - 4, y + 30], fill=(178, 34, 52))
        d.rectangle([x + s / 2 - 2, y + 14, x + s - 4, y + 19], fill=(255, 255, 255))
    elif kind == "boat":
        d.polygon([(x + 4, y + 20), (x + s - 4, y + 20), (x + s - 10, y + s - 6),
                   (x + 10, y + s - 6)], fill=color)
        d.line([(x + s / 2, y + 6), (x + s / 2, y + 20)], fill=color, width=3)
        d.polygon([(x + s / 2, y + 6), (x + s / 2, y + 18), (x + s - 8, y + 18)], fill=RED)
    elif kind == "rocket":
        d.polygon([(x + s / 2, y + 2), (x + s - 8, y + 22), (x + s / 2, y + 17),
                   (x + 8, y + 22)], fill=color)
        d.polygon([(x + s / 2, y + 22), (x + s / 2 + 6, y + s - 2),
                   (x + s / 2 - 6, y + s - 2)], fill=RED)


# ---------------------------------------------------------------- build
def build(out_path):
    rc, fc = check_counts()
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    X0, X1 = 14, 1010
    CW = X1 - X0  # 996

    # --- masthead ---
    d.rectangle([0, 0, W, 58], fill=NAVY)
    d.text((X0, 12), "THE WORLD IN ONE DAY", font=font(30, True), fill=LIGHT)
    d.text((X1 - d.textlength("FRIDAY \u2022 27 NOVEMBER 2026", font=font(22, True)), 16),
           "FRIDAY \u2022 27 NOVEMBER 2026", font=font(22, True), fill=GOLD)
    d.rectangle([0, 58, W, 62], fill=GOLD)

    # --- giant date line ---
    d.text((X0, 68), "FRIDAY 27 NOVEMBER 2026", font=font(38, True), fill=NAVY)
    right = "50 STORIES \u2022 9 REGIONS \u2022 14 FIELDS"
    d.text((X1 - d.textlength(right, font=font(20, True)), 78), right,
           font=font(20, True), fill=INK)
    # --- sub-line ---
    sub = ("ALL FIRST REPORTED TODAY \u2022 AS OF %s \u2014 THE DAY CONTINUES AFTER THIS IMAGE"
           % BUILD_STAMP)
    d.text((X0, 112), sub, font=font(15, True), fill=RED)

    # --- region chips ---
    y = 132
    chip_f = font(13, True)
    total_w = sum(d.textlength("%s %d" % (n, c), font=chip_f) + 18 for n, c in REGIONS) \
        + 10 * (len(REGIONS) - 1)
    assert total_w <= CW, "chips too wide: %d" % total_w
    cx = X0
    for name, cnt in REGIONS:
        label = "%s %d" % (name.upper(), cnt)
        w = d.textlength(label, font=chip_f) + 18
        d.rounded_rectangle([cx, y, cx + w, y + 24], radius=12, fill=NAVY)
        d.text((cx + 9, y + 4), label, font=chip_f, fill=LIGHT)
        cx += w + 10

    # --- key numbers strip ---
    y = 164
    bw = (CW - 7 * 6) / 8
    for i, (val, lab) in enumerate(KEY_NUMBERS):
        bx = X0 + i * (bw + 6)
        d.rectangle([bx, y, bx + bw, y + 46], fill=PANEL, outline=NAVY, width=1)
        vf = font(20, True)
        while d.textlength(val, font=vf) > bw - 8 and vf.size > 13:
            vf = font(vf.size - 1, True)
        d.text((bx + (bw - d.textlength(val, font=vf)) / 2, y + 3), val, font=vf, fill=RED)
        lf = font(10, True)
        d.text((bx + (bw - d.textlength(lab, font=lf)) / 2, y + 28), lab, font=lf, fill=NAVY)

    # --- timeline ---
    y = 226
    d.line([(X0, y), (X1, y)], fill=NAVY, width=2)
    step = CW / len(TIMELINE)
    for i, (t, txt) in enumerate(TIMELINE):
        ex = X0 + step * i + step / 2
        d.ellipse([ex - 5, y - 5, ex + 5, y + 5], fill=RED, outline=LIGHT, width=1)
        tf = font(11, True)
        d.text((ex - d.textlength(t, font=tf) / 2, y + 8), t, font=tf, fill=RED)
        one_line(d, ex - 56, y + 22, txt, font(11), 112, fill=INK)

    # --- big scenes ---
    y = 268
    bh = 178
    bw3 = (CW - 20) / 3
    big_colors = [NAVY, MAROON, GREEN]
    for i, (head, body, region, field, src) in enumerate(PICTURED_BIG):
        bx = X0 + i * (bw3 + 10)
        d.rectangle([bx, y, bx + bw3, y + bh], fill=PANEL, outline=big_colors[i], width=2)
        d.rectangle([bx, y, bx + bw3, y + 34], fill=big_colors[i])
        hf = font(17, True)
        while d.textlength(head, font=hf) > bw3 - 14 and hf.size > 12:
            hf = font(hf.size - 1, True)
        d.text((bx + 7, y + 7), head, font=hf, fill=LIGHT)
        by = y + 42
        for line in body:
            by = draw_wrapped(d, bx + 8, by, line, font(13), bw3 - 16, 2, fill=INK)
            by += 2
        # pictogram strip at bottom of panel
        py = y + bh - 34
        if i == 0:
            # circle of stars + red X
            cx0, cy0 = bx + bw3 - 52, py + 16
            import math
            for k in range(12):
                a = k * math.pi / 6
                d.ellipse([cx0 + 20 * math.cos(a) - 2, cy0 + 13 * math.sin(a) - 2,
                           cx0 + 20 * math.cos(a) + 2, cy0 + 13 * math.sin(a) + 2],
                          fill=GOLD)
            d.line([(cx0 - 10, cy0 - 8), (cx0 + 10, cy0 + 8)], fill=RED, width=4)
            d.line([(cx0 - 10, cy0 + 8), (cx0 + 10, cy0 - 8)], fill=RED, width=4)
            d.text((bx + 8, py + 4), "\u20ac1.58tn  \u00d7  \u20ac45bn", font=font(15, True), fill=RED)
        elif i == 1:
            # skyline silhouette below the toll line (no overlap)
            d.text((bx + 8, py - 2), "19 IN 48 H  \u2022  74,772 TOTAL", font=font(13, True), fill=MAROON)
            heights = [6, 10, 5, 12, 8, 11, 6]
            sx = bx + 8
            for hh in heights:
                d.rectangle([sx, py + 30 - hh, sx + 16, py + 30], fill=MAROON)
                sx += 19
        else:
            # 65 vs 65 seat bars
            d.text((bx + 8, py - 2), "COALITION 65", font=font(12, True), fill=RED)
            d.rectangle([bx + 8, py + 14, bx + 8 + 150, py + 24], fill=RED)
            d.text((bx + 168, py - 2), "OPP. 65", font=font(12, True), fill=BLUE)
            d.rectangle([bx + 168, py + 14, bx + 168 + 150, py + 24], fill=BLUE)

    # --- small scenes: 4 cols x 3 rows ---
    y = 458
    sw = (CW - 3 * 8) / 4
    sh = 66
    small_colors = [NAVY, TEAL, RED, MAROON, BLUE, (146, 64, 14), (21, 94, 117),
                    (120, 53, 15), (88, 28, 135), (6, 95, 70), (30, 64, 175), GREEN]
    for i, (head, fact, region, field, src, icon) in enumerate(PICTURED_SMALL):
        r, c = divmod(i, 4)
        sx = X0 + c * (sw + 8)
        sy = y + r * (sh + 6)
        d.rectangle([sx, sy, sx + sw, sy + sh], fill=PANEL, outline=(200, 196, 182), width=1)
        d.rectangle([sx, sy, sx + 46, sy + sh], fill=PANEL_BG)
        draw_icon(d, icon, sx + 4, sy + 12, 38, small_colors[i])
        hf = font(13, True)
        while d.textlength(head, font=hf) > sw - 56 and hf.size > 10:
            hf = font(hf.size - 1, True)
        d.text((sx + 52, sy + 5), head, font=hf, fill=NAVY)
        draw_wrapped(d, sx + 52, sy + 24, fact, font(12), sw - 58, 2, fill=INK)

    # --- ALSO LISTED ---
    y = 676
    d.rectangle([X0, y, X1, y + 22], fill=NAVY)
    d.text((X0 + 8, y + 3), "ALSO LISTED \u2014 35 MORE STORIES, ALL FIRST REPORTED TODAY",
           font=font(14, True), fill=LIGHT)
    col_w = (CW - 2 * 14) / 3
    row_h = 21
    list_f = font(11)
    for idx, (txt, region, field, src) in enumerate(LISTED):
        col, row = divmod(idx, 12)
        lx = X0 + col * (col_w + 14)
        ly = y + 28 + row * row_h
        num = "L%d" % (idx + 1)
        d.text((lx, ly), num, font=font(11, True), fill=RED)
        one_line(d, lx + 26, ly, txt, list_f, col_w - 26, fill=INK)

    # --- bottom boxes ---
    y = 944
    bw2 = (CW - 12) / 2
    d.rectangle([X0, y, X0 + bw2, y + 56], fill=PANEL, outline=NAVY, width=1)
    d.text((X0 + 8, y + 4), "TOMORROW", font=font(12, True), fill=NAVY)
    draw_wrapped(d, X0 + 8, y + 20,
                 "EU talks resume Dec 17\u201318 \u2022 OPEC+ meets Sunday \u2022 NZ coalition talks \u2022 "
                 "Victoria votes Sat \u2022 Duterte ICC trial Nov 30",
                 font(12), bw2 - 16, 2, fill=INK)
    bx = X0 + bw2 + 12
    d.rectangle([bx, y, bx + bw2, y + 56], fill=PANEL, outline=NAVY, width=1)
    d.text((bx + 8, y + 4), "DATE CHECK \u2014 LEFT OUT (FIRST REPORTED 26 NOV OR EARLIER)",
           font=font(12, True), fill=NAVY)
    draw_wrapped(d, bx + 8, y + 20,
                 "EU summit opening \u2022 Jazan strike \u2022 Brazil\u2013Milei rift \u2022 "
                 "tariffs blitz \u2022 Bogor toll \u2022 F1 Abu Dhabi",
                 font(12), bw2 - 16, 2, fill=INK)

    # --- footer ---
    d.text((X0, 1008),
           "All 50 stories first reported Friday 27 November 2026 (any time zone). Sources: Reuters, AP, "
           "Al Jazeera, Consilium, BBC, NBS, NZ Herald, Xinhua, WSJ.",
           font=font(11), fill=GREY)

    img.save(out_path, "JPEG", quality=88, optimize=False)
    return rc, fc


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    regions, fields = build(out)
    print("wrote", out)
    print("regions:", regions)
    print("fields:", fields)
