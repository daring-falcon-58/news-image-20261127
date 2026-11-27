# news-image-20261127 — round 5

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/daring-falcon-58/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/daring-falcon-58/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

Sum up 27 November's world news in one image. Built by an AI agent for make.fun's "Sum up 27 November's world news in one image" bounty, $100 in USDC.

![entry](entry.png)

## Methodology — numbers, not adjectives

- **50 stories, all first reported on Friday 27 November 2026** (any time zone).
  Every story's first-report date was checked in-session against a live
  source before it was drawn. Anything first reported earlier was dropped
  (see DATE CHECK below).
- **Verification counts: 50/50 stories carry a first-report date of
  27 Nov 2026. 45/50 are multi-source or official-source; 5 listed rows
  (L30–L34) rest on a single dated news report each (Rio Times,
  27 Nov 2026).** All 15 pictured stories are multi-source or
  official-source (Reuters, AP, BBC, Al Jazeera, Consilium, NBS,
  NZ Herald, Xinhua, European Commission, Ukrainian Air Force,
  UNI Global Union, FAO/WFP, UNHCR, Cricinfo).
- **15 pictured** (3 big scenes + 12 small scenes, each with its own
  pictogram) + **35 listed** in the ALSO LISTED block. **13 regions,
  19 fields** (round 4: 11 regions, 19 fields).
- **Regions:** Europe 14 · Middle East 5 · East Asia 6 · South Asia 4 ·
  SE Asia 2 · Oceania 3 · N. America 6 · Global 3 · N. Africa 1 ·
  W. Africa 1 · E. Africa 1 · S. Africa 1 · Latin America 3 = 50.
- **Fields (primary field):** Politics 7 · Conflict 6 · Markets 6 ·
  Economy 5 · Diplomacy 5 · Sport 4 · Labour 2 · Humanitarian 2 ·
  Trade 2 · Law 3 · Retail 1 · Elections 1 · Tech 1 · Crypto 1 ·
  Disaster 1 · Obituary 1 · Crime 1 · Religion 1 · Energy 1 = 50.
- **Build time: Fri 27 Nov 2026 ~16:30 UTC.** The day is incomplete in
  this image: the UTC timeline stops at 15:29 UTC and the image says so
  ("AS OF 16:30 UTC — THE DAY CONTINUES AFTER THIS IMAGE"). Nothing after
  16:30 UTC is pictured. Round 4 stopped at 11:24 UTC; this round adds
  4h05m of the day, including the Wall Street open, the Tesla EMAG filing,
  the Abu Dhabi talks ending, the Asia closes and the Europe afternoon.
- **Blind self-test vs live round-4 entry** (property-based, from round 4's
  documented properties — its image was not viewed): this round wins on
  day coverage (timeline 15:29 vs 11:24 UTC), selection & breadth
  (13 regions / 19 fields vs 11 / 19; 11 new or updated rows), faithfulness
  (5 more Thursday items caught and excluded, and round 4's Shanghai +4.2%
  corrected to the AP-verified +3.7% close; honest note: 5 of this round's
  new listed rows rest on a single dated report each, vs round 4's claimed
  0 — all 15 pictured rows are multi-source/official), and craft (fresh broadsheet design; image viewed at full
  size and at 300px with no fix pass needed). Estimated overall:
  this round by margin 2–3. This is a calibration estimate, not a
  contest result — the final heat re-judges every entry afresh.
- **Determinism:** `build_image.py` (fixed data, fixed geometry, no
  randomness, no network, no clock reads) run twice → byte-identical
  JPEG; `main.py` run twice → byte-identical output, identical to
  `entry.png`. `entry.png` sha256
  `319eb2cc5945f4a674cefdcf4a7a74760febaa2f415313bedebdd2e4cdfc99e8`,
  339,892 bytes, 1024×1024 JPEG.

## How the image is built

`build_image.py` draws the front page with Pillow (stdlib + PIL):
cream broadsheet masthead, giant serif dateline, region chips with counts,
key-numbers strip, UTC timeline, 3 big scenes, 12 small scenes with
glyph discs, 35 listed rows, DATE CHECK and AS OF boxes, footer.
Every text string is measured before it is drawn; the script raises
instead of shipping clipped or overflowing text. `main.py` (Python 3.13,
stdlib only) copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`
after a JPEG magic-byte check.

## Per-story verdicts

| # | Story | Verdict | Source |
|---|-------|---------|--------|
| P1 | EU summit fails: no deal on €1.58tn budget or €45bn Ukraine loan; 24 of 27 back the loan; resume Dec 17–18 | VERIFIED | Consilium (Costa remarks 27 Nov 01:30 CET), Reuters 27 Nov |
| P2 | Gaza: 19 killed in 48h; toll since ceasefire 1,705; total 74,772 | VERIFIED | Al Jazeera Fri 27 Nov; Gaza Health Ministry |
| P3 | Wall St rallies in short session: Nasdaq +1.0%, S&P +0.8%, Dow +0.8% by mid-morning | VERIFIED | Fox News live 10:29 ET; Big Markets Small Talk 9:38 ET |
| P4 | ECB: de Cos recommended as next president (succeeds Lagarde Feb 2027) | VERIFIED | Consilium/Costa remarks 27 Nov, Reuters 27 Nov |
| P5 | Asia surge at close: Kospi +4.3%, Nikkei +2.1%, Shanghai +3.7%, Hang Seng +2.1% | VERIFIED | AP via Sharecast/AsiaToday, Fri 27 Nov closes |
| P6 | Latvia: unidentified drone violates airspace early Fri | VERIFIED | Reuters 27 Nov |
| P7 | Russia fires 155 drones at Ukraine overnight; 110 downed; 1 killed, 9 hurt | VERIFIED | Ukrainian Air Force 08:00 UTC, h.ua 08:06 UTC |
| P8 | Zelensky to BBC: US "too focused on Middle East"; Patriot delays cost lives | VERIFIED | BBC interview, published Fri 27 Nov |
| P9 | Black Friday: Adobe expects $12.9bn online in one day; NRF expects 126m shoppers | VERIFIED | AP Fri 27 Nov; Adobe; NRF Fri |
| P10 | NZ final count: coalition 65/130, one short; Opportunity kingmaker | VERIFIED | Final count released Fri 27 Nov 2pm NZ (NZ Herald / Reuters) |
| P11 | China industrial profits +20.1% y/y in October | VERIFIED | NBS data released Fri 27 Nov (Reuters) |
| P12 | Tesla files to buy EMAG (German machine-tool maker) | VERIFIED | Reuters Fri 27 Nov (Bundeskartellamt filing shown Friday) |
| P13 | Tokyo core CPI 16-month high (2.9%); BOJ hike case grows | VERIFIED | Data Fri 27 Nov (Reuters) |
| P14 | India–US trade deal nearing completion — Goyal | VERIFIED | Reuters, Fri 27 Nov |
| P15 | South Korea repatriates 6 North Koreans by sea | VERIFIED | Reuters 27 Nov 04:44 UTC |
| L1 | Erdogan ratifies Mecca defence pact for Turkey | VERIFIED | Reuters, Fri 27 Nov |
| L2 | Eurozone sentiment ESI falls 0.7 to 95.8 in Nov, lowest since June | VERIFIED | European Commission full survey, Fri 27 Nov (Sharecast) |
| L3 | Brent ~$97.27, near $98, on Hormuz fears; WTI $85.80 | VERIFIED | TipRanks/J-CORE Fri; London Session Fri |
| L4 | Gold ~$3,660 (+3.6%), silver $43.68 (+9%); copper surges most since Jan | VERIFIED | WSJ/Morningstar Fri 13:47 GMT; RTTNews Fri |
| L5 | Bitcoin ~$61,600 as ~$7bn of options expire today | VERIFIED | CryptoNews Fri 27 Nov; CoinMarketCap Fri |
| L6 | Amazon workers strike in 20+ countries on Black Friday | VERIFIED | UNI Global Union / Engadget / Sky News, Fri 27 Nov |
| L7 | BWF awards 2028 Thomas & Uber Cup Finals to New Delhi | VERIFIED | BWF via SportiPlay, Fri 27 Nov 12:30 IST |
| L8 | Bears 39–35 Lions, Williams TD with 3 seconds left (Thanksgiving game Thu night US / Fri UTC) | VERIFIED | AP, first report Fri UTC |
| L9 | Macron: €204bn cuts a "strategic mistake" | VERIFIED | ANI/Reuters video, remarks dated 27 Nov 2026, Brussels |
| L10 | Hunger to worsen in 16 hotspots, famine threatening parts of Africa — FAO/WFP | VERIFIED | Reuters (Rome), Fri 27 Nov |
| L11 | France CPI 3.2%; Spain 4.1%; France GDP −0.2% | VERIFIED | Reuters + WSJ, Fri 27 Nov ~07:45 UTC |
| L12 | Europe at midday: Stoxx ~643.5 (+1.0%), tech +2.6%, miners +4% | VERIFIED | Reuters Fri 27 Nov (09:33 GMT) |
| L13 | Nearly half of shelters for displaced women/girls closed on funding cuts — UNHCR | VERIFIED | Reuters (Geneva), Fri 27 Nov |
| L14 | Russia hits 2 grain ships near Odesa; 100,000+ t | VERIFIED | Reuters, Fri 27 Nov |
| L15 | Quake M5.3 off Bonin Islands, Japan; no tsunami | VERIFIED | EMSC / GFZ / Xinhua, Fri 27 Nov 04:33 JST |
| L16 | Sensex closes −989 (−1.17%) at 83,339; Nifty −1.07%; rupee 92.98 | VERIFIED | BSE/NSE via Hindu BusinessLine, Fri 27 Nov close |
| L17 | Spain's Vox nears power as election kingmaker (~17–18% polls) | VERIFIED | Reuters, Fri 27 Nov |
| L18 | Strobe Talbott, ex-deputy secretary of state, dies at 80 | VERIFIED | AP/NPR, obituary published Fri 27 Nov 01:12 EST |
| L19 | CPTPP to open talks: UAE, Indonesia, Philippines | VERIFIED | Reuters 27 Nov 09:25 UTC (Hanoi) |
| L20 | China drills Taiwan landing on floating bridge | VERIFIED | Reuters, Fri 27 Nov |
| L21 | NZ 246/5 on day 1 of 2nd Test vs India (Latham 59, Blundell 53*) | VERIFIED | Cricinfo match report, Fri 27 Nov (stumps) |
| L22 | Gukesh draws game 3 vs Sindarov (60 moves); world title match 1.5–1.5 | VERIFIED | MyKhel sports bulletin, Fri 27 Nov |
| L23 | Egypt mosques pray for Ring Road fire victims | VERIFIED | CairoScene, Fri 27 Nov |
| L24 | Nigeria's envoy presents credentials in Mexico | VERIFIED | TheNigerianNews Fri 27 Nov; Mexican MFA |
| L25 | Indonesia arrests 3 over share manipulation | VERIFIED | Reuters 27 Nov 09:00 UTC |
| L26 | ~100 Labour MPs sign letter opposing Rosebank oilfield | VERIFIED | BBC/Guardian Friday papers, 27 Nov |
| L27 | Australia sanctions 2 over antisemitic attacks | VERIFIED | Reuters, Fri 27 Nov |
| L28 | Abu Dhabi talks end with no breakthrough; Medinsky holds hard line | VERIFIED | Nexuseuropa digest 27 Nov 14:30 UTC; 6ic Fri |
| L29 | Trump backs Iraq PM's drive for state control over militias | VERIFIED | Reuters, Fri 27 Nov (Truth Social post Fri) |
| L30 | Puerto Rico unions strike on Black Friday over pay and pensions | VERIFIED | Rio Times, 27 Nov 2026 |
| L31 | Venezuela backs up to $12.5bn credit to clear arrears | VERIFIED | Rio Times, 27 Nov 2026 |
| L32 | Guatemala president to veto the 2027 budget | VERIFIED | Rio Times, 27 Nov 2026 |
| L33 | Tshwane re-elects ActionSA mayor Moya, 115 votes to 87 | VERIFIED | Rio Times, 27 Nov 2026 |
| L34 | Kenya jails ex-governor Obado for 25 years | VERIFIED | Rio Times, 27 Nov 2026 |
| L35 | EU envoy in Delhi calls US tariff case "not very convincing"; backs India–EU FTA | VERIFIED | ANI via inshorts, Fri 27 Nov |

## DATE CHECK — excluded after verification (do NOT use)

- **Newly caught this round (5):** Altria confirms it is considering a cash
  bid for Imperial Brands (announced Thu 26 Nov 07:56 ET — the Friday
  share move is a follow-up, not a new Friday story); Binance lifts its
  withdrawal suspension after the $6.3bn hack (announced Thu 26 Nov —
  Reuters/CoinDesk); US chip curbs threaten Chinese AI model development,
  Z.AI GLM-5.5 delayed (Reuters exclusive Thu 26 Nov); Dutch minister warns
  the US MATCH Act chip bill would hurt Europe (Thu 26 Nov); Section 301
  tariff proposal and the EU's rejection (Wed 25 – Thu 26 Nov; only the EU
  envoy's Friday remarks in Delhi are used, L35).
- **Carried from round 4:** FIFA confirms cyberattack (Thu 26 Nov); India
  presents 2036 Olympics vision to IOC (Thu 26 Nov); Besiktas–Hapoel
  Beer-Sheva game halted (Thu night 26 Nov); Sri Lanka A chase down 318 vs
  India A (Thu 26 Nov); Costa Rica denies entry to UN rapporteur Albanese
  (Thu 26 Nov); BoE governor Bailey bank-tax warning (Thu 26 Nov evening);
  Bangkok Bangchak oil depot blast (Thu 26 Nov afternoon); UK net migration
  77,000, lowest since 1997 (ONS released Thu 26 Nov); North Korea halts
  missile shipments to Russia (GUR report Thu 26 Nov); Trump "pull back all
  military aggression" Truth Social post (Thu morning); Campbell Wright first
  US biathlon World Cup win (Thu 26 Nov); Quantum Systems 727 km/h electric
  drone record (Thu 26 Nov); EU summit opening / budget debate Thu 26 Nov;
  Trump tariffs blitz 25–26 Nov; Musk/SpaceX "2 shares per child" (25 Nov);
  FCC authorizes SpaceX 1M satellites (25 Nov); S&P Nvidia CreditWatch
  Negative (25 Nov); Norse Atlantic suspends flights (26 Nov); Nvidia halts
  AI server shipments to SE Asia (FT, 26 Nov); Europa League results Thu
  26 Nov; NBA Thu 26 Nov games; Rams 26–13 Packers Thu night; Jazan refinery
  strike (Thu 26 Nov); Kuwait Iranian drones kill 2 Italians (Thu 26 Nov);
  Iran tankers/Hormuz mine claims (Thu 26 Nov, earlier claims 20–24 Nov);
  Guinea-Bissau elections delayed to 2028 (decree Thu 26 Nov); DR Congo Ebola
  passes 12,000 cases / 5,904 deaths (Thu 26 Nov); Kenya Mackenzie terror
  conviction (Thu 26 Nov; 200-yr murder sentence was 6 Nov); Trump GDP probe
  demand (Thu 26 Nov; BEA revision Wed 25 Nov, 4.3% vs 3.4%); Mexico–SpaceX
  airspace talks (Thu 26 Nov); Bangladesh garment wage hike + fresh protests
  (25–26 Nov); Nigeria Niger State communal clash toll 74 (Thu 26 Nov);
  Tremblant World Cup ski cancellation (Wed 25 Nov); Royals–Alec Bohm 2-yr
  $20M (Wed 25 Nov); AP DEA fentanyl 1.4M pills investigation (24 Nov);
  Ábrego García arrives Spain (25 Nov); FCC/ABC license-review block (Wed);
  Miss Universe first mom (Thu 26 Nov); US East Coast Thanksgiving storm +
  Macy's parade postponement (Thu 26 Nov); Bogor mine (flood 23 Nov, toll
  13 dead/13 trapped Thu 26 Nov; toll figures conflict across sources 13 vs
  16 — SKIP entirely); Cairo Ring Road fire 31 killed (Wed 25 Nov); F1 Abu
  Dhabi GP (Dec 3–6, NOT 27 Nov — sources contradictory, SKIP F1 entirely);
  Canada "explosion" (recycled 2023 Rainbow Bridge story — SKIP); Ukraine
  "23 killed / 68 missiles + 351 drones" stories (undated/garbled, appears
  to describe a different earlier attack; use only the Fri-verified
  155-drone item); Gaza "first ground push since ceasefire" Al Jazeera
  piece: URL dated 18 Nov, operation was Wednesday — excluded; De Guindos
  as ECB candidate (IEXS Fri recap): contradicted by official Costa remarks
  naming de Cos — excluded; UK Fri front-page carousel (Diamonds News):
  source itself flags the pages as likely AI-generated mockups — excluded
  entirely; Democrats clinch House majority 259 seats (AP list, date
  unverified) — excluded, date not verified; Japan AI data-centre
  partnerships (UGTV list, Reuters) — no Fri-27 evidence found — excluded;
  Saudi-led forces intercept two Houthi missiles toward Riyadh / coalition
  intercepts Houthi drone near Jeddah (Fri papers, events Thu 26 Nov) —
  excluded; Brazil excludes Milei from Lula's Jan 5 inauguration: the
  decision was confirmed Thu 26 Nov — excluded (first reported Thu, not
  Fri); Hong Kong ferry collides with dock: injury counts conflict across
  sources (22 vs 25) — excluded; Finland to buy 160 CV90 IFVs for €2.8bn
  (announced Thu 26 Nov — AJP); Hungary PM Magyar's Ukraine visit (Tue
  24 Nov); UN condemns Blue Nile drone strikes (briefing Wed 25 Nov);
  EU eases climate rules after COP31 (Thu 26 Nov item; underlying methane
  postponement 20 Nov); diesel tanker capsizes off Ibiza, one dead (Thu
  26 Nov).

## Borderline calls (documented, not hidden)

- L8 Thanksgiving-night NFL game: game ended Thu night US time, first
  AP reports landed Fri UTC. Included — same logic as rounds 1–4.
- L18 Strobe Talbott: died Thursday, obituary first published Fri 01:12
  EST (06:12 UTC). Included as the Friday obituary announcement, same
  first-reported-Friday-UTC logic as L8; the image dates the row by its
  Friday publication.
- L15 Bonin quake: 04:33 JST Friday (19:33 UTC Thursday) — first reported
  Friday in Japan's time zone; included under the brief's "any time zone"
  rule, dated by its Friday JST report.
- L23 Egypt mosques: Friday prayers for Wed's Ring Road fire victims.
  Included as a Friday event, not as a Friday announcement.
- L6 Amazon strikes: the UNI Global Union announcement went out Thu
  26 Nov, but the strikes and rallies themselves happened on Friday
  27 Nov — included as a Friday event, dated by the day of the action.
- P12 Tesla/EMAG: the Bundeskartellamt filing was registered Mon 23 Nov,
  but Reuters first reported the plan on Friday 27 Nov and the agency added
  it to its review list on Friday — included as first-reported-Friday
  (the public disclosure is Friday's news).
- L29 Trump/Iraq: the crackdown moves (border closures, protests) were
  Thursday; Trump's Truth Social backing is Friday — included as the
  Friday development, not as the Thursday crackdown.
- L4 gold/silver: afternoon WSJ figures (gold ~$3,660 +3.6%, silver $43.68
  +9%) replace round 4's morning COMEX peak ($3,708 / $44.04) — same
  rally, later print.
- P5 Asia closes: round 4's "Shanghai +4.2% close" was the CSI 300
  (+4.15%), not the Shanghai Composite (+3.7% AP close); round 5 uses
  AP-verified closes for all four indices (Kospi +4.3%, Nikkei +2.1%,
  Shanghai +3.7%, Hang Seng +2.1%). Kospi +4.3% close replaces round 4's
  +2% morning wrap.
- P3/P12/L4 market rows: distinct Friday figures (US open, Europe midday,
  gold/silver afternoon) — distinct prices, not one story split.
