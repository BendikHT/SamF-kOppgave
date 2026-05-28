from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
import matplotlib.cm as cm

# -----------------------------
# LOAD DATA
# -----------------------------
CURRENT_DIR = Path(__file__).parent
filnavn = CURRENT_DIR / "data/EXR.csv"

aar = []
kronekurs = []

with open(filnavn, encoding="utf-8-sig") as fil:
    filinnhold = csv.reader(fil, delimiter=";")
    next(filinnhold)

    for rad in filinnhold:
        try:
            aar.append(int(rad[14]))
            kronekurs.append(float(rad[15].replace(",", ".")))
        except:
            pass

aar = np.array(aar)
kronekurs = np.array(kronekurs)

# -----------------------------
# FIGURE SETUP
# -----------------------------
plt.style.use("dark_background")

fig, ax = plt.subplots(figsize=(16, 9))

# Background colors
fig.patch.set_facecolor("#050816")
ax.set_facecolor("#0B1026")

# -----------------------------
# CREATE GLOWING GRADIENT LINE
# -----------------------------
points = np.array([aar, kronekurs]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

norm = Normalize(kronekurs.min(), kronekurs.max())

# Main neon line
lc = LineCollection(
    segments,
    cmap="plasma",
    norm=norm,
    linewidth=4,
)
lc.set_array(kronekurs)
ax.add_collection(lc)

# Glow effect
for glow in [18, 14, 10]:
    glow_line = LineCollection(
        segments,
        cmap="plasma",
        norm=norm,
        linewidth=glow,
        alpha=0.05,
    )
    glow_line.set_array(kronekurs)
    ax.add_collection(glow_line)

# -----------------------------
# SCATTER POINTS
# -----------------------------
scatter = ax.scatter(
    aar,
    kronekurs,
    c=kronekurs,
    cmap="plasma",
    s=80,
    edgecolors="white",
    linewidths=0.7,
    zorder=10,
)

# -----------------------------
# TREND LINE
# -----------------------------
z = np.polyfit(aar, kronekurs, 1)
p = np.poly1d(z)

ax.plot(
    aar,
    p(aar),
    linestyle="--",
    linewidth=2.5,
    color="white",
    alpha=0.7,
    label="Trend",
)

# -----------------------------
# AREA GLOW
# -----------------------------
ax.fill_between(
    aar,
    kronekurs,
    kronekurs.min() - 1,
    color="#7A00FF",
    alpha=0.08,
)

# -----------------------------
# TITLES
# -----------------------------
ax.set_title(
    "KRONEKURS GJENNOM TID",
    fontsize=30,
    fontweight="bold",
    pad=25,
)

subtitle = (
    "En cinematisk visualisering av økonomisk utvikling"
)

fig.text(
    0.5,
    0.91,
    subtitle,
    ha="center",
    fontsize=14,
    alpha=0.7,
)

# -----------------------------
# AXIS STYLING
# -----------------------------
ax.set_xlabel("År", fontsize=16, labelpad=12)
ax.set_ylabel("Kronekurs", fontsize=16, labelpad=12)

ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)

# Remove ugly borders
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Stylish grid
ax.grid(
    True,
    linestyle="--",
    linewidth=0.5,
    alpha=0.15,
)

# Padding
ax.margins(x=0.02)

# -----------------------------
# COLORBAR
# -----------------------------
cbar = fig.colorbar(lc, ax=ax, pad=0.02)
cbar.set_label("Kronekurs Intensity", fontsize=13)

# -----------------------------
# WATERMARK
# -----------------------------
fig.text(
    0.99,
    0.02,
    "Generated with Python",
    ha="right",
    fontsize=10,
    alpha=0.4,
)

# -----------------------------
# SHOW
# -----------------------------
plt.tight_layout()
plt.show()