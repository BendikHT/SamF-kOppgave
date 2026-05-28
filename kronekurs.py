from pathlib import Path
import csv
from pprint import pprint
# pprint er "handy" om man skal printe ut mye data, f eks en stor ordbok
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate

# La oss bruke denne måten nå, så funker det uansett hvor man står og kjører programmet:
CURRENT_DIR = Path(__file__).parent
filnavn = CURRENT_DIR / "data/EXR.csv"

index = 1

kronekurs = []
aar = []

with open(filnavn, encoding="utf-8-sig") as fil:
    filinnhold = csv.reader(fil, delimiter=";")
    overskrifter = next(filinnhold)
    print(overskrifter)
    print("Antall overskrifter:", len(overskrifter))
    
    
    for rad in filinnhold:
        if len(rad) > index:
            aar.append(int(rad[14]))
            kronekurs.append(float(rad[15].replace(",", ".")))
            
print(aar)
print(kronekurs)

plt.style.use("dark_background")

fig, ax = plt.subplots(figsize=(14, 7))

# Gradient-ish line effect
for i in range(6, 0, -1):
    ax.plot(
        aar,
        kronekurs,
        linewidth=i * 2,
        alpha=0.05,
    )

# Hovedlinje
ax.plot(
    aar,
    kronekurs,
    linewidth=3,
    marker="o",
    markersize=5,
)

# Trendlinje
z = np.polyfit(aar, kronekurs, 1)
p = np.poly1d(z)

ax.plot(
    aar,
    p(aar),
    linestyle="--",
    linewidth=2,
    alpha=0.8,
    label="Trendlinje",
)

# Tittel og labels
ax.set_title(
    "Utvikling i Kronekurs over Tid",
    fontsize=24,
    pad=20,
    fontweight="bold",
)

ax.set_xlabel("År", fontsize=14)
ax.set_ylabel("Kronekurs", fontsize=14)

# Grid
ax.grid(True, linestyle="--", alpha=0.3)

# Fjerner stygge kanter
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Litt padding
ax.margins(x=0.02)

# Legende
ax.legend()

# Automatisk layout
plt.tight_layout()

# Vis plottet
plt.show()