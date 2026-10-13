# Builds images/hero-background.svg: a seamless tile of the three characters of
# the mia logo (images/characters/*.svg, exported from microbiome/outreach
# figures/mia_logo.svg), drawn as faint white silhouettes.
#
# Characters are placed with Poisson-disc sampling on a torus, so they are
# evenly spread, never overlap, and the tile repeats without visible seams.
#
# Usage: python3 scripts/make-hero-background.py
# Change SEED for a different arrangement, SPACING for density.
import math, random, re, xml.etree.ElementTree as ET
from pathlib import Path

SEED = 11
TILE = 900          # tile size in px; must match background-size in styles/theme.scss
SPACING = 125       # minimum distance between character centres
SIZE = (55, 85)      # character height range
ANGLE = 30          # max rotation either way
OPACITY = (.12, .2)

SVG = "http://www.w3.org/2000/svg"; XL = "http://www.w3.org/1999/xlink"
root_dir = Path(__file__).resolve().parent.parent
names = ["bow", "virus", "hat"]


def symbol(name):
    """Return the character as a <symbol>, with ids prefixed so files don't clash."""
    text = (root_dir / "images/characters" / f"{name}.svg").read_text()
    text = re.sub(r'\bid="([^"]+)"', rf'id="{name}-\1"', text)
    text = re.sub(r'url\(#([^)]+)\)', rf'url(#{name}-\1)', text)
    text = re.sub(r'href="#([^"]+)"', rf'href="#{name}-\1"', text)
    el = ET.fromstring(text)
    inner = "".join(ET.tostring(c, encoding="unicode") for c in el)
    inner = inner.replace(f'xmlns="{SVG}"', "").replace(f'xmlns:xlink="{XL}"', "").replace("ns0:", "").replace("ns1:", "xlink:")
    vb = el.get("viewBox").split()
    return f'<symbol id="{name}" viewBox="{" ".join(vb)}">{inner}</symbol>', float(vb[2]) / float(vb[3])


def torus_dist(a, b):
    dx = abs(a[0] - b[0]); dy = abs(a[1] - b[1])
    return math.hypot(min(dx, TILE - dx), min(dy, TILE - dy))


def poisson_disc(r, k=30):
    """Bridson's algorithm on a TILE x TILE torus."""
    pts = [(random.uniform(0, TILE), random.uniform(0, TILE))]
    active = [0]
    while active:
        i = random.choice(active)
        for _ in range(k):
            a = random.uniform(0, 2 * math.pi); d = random.uniform(r, 2 * r)
            p = ((pts[i][0] + d * math.cos(a)) % TILE, (pts[i][1] + d * math.sin(a)) % TILE)
            if all(torus_dist(p, q) >= r for q in pts):
                pts.append(p); active.append(len(pts) - 1)
                break
        else:
            active.remove(i)
    return pts


random.seed(SEED)
symbols, aspect = {}, {}
for n in names:
    symbols[n], aspect[n] = symbol(n)

points = poisson_disc(SPACING)
# Pick characters so that close neighbours tend to differ
chosen = []
for i, p in enumerate(points):
    near = {chosen[j] for j, q in enumerate(points[:i]) if torus_dist(p, q) < SPACING * 1.5}
    options = [n for n in names if n not in near] or names
    chosen.append(random.choice(options))

items = []
for (x, y), name in zip(points, chosen):
    h = random.uniform(*SIZE); w = h * aspect[name]
    angle = random.uniform(-ANGLE, ANGLE); op = random.uniform(*OPACITY)
    # Draw copies across the tile edges so the pattern wraps seamlessly
    for dx in (-TILE, 0, TILE):
        for dy in (-TILE, 0, TILE):
            cx, cy = x + dx, y + dy
            if -h < cx < TILE + h and -h < cy < TILE + h:
                items.append(f'<g transform="translate({cx:.0f} {cy:.0f}) rotate({angle:.0f})" opacity="{op:.2f}" filter="url(#ghost)">'
                             f'<use href="#{name}" xlink:href="#{name}" x="{-w/2:.0f}" y="{-h/2:.0f}" width="{w:.0f}" height="{h:.0f}"/></g>')

svg = f'''<svg xmlns="{SVG}" xmlns:xlink="{XL}" width="{TILE}" height="{TILE}" viewBox="0 0 {TILE} {TILE}">
<defs>
<filter id="ghost"><feFlood flood-color="#ffffff"/><feComposite in2="SourceAlpha" operator="in"/></filter>
{"".join(symbols.values())}
</defs>
{"".join(items)}
</svg>'''
(root_dir / "images/hero-background.svg").write_text(svg)
print(f"wrote images/hero-background.svg: {len(points)} characters, {len(svg) // 1024} KB")
