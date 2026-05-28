#!/usr/bin/env python3
"""Generate the Open Graph share image for rallyup.team (1200x630).

Matches the site's brand: blue gradient (#3d68f5 -> #1e3a8a), dot texture,
lowercase wordmark, and a yellow (#DDFF4D) accent. Headline reflects the
current "linkedin audience building for b2b founders & execs" positioning.

Run: python3 scripts/make_og_image.py
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BLUE = (61, 104, 245)        # --ru-blue  #3d68f5
DEEP = (30, 58, 138)         # --ru-blue-deep #1e3a8a
YELLOW = (221, 255, 77)      # --ru-yellow #DDFF4D
WHITE = (255, 255, 255)

ARIAL_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"
TIMES_ITALIC = "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


# --- vertical gradient background (blue -> deep blue) ---
img = Image.new("RGB", (W, H))
px = img.load()
for y in range(H):
    row = lerp(BLUE, DEEP, y / (H - 1))
    for x in range(W):
        px[x, y] = row

draw = ImageDraw.Draw(img, "RGBA")

# --- subtle dot texture (like the site's dot-pattern) ---
for gy in range(0, H, 34):
    for gx in range(0, W, 34):
        draw.ellipse([gx, gy, gx + 2, gy + 2], fill=(255, 255, 255, 22))

# --- soft yellow glow blobs (echo the CTA section) ---
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([W - 320, -160, W + 120, 280], fill=(221, 255, 77, 26))
gd.ellipse([-160, H - 280, 260, H + 160], fill=(221, 255, 77, 20))
img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"), (0, 0))
draw = ImageDraw.Draw(img, "RGBA")

PAD = 80

# --- logo badge + wordmark (top-left) ---
bx, by, bsz = PAD, PAD, 60
draw.rounded_rectangle([bx, by, bx + bsz, by + bsz], radius=15,
                       fill=(106, 127, 240, 255))
# simple megaphone glyph inside the badge
draw.rounded_rectangle([bx + 14, by + 24, bx + 22, by + 38], radius=3, fill=WHITE)
draw.polygon([(bx + 22, by + 22), (bx + 46, by + 15), (bx + 46, by + 47),
              (bx + 22, by + 40)], fill=WHITE)
wordmark = font(ARIAL_BOLD, 44)
draw.text((bx + bsz + 18, by + 4), "rallyup", font=wordmark, fill=WHITE)
# yellow accent dot after the wordmark
ww = draw.textlength("rallyup", font=wordmark)
dot_x = bx + bsz + 18 + ww + 4
draw.ellipse([dot_x, by + 40, dot_x + 12, by + 52], fill=YELLOW)

# --- headline (auto-fit two lines within content width) ---
lines = ["linkedin audience building", "for b2b founders & execs."]
max_w = W - 2 * PAD
size = 92
while size > 40:
    hf = font(ARIAL_BOLD, size)
    if max(draw.textlength(l, font=hf) for l in lines) <= max_w:
        break
    size -= 2
hf = font(ARIAL_BOLD, size)
line_h = size + 12
y = 230
for i, line in enumerate(lines):
    draw.text((PAD, y + i * line_h), line, font=hf, fill=WHITE)

# yellow underline beneath "audience building" on line 1
pre = draw.textlength("linkedin ", font=hf)
phrase_w = draw.textlength("audience building", font=hf)
uy = y + size + 4
draw.rounded_rectangle([PAD + pre, uy, PAD + pre + phrase_w, uy + 9],
                       radius=4, fill=YELLOW)

# --- tagline (serif italic) ---
tf = font(TIMES_ITALIC, 36)
ty = y + 2 * line_h + 30
draw.text((PAD, ty), "we are storytellers.", font=tf, fill=(255, 255, 255, 230))

# --- footer: domain (left) ---
df = font(ARIAL_BOLD, 30)
draw.text((PAD, H - PAD - 22), "rallyup.team", font=df, fill=WHITE)

img.save("assets/og-image.png", "PNG", optimize=True)
print(f"wrote assets/og-image.png ({img.size[0]}x{img.size[1]})")
