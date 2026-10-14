"""Con-side visualizations (Alina) - DSC106 Project 2.
Proposition: "Access to abortion care in the United States is severely restricted."
This side argues: NO, not severely.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd

SURFACE   = "#fcfcfb"
INK       = "#0b0b0b"
INK_2     = "#52514e"
MUTED     = "#898781"
GRID      = "#e1e0d9"
BLUE      = "#2a78d6"
ORANGE    = "#eb345c"
EMPTY     = "#e1e0d9"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
})

df = pd.read_csv("abortion_clean.csv")
w = df.women_15_44_2020
pct_without = (df.pct_women_no_clinic_2020 * w).sum() / w.sum()
pct_with = 100 - pct_without


# ---------------------------------------------- figure 1
def fig1(path="con_1_hero.png"):
    fig = plt.figure(figsize=(9, 6.2))

    fig.text(0.065, 0.93, "Most American women live within reach of a clinic",
             fontsize=18, fontweight="bold", color=INK, va="top")

    fig.text(0.065, 0.80, f"{pct_with:.1f}%", fontsize=74,
             fontweight="bold", color=BLUE, va="top")
    fig.text(0.065, 0.545,
             "of U.S. women aged 15-44 live in a county\nthat has an abortion clinic",
             fontsize=13.5, color=INK_2, va="top", linespacing=1.5)

    #10x10 unit chart: each square = 1% of women aged 15-44
    ax = fig.add_axes([0.52, 0.22, 0.40, 0.58])
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax.set_aspect("equal"); ax.axis("off")
    filled = round(pct_with)
    for i in range(100):
        row, col = divmod(i, 10)
        ax.add_patch(Rectangle(
            (col + 0.06, 9 - row + 0.06), 0.88, 0.88,
            facecolor=BLUE if i < filled else EMPTY,
            edgecolor="none", linewidth=0))
    ax.text(5, -0.75, "each square = 1% of U.S. women aged 15–44",
            ha="center", fontsize=9.5, color=MUTED)

    fig.text(0.065, 0.085,
             "Population-weighted across all 50 states and DC. Guttmacher Institute, 2020.",
             fontsize=8.5, color=MUTED)
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("wrote", path, f"| hero = {pct_with:.1f}% | squares filled = {filled}")


# ---------------------------------------------------------------- figure 2
def fig2(path="con_2_gap.png", n=10):
    d = df.copy()
    d["gap"] = d.pct_counties_no_clinic_2020 - d.pct_women_no_clinic_2020
    d = d.nlargest(n, "gap").sort_values("gap")

    fig, ax = plt.subplots(figsize=(9, 6.2))
    y = range(len(d))

    for yi, (_, r) in zip(y, d.iterrows()):
        ax.plot([r.pct_women_no_clinic_2020, r.pct_counties_no_clinic_2020],
                [yi, yi], color=GRID, linewidth=2.5, zorder=1,
                solid_capstyle="round")
    ax.scatter(d.pct_counties_no_clinic_2020, y, s=130, color=ORANGE,
               zorder=3, label="Share of counties with no clinic",
               edgecolor=SURFACE, linewidth=2)
    ax.scatter(d.pct_women_no_clinic_2020, y, s=130, color=BLUE,
               zorder=3, label="Share of women with no clinic nearby",
               edgecolor=SURFACE, linewidth=2)

    for yi, (_, r) in zip(y, d.iterrows()):
        ax.text(r.pct_counties_no_clinic_2020 + 2.4, yi, f"{r.pct_counties_no_clinic_2020:.0f}%",
                va="center", fontsize=10, color=ORANGE, fontweight="bold")
        ax.text(r.pct_women_no_clinic_2020 - 2.4, yi, f"{r.pct_women_no_clinic_2020:.0f}%",
                va="center", ha="right", fontsize=10, color=BLUE, fontweight="bold")

    ax.set_yticks(list(y)); ax.set_yticklabels(d.state, fontsize=11, color=INK)
    ax.set_xlim(-12, 112)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=10, color=MUTED)
    ax.xaxis.grid(True, color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#c3c2b7")
    ax.tick_params(axis="y", length=0)

    ax.set_title("Counting counties overstates how many women lack access",
                 fontsize=16, fontweight="bold", color=INK, loc="left", pad=62)
    ax.text(0, 1.105,
            "Counties are mostly rural and nearly empty; women live in cities. "
            "The ten states where the two measures diverge most.",
            transform=ax.transAxes, fontsize=10.5, color=INK_2)
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.005), ncol=2, frameon=False,
              fontsize=10.5, labelcolor=INK_2, handletextpad=0.5, columnspacing=2.2)
    fig.text(0.012, 0.012, "Guttmacher Institute, 2020.", fontsize=8.5, color=MUTED)

    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("wrote", path, "| states:", ", ".join(d.state.tolist()[::-1]))


fig1(); fig2()
