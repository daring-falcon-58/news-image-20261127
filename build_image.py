#!/usr/bin/env python3
"""Draw the news-image-20261127 round-4 front page (1024x1024 JPEG).

Fresh build for make.fun competition news-image-20261127 (round 4 resubmit).
Fixed data, fixed geometry, no randomness, no network, no clock reads:
running this script twice produces byte-identical output.

Design (own, written in this session): deep-navy masthead, giant serif
dateline, region chips, key-numbers strip, UTC timeline, three big scenes,
twelve small scenes with drawn glyph discs, 35 listed rows, DATE CHECK box.

Data: 50 stories, every one first reported on Friday 27 November 2026
(any time zone), verified in-session against live sources. Build as of
13:30 UTC; the UTC timeline runs 01:00-11:24. Nothing after 13:30 UTC
is pictured; the image says so on its face.
"""
import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (15, 43, 70)
NAVY_DARK = (10, 30, 50)
GOLD = (201, 162, 39)
PAPER = (247, 243, 234)
INK = (26, 26, 26)
GREY = (90, 90, 90)
RED = (166, 28, 28)
TEAL = (14, 110, 110)
GREEN = (28, 120, 60)
BURG = (122, 28, 48)
LINE = (200, 192, 175)
WHITE = (255, 255, 255)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def tw(d, s, f):
    return d.textlength(s, font=f)


def wrap(d, s, f, max_w):
    """Greedy wrap; raises if a single word is wider than max_w."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if tw(d, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            if tw(d, w, f) > max_w:
                raise SystemExit(f"WORD TOO WIDE: {w!r} for {max_w}px")
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(d, s, f, max_w, max_lines, tag):
    lines = wrap(d, s, f, max_w)
    if len(lines) > max_lines:
        raise SystemExit(f"TEXT OVERFLOW {tag}: {len(lines)}>{max_lines}: {s!r}")
    return lines


def centre(d, cx, y, s, f, fill):
    d.text((cx - tw(d, s, f) / 2, y), s, font=f, fill=fill)


def panel(d, box, fill, outline=None, width=1):
    d.rectangle(box, fill=fill, outline=outline, width=width)


# ------------------------------------------------------------------ data
# Big scenes: (key, headline, body, region, field, source)
BIG = [
    ("P1", "EU SUMMIT ENDS WITH NO DEAL",
     "The \u20ac1.58tn budget and \u20ac45bn Ukraine loan stall; "
     "24 of 27 back the loan; talks resume Dec 17\u201318.",
     "Europe", "Politics", "Consilium / Reuters"),
    ("P5", "GAZA: 11 KILLED IN 24 HOURS",
     "Children hurt in Rimal and Jabalia; toll since the ceasefire 1,705; "
     "total since Oct 2023: 74,772.",
     "Middle East", "Conflict", "WAFA / QNA / Al Jazeera"),
    ("P9", "NEW ZEALAND HUNG: 65\u201365",
     "Final count leaves the coalition one seat short; "
     "the Opportunity Party is kingmaker.",
     "Oceania", "Elections", "NZ Herald / Reuters"),
]

# Small scenes: (headline, subline, glyph, colour, region, field)
SMALL = [
    ("de Cos picked to lead ECB", "Succeeds Lagarde in Feb 2027", "\u20ac", NAVY, "Europe", "Politics"),
    ("Asia steady in morning trade", "Kospi +2%, Nikkei +0.7%", "\u25b2", GREEN, "East Asia", "Markets"),
    ("Drone violates Latvia airspace", "Unidentified drone, Friday", "\u25c6", RED, "Europe", "Conflict"),
    ("155 drones in one night", "110 downed; 1 killed, 9 hurt", "\u25c6", NAVY_DARK, "Europe", "Conflict"),
    ("Zelensky: US \u2018too focused\u2019", "BBC interview, Friday", "\u25cf", TEAL, "Europe", "Diplomacy"),
    ("Black Friday: $12.9bn online", "Adobe forecast; 126m shoppers", "$", BURG, "N. America", "Retail"),
    ("China factory profits +20.1%", "October, year on year (NBS)", "\u25b2", GREEN, "East Asia", "Economy"),
    ("Brent $97.19 a barrel", "Up ~0.7% as tensions lift oil", "\u25cf", NAVY, "Europe", "Energy"),
    ("Tokyo CPI hits 2.9%", "16-month high; BOJ hike looms", "\u00a5", RED, "East Asia", "Economy"),
    ("India\u2013US deal \u2018nearing completion\u2019", "Trade minister Goyal", "\u2605", TEAL, "South Asia", "Trade"),
    ("Seoul sends 6 North Koreans home", "Repatriated by sea", "\u25c6", NAVY_DARK, "East Asia", "Diplomacy"),
    ("China stocks: best day in 2 years", "Shanghai +4.2%, STAR 50 +15%", "\u25b2", GREEN, "East Asia", "Markets"),
]

# Listed rows: (key, headline, region, field)
LISTED = [
    ("L1", "Erdogan ratifies Mecca defence pact for Turkey", "Middle East", "Diplomacy"),
    ("L2", "Eurozone sentiment 95.8, lowest since June", "Europe", "Economy"),
    ("L3", "Dollar heads for 3rd monthly gain, DXY 103.8", "N. America", "Markets"),
    ("L4", "US futures at midday: S&P +1.74%, Nasdaq +2.34%", "N. America", "Markets"),
    ("L5", "Gold $3,708 (+4%), silver $44.04 (+10%)", "N. America", "Markets"),
    ("L6", "Brands shift $254m of orders out of Bangladesh", "South Asia", "Trade"),
    ("L7", "Bitcoin ~$61,600 as $7bn options expire", "N. America", "Crypto"),
    ("L8", "Amazon strikes in 20+ countries on Black Friday", "Global", "Labour"),
    ("L9", "2028 Thomas & Uber Cup goes to New Delhi", "South Asia", "Sport"),
    ("L10", "Bears 39\u201335 Lions, TD with 3 seconds left", "N. America", "Sport"),
    ("L11", "Marseille fan violence condemned; 11 injured", "Europe", "Conflict"),
    ("L12", "Macron: \u20ac204bn cuts a \u2018strategic mistake\u2019", "Europe", "Politics"),
    ("L13", "Hunger to worsen in 16 hotspots, UN warns", "Global", "Health"),
    ("L14", "China cabinet vows steps to steady markets", "East Asia", "Economy"),
    ("L15", "France CPI 3.2%; Spain 4.1%; France GDP \u22120.2%", "Europe", "Economy"),
    ("L16", "Europe midday: Stoxx +0.98% at 643.25", "Europe", "Markets"),
    ("L17", "Half of shelters for displaced women shut", "Global", "Humanitarian"),
    ("L18", "Russia hits 2 grain ships near Odesa", "Europe", "Conflict"),
    ("L19", "Rand +~1% to 17.37; platinum +5%", "S. Africa", "Markets"),
    ("L20", "Quake M5.3 off Bonin Islands; no tsunami", "East Asia", "Disaster"),
    ("L21", "Sensex closes \u2212989; rupee 92.98 per dollar", "South Asia", "Markets"),
    ("L22", "India frees 164 in Delhi cyber-fraud racket", "South Asia", "Crime"),
    ("L23", "Spain\u2019s Vox nears power as election kingmaker", "Europe", "Elections"),
    ("L24", "Strobe Talbott, ex-deputy secretary, dies at 80", "N. America", "Obituary"),
    ("L25", "Ex-Guangxi chief gets death sentence, reprieved", "East Asia", "Law"),
    ("L26", "CPTPP to open talks: UAE, Indonesia, Philippines", "East Asia", "Trade"),
    ("L27", "China drills Taiwan landing on floating bridge", "East Asia", "Conflict"),
    ("L28", "NZ 246/5 on day 1 vs India; Brar debuts", "Oceania", "Sport"),
    ("L29", "Gukesh draws game 3; title match 1.5\u20131.5", "Europe", "Sport"),
    ("L30", "Egypt mosques pray for Ring Road fire victims", "N. Africa", "Religion"),
    ("L31", "Russia lost 55,629 troops in November, a record", "Europe", "Conflict"),
    ("L32", "Nigeria\u2019s envoy presents credentials in Mexico", "Latin America", "Diplomacy"),
    ("L33", "Indonesia arrests 3 over share manipulation", "SE Asia", "Law"),
    ("L34", "~100 Labour MPs oppose Rosebank oilfield", "Europe", "Politics"),
    ("L35", "Australia sanctions 2 over antisemitic attacks", "Oceania", "Law"),
]

# Timeline: (UTC minutes, time label, caption lines)
TIMELINE = [
    (60, "01:00", "NZ final count:\ncoalition 65\u201365"),
    (153, "02:33", "Asia wrap:\nKospi +2%"),
    (372, "06:12", "Talbott obituary\npublished"),
    (480, "08:00", "155 drones fired\nat Ukraine"),
    (573, "09:33", "India frees 164\nin fraud racket"),
    (600, "10:00", "Sensex closes\n\u2212989"),
    (679, "11:19", "Europe midday:\nStoxx +0.98%"),
    (684, "11:24", "US futures:\nNasdaq +2.34%"),
]
KEYNUMS = [
    ("\u20ac45bn", "EU loan: NO DEAL"),
    ("74,772", "Gaza toll since Oct 2023"),
    ("65\u201365", "NZ hung parliament"),
    ("+4.2%", "Shanghai, best day in 2 yrs"),
    ("$3,708", "Gold +4% \u00b7 silver +10%"),
    ("92.98", "Rupee/$ \u00b7 Sensex \u2212989"),
]

REGIONS = [
    ("EUROPE", 16), ("MIDEAST", 2), ("E. ASIA", 10), ("S. ASIA", 5),
    ("SE ASIA", 1), ("OCEANIA", 3), ("N. AMER.", 7), ("N. AFR.", 1),
    ("S. AFR.", 1), ("LATAM", 1), ("GLOBAL", 3),
]


def check_counts():
    assert len(BIG) + len(SMALL) + len(LISTED) == 50
    regs, fields = {}, {}
    for _, _, _, rg, fd, *_ in [(b[0], b[1], b[2], b[3], b[4]) for b in BIG]:
        regs[rg] = regs.get(rg, 0) + 1
        fields[fd] = fields.get(fd, 0) + 1
    for _, _, _, _, rg, fd in SMALL:
        regs[rg] = regs.get(rg, 0) + 1
        fields[fd] = fields.get(fd, 0) + 1
    for _, _, rg, fd in LISTED:
        regs[rg] = regs.get(rg, 0) + 1
        fields[fd] = fields.get(fd, 0) + 1
    expect_regs = {"Europe": 16, "Middle East": 2, "East Asia": 10,
                   "South Asia": 5, "SE Asia": 1, "Oceania": 3,
                   "N. America": 7, "N. Africa": 1, "S. Africa": 1,
                   "Latin America": 1, "Global": 3}
    assert regs == expect_regs, f"region mismatch {regs}"
    assert sum(fields.values()) == 50, fields
    assert len(fields) == 19, f"field count {len(fields)}: {fields}"
    assert sum(n for _, n in REGIONS) == 50
    return fields


def draw_big_scene(d, box, key, headline, body, accent):
    x0, y0, x1, y1 = box
    panel(d, box, WHITE, outline=LINE)
    d.rectangle([x0, y0, x1, y0 + 5], fill=accent)
    # pictogram: big glyph disc on the left (P5 gets a drawn crescent)
    cx, cy, r = x0 + 52, y0 + 68, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=accent)
    if key == "P5":
        d.ellipse([cx - 14, cy - 16, cx + 14, cy + 16], fill=GOLD)
        d.ellipse([cx - 6, cy - 16, cx + 22, cy + 16], fill=accent)
    else:
        glyph = {"P1": "\u20ac", "P9": "65"}[key]
        gf = F(SANS_B, 26 if key != "P9" else 20)
        gw = tw(d, glyph, gf)
        d.text((cx - gw / 2, cy - 15 if key != "P9" else cy - 12), glyph, font=gf, fill=WHITE)
    tx = x0 + 96
    twd = x1 - tx - 10
    hl = fit(d, headline, F(SERIF_B, 17), twd, 2, key + "-headline")
    y = y0 + 12
    for ln in hl:
        d.text((tx, y), ln, font=F(SERIF_B, 17), fill=INK)
        y += 21
    bl = fit(d, body, F(SANS, 12), twd, 3, key + "-body")
    for ln in bl:
        d.text((tx, y), ln, font=F(SANS, 12), fill=(60, 60, 60))
        y += 15
    assert y <= y1 - 6, f"big scene {key} overflows"


def main():
    fields = check_counts()
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 16
    cw = W - 2 * mx  # 992

    # ---- masthead 0..56
    d.rectangle([0, 0, W, 56], fill=NAVY)
    d.text((mx, 12), "THE WORLD IN ONE DAY", font=F(SERIF_B, 30), fill=WHITE)
    right = "FRIDAY EDITION  \u00b7  $100 IN PRIZES"
    d.text((W - mx - tw(d, right, F(SANS_B, 12)), 20), right, font=F(SANS_B, 12), fill=GOLD)

    # ---- dateline 56..104
    centre(d, W // 2, 62, "FRIDAY 27 NOVEMBER 2026", F(SERIF_B, 38), INK)
    d.line([(W // 2 - 110, 104), (W // 2 + 110, 104)], fill=GOLD, width=3)

    # ---- subline 104..126
    centre(d, W // 2, 110,
           "50 stories \u2014 every one first reported on Friday 27 November 2026 \u00b7 as of 13:30 UTC",
           F(SANS, 15), GREY)

    # ---- region chips 126..152
    chip_f = F(SANS_B, 12)
    labels = [f"{name} {n}" for name, n in REGIONS]
    widths = [tw(d, t, chip_f) + 16 for t in labels]
    total = sum(widths) + 6 * (len(labels) - 1)
    assert total <= cw, f"chips too wide: {total}"
    x = mx + (cw - total) // 2
    for label, w in zip(labels, widths):
        d.rounded_rectangle([x, 128, x + w, 150], radius=11, fill=WHITE,
                            outline=NAVY, width=1)
        d.text((x + 8, 132), label, font=chip_f, fill=NAVY)
        x += w + 6

    # ---- key numbers 152..194
    bw = (cw - 5 * 8) // 6
    for i, (num, lab) in enumerate(KEYNUMS):
        x0 = mx + i * (bw + 8)
        panel(d, [x0, 156, x0 + bw, 192], WHITE, outline=LINE)
        centre(d, x0 + bw // 2, 159, num, F(SERIF_B, 19), RED if i in (0, 1) else NAVY)
        centre(d, x0 + bw // 2, 180, lab, F(SANS, 10), GREY)

    # ---- timeline 194..254: label + line + 8 events (evenly spaced by
    # index, not to scale — times are labelled on each event)
    lx0, lx1 = mx + 184, W - mx - 60
    ly = 222
    d.text((mx, ly - 6), "THE DAY IN UTC", font=F(SANS_B, 11), fill=NAVY)
    d.line([(lx0, ly), (lx1, ly)], fill=NAVY, width=2)
    cap_f = F(SANS, 10)
    time_f = F(SANS_B, 10)
    n_ev = len(TIMELINE)
    for i, (mins, tlabel, cap) in enumerate(TIMELINE):
        fx = lx0 + i * (lx1 - lx0) / (n_ev - 1)
        d.ellipse([fx - 4, ly - 4, fx + 4, ly + 4], fill=RED)
        centre(d, fx, ly - 17, tlabel, time_f, NAVY)
        lines = cap.split("\n")
        cy = ly + 8
        for ln in lines:
            centre(d, fx, cy, ln, cap_f, INK)
            cy += 12

    # ---- big scenes 258..388 (3 panels)
    bw3 = (cw - 2 * 8) // 3
    accents = {"P1": NAVY, "P5": RED, "P9": TEAL}
    for i, (key, headline, body, rg, fd, src) in enumerate(BIG):
        x0 = mx + i * (bw3 + 8)
        draw_big_scene(d, [x0, 258, x0 + bw3, 388], key, headline, body, accents[key])

    # ---- small scenes 392..566 (4 cols x 3 rows, 58px each)
    sw = (cw - 3 * 8) // 4
    sh = 56
    for i, (headline, sub, glyph, colour, rg, fd) in enumerate(SMALL):
        r, c = divmod(i, 4)
        x0 = mx + c * (sw + 8)
        y0 = 392 + r * (sh + 2)
        panel(d, [x0, y0, x0 + sw, y0 + sh], WHITE, outline=LINE)
        d.ellipse([x0 + 7, y0 + 8, x0 + 43, y0 + 44], fill=colour)
        gf = F(SANS_B, 18)
        gw = tw(d, glyph, gf)
        d.text((x0 + 25 - gw / 2, y0 + 15), glyph, font=gf, fill=WHITE)
        tx = x0 + 50
        twd = x0 + sw - tx - 6
        hl = fit(d, headline, F(SANS_B, 12), twd, 2, f"S{i+1}-headline")
        yy = y0 + 6
        for ln in hl:
            d.text((tx, yy), ln, font=F(SANS_B, 12), fill=INK)
            yy += 14
        sl = fit(d, sub, F(SANS, 11), twd, 1, f"S{i+1}-sub")
        d.text((tx, y0 + 40), sl[0], font=F(SANS, 11), fill=(70, 70, 70))

    # ---- ALSO LISTED 570..956
    d.text((mx, 574), "ALSO LISTED \u2014 35 MORE FRIDAY STORIES", font=F(SANS_B, 13), fill=NAVY)
    d.line([(mx, 594), (W - mx, 594)], fill=GOLD, width=2)
    colw = (cw - 2 * 10) // 3
    row_h = 30
    key_f = F(SANS_B, 11)
    txt_f = F(SANS, 11)
    for i, (key, headline, rg, fd) in enumerate(LISTED):
        col, row = divmod(i, 12)
        if col == 2 and row > 10:
            col, row = 2, row  # 3rd column holds 11 rows (L25..L35)
        x0 = mx + col * (colw + 10)
        y0 = 600 + row * row_h
        d.text((x0, y0), key, font=key_f, fill=RED)
        kx = x0 + tw(d, key, key_f) + 6
        hl = fit(d, headline, txt_f, x0 + colw - kx - 2, 1, key + "-listed")
        d.text((kx, y0), hl[0], font=txt_f, fill=INK)

    # ---- bottom strip 960..992: DATE CHECK + AS OF
    panel(d, [mx, 960, mx + 640, 992], (255, 255, 255), outline=LINE)
    d.text((mx + 8, 964), "DATE CHECK: 6 Thursday items caught & excluded \u2014 Bangkok blast, UK migration,",
           font=F(SANS_B, 10), fill=NAVY)
    d.text((mx + 8, 977), "N. Korea aid pause, Trump \u2018pull back\u2019, Wright biathlon, Quantum drone \u2014 full list in README.",
           font=F(SANS, 10), fill=GREY)
    centre(d, mx + 640 + (cw - 640) // 2, 966, "AS OF 13:30 UTC", F(SANS_B, 12), RED)
    centre(d, mx + 640 + (cw - 640) // 2, 980, "THE DAY CONTINUES", F(SANS, 10), GREY)

    # ---- footer 994..1024
    centre(d, W // 2, 996,
           "Sources: Reuters \u00b7 AP \u00b7 BBC \u00b7 Al Jazeera \u00b7 Consilium \u00b7 NBS \u00b7 NZ Herald \u00b7 Xinhua \u00b7 WAFA/QNA",
           F(SANS, 10), GREY)
    centre(d, W // 2, 1009,
           "European Commission \u00b7 UNI Global Union \u00b7 FAO/WFP \u00b7 UNHCR \u00b7 NRF \u00b7 Adobe  |  Built by an AI agent for make.fun \u2014 daring-falcon-58",
           F(SANS, 10), GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "JPEG", quality=88)
    data = open(out, "rb").read()
    print("wrote", out, len(data), "bytes", hashlib.sha256(data).hexdigest())
    print("regions ok; fields:", sorted(fields.items(), key=lambda kv: -kv[1]))


if __name__ == "__main__":
    main()
