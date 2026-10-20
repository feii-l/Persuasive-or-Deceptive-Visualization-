"""Con-side visualization (Alina) - DSC106 Project 2 final.
Proposition: "Access to abortion care in the United States is severely restricted."
This side argues: no, not severely.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd

SURFACE, INK, INK_2, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"
RULE, BLUE, EMPTY = "#e1e0d9", "#2a78d6", "#d8d7d0"

plt.rcParams.update({"font.family": "DejaVu Sans", "figure.facecolor": SURFACE,
                     "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE})

df = pd.read_csv("abortion_clean.csv")
w = df.women_15_44_2020
pct_with = 100 - (df.pct_women_no_clinic_2020 * w).sum() / w.sum()
pct_instate = 100 - (df.pct_traveled_out_of_state_2020 * w).sum() / w.sum()


def swatch(fig, x, y, color, label, size=0.016):
    fig.patches.append(Rectangle((x, y), size, size * 9 / 7.2,
                                 facecolor=color, edgecolor="none",
                                 transform=fig.transFigure, figure=fig))
    fig.text(x + size + 0.009, y + size * 9 / 15.2, label, fontsize=9.5,
             color=INK_2, va="center")


def build(path="con_1_hero.png"):
    fig = plt.figure(figsize=(9, 7.2))

    fig.text(0.065, 0.955, "Most American women live in a county that has a clinic",
             fontsize=17.5, fontweight="bold", color=INK, va="top")

    fig.text(0.065, 0.855, f"{pct_with:.1f}%", fontsize=66,
             fontweight="bold", color=BLUE, va="top")
    fig.text(0.065, 0.675,
             "of U.S. women aged 15–44 live in a county\n"
             "with at least one abortion clinic",
             fontsize=13, color=INK_2, va="top", linespacing=1.5)

    # 10x10 unit chart: each square = 1% of women aged 15-44
    ax = fig.add_axes([0.55, 0.50, 0.36, 0.42])
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.set_aspect("equal"); ax.axis("off")
    filled = round(pct_with)
    for i in range(100):
        row, col = divmod(i, 10)
        ax.add_patch(Rectangle((col + 0.07, 9 - row + 0.07), 0.86, 0.86,
                               facecolor=BLUE if i < filled else EMPTY,
                               edgecolor="none"))
    ax.text(5, -0.8, "each square = 1% of U.S. women aged 15–44",
            ha="center", fontsize=9, color=MUTED)

    swatch(fig, 0.55, 0.435, BLUE,  "lives in a county with a clinic")
    swatch(fig, 0.55, 0.395, EMPTY, "lives in a county with no clinic")

    fig.lines.append(plt.Line2D([0.065, 0.935], [0.325, 0.325], color=RULE,
                                linewidth=1, transform=fig.transFigure, figure=fig))

    fig.text(0.065, 0.285,
             "Having a clinic in the county is not the same as it being close by. "
             "Travel tells a similar story:",
             fontsize=11.5, color=INK, va="top")

    bar = fig.add_axes([0.065, 0.145, 0.66, 0.055])
    bar.set_xlim(0, 100); bar.set_ylim(0, 1); bar.axis("off")
    bar.add_patch(Rectangle((0, 0), pct_instate - 0.3, 1, facecolor=BLUE))
    bar.add_patch(Rectangle((pct_instate + 0.3, 0), 100 - pct_instate - 0.3, 1,
                            facecolor=EMPTY))
    bar.text(1.6, 0.5, f"{pct_instate:.0f}%  stayed in their own state",
             va="center", fontsize=11.5, color="white", fontweight="bold")
    bar.text(102.5, 0.5, f"{100 - pct_instate:.0f}%  crossed a state line",
             va="center", ha="left", fontsize=11.5, color=INK_2, clip_on=False)

    fig.text(0.065, 0.105,
             "Share of people who obtained an abortion in 2020, by whether they left their state for care.",
             fontsize=9, color=MUTED, va="top")

    fig.text(0.065, 0.045,
             "Guttmacher Institute, 2020. Both figures are weighted by state population.\n"
             "Note the two measures cover different groups: the 62.5% is all women aged 15–44; "
             "the 88% is only those who obtained an abortion.",
             fontsize=8.5, color=MUTED, va="top", linespacing=1.5)

    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {path} | hero={pct_with:.1f}% squares={filled} | in-state={pct_instate:.1f}%")


build()
