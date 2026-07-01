"""Plotting utilities for ISM hierarchy and Fuzzy MICMAC classification."""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np


_CLUSTER_COLORS = {
    "Independent": "#2ecc71",
    "Linkage":     "#e67e22",
    "Dependent":   "#e74c3c",
    "Autonomous":  "#95a5a6",
}


def plot_driving_dependence(
    driving: np.ndarray,
    dependence: np.ndarray,
    labels: List[str],
    save_path: Optional[str] = None,
) -> Tuple[plt.Figure, plt.Axes]:
    """Scatter plot of driving vs. dependence power with MICMAC quadrant labels.

    Args:
        driving:    Row sums of stabilized FDRM.
        dependence: Column sums of stabilized FDRM.
        labels:     Factor label strings.
        save_path:  If given, saves the figure to this path at 150 dpi.

    Returns:
        (fig, ax)
    """
    fig, ax = plt.subplots(figsize=(11, 8))

    med_dep = np.median(dependence)
    med_drv = np.median(driving)

    point_colors = []
    for drv, dep in zip(driving, dependence):
        if drv >= med_drv and dep < med_dep:
            point_colors.append(_CLUSTER_COLORS["Independent"])
        elif drv >= med_drv and dep >= med_dep:
            point_colors.append(_CLUSTER_COLORS["Linkage"])
        elif drv < med_drv and dep >= med_dep:
            point_colors.append(_CLUSTER_COLORS["Dependent"])
        else:
            point_colors.append(_CLUSTER_COLORS["Autonomous"])

    ax.scatter(dependence, driving, c=point_colors, s=120, zorder=5,
               edgecolors="white", linewidths=0.5)

    for i, label in enumerate(labels):
        ax.annotate(label, (dependence[i], driving[i]),
                    textcoords="offset points", xytext=(8, 4), fontsize=8)

    ax.axhline(y=med_drv, color="#7f8c8d", linestyle="--", linewidth=0.8, alpha=0.7)
    ax.axvline(x=med_dep, color="#7f8c8d", linestyle="--", linewidth=0.8, alpha=0.7)

    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    dx = (xlim[1] - xlim[0]) * 0.02
    dy = (ylim[1] - ylim[0]) * 0.02

    ax.text(xlim[0] + dx, med_drv + dy, "INDEPENDENT\n(root causes)",
            fontsize=8, color=_CLUSTER_COLORS["Independent"], weight="bold", va="bottom")
    ax.text(med_dep + dx, med_drv + dy, "LINKAGE\n(critical nodes)",
            fontsize=8, color=_CLUSTER_COLORS["Linkage"], weight="bold", va="bottom")
    ax.text(xlim[0] + dx, ylim[0] + dy, "AUTONOMOUS\n(isolated)",
            fontsize=8, color=_CLUSTER_COLORS["Autonomous"], weight="bold", va="bottom")
    ax.text(med_dep + dx, ylim[0] + dy, "DEPENDENT\n(outcomes)",
            fontsize=8, color=_CLUSTER_COLORS["Dependent"], weight="bold", va="bottom")

    legend_patches = [
        mpatches.Patch(color=c, label=k) for k, c in _CLUSTER_COLORS.items()
    ]
    ax.legend(handles=legend_patches, loc="upper left", fontsize=9)

    ax.set_xlabel("Dependence Power", fontsize=12)
    ax.set_ylabel("Driving Power", fontsize=12)
    ax.set_title("Fuzzy MICMAC — Driving vs. Dependence Power Classification", fontsize=13)
    ax.grid(True, alpha=0.2)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig, ax


def plot_ism_hierarchy(
    levels: Dict[int, List[int]],
    labels: List[str],
    save_path: Optional[str] = None,
) -> Tuple[plt.Figure, plt.Axes]:
    """Layered box diagram of the ISM hierarchy.

    Args:
        levels:    Output of level_partition() — {level: [factor_indices]}.
        labels:    Factor label strings indexed by factor index.
        save_path: If given, saves the figure to this path at 150 dpi.

    Returns:
        (fig, ax)
    """
    n_levels = max(levels.keys())
    fig, ax = plt.subplots(figsize=(13, 2.2 * n_levels + 1))

    BOX_W, BOX_H = 2.6, 0.65
    H_GAP, V_GAP = 0.3, 0.9
    level_label = {
        1: "Level I — Outcomes",
        2: "Level II — Middle tier",
        3: "Level III — Root causes",
    }

    for lvl in sorted(levels.keys(), reverse=True):
        factors = levels[lvl]
        y = (n_levels - lvl) * (BOX_H + V_GAP)
        total_w = len(factors) * BOX_W + (len(factors) - 1) * H_GAP
        x0 = -total_w / 2

        ax.text(-7.2, y, level_label.get(lvl, f"Level {lvl}"),
                va="center", ha="left", fontsize=9, color="#7f8c8d")

        for k, fi in enumerate(factors):
            x = x0 + k * (BOX_W + H_GAP)
            rect = plt.Rectangle(
                (x, y - BOX_H / 2), BOX_W, BOX_H,
                linewidth=1, edgecolor="#2c3e50", facecolor="#ecf0f1", zorder=3,
            )
            ax.add_patch(rect)
            ax.text(x + BOX_W / 2, y, labels[fi],
                    ha="center", va="center", fontsize=7.5)

    ax.set_xlim(-7.5, 7.5)
    ax.set_ylim(-0.6, n_levels * (BOX_H + V_GAP) + 0.6)
    ax.axis("off")
    ax.set_title("ISM Hierarchical Model", fontsize=13, pad=10)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig, ax
