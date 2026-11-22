# Re-creates the paper's original Fig. 2 design (notebook style: colors, hatches, line styles, DejaVu Sans).
# Only change from the original figure: the metric label "LASR" is shown as "OPER" (Oracle-PERMIT Execution Rate).
# Usage: python make_paper_fig2.py <results_dir> <output_stem>
import sys, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib as mpl, matplotlib.pyplot as plt
R, out = sys.argv[1], sys.argv[2]
mpl.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white",
    "font.family": "DejaVu Sans", "font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9,
    "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 8,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": False})
C = {"Direct Execution": "#4D4D4D", "Static Authorization": "#4C78A8", "AC-AZT": "#009E73",
     "danger": "#D55E00", "amber": "#E69F00", "safe": "#009E73", "blue": "#0072B2"}
ms = pd.read_csv(f"{R}/metric_summary.csv").set_index("Method")
ab = pd.read_csv(f"{R}/ablation_results.csv").set_index("Configuration")
th = pd.read_csv(f"{R}/threshold_sensitivity.csv")
fig, axs = plt.subplots(1, 3, figsize=(11.5, 2.45), gridspec_kw={"wspace": .42})
# (a)
ax = axs[0]; mets = ["LASR", "UAR", "ASR"]; labs = ["OPER ↑", "UAR ↓", "ASR ↓"]
x = np.arange(3); w = .24
for j, (m, n) in enumerate([("Direct Execution", "Direct"), ("Static Authorization", "Static"), ("AC-AZT", "AC-AZT")]):
    v = 100 * ms.loc[m, mets].astype(float).values
    bars = ax.bar(x + (j - 1) * w, v, w, label=n, color=C[m], edgecolor="black", linewidth=.5, hatch=["//", "..", "xx"][j], alpha=.92)
    for b, val in zip(bars, v):
        if val > 0:
            ax.text(b.get_x() + b.get_width() / 2, val + 1.5, f"{val:.1f}", ha="center", va="bottom", fontsize=6.5, rotation=90 if val > 80 else 0)
ax.set_xticks(x, labs); ax.set_ylim(0, 112); ax.set_ylabel("Rate (%)"); ax.set_title("(a) Safety and utility")
ax.legend(ncol=3, frameon=False, loc="upper center", bbox_to_anchor=(.5, -.17))
# (b)
order = ["Full AC-AZT", "− Hard rules", "− Contextual risk", "− Scope bounding", "− Freshness check", "− Verification"]
short = ["Full", "No hard", "No risk", "No scope", "No fresh.", "No verify"]
ab = ab.loc[order]; ax = axs[1]; x = np.arange(6); w = .36
for j, (k, n, col, h) in enumerate([("UAR", "UAR ↓", C["danger"], "/"), ("FailedEffectCommitRate", "Failed commit ↓", C["blue"], ".")]):
    v = 100 * ab[k].astype(float).values
    bars = ax.bar(x + (j - .5) * w, v, w, label=n, color=col, edgecolor="black", linewidth=.45, hatch=h)
    for b, val in zip(bars, v):
        if val > 0:
            ax.text(b.get_x() + b.get_width() / 2, val + .6, f"{val:.1f}", ha="center", va="bottom", fontsize=6.5)
ax.set_xticks(x, short, rotation=30, ha="right"); ax.set_ylabel("Rate (%)"); ax.set_title("(b) Control ablation")
ax.legend(ncol=2, frameon=False, loc="upper center", bbox_to_anchor=(.5, -.30))
# (c)
ax = axs[2]
for k, (col, mk, ls, lab) in {"LASR": (C["safe"], "o", "-", "OPER ↑"), "UAR": (C["danger"], "s", "--", "UAR ↓"),
                             "FER": (C["amber"], "^", ":", "FER ↓")}.items():
    ax.plot(th["threshold"], 100 * th[k], color=col, marker=mk, ls=ls, lw=1.6, ms=4.5, label=lab)
ax.axvline(0.45, color="#555555", lw=.9, ls="-.", label="Default")
ax.set_xlabel("Permit threshold"); ax.set_ylabel("Rate (%)"); ax.set_ylim(-3, 105); ax.set_title("(c) Threshold sensitivity")
ax.legend(frameon=False, ncol=2, loc="center right")
fig.savefig(out + ".pdf", bbox_inches="tight"); fig.savefig(out + ".png", dpi=400, bbox_inches="tight")
