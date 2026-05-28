from pathlib import Path
import csv
import matplotlib.pyplot as plt

CURRENT_DIR = Path(__file__).parent
filnavn_csv = CURRENT_DIR / "data/IR.csv"

rente = {}

with open(filnavn_csv, encoding="utf-8-sig") as fil:
    filinnhold = csv.reader(fil, delimiter=";")
    overskrifter = next(filinnhold)

    for rad in filinnhold:
        rente[int(rad[11])] = float(rad[12].replace(",", "."))

# Data
x = list(rente.keys())
y = list(rente.values())

# Størrelse på figur
plt.figure(figsize=(12, 6))

# Plot linje
plt.plot(
    x,
    y,
    color="royalblue",
    linewidth=3,
    marker="o",
    markersize=6,
    label="Rente"
)

# Fyll området under grafen
plt.fill_between(x, y, color="skyblue", alpha=0.3)

# Overskrift og akser
plt.title("Renteutvikling", fontsize=22, fontweight="bold")
plt.xlabel("År", fontsize=14)
plt.ylabel("Rente (%)", fontsize=14)

# Rutenett
plt.grid(
    True,
    linestyle="--",
    alpha=0.6
)

# x-akse ved y = 0
plt.axhline(y=0, color="black", linewidth=1.5)

# Legende
plt.legend()

# Litt luft rundt grafen
plt.tight_layout()

# Vis graf
plt.show()