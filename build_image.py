#!/usr/bin/env python3
"""Draw the round-5 news image for make.fun news-image-20261127.

Fresh build, written in this session. Fixed data, fixed geometry, no
randomness, no network, no clock reads: two runs write byte-identical JPEG.

Layout (1024x1024, cream broadsheet): masthead -> giant dateline ->
region chips -> key-numbers strip -> UTC timeline -> 3 big scenes ->
12 small scenes -> ALSO LISTED (35 rows, 3 columns) -> DATE CHECK +
AS OF boxes -> footer with sources.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# --- palette: warm broadsheet paper, ink, red accent ----------------------
PAPER = (247, 242, 231)
INK = (26, 26, 24)
RED = (178, 34, 34)
NAVY = (31, 58, 95)
GREY = (110, 105, 94)
LIGHT = (233, 226, 210)
GOLD = (176, 132, 30)
GREEN = (31, 110, 62)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy wrap; returns list of lines, each <= max_w px."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, fnt, max_w, max_lines):
    """Wrap text; raise if it does not fit in max_lines lines."""
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) > max_lines:
        raise ValueError("text does not fit (%d lines): %r" % (len(lines), text))
    return lines


# --- the 50 stories: all first reported Friday 27 November 2026 ----------
# PICTURED: (glyph, title, fact, region, field)
PICTURED_BIG = [
    ("stars", "EU SUMMIT ENDS: NO DEAL",
     "No deal on \u20ac1.58tn budget or \u20ac45bn loan; 24 of 27 back it. "
     "Talks resume Dec 17\u201318.",
     "Europe", "Politics"),
    ("skyline", "GAZA: 19 KILLED IN 48 HOURS",
     "19 killed in 48 hours despite the ceasefire; toll since ceasefire "
     "1,705; total 74,772.",
     "Middle East", "Conflict"),
    ("chart", "WALL ST RALLIES",
     "Short session: Nasdaq +1.0%, S&P +0.8%, Dow +0.8%; tech rebounds.",
     "N. America", "Markets"),
]

PICTURED_SMALL = [
    ("euro", "ECB: DE COS TO LEAD",
     "Spain's de Cos recommended as next ECB president.",
     "Europe", "Politics"),
    ("bars", "ASIA SURGES: KOSPI +4.3%",
     "Nikkei +2.1%, Shanghai +3.7%, Hang Seng +2.1%.",
     "East Asia", "Markets"),
    ("drone", "DRONE OVER LATVIA",
     "Unidentified drone briefly enters Latvian airspace.",
     "Europe", "Conflict"),
    ("burst", "RUSSIA FIRES 155 DRONES",
     "110 downed overnight; 1 killed, 9 hurt; Vinnytsia energy hit.",
     "Europe", "Conflict"),
    ("mic", "ZELENSKY TO THE BBC",
     "US 'too focused on Middle East'; Patriot delays cost lives.",
     "Europe", "Conflict"),
    ("bag", "BLACK FRIDAY: $12.9BN ONLINE",
     "Adobe expects $12.9bn online in a day; NRF: 126m shoppers.",
     "N. America", "Retail"),
    ("beehive", "NZ: COALITION 65\u201365",
     "Final count: coalition one short; Opportunity kingmaker.",
     "Oceania", "Elections"),
    ("factory", "CHINA PROFITS +20.1%",
     "Industrial profits up 20.1% y/y in Oct, fastest in 5 months.",
     "East Asia", "Economy"),
    ("robot", "TESLA FILES TO BUY EMAG",
     "Files with Germany's cartel office to buy EMAG.",
     "Europe", "Tech"),
    ("yen", "TOKYO CPI 2.9%: 16-MO HIGH",
     "Core CPI at a 16-month high; BOJ hike case grows.",
     "East Asia", "Economy"),
    ("flags", "INDIA\u2013US DEAL NEAR",
     "Trade deal nearing completion, says minister Piyush Goyal.",
     "South Asia", "Diplomacy"),
    ("boat", "KOREA SENDS 6 HOME",
     "South Korea repatriates 6 North Koreans by sea; a 7th stays.",
     "East Asia", "Diplomacy"),
]

# LISTED: (headline, region, field)
LISTED = [
    ("Erdogan completes Turkey's ratification of the Mecca defence pact",
     "Middle East", "Diplomacy"),
    ("Eurozone sentiment ESI falls 0.7 to 95.8 in Nov, lowest since June",
     "Europe", "Economy"),
    ("Brent ~$97.27, near $98, on Hormuz supply fears; WTI $85.80",
     "Middle East", "Energy"),
    ("Gold ~$3,660 (+3.6%), silver $43.68 (+9%); copper surges most since Jan",
     "N. America", "Markets"),
    ("Bitcoin ~$61,600 as ~$7bn of options expire today",
     "N. America", "Crypto"),
    ("Amazon workers strike in 20+ countries on Black Friday",
     "Global", "Labour"),
    ("BWF awards 2028 Thomas & Uber Cup Finals to New Delhi",
     "South Asia", "Sport"),
    ("Bears 39\u201335 Lions: Williams TD with 3 seconds left",
     "N. America", "Sport"),
    ("Macron: \u20ac204bn budget cuts a 'strategic mistake'",
     "Europe", "Politics"),
    ("Hunger to worsen in 16 hotspots; famine threatens parts of Africa \u2014 FAO/WFP",
     "Global", "Humanitarian"),
    ("France CPI 3.2%; Spain 4.1%; France GDP \u22120.2%",
     "Europe", "Economy"),
    ("Europe at midday: Stoxx ~643.5 (+1.0%); tech +2.6%, miners +4%",
     "Europe", "Markets"),
    ("Nearly half of shelters for displaced women closed on funding cuts \u2014 UNHCR",
     "Global", "Humanitarian"),
    ("Russia hits 2 grain ships near Odesa; 100,000+ t",
     "Europe", "Conflict"),
    ("Quake M5.3 off Japan's Bonin Islands; no tsunami",
     "East Asia", "Disaster"),
    ("Sensex closes \u2212989 (\u22121.17%) at 83,339; rupee 92.98 per dollar",
     "South Asia", "Markets"),
    ("Spain's Vox nears power as election kingmaker (~17\u201318% in polls)",
     "Europe", "Politics"),
    ("Strobe Talbott, ex-deputy secretary of state, dies at 80",
     "N. America", "Obituary"),
    ("CPTPP to open talks with UAE, Indonesia, Philippines",
     "SE Asia", "Trade"),
    ("China stages Taiwan landing drill on a floating bridge",
     "East Asia", "Conflict"),
    ("NZ 246/5 on day 1 of 2nd Test vs India (Latham 59, Blundell 53*)",
     "Oceania", "Sport"),
    ("Gukesh draws game 3 vs Sindarov (60 moves); match 1.5\u20131.5",
     "Europe", "Sport"),
    ("Egypt mosques pray Friday for Ring Road fire victims",
     "N. Africa", "Religion"),
    ("Nigeria's envoy presents credentials in Mexico",
     "West Africa", "Diplomacy"),
    ("Indonesia arrests 3 over share manipulation",
     "SE Asia", "Crime"),
    ("~100 Labour MPs sign letter opposing the Rosebank oilfield",
     "Europe", "Law"),
    ("Australia sanctions 2 over antisemitic attacks",
     "Oceania", "Law"),
    ("Abu Dhabi talks end with no breakthrough; Medinsky holds hard line",
     "Middle East", "Diplomacy"),
    ("Trump backs Iraq PM's drive for state control over militias",
     "Middle East", "Politics"),
    ("Puerto Rico unions strike on Black Friday over pay and pensions",
     "Latin America", "Labour"),
    ("Venezuela backs up to $12.5bn credit to clear arrears",
     "Latin America", "Economy"),
    ("Guatemala president to veto the 2027 budget",
     "Latin America", "Politics"),
    ("Tshwane re-elects ActionSA mayor Moya, 115 votes to 87",
     "S. Africa", "Politics"),
    ("Kenya jails ex-governor Obado for 25 years",
     "East Africa", "Law"),
    ("EU envoy in Delhi calls US tariff case 'not very convincing'",
     "South Asia", "Trade"),
]

# UTC timeline (first-report times, all Friday 27 Nov 2026 UTC)
TIMELINE = [
    ("00:30", "Costa: EU summit ends, NO DEAL"),
    ("02:33", "Asia opens: Kospi +2%, Nikkei +0.7%"),
    ("04:44", "S. Korea repatriates 6 North Koreans"),
    ("06:12", "Talbott obituary published (01:12 EST)"),
    ("08:00", "Ukraine: 155 drones, 110 downed"),
    ("09:25", "CPTPP to open talks (Hanoi)"),
    ("13:21", "Tesla files to buy EMAG (Reuters)"),
    ("15:29", "Wall St midday: Dow 50,550, S&P 7,243"),
]

KEY_NUMBERS = [
    ("\u20ac1.58tn", "EU BUDGET: NO DEAL"),
    ("74,772", "GAZA DEATH TOLL"),
    ("+4.3%", "KOSPI CLOSE"),
    ("$3,660", "GOLD (+3.6%)"),
    ("65\u201365", "NZ COALITION"),
    ("$97.27", "BRENT CRUDE"),
]

AS_OF = "16:30 UTC"

# Thursday (and earlier) items checked and EXCLUDED from this image:
EXCLUDED = (
    "Altria/Imperial bid (Thu) \u00b7 Binance recovery (Thu) \u00b7 "
    "US chip curbs / Z.AI (Thu) \u00b7 Section 301 tariffs (Wed\u2013Thu) \u00b7 "
    "UK migration 77,000 (Thu) \u00b7 Kuwait drone strike (Thu) \u00b7 Jazan refinery (Thu) \u00b7 "
    "FIFA cyberattack (Thu) \u00b7 Thanksgiving storm (Thu) \u00b7 F1 Abu Dhabi GP (Dec 3\u20136)"
)

SOURCES = (
    "Sources: Reuters, AP, BBC, Al Jazeera, Consilium, NBS, NZ Herald, "
    "European Commission, Ukrainian Air Force, UNI Global Union, FAO/WFP, UNHCR, "
    "BSE/NSE, Cricinfo, Rio Times, Nexuseuropa digest. All 50 stories first reported "
    "Friday 27 November 2026 (any time zone)."
)

# --- glyphs: one distinct pictogram per small scene ------------------------
def glyph(draw, kind, cx, cy, r, ink, accent):
    """Draw a small pictogram centred at (cx, cy) inside radius r."""
    if kind == "stars":  # EU: circle of 12 stars + red X
        import math
        for i in range(12):
            a = 2 * math.pi * i / 12 - math.pi / 2
            draw.ellipse([cx + int(0.62 * r * math.cos(a)) - 2,
                          cy + int(0.62 * r * math.sin(a)) - 2,
                          cx + int(0.62 * r * math.cos(a)) + 2,
                          cy + int(0.62 * r * math.sin(a)) + 2], fill=GOLD)
        draw.line([cx - 8, cy - 8, cx + 8, cy + 8], fill=accent, width=4)
        draw.line([cx - 8, cy + 8, cx + 8, cy - 8], fill=accent, width=4)
    elif kind == "skyline":  # Gaza: skyline + minaret
        draw.rectangle([cx - r, cy + 2, cx - r + 9, cy + r - 4], fill=ink)
        draw.rectangle([cx - r + 11, cy - 4, cx - r + 20, cy + r - 4], fill=ink)
        draw.rectangle([cx + 2, cy - 10, cx + 6, cy + r - 4], fill=ink)
        draw.polygon([(cx + 1, cy - 10), (cx + 7, cy - 10), (cx + 4, cy - r + 2)],
                     fill=accent)
        draw.rectangle([cx + 9, cy + 6, cx + r, cy + r - 4], fill=ink)
    elif kind == "chart":  # Wall St: rising bars + arrow
        draw.rectangle([cx - r, cy + 6, cx - r + 7, cy + r - 4], fill=ink)
        draw.rectangle([cx - r + 10, cy - 2, cx - r + 17, cy + r - 4], fill=ink)
        draw.rectangle([cx - r + 20, cy - 10, cx - r + 27, cy + r - 4], fill=GREEN)
        draw.line([cx - r, cy - 12, cx + r, cy - r + 2], fill=accent, width=3)
        draw.polygon([(cx + r - 6, cy - r + 2), (cx + r + 2, cy - r + 2),
                      (cx + r - 2, cy - r - 4)], fill=accent)
    elif kind == "euro":
        f = font(SANS_B, int(r * 1.5))
        draw.text((cx, cy), "\u20ac", font=f, fill=ink, anchor="mm")
    elif kind == "bars":
        hs = [0.4, 0.7, 0.55, 1.0, 0.85]
        bw = int(2 * r / 5)
        for i, h in enumerate(hs):
            x0 = cx - r + i * bw
            draw.rectangle([x0, cy + r - int(2 * r * h), x0 + bw - 2, cy + r],
                           fill=GREEN if h == 1.0 else ink)
    elif kind == "drone":
        draw.ellipse([cx - 5, cy - 4, cx + 5, cy + 4], fill=ink)
        draw.line([cx - r, cy - r + 4, cx - 4, cy - 2], fill=ink, width=2)
        draw.line([cx + 4, cy - 2, cx + r, cy - r + 4], fill=ink, width=2)
        draw.line([cx - r, cy + r - 6, cx - 4, cy + 2], fill=ink, width=2)
        draw.line([cx + 4, cy + 2, cx + r, cy + r - 6], fill=ink, width=2)
        for px, py in [(-r, -r + 4), (r, -r + 4), (-r, r - 6), (r, r - 6)]:
            draw.ellipse([cx + px - 3, cy + py - 2, cx + px + 3, cy + py + 2],
                         outline=ink, width=2)
    elif kind == "burst":
        import math
        pts = []
        for i in range(16):
            ang = 2 * math.pi * i / 16
            rad = r if i % 2 == 0 else r * 0.45
            pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
        draw.polygon(pts, fill=accent)
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=PAPER)
    elif kind == "mic":
        draw.rounded_rectangle([cx - 6, cy - r, cx + 6, cy + 2], radius=5,
                               fill=ink)
        draw.arc([cx - 10, cy - 4, cx + 10, cy + 12], 0, 180, fill=ink, width=2)
        draw.line([cx, cy + 12, cx, cy + r - 2], fill=ink, width=2)
    elif kind == "bag":
        draw.rectangle([cx - 9, cy - 6, cx + 9, cy + r - 2], fill=accent)
        draw.arc([cx - 6, cy - r + 2, cx + 6, cy - 2], 0, 180, fill=ink, width=2)
    elif kind == "beehive":
        draw.polygon([(cx, cy - r), (cx - r + 2, cy + 2), (cx + r - 2, cy + 2)],
                     fill=GOLD)
        draw.rectangle([cx - r + 2, cy + 2, cx + r - 2, cy + r - 2], fill=ink)
        draw.line([cx - r + 2, cy + 6, cx + r - 2, cy + 6], fill=PAPER, width=1)
    elif kind == "factory":
        draw.rectangle([cx - r, cy, cx + r, cy + r - 2], fill=ink)
        draw.rectangle([cx - r + 2, cy - 6, cx - r + 6, cy], fill=ink)
        draw.polygon([(cx + 2, cy), (cx + r - 4, cy), (cx + r - 4, cy - r + 4),
                      (cx + r - 8, cy - r + 4)], fill=accent)
    elif kind == "robot":
        draw.rectangle([cx - 8, cy - r + 2, cx + 8, cy - 2], fill=ink)
        draw.line([cx, cy - r + 2, cx, cy - r - 2], fill=ink, width=2)
        draw.ellipse([cx - 2, cy - r - 4, cx + 2, cy - r], fill=accent)
        draw.ellipse([cx - 5, cy - r + 7, cx - 1, cy - r + 11], fill=PAPER)
        draw.ellipse([cx + 1, cy - r + 7, cx + 5, cy - r + 11], fill=PAPER)
        draw.rectangle([cx - 10, cy + 2, cx + 10, cy + r - 2], fill=ink)
    elif kind == "yen":
        f = font(SANS_B, int(r * 1.5))
        draw.text((cx, cy), "\u00a5", font=f, fill=ink, anchor="mm")
    elif kind == "flags":
        draw.line([cx - 8, cy - r, cx - 8, cy + r - 2], fill=ink, width=2)
        draw.polygon([(cx - 8, cy - r), (cx + 2, cy - r + 6), (cx - 8, cy - r + 12)],
                     fill=accent)
        draw.line([cx + 8, cy - r, cx + 8, cy + r - 2], fill=ink, width=2)
        draw.polygon([(cx + 8, cy - r), (cx + r, cy - r + 6), (cx + 8, cy - r + 12)],
                     fill=NAVY)
    elif kind == "boat":
        draw.polygon([(cx - r, cy + 2), (cx + r, cy + 2), (cx + r - 5, cy + r - 2),
                      (cx - r + 5, cy + r - 2)], fill=NAVY)
        draw.line([cx, cy + 2, cx, cy - r + 2], fill=ink, width=2)
        draw.polygon([(cx, cy - r + 2), (cx + r - 4, cy - 2), (cx, cy - 2)],
                     fill=accent)
    else:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ink, width=2)


def big_scene(draw, x, y, w, h, item):
    kind, title, fact, region, field = item
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6, outline=INK, width=2,
                           fill=(255, 255, 255))
    # art band
    draw.rectangle([x + 2, y + 2, x + w - 2, y + 78], fill=LIGHT)
    glyph(draw, kind, x + w // 2, y + 40, 26, INK, RED)
    # region/field tag
    tag = "%s \u00b7 %s" % (region.upper(), field.upper())
    f_tag = font(SANS_B, 10)
    draw.text((x + 10, y + 82), tag, font=f_tag, fill=RED)
    f_t = font(SANS_B, 15)
    lines = fit(draw, title, f_t, w - 20, 1)
    draw.text((x + 10, y + 98), lines[0], font=f_t, fill=INK)
    f_f = font(SANS, 11)
    flines = fit(draw, fact, f_f, w - 20, 2)
    ty = y + 118
    for ln in flines:
        draw.text((x + 10, ty), ln, font=f_f, fill=INK)
        ty += 13


def small_scene(draw, x, y, w, h, item):
    kind, title, fact, region, field = item
    draw.rounded_rectangle([x, y, x + w, y + h], radius=5, outline=GREY, width=1,
                           fill=(255, 255, 255))
    draw.ellipse([x + 6, y + 8, x + 50, y + 52], fill=LIGHT, outline=INK, width=1)
    glyph(draw, kind, x + 28, y + 30, 13, INK, RED)
    f_t = font(SANS_B, 11)
    lines = fit(draw, title, f_t, w - 60, 2)
    ty = y + 6
    for ln in lines:
        draw.text((x + 56, ty), ln, font=f_t, fill=INK)
        ty += 13
    f_f = font(SANS, 10)
    flines = fit(draw, fact, f_f, w - 60, 2)
    for ln in flines:
        draw.text((x + 56, ty), ln, font=f_f, fill=INK)
        ty += 12


def build():
    # --- data assertions ---------------------------------------------------
    assert len(PICTURED_BIG) == 3 and len(PICTURED_SMALL) == 12
    assert len(LISTED) == 35
    assert len(TIMELINE) == 8
    all_rows = [(r[3], r[4]) for r in PICTURED_BIG + PICTURED_SMALL] + \
               [(r[1], r[2]) for r in LISTED]
    assert len(all_rows) == 50
    from collections import Counter
    regions = Counter(r[0] for r in all_rows)
    fields = Counter(r[1] for r in all_rows)
    assert sum(regions.values()) == 50 and sum(fields.values()) == 50
    assert len(regions) == 13, regions
    assert len(fields) == 19, fields

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 24  # margin

    # top rule
    d.rectangle([0, 0, W, 6], fill=RED)
    # masthead
    f_mast = font(SERIF, 30)
    d.text((MX, 12), "THE WORLD IN ONE DAY", font=f_mast, fill=INK)
    f_mast_r = font(SANS_B, 14)
    rt = "FRIDAY \u00b7 27 NOVEMBER 2026"
    d.text((W - MX - d.textlength(rt, font=f_mast_r), 20), rt, font=f_mast_r,
           fill=RED)
    d.line([MX, 56, W - MX, 56], fill=INK, width=2)
    # giant dateline
    f_date = font(SERIF, 40)
    dt = "FRIDAY 27 NOVEMBER 2026"
    d.text(((W - d.textlength(dt, font=f_date)) / 2, 62), dt, font=f_date,
           fill=INK)
    f_sub = font(SANS_B, 12)
    sub = ("50 STORIES  \u00b7  13 REGIONS  \u00b7  19 FIELDS  \u00b7  ALL FIRST REPORTED "
           "TODAY  \u00b7  AS OF %s" % AS_OF)
    d.text(((W - d.textlength(sub, font=f_sub)) / 2, 108), sub, font=f_sub,
           fill=NAVY)
    # region chips
    chip_order = [("EUROPE", 14), ("M. EAST", 5), ("E. ASIA", 6), ("S. ASIA", 4),
                  ("SE ASIA", 2), ("OCEANIA", 3), ("N. AMER.", 6), ("GLOBAL", 3),
                  ("N. AFR.", 1), ("W. AFR.", 1), ("E. AFR.", 1), ("S. AFR.", 1),
                  ("LATAM", 3)]
    assert sum(c for _, c in chip_order) == 50
    f_chip = font(SANS_B, 11)
    total_w = W - 2 * MX
    cw = total_w // len(chip_order)
    for i, (name, cnt) in enumerate(chip_order):
        x0 = MX + i * cw
        d.rounded_rectangle([x0 + 2, 128, x0 + cw - 2, 150], radius=4,
                            outline=INK, width=1, fill=(255, 255, 255))
        label = "%s %d" % (name, cnt)
        d.text((x0 + cw / 2, 139), label, font=f_chip, fill=INK, anchor="mm")
    # key numbers strip
    f_kv = font(SANS_B, 17)
    f_kl = font(SANS_B, 9)
    kw = total_w // len(KEY_NUMBERS)
    for i, (val, lab) in enumerate(KEY_NUMBERS):
        x0 = MX + i * kw
        d.rectangle([x0 + 2, 156, x0 + kw - 2, 192], fill=INK)
        d.text((x0 + kw / 2, 168), val, font=f_kv, fill=(255, 255, 255),
               anchor="mm")
        d.text((x0 + kw / 2, 185), lab, font=f_kl, fill=(220, 220, 220),
               anchor="mm")
    # UTC timeline
    f_tl = font(SANS_B, 11)
    d.text((MX, 200), "THE DAY IN UTC", font=f_tl, fill=RED)
    d.text((W - MX - d.textlength("00:30 \u2014 15:29 UTC", font=f_tl), 200),
           "00:30 \u2014 15:29 UTC", font=f_tl, fill=GREY)
    d.line([MX, 222, W - MX, 222], fill=INK, width=2)
    tw = total_w // len(TIMELINE)
    f_tt = font(SANS_B, 10)
    f_td = font(SANS, 9)
    for i, (t, label) in enumerate(TIMELINE):
        cx = MX + i * tw + tw // 2
        d.ellipse([cx - 4, 218, cx + 4, 226], fill=RED)
        d.text((cx, 230), t, font=f_tt, fill=INK, anchor="ma")
        lines = fit(d, label, f_td, tw - 8, 2)
        ty = 244
        for ln in lines:
            d.text((cx, ty), ln, font=f_td, fill=INK, anchor="ma")
            ty += 11
    # big scenes
    bw = (total_w - 16) // 3
    for i, item in enumerate(PICTURED_BIG):
        big_scene(d, MX + i * (bw + 8), 272, bw, 148, item)
    # small scenes: 4 x 3
    sw = (total_w - 24) // 4
    for i, item in enumerate(PICTURED_SMALL):
        row, col = divmod(i, 4)
        small_scene(d, MX + col * (sw + 8), 428 + row * 64, sw, 58, item)
    # ALSO LISTED
    f_al = font(SANS_B, 12)
    d.text((MX, 626), "ALSO LISTED \u2014 35 MORE STORIES, ALL FIRST REPORTED TODAY",
           font=f_al, fill=RED)
    d.line([MX, 644, W - MX, 644], fill=INK, width=2)
    col_w = (total_w - 32) // 3
    f_row = font(SANS, 10)
    per_col = [12, 12, 11]
    idx = 0
    for c in range(3):
        x0 = MX + c * (col_w + 16)
        y = 652
        for _ in range(per_col[c]):
            headline, region, field = LISTED[idx]
            idx += 1
            text = "\u2022 %s" % headline
            lines = fit(d, text, f_row, col_w, 2)
            for ln in lines:
                d.text((x0, y), ln, font=f_row, fill=INK)
                y += 12
            y += 2
    assert idx == 35
    # DATE CHECK + AS OF boxes
    d.rounded_rectangle([MX, 912, MX + 640, 978], radius=5, outline=RED, width=2,
                        fill=(255, 255, 255))
    f_dc = font(SANS_B, 11)
    d.text((MX + 10, 920), "DATE CHECK \u2014 LEFT OUT AFTER VERIFICATION", font=f_dc,
           fill=RED)
    f_dct = font(SANS, 10)
    lines = fit(d, EXCLUDED, f_dct, 620, 3)
    ty = 936
    for ln in lines:
        d.text((MX + 10, ty), ln, font=f_dct, fill=INK)
        ty += 12
    d.rounded_rectangle([MX + 652, 912, W - MX, 978], radius=5, outline=INK,
                        width=2, fill=INK)
    d.text((MX + 662, 920), "AS OF %s" % AS_OF, font=f_dc, fill=(255, 255, 255))
    f_at = font(SANS, 10)
    alines = fit(d, "The day continues after this image. Built Fri 27 Nov 2026.",
                 f_at, W - MX - (MX + 662) - 10, 3)
    ty = 936
    for ln in alines:
        d.text((MX + 662, ty), ln, font=f_at, fill=(255, 255, 255))
        ty += 12
    # footer
    f_ft = font(SANS, 9)
    flines = fit(d, SOURCES, f_ft, total_w, 2)
    ty = 986
    for ln in flines:
        d.text((MX, ty), ln, font=f_ft, fill=GREY)
        ty += 11
    d.text((MX, 1008), "Round 5 \u00b7 daring-falcon-58 \u00b7 make.fun news-image-20261127",
           font=f_ft, fill=GREY)

    img.save(OUT, "JPEG", quality=88)
    return OUT


if __name__ == "__main__":
    path = build()
    size = os.path.getsize(path)
    print("wrote %s (%d bytes)" % (path, size))
    assert size <= 1048576, "image over 1 MiB"
    with Image.open(path) as im:
        assert im.size == (1024, 1024), im.size
    print("OK: 1024x1024, under 1 MiB")
