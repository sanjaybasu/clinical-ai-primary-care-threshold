#!/usr/bin/env python3
"""
Reproducible figures for "How Much Benefit Would Clinical Artificial Intelligence Need to
Match the Mortality Cost of Primary Care Loss, Without Widening Inequality? A Decision-Analytic
Threshold Analysis." Reads results/rederived_threshold_* and writes PNGs to figures/.
Colorblind-safe palette; legends below panels. Deterministic (reads fixed model outputs).

Usage: python3 make_figures.py
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
FIGURES = os.path.join(HERE, "figures")
os.makedirs(FIGURES, exist_ok=True)

CB = {"blue": "#0072B2", "orange": "#E69F00", "green": "#009E73",
      "red": "#D55E00", "grey": "#999999", "purple": "#CC79A7"}


def fig_shortfall():
    import json
    inp = json.load(open(os.path.join(HERE, "code", "inputs.json")))
    realized = inp["pcp_supply"]["decline_per_100k"]
    projected = round(inp["adequacy_sensitivity"]["shortage_per_100k"])
    fig, ax = plt.subplots(figsize=(5.8, 4.0))
    bars = ax.bar(["Realized, 2005-2015", "Projected, early 2030s"], [realized, projected],
                  color=[CB["blue"], CB["orange"]], width=0.6)
    for b, v in zip(bars, [realized, projected]):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.4, f"{v:g}", ha="center", fontsize=10)
    ax.set_ylabel("Primary care physician supply loss (per 100,000)")
    ax.set_ylim(0, projected * 1.25)
    ax.set_title("Primary care physician supply loss, realized and projected")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES, "figure1_shortfall.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig_required_by_reach():
    g = pd.read_csv(os.path.join(RESULTS, "rederived_threshold_reach_grid.csv"))
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    ax.plot(g["reach"], g["required_HR_to_offset"], color=CB["blue"], linewidth=2,
            label="required effect to match the benchmark")
    ax.axhline(0.94, color=CB["purple"], linestyle="-", linewidth=1.2, label="digital hypertension 0.94")
    ax.axhline(1.00, color=CB["red"], linestyle=":", linewidth=1.2, label="no effect 1.00")
    ax.axvline(0.20, color=CB["grey"], linestyle="--", linewidth=1.0, label="current high-vulnerability reach")
    ax.set_xlabel("Reach (fraction of the community served)")
    ax.set_ylabel("Required clinical AI hazard ratio")
    ax.set_xlim(0, 1.0); ax.set_ylim(0.90, 1.005)
    ax.set_title("Required clinical AI hazard ratio, by reach")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=2, fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES, "figure2_required_by_reach.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig_equity():
    by = pd.read_csv(os.path.join(RESULTS, "rederived_threshold_by_stratum.csv")).set_index("stratum")
    Dh = float(by.loc["high", "attributable_excess_per_1000"]); Dl = float(by.loc["low", "attributable_excess_per_1000"])
    eq = pd.read_csv(os.path.join(RESULTS, "rederived_threshold_equity.csv"))
    cross = float(eq[eq["demonstrated_tool"] == "digital_htn_transmitted"]["high_vuln_reach_needed_to_not_widen"].iloc[0])
    m_high, m_low, r_low, k = 9.6, 7.2, 0.40, (1 - 0.94)
    r = np.arange(0.05, 0.601, 0.005)
    prevented_high = m_high * r * k
    threshold = m_low * r_low * k + (Dh - Dl)
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    ax.plot(r, prevented_high, color=CB["blue"], linewidth=2, label="mortality prevented in high-vulnerability communities")
    ax.axhline(threshold, color=CB["orange"], linestyle="-", linewidth=1.4, label="level needed to not widen the difference")
    ax.axvline(cross, color=CB["green"], linestyle="--", linewidth=1.1, label=f"reach needed {cross:.2f}")
    ax.axvline(0.20, color=CB["grey"], linestyle="--", linewidth=1.0, label="current reach 0.20")
    ax.axvspan(0.05, cross, color=CB["red"], alpha=0.06)
    ax.set_xlabel("Reach in high-vulnerability communities")
    ax.set_ylabel("Mortality prevented per 1,000")
    ax.set_xlim(0.05, 0.60)
    ax.set_title("Mortality prevented, by reach in high-vulnerability communities")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=2, fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES, "figure3_equity.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig_required_psa():
    hr = np.load(os.path.join(RESULTS, "rederived_threshold_psa_draws.npy"))
    s = pd.read_csv(os.path.join(RESULTS, "rederived_threshold_summary.csv")).set_index("metric")["value"]
    med = float(s["required_HR_high_median"]); lo = float(s["required_HR_high_p2.5"]); hi = float(s["required_HR_high_p97.5"])
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    ax.hist(np.clip(hr, 0.9, 1.0), bins=60, color=CB["blue"], alpha=0.75, edgecolor="white", linewidth=0.3)
    ax.axvline(med, color=CB["blue"], linestyle="--", linewidth=1.4, label=f"required effect median {med:.3f}")
    ax.axvspan(lo, hi, color=CB["blue"], alpha=0.10, label=f"95% interval {lo:.3f}-{hi:.3f}")
    ax.axvline(0.94, color=CB["purple"], linestyle="-", linewidth=1.2, label="digital hypertension 0.94")
    ax.set_xlabel("Required clinical AI hazard ratio, high-vulnerability communities")
    ax.set_ylabel("Probabilistic draws")
    ax.set_xlim(0.90, 1.0)
    ax.set_title("Distribution of the required clinical AI hazard ratio (20,000 samples)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=2, fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES, "figure4_required_psa.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig_shortfall()
    fig_required_by_reach()
    fig_equity()
    fig_required_psa()
    print("Figures written:")
    for f in sorted(os.listdir(FIGURES)):
        if f.endswith(".png"):
            print(" ", os.path.join(FIGURES, f))
