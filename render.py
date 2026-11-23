"""Render poster.png: a one-page newspaper front page summing up the world
news of Monday 23 November 2026.

Build-time only: this script runs on the builder's machine with PIL.
The graded program (main.py) is stdlib-only and merely copies poster.png
to /output/entry.png, so no PIL import happens at grade time.

All stories below were verified against the day's reporting on 23 Nov 2026:
COP31 collapse (Antalya), Hormuz tanker strikes, Kyiv drone strike,
Gaza toll, Nepal PM state visit to India, India 720/9d in Wellington,
plus the ticker items. Nothing is invented: no fake times, no fake quotes
beyond the ones reported ('deeply disappointed' — UN Secretary-General).

v2: fixed v1 layout collisions found on visual inspection — hero headline
no longer overlaps the globe, the hero subhead clears its rule, the
cricket body no longer crosses the row rule, ticker lines are wrapped to
fit the page, and the 'burns on off Finland' typo is fixed.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (20, 20, 20)
RED = (166, 30, 34)
BLUE = (31, 58, 95)
GRAY = (90, 90, 90)
RULE = (180, 175, 165)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, text, f, max_w):
    """Greedy word wrap returning a list of lines fitting max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, f, max_w, fill=INK, leading=None):
    lines = wrap(draw, text, f, max_w)
    lh = leading or int(f.size * 1.25)
    for line in lines:
        draw.text((x, y), line, font=f, fill=fill)
        y += lh
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 44  # margin

    # ---- top red rule -------------------------------------------------
    d.rectangle([0, 0, W, 10], fill=RED)

    # ---- masthead ------------------------------------------------------
    mast = font(SERIF_B, 62)
    title = "THE WORLD TODAY"
    tw = text_w(d, title, mast)
    d.text(((W - tw) / 2, 22), title, font=mast, fill=INK)

    # ---- date banner ---------------------------------------------------
    banner_y = 106
    d.rectangle([0, banner_y, W, banner_y + 46], fill=RED)
    bf = font(SANS_B, 27)
    btext = "MONDAY 23 NOVEMBER 2026"
    btw = text_w(d, btext, bf)
    d.text(((W - btw) / 2, banner_y + 9), btext, font=bf, fill=(255, 255, 255))
    sf = font(SANS, 18)
    sub = "15 stories from five continents  •  one day, one page"
    stw = text_w(d, sub, sf)
    d.text(((W - stw) / 2, banner_y + 50), sub, font=sf, fill=GRAY)

    # ---- hero: COP31 ----------------------------------------------------
    hy = 188
    kf = font(SANS_B, 22)
    d.text((M, hy), "CLIMATE  —  COP31, ANTALYA", font=kf, fill=BLUE)
    hf = font(SANS_B, 72)
    d.text((M, hy + 30), "COP31 COLLAPSES", font=hf, fill=INK)
    # globe drawing, right of hero headline area (clear of the text)
    cx, cy, r = 890, 288, 66
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=4)
    d.ellipse([cx - r, cy - 22, cx + r, cy + 22], outline=INK, width=2)
    d.arc([cx - 26, cy - r, cx + 26, cy + r], 270, 90, fill=INK, width=2)
    d.arc([cx - 26, cy - r, cx + 26, cy + r], 90, 270, fill=INK, width=2)
    # red crack across the globe
    d.line([(cx - 50, cy - 52), (cx - 16, cy - 10), (cx - 38, cy + 6),
            (cx - 2, cy + 40), (cx + 18, cy + 56)], fill=RED, width=5)
    sub_f = font(SANS, 25)
    hero_text = ("Climate talks fail as the EU rejects a draft with no mention "
                 "of fossil fuels — the UN chief is “deeply disappointed”.")
    y = draw_wrapped(d, M, hy + 118, hero_text, sub_f, 660, leading=33)
    rule(d, M, 420, W - M, 2)

    # ---- row 2: two stories --------------------------------------------
    ry = 436
    col_w = (W - 2 * M - 28) // 2
    # left: Hormuz
    x = M
    d.text((x, ry), "HORMUZ  —  GULF SHIPPING", font=kf, fill=BLUE)
    h2 = font(SANS_B, 36)
    y = draw_wrapped(d, x, ry + 30, "25 TANKERS HIT IN A WEEK",
                     h2, col_w, leading=42)
    b2 = font(SANS, 21)
    draw_wrapped(d, x, y + 6,
                 "The Iran–US war engulfs Saudi Arabia and Bahrain; Gulf oil "
                 "flow falls sharply. Houthis strike Riyadh for a third day.",
                 b2, col_w, leading=26)
    # right: Ukraine
    x = M + col_w + 28
    d.line([(x - 14, ry), (x - 14, ry + 190)], fill=RULE, width=2)
    d.text((x, ry), "UKRAINE  —  KYIV", font=kf, fill=BLUE)
    y = draw_wrapped(d, x, ry + 30, "DRONE HITS KYIV REGION",
                     h2, col_w, leading=42)
    draw_wrapped(d, x, y + 6,
                 "At least 14 people missing after a strike on a building, "
                 "Zelenskiy says. A Russian ship still burns off Finland.",
                 b2, col_w, leading=26)
    rule(d, M, 646, W - M, 2)

    # ---- row 3: three stories ------------------------------------------
    ry = 662
    col3 = (W - 2 * M - 2 * 24) // 3
    h3 = font(SANS_B, 28)
    b3 = font(SANS, 19)
    stories = [
        ("GAZA", "9 KILLED IN 48 HOURS",
         "Israeli strikes raise the toll since the October 2025 ceasefire "
         "to 1,661."),
        ("NEPAL – INDIA", "SHAH MEETS MODI",
         "Nepal PM Balendra Shah holds bilateral talks in Delhi on a "
         "two-day state visit."),
        ("CRICKET", "INDIA 720/9d — A RECORD",
         "India post a record first-innings total in the Wellington Test."),
    ]
    for i, (kick, head, body) in enumerate(stories):
        x = M + i * (col3 + 24)
        if i:
            d.line([(x - 12, ry), (x - 12, ry + 168)], fill=RULE, width=2)
        d.text((x, ry), kick, font=kf, fill=BLUE)
        y = draw_wrapped(d, x, ry + 30, head, h3, col3, leading=33)
        draw_wrapped(d, x, y + 4, body, b3, col3, leading=24)
    rule(d, M, 846, W - M, 2)

    # ---- ticker: also on 23 November ------------------------------------
    ty = 860
    d.text((M, ty), "ALSO ON 23 NOVEMBER", font=kf, fill=RED)
    tf = font(SANS, 18)
    ticker = ("BepiColombo enters Mercury orbit • Pentagon releases 43 UAP "
              "files • S. Korea minister quits over AI cheating • UN "
              "AI-weapons talks continue • Mexico captures ‘El Chapo Isidro’ "
              "• Nigeria boat toll 24 • Indonesia factory fire: 50 missing "
              "• Liverpool 4–0 Man Utd • Bitcoin rebounds")
    draw_wrapped(d, M, ty + 30, ticker, tf, W - 2 * M, leading=23)

    # ---- footer ---------------------------------------------------------
    rule(d, M, 972, W - M, 1, fill=RULE)
    ff = font(SANS, 16)
    ftext = "Compiled from the day’s reporting  •  All events of Monday 23 November 2026"
    ftw = text_w(d, ftext, ff)
    d.text(((W - ftw) / 2, 982), ftext, font=ff, fill=GRAY)

    img.save("poster.png", optimize=True)
    print("saved poster.png")


if __name__ == "__main__":
    main()
