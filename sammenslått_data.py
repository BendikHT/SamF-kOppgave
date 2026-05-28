from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize


CURRENT_DIR = Path(__file__).parent

# ================================================
# FELLES STIL-KONFIGURASJON
# ================================================

STYLE = {
    "fig_facecolor": "#050816",
    "ax_facecolor": "#0B1026",
    "figsize": (16, 9),
    "line_width": 4,
    "glow_layers": [18, 14, 10],
    "glow_alpha": 0.05,
    "scatter_size": 80,
    "scatter_edge_color": "white",
    "scatter_edge_width": 0.7,
    "trend_width": 2.5,
    "trend_alpha": 0.6,
    "area_alpha": 0.07,
    "title_fontsize": 30,
    "subtitle_fontsize": 14,
    "subtitle_alpha": 0.7,
    "label_fontsize": 16,
    "label_pad": 12,
    "tick_fontsize": 12,
    "colorbar_fontsize": 13,
    "watermark_fontsize": 10,
    "watermark_alpha": 0.4,
    "grid_alpha": 0.15,
    "grid_linewidth": 0.5,
    "margins_x": 0.02,
    # Per-datasett fargevalg
    "kronekurs": {
        "cmap": "plasma",
        "area_color": "#7A00FF",
        "trend_color": "#FF88FF",
        "label_color": "#FF88FF",
    },
    "rente": {
        "cmap": "cool",
        "area_color": "#00AAFF",
        "trend_color": "#88FFFF",
        "label_color": "#88FFFF",
    },
}


def teikn_datasett(ax, x, y, cfg):
    """
    Teiknar gradient-linje, glow, scatter, trendlinje og areal på ein gitt akse.
    Returnerer LineCollection (for colorbar).
    """
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    norm = Normalize(y.min(), y.max())

    # Hovudlinje
    lc = LineCollection(segments, cmap=cfg["cmap"], norm=norm, linewidth=STYLE["line_width"])
    lc.set_array(y)
    ax.add_collection(lc)

    # Glow
    for glow_w in STYLE["glow_layers"]:
        glow = LineCollection(segments, cmap=cfg["cmap"], norm=norm,
                              linewidth=glow_w, alpha=STYLE["glow_alpha"])
        glow.set_array(y)
        ax.add_collection(glow)

    # Scatter
    ax.scatter(x, y, c=y, cmap=cfg["cmap"], norm=norm,
               s=STYLE["scatter_size"],
               edgecolors=STYLE["scatter_edge_color"],
               linewidths=STYLE["scatter_edge_width"],
               zorder=10)

    # Trendlinje
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    ax.plot(x, p(x), linestyle="--", linewidth=STYLE["trend_width"],
            color=cfg["trend_color"], alpha=STYLE["trend_alpha"])

    # Areal-glow
    ax.fill_between(x, y, y.min() - 1,
                    color=cfg["area_color"], alpha=STYLE["area_alpha"])

    ax.margins(x=STYLE["margins_x"])
    return lc


# ================================================
# LES DATA
# ================================================

rente = {}
with open(CURRENT_DIR / "data/IR.csv", encoding="utf-8-sig") as fil:
    filinnhold = csv.reader(fil, delimiter=";")
    next(filinnhold)
    for rad in filinnhold:
        rente[int(rad[11])] = float(rad[12].replace(",", "."))

rente_x = np.array(list(rente.keys()))
rente_y = np.array(list(rente.values()))

aar = []
kronekurs = []
with open(CURRENT_DIR / "data/EXR.csv", encoding="utf-8-sig") as fil:
    filinnhold = csv.reader(fil, delimiter=";")
    next(filinnhold)
    for rad in filinnhold:
        try:
            aar.append(int(rad[14]))
            kronekurs.append(float(rad[15].replace(",", ".")))
        except Exception:
            pass

kurs_x = np.array(aar)
kurs_y = np.array(kronekurs)


# ================================================
# BYGG KOMBINERT GRAF MED TO Y-AKSER
# ================================================

plt.style.use("dark_background")

fig, ax1 = plt.subplots(figsize=STYLE["figsize"])
fig.patch.set_facecolor(STYLE["fig_facecolor"])
ax1.set_facecolor(STYLE["ax_facecolor"])

# Andre y-akse deler x-aksen
ax2 = ax1.twinx()
ax2.set_facecolor("none")          # gjennomsiktig – viser ax1 sin bakgrunn

# --- Teikn begge datasett ---
lc_kurs  = teikn_datasett(ax1, kurs_x,  kurs_y,  STYLE["kronekurs"])
lc_rente = teikn_datasett(ax2, rente_x, rente_y, STYLE["rente"])

# --- Akseetiketter med matchande fargar ---
kurs_cfg  = STYLE["kronekurs"]
rente_cfg = STYLE["rente"]

ax1.set_xlabel("År", fontsize=STYLE["label_fontsize"], labelpad=STYLE["label_pad"])
ax1.set_ylabel("Kronekurs",       fontsize=STYLE["label_fontsize"],
               labelpad=STYLE["label_pad"], color=kurs_cfg["label_color"])
ax2.set_ylabel("Styringsrente (%)", fontsize=STYLE["label_fontsize"],
               labelpad=STYLE["label_pad"], color=rente_cfg["label_color"])

ax1.tick_params(axis="y", labelsize=STYLE["tick_fontsize"], colors=kurs_cfg["label_color"])
ax2.tick_params(axis="y", labelsize=STYLE["tick_fontsize"], colors=rente_cfg["label_color"])
ax1.tick_params(axis="x", labelsize=STYLE["tick_fontsize"])

# --- Rutenett og rammer (berre ax1 teiknar grid) ---
ax1.spines["top"].set_visible(False)
ax2.spines["top"].set_visible(False)
ax1.spines["right"].set_color(rente_cfg["label_color"])
ax2.spines["right"].set_color(rente_cfg["label_color"])
ax1.spines["left"].set_color(kurs_cfg["label_color"])

ax1.grid(True, linestyle="--", linewidth=STYLE["grid_linewidth"], alpha=STYLE["grid_alpha"])

# --- Titler ---
ax1.set_title(
    "KRONEKURS OG STYRINGSRENTE GJENNOM TID",
    fontsize=STYLE["title_fontsize"],
    fontweight="bold",
    pad=25,
)
fig.text(
    0.5, 0.91,
    "En cinematisk visualisering av kronekurs (plasma) og styringsrente (cool)",
    ha="center",
    fontsize=STYLE["subtitle_fontsize"],
    alpha=STYLE["subtitle_alpha"],
)

# --- Fargebarar --

plt.tight_layout()
plt.show()