import math
from PIL import Image, ImageDraw

S = 8                      # supersample factor
N = 200 * S                # working canvas
c = N / 2                  # center
W = int(6 * S)             # line width (scaled)

img = Image.new("L", (N, N), 255)      # white background
d = ImageDraw.Draw(img)

BLACK = 0

def poly(pts, w=W):
    d.line(list(pts) + [pts[0]], fill=BLACK, width=w, joint="curve")

def circle(r, w=W):
    d.ellipse([c - r, c - r, c + r, c + r], outline=BLACK, width=w)

def down_triangle(r, rot=0):
    # inverted (downward) equilateral triangle inscribed in radius r
    # apex pointing down => start angle at 90 (bottom)
    pts = []
    for a in (90, 210, 330):
        ang = math.radians(a + rot)
        pts.append((c + r * math.cos(ang), c + r * math.sin(ang)))
    poly(pts)

def lotus(r_in, r_out, petals=8, rot=0):
    for i in range(petals):
        a = math.radians(i * 360 / petals + rot)
        px = c + r_in * math.cos(a)
        py = c + r_in * math.sin(a)
        # petal tip
        tx = c + r_out * math.cos(a)
        ty = c + r_out * math.sin(a)
        # two side control points
        half = math.radians(360 / petals / 2)
        s1 = (c + r_in * math.cos(a - half), c + r_in * math.sin(a - half))
        s2 = (c + r_in * math.cos(a + half), c + r_in * math.sin(a + half))
        d.line([s1, (tx, ty)], fill=BLACK, width=W)
        d.line([s2, (tx, ty)], fill=BLACK, width=W)

# ---- Bhupura: outer square with four T-shaped gates ----
m = int(10 * S)                         # margin
sq = [(m, m), (N - m, m), (N - m, N - m), (m, N - m)]
poly(sq)
sq2 = int(m + 12 * S)
d.rectangle([sq2, sq2, N - sq2, N - sq2], outline=BLACK, width=W)

# gates (T shapes) on each side of inner square
g = int(18 * S)      # gate half-width
gd = int(22 * S)     # gate depth
def gate(cx, cy, horiz):
    if horiz:  # top/bottom gate opening
        d.rectangle([cx - g, cy - gd, cx + g, cy + gd], outline=BLACK, width=W, fill=255)
    else:
        d.rectangle([cx - gd, cy - g, cx + gd, cy + g], outline=BLACK, width=W, fill=255)

mid = N / 2
gate(mid, sq2, True)          # top
gate(mid, N - sq2, True)      # bottom
gate(sq2, mid, False)         # left
gate(N - sq2, mid, False)     # right

# ---- Circles ----
R = int(78 * S)
circle(R)

# ---- Eight-petal lotus ----
lotus(int(58 * S), int(74 * S), petals=8, rot=22.5)

circle(int(56 * S))

# ---- Five downward triangles (Kali) ----
for i, r in enumerate([50, 42, 34, 26, 18]):
    down_triangle(int(r * S))

# ---- Central bindu ----
d.ellipse([c - 5 * S, c - 5 * S, c + 5 * S, c + 5 * S], fill=BLACK)

# downscale to exact 200x200
out = img.resize((200, 200), Image.LANCZOS).convert("RGB")
out.save("~/Desktop/catalog/kali_yantra.jpg", "JPEG", quality=95)
print("saved", out.size, out.mode)
