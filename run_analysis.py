#!/usr/bin/env python3
"""Run the complete ISM + Fuzzy MICMAC supply chain analysis pipeline."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import numpy as np

from scfa.data.bdrm import BDRM
from scfa.data.factors import FACTOR_LABELS, FACTOR_NAMES
from scfa.data.fdrm import FDRM
from scfa.fuzzy_micmac import classify_clusters, stabilize
from scfa.ism import driving_dependence, level_partition
from scfa.visualization import plot_driving_dependence, plot_ism_hierarchy

os.makedirs("results", exist_ok=True)

# ── ISM analysis ─────────────────────────────────────────────────────────────
print("=" * 60)
print("ISM ANALYSIS")
print("=" * 60)

drv_b, dep_b = driving_dependence(BDRM)
print(f"\n{'Factor':<22} {'Driving':>8} {'Dependence':>12}")
print("-" * 44)
for i, label in enumerate(FACTOR_LABELS):
    print(f"{label:<22} {drv_b[i]:>8} {dep_b[i]:>12}")

levels = level_partition(BDRM)
print("\nISM Hierarchy:")
for lvl in sorted(levels.keys(), reverse=True):
    names = [FACTOR_LABELS[f] for f in levels[lvl]]
    tag = {1: "Outcomes", 2: "Middle", 3: "Root causes"}.get(lvl, "")
    print(f"  Level {lvl} ({tag}): {', '.join(names)}")

fig_ism, _ = plot_ism_hierarchy(levels, FACTOR_LABELS,
                                 save_path="results/ism_hierarchy.png")
print("\nSaved: results/ism_hierarchy.png")

# ── Fuzzy MICMAC ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("FUZZY MICMAC")
print("=" * 60)

stabilized, iters = stabilize(FDRM)
print(f"\nConverged in {iters} iteration(s)")

drv = stabilized.sum(axis=1)
dep = stabilized.sum(axis=0)

print(f"\n{'Factor':<22} {'Driving':>10} {'Dependence':>12}")
print("-" * 46)
for i, label in enumerate(FACTOR_LABELS):
    print(f"{label:<22} {drv[i]:>10.2f} {dep[i]:>12.2f}")

clusters = classify_clusters(drv, dep, FACTOR_LABELS)
print("\nCluster classification:")
for cluster, factors in clusters.items():
    print(f"  {cluster:<14}: {', '.join(factors) if factors else '(none)'}")

fig_micmac, _ = plot_driving_dependence(drv, dep, FACTOR_LABELS,
                                         save_path="results/driving_dependence.png")
print("\nSaved: results/driving_dependence.png")
