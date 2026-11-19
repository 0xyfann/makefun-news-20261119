from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
PAPER = "#fcfcfa"
INK = "#161b22"
MUTED = "#333e48"
BLUE = "#153e63"
RED = "#ab2437"
RULE = "#a6aeb3"
FONT_DIR = Path("/usr/share/fonts/truetype/noto")


@lru_cache(maxsize=None)
def font(size, bold=False):
    weight = "Bold" if bold else "Regular"
    return ImageFont.truetype(str(FONT_DIR / f"NotoSans-{weight}.ttf"), size)


def draw_front_page():
    image = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(image)
    text_boxes = []

    def text(x, y, value, size, *, bold=False, color=INK, width=944):
        face = font(size, bold)
        left, top, right, bottom = draw.textbbox((x, y), value, font=face, anchor="lt")
        if not (0 <= left < right <= min(x + width, SIZE) and 0 <= top < bottom <= SIZE):
            raise ValueError(f"Text exceeds its column: {value!r}")
        for a, b, c, d in text_boxes:
            if left < c and a < right and top < d and b < bottom:
                raise ValueError(f"Text overlaps another line: {value!r}")
        text_boxes.append((left, top, right, bottom))
        draw.text((x, y), value, font=face, fill=color, anchor="lt")

    def block(x, y, lines, size, step, *, bold=False, color=INK, width=944):
        for i, line in enumerate(lines):
            text(x, y + i * step, line, size, bold=bold, color=color, width=width)

    def card(x, y, section, headline, summary):
        text(x, y, section, 23, bold=True, color=BLUE, width=450)
        text(x, y + 34, headline, 38, bold=True, width=450)
        block(x, y + 84, summary, 30, 39, color=MUTED, width=450)

    draw.rectangle((40, 33, 984, 40), fill=INK)
    text(37, 57, "THE WORLD", 104, bold=True)
    text(43, 167, "THURSDAY, 19 NOVEMBER 2026", 31, bold=True, color=BLUE)
    draw.rectangle((40, 213, 984, 217), fill=RED)

    text(42, 238, "UNITED STATES  /  POLITICS", 24, bold=True, color=RED)
    block(39, 276, ("Democrats nominate", "Jeffries for Speaker"),
          58, 66, bold=True, width=703)
    block(43, 419, ("If elected, he would be the first Black", "Speaker of the U.S. House."),
          32, 39, color=MUTED, width=708)

    # Stylized Capitol on a halftone field; separate from the editorial text.
    x, y, w, h = 762, 239, 222, 258
    draw.rectangle((x, y, x+w, y+h), fill=BLUE)
    for iy in range(y + 14, y + h - 8, 12):
        for ix in range(x + 14, x + w - 8, 12):
            draw.ellipse((ix, iy, ix + 2, iy + 2), fill="#7996ac")
    mid, base = x + w // 2, y + 169
    draw.pieslice((mid-53, base-100, mid+53, base+6), 180, 360, fill=PAPER)
    for rx in (18, 36):
        draw.arc((mid-rx, base-100, mid+rx, base+6), 180, 360, fill=BLUE, width=2)
    draw.rectangle((mid-4, base-117, mid+4, base-102), fill=PAPER)
    draw.line((mid, base-126, mid, base-116), fill=PAPER, width=3)
    draw.rectangle((mid-63, base-43, mid+63, base-35), fill=PAPER)
    draw.rectangle((mid-68, base-30, mid+68, base-23), fill="#a9c5d9")
    for offset in (-52, -26, 0, 26, 52):
        draw.rectangle((mid+offset-5, base-21, mid+offset+5, base+15), fill=PAPER)
    for half, level in ((68, 16), (77, 25), (88, 35)):
        draw.rectangle((mid-half, base+level, mid+half, base+level+4), fill=PAPER)

    draw.line((40, 514, 984, 514), fill=RULE, width=2)
    text(42, 531, "MIDDLE EAST  /  HUMANITARIAN AID", 23, bold=True, color=RED)
    text(40, 561, "Four nations urge Israel to let aid into Gaza", 38, bold=True)
    text(42, 609, "Australia, Canada, Italy and the U.K. call for relief after floods.", 30, color=MUTED)
    draw.line((40, 651, 984, 651), fill=RULE, width=2)

    draw.line((510, 665, 510, 951), fill=RULE, width=2)
    draw.line((40, 807, 984, 807), fill=RULE, width=2)
    card(42, 668, "EUROPE  /  UKRAINE", "EU proposes €45B loan",
         ("Ukraine would repay after", "Russia pays reparations."))
    card(533, 668, "BUSINESS  /  AI", "Anthropic raises $81.3B",
         ("The AI company sets", "a record for IPO proceeds."))
    card(42, 823, "SCIENCE  /  SPACE", "Voyager 1 sets mark",
         ("NASA’s probe reaches", "one light-day from Earth."))
    card(533, 823, "CULTURE  /  GAMING", "GTA VI rolls out",
         ("Global launch takes", "players to Vice City."))

    draw.rectangle((40, 963, 984, 966), fill=INK)
    text(42, 978, "19 November 2026 — World news in one image", 23, bold=True, color=BLUE)
    return image


if __name__ == "__main__":
    draw_front_page().save(Path(__file__).with_name("entry.png"), optimize=True)
