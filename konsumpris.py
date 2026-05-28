from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
import matplotlib.patheffects as pe

# -----------------------------
# LOAD DATA
# -----------------------------
CURRENT_DIR = Path(__file__).parent
filnavn = CURRENT_DIR / "data/konsumpris.csv"

aar = []
kpi = []

with open(filnavn, encoding="utf-8-sig") as fil:
    filinnhold = csv.reader(fil, delimiter=";")
    next(filinnhold)

    for rad in filinnhold:
        try:
            aarstall = int(rad[0])
            verdi = float(rad[1].replace(",", "."))

            if 1996 <= aarstall <= 2025:
                aar.append(aarstall)
                kpi.append(verdi)
        except:
            pass

aar = np.array(aar)
kpi = np.array(kpi)

# Sorter data
sortering = np.argsort(aar)
aar = aar[sortering]
kpi = kpi[sortering]

# -----------------------------
# FIGURE SETUP
# -----------------------------
plt.style.use("dark_background")

fig, ax = plt.subplots(figsize=(18, 10))
fig.patch.set_facecolor("#020617")
ax.set_facecolor("#020617")

# -----------------------------
# BACKGROUND GRADIENT
# -----------------------------
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))

ax.imshow(
    gradient,
    extent=[1995, 2026, kpi.min() - 8, kpi.max() + 10],
    aspect="auto",
    cmap="magma",
    alpha=0.18,
    zorder=0
)

# -----------------------------
# GRADIENT LINE
# -----------------------------
points = np.array([aar, kpi]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

norm = Normalize(kpi.min(), kpi.max())

# Glow layers
for linewidth, alpha in [(30, 0.035), (22, 0.05), (14, 0.08), (8, 0.13)]:
    glow = LineCollection(
        segments,
        cmap="plasma",
        norm=norm,
        linewidth=linewidth,
        alpha=alpha,
        zorder=2
    )
    glow.set_array(kpi)
    ax.add_collection(glow)

# Main line
line = LineCollection(
    segments,
    cmap="plasma",
    norm=norm,
    linewidth=5,
    zorder=5
)
line.set_array(kpi)
ax.add_collection(line)

# -----------------------------
# SCATTER POINTS
# -----------------------------
ax.scatter(
    aar,
    kpi,
    c=kpi,
    cmap="plasma",
    s=95,
    edgecolors="white",
    linewidths=1,
    zorder=10
)

# -----------------------------
# AREA UNDER LINE
# -----------------------------
ax.fill_between(
    aar,
    kpi,
    kpi.min() - 8,
    color="#9333EA",
    alpha=0.13,
    zorder=1
)

# -----------------------------
# TREND LINE
# -----------------------------
z = np.polyfit(aar, kpi, 1)
p = np.poly1d(z)

ax.plot(
    aar,
    p(aar),
    linestyle="--",
    linewidth=2.5,
    color="white",
    alpha=0.55,
    zorder=4
)

# -----------------------------
# HIGHLIGHT START AND END
# -----------------------------
ax.scatter(aar[0], kpi[0], s=260, color="#22D3EE", edgecolors="white", linewidths=2, zorder=15)
ax.scatter(aar[-1], kpi[-1], s=300, color="#FACC15", edgecolors="white", linewidths=2, zorder=15)

ax.annotate(
    f"Start: {aar[0]}\nKPI {kpi[0]:.1f}",
    xy=(aar[0], kpi[0]),
    xytext=(aar[0] + 1.2, kpi[0] + 6),
    arrowprops=dict(arrowstyle="->", color="white", lw=1.5),
    fontsize=13,
    color="white",
    zorder=20
)

ax.annotate(
    f"2025\nKPI {kpi[-1]:.1f}",
    xy=(aar[-1], kpi[-1]),
    xytext=(aar[-1] - 6, kpi[-1] - 8),
    arrowprops=dict(arrowstyle="->", color="white", lw=1.5),
    fontsize=15,
    color="white",
    fontweight="bold",
    zorder=20
)

# -----------------------------
# BIG NUMBER
# -----------------------------
økning = ((kpi[-1] - kpi[0]) / kpi[0]) * 100

big_text = ax.text(
    1997,
    kpi.max() + 4,
    f"+{økning:.0f}%",
    fontsize=58,
    fontweight="bold",
    color="#FACC15",
    alpha=0.95
)

big_text.set_path_effects([
    pe.withStroke(linewidth=6, foreground="#7C2D12")
])

ax.text(
    1997,
    kpi.max() + 1,
    "økning i KPI fra 1996 til 2025",
    fontsize=16,
    color="white",
    alpha=0.75
)

# -----------------------------
# TITLES
# -----------------------------
title = ax.set_title(
    "KPI I NORGE 1996–2025",
    fontsize=34,
    fontweight="bold",
    pad=30,
    color="white"
)

title.set_path_effects([
    pe.withStroke(linewidth=5, foreground="#7E22CE")
])

fig.text(
    0.5,
    0.91,
    "En neon-inspirert visualisering av prisvekst over tid",
    ha="center",
    fontsize=15,
    alpha=0.75,
    color="white"
)

# -----------------------------
# AXIS STYLING
# -----------------------------
ax.set_xlabel("År", fontsize=16, labelpad=14)
ax.set_ylabel("KPI årsgjennomsnitt", fontsize=16, labelpad=14)

ax.set_xlim(1995.5, 2025.5)
ax.set_ylim(kpi.min() - 8, kpi.max() + 10)

ax.tick_params(axis="x", labelsize=12, colors="white")
ax.tick_params(axis="y", labelsize=12, colors="white")

ax.set_xticks(np.arange(1996, 2026, 2))

ax.grid(
    True,
    linestyle="--",
    linewidth=0.6,
    alpha=0.18
)

for spine in ax.spines.values():
    spine.set_visible(False)

# -----------------------------
# COLORBAR
# -----------------------------
cbar = fig.colorbar(line, ax=ax, pad=0.015)
cbar.set_label("KPI-nivå", fontsize=13)
cbar.ax.tick_params(labelsize=11)

# -----------------------------
# WATERMARK
# -----------------------------
fig.text(
    0.99,
    0.02,
    "Generated with Python",
    ha="right",
    fontsize=10,
    alpha=0.35,
    color="white"
)

plt.tight_layout()
plt.show()