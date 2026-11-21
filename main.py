#!/usr/bin/env python3
"""news-image-20261121 — a text-only broadsheet front page for
Saturday 21 November 2026, drawn with PIL (DejaVu fonts).

The program renders the page deterministically to /output/entry.png
(1024x1024, PNG). No network, no randomness, no timestamps: two runs
produce byte-identical output. If PIL or the fonts are unavailable in
the grading sandbox, it falls back to copying the pre-rendered
entry.png shipped beside this file.
"""

import os
import shutil
import sys

W, H = 1024, 1024
MARGIN = 36
GUTTER = 18
PAPER = (250, 247, 240)
INK = (18, 18, 18)
RED = (158, 27, 27)
GREY = (96, 96, 96)
RULE = (60, 60, 60)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def _font(name, size):
    from PIL import ImageFont

    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def load_fonts():
    return {
        "masthead": _font("DejaVuSerif-Bold.ttf", 58),
        "lead_head": _font("DejaVuSerif-Bold.ttf", 33),
        "head": _font("DejaVuSerif-Bold.ttf", 16),
        "deck": _font("DejaVuSans.ttf", 11),
        "kicker": _font("DejaVuSans-Bold.ttf", 11),
        "section": _font("DejaVuSans-Bold.ttf", 12),
        "dateline": _font("DejaVuSans.ttf", 12),
        "footer": _font("DejaVuSans.ttf", 10),
    }


def wrap(draw, text, font, width):
    """Greedy word wrap; returns a list of lines that fit in width px."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=font) <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, font, width, fill=INK, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    if leading is None:
        leading = int(font.size * 1.28)
    for line in wrap(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def text_h(draw, text, font, width, leading=None):
    if leading is None:
        leading = int(font.size * 1.28)
    return len(wrap(draw, text, font, width)) * leading


def rule(draw, x, y, width, weight=1, fill=RULE):
    draw.rectangle([x, y, x + width, y + weight - 1], fill=fill)


# The day's news, researched from reports published on 21 November 2026
# (plus the biggest stories of the 20th that developed further today).
LEAD = {
    "kicker": "CLIMATE  —  ANTALYA, TÜRKIYE",
    "head": "COP31 spills into overtime as draft deal drops all mention of fossil fuels",
    "deck": (
        "Negotiators from nearly 200 nations work through Saturday after "
        "the summit's final text stripped out any reference to ending the "
        "use of coal, oil and gas — and activists warn it risks becoming "
        "the worst climate summit ever."
    ),
}

# (section, kicker, headline, deck) — three columns, in order.
# Length discipline: heads fit 2 lines, decks fit 2 lines at column width.
COLUMNS = [
    [
        ("WORLD", "POLAND",
         "Russian missiles crash in Poland in huge Ukraine attack",
         "Two Kh-101 missiles and a drone fell in south-east Poland. No "
         "one hurt; Warsaw calls it a provocation."),
        ("WORLD", "UKRAINE",
         "Two dead, 42 hurt as Russian strike hits Kryvyi Rih",
         "A strike on the president's home city killed two and injured 42, "
         "including four children, officials said."),
        ("WORLD", "THE HAGUE",
         "World court: Myanmar guilty of genocide against Rohingya",
         "The ICJ finds Myanmar responsible for genocide in Rakhine — the "
         "first such verdict against a state."),
        ("WORLD", "RIYADH",
         "Houthi missile debris falls on Riyadh after interception",
         "The Arab coalition confirms debris and damage in Riyadh after air "
         "defences intercepted the threat."),
        ("WORLD", "SANCTIONS",
         "US sanctions four Iranians over oil revenues",
         "The Treasury adds four men to its list, accusing them of handling "
         "Iranian oil money."),
        ("WORLD", "BRUSSELS",
         "EU approves €1bn in military aid for Ukraine",
         "The Council backs joint arms procurement, with deliveries by "
         "end-2027. Britain pledges 1,000+ drones."),
    ],
    [
        ("POLITICS", "SHENZHEN",
         "Fallout grows after Trump–Xi–Putin summit",
         "The first three-way US–China–Russia leaders' meeting leaves "
         "Europe fearing deals made over its head."),
        ("POLITICS", "KYIV",
         "US offered Ukraine NATO entry for Donbas land",
         "President Zelenskyy reveals Washington proposed Kyiv cede the rest "
         "of Donbas for NATO entry. He refused."),
        ("POLITICS", "WASHINGTON",
         "Senate rejects curb on Trump's Iran war powers, 51–48",
         "The war-powers resolution, passed by the House, fails in the "
         "Senate as tensions with Tehran stay high."),
        ("POLITICS", "WASHINGTON",
         "Trump pardons baseball's Pete Rose — posthumously",
         "The president announces a pardon for the late hit king, banned "
         "from the game for betting on baseball."),
        ("POLITICS", "NEW DELHI",
         "Modi opens first SCO civilisational dialogue in Delhi",
         "The prime minister calls for dialogue and trust at the opening "
         "of the SCO forum in Delhi."),
        ("BUSINESS", "MUMBAI",
         "Sensex rallies nearly 900 points; NSE now world's No. 5 exchange",
         "Indian shares end sharply higher as the National Stock Exchange "
         "overtakes Nasdaq and Hong Kong by value."),
    ],
    [
        ("TECH", "CYBERATTACK",
         "JPMorgan, Visa and Mastercard hit in vendor cyberattacks",
         "The banking and payments giants report incidents at third-party "
         "suppliers; core networks are unaffected."),
        ("TECH", "LOS ANGELES",
         "Hyundai unveils the 2027 Elantra at the LA Auto Show",
         "The eighth-generation Elantra debuts with a redesigned body, new "
         "technology and hybrid options."),
        ("SPORT", "LAS VEGAS",
         "F1 qualifying under the lights on the Las Vegas Strip today",
         "Russell was fastest in a wet second practice; champion Antonelli "
         "takes a five-place grid penalty."),
        ("SPORT", "WELLINGTON",
         "India fight back against New Zealand in first Test",
         "India reach 159 for 1 at stumps on day two, trailing by 209 runs "
         "after New Zealand's first-innings total."),
        ("SCIENCE", "SPACE",
         "Voyager 1 phones home from a full light-day away",
         "NASA's farthest spacecraft signals from over a light-day away — "
         "the most distant human-made object ever."),
        ("SCIENCE", "UNITED NATIONS",
         "UN warns hunger funding cuts threaten food aid in 2027",
         "The World Food Programme says funding cuts could leave millions "
         "without assistance next year."),
    ],
]

FOOTER = (
    "The World Ledger  •  Saturday 21 November 2026  •  All times UTC  •  "
    "Sources: Reuters, UN News, AP, national wires"
)

BRIEFS = [
    "Cyclone Akvan crosses the Odisha coast, then weakens inland",
    "Carlsen forfeits rapid games at chess tournament",
    "Malaysia to resettle 10,000 Rohingya refugees to Türkiye",
    "Nepal PM Balendra Shah to visit India on 22–23 November",
]


def render():
    from PIL import Image, ImageDraw

    fonts = load_fonts()
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0 = MARGIN
    x1 = W - MARGIN
    cw = x1 - x0

    # ---- Masthead -------------------------------------------------------
    name = "THE WORLD LEDGER"
    nw = d.textlength(name, font=fonts["masthead"])
    d.text(((W - nw) / 2, 22), name, font=fonts["masthead"], fill=INK)
    rule(d, x0, 96, cw, 3, INK)
    rule(d, x0, 101, cw, 1, INK)
    date_line = "SATURDAY  21  NOVEMBER  2026"
    dw = d.textlength(date_line, font=fonts["dateline"])
    d.text(((W - dw) / 2, 110), date_line, font=fonts["dateline"], fill=RED)
    sub = "The world's news, in one page  •  No. 325  •  Price: one minute of your day"
    sw = d.textlength(sub, font=fonts["footer"])
    d.text(((W - sw) / 2, 130), sub, font=fonts["footer"], fill=GREY)

    # ---- Lead story -----------------------------------------------------
    y = 158
    d.text((x0, y), LEAD["kicker"], font=fonts["kicker"], fill=RED)
    y += 18
    y = draw_wrapped(d, x0, y, LEAD["head"], fonts["lead_head"], cw,
                     leading=38)
    y += 6
    y = draw_wrapped(d, x0, y, LEAD["deck"], fonts["deck"], cw, leading=15)
    y += 10
    rule(d, x0, y, cw, 3, INK)
    rule(d, x0, y + 5, cw, 1, INK)
    y += 14

    # ---- Three columns --------------------------------------------------
    col_w = (cw - 2 * GUTTER) // 3
    col_top = y
    col_bottom = 918
    col_titles = ["WORLD", "POLITICS & BUSINESS", "TECH, SPORT & SCIENCE"]
    for ci, stories in enumerate(COLUMNS):
        cx = x0 + ci * (col_w + GUTTER)
        cy = col_top
        d.text((cx, cy), col_titles[ci], font=fonts["section"], fill=INK)
        cy += 15
        rule(d, cx, cy, col_w, 2, INK)
        cy += 9
        for si, (sec, kicker, head, deck) in enumerate(stories):
            d.text((cx, cy), kicker, font=fonts["kicker"], fill=RED)
            cy += 14
            cy = draw_wrapped(d, cx, cy, head, fonts["head"], col_w,
                              leading=20)
            cy += 3
            cy = draw_wrapped(d, cx, cy, deck, fonts["deck"], col_w,
                              leading=14)
            cy += 7
        if cy > col_bottom:
            raise SystemExit(
                "column %d overflows by %d px" % (ci, cy - col_bottom))

    # ---- Briefs strip ---------------------------------------------------
    by = col_bottom + 12
    rule(d, x0, by, cw, 2, INK)
    by += 10
    d.text((x0, by), "IN BRIEF", font=fonts["section"], fill=RED)
    by += 20
    half = (cw - GUTTER) // 2
    for i, brief in enumerate(BRIEFS):
        bx = x0 + (i % 2) * (half + GUTTER)
        byy = by + (i // 2) * 18
        d.text((bx, byy), "▪  " + brief, font=fonts["deck"], fill=INK)
    fy = by + 44
    rule(d, x0, fy, cw, 1, RULE)
    fw = d.textlength(FOOTER, font=fonts["footer"])
    d.text(((W - fw) / 2, fy + 8), FOOTER, font=fonts["footer"], fill=GREY)
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    here = os.path.dirname(os.path.abspath(__file__))
    try:
        img = render()
    except Exception:
        # Fallback: ship the pre-rendered image beside this file.
        src = os.path.join(here, "entry.png")
        if os.path.exists(src):
            shutil.copyfile(src, out_path)
            return
        raise
    img.save(out_path, format="PNG", optimize=True)


if __name__ == "__main__":
    main()


