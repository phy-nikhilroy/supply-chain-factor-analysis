"""Fuzzy MICMAC algorithms: max-min composition, stabilization, cluster classification."""

from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np


def fuzzy_multiply(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """Fuzzy matrix multiplication via max-min composition.

    C[i, j] = max_k { min(A[i, k], B[k, j]) }

    Vectorized using broadcasting:
        A reshaped to (n, n, 1) — axis 0=i, axis 1=k
        B reshaped to (1, n, n) — axis 1=k, axis 2=j
        element-wise min then max over axis 1 (k)
    """
    return np.max(np.minimum(A[:, :, np.newaxis], B[np.newaxis, :, :]), axis=1)


def stabilize(
    fdrm: np.ndarray,
    max_iter: int = 100,
) -> Tuple[np.ndarray, int]:
    """Iteratively multiply the FDRM until driving/dependence rankings stabilize.

    At each step the current matrix is multiplied by the original FDRM using
    max-min composition. Convergence is declared when the rank ordering of
    both row sums (driving power) and column sums (dependence power) is
    unchanged from the previous iteration.

    Args:
        fdrm:     Fuzzy Direct Reachability Matrix, shape (n, n).
        max_iter: Hard ceiling on iterations.

    Returns:
        (stabilized_matrix, iteration_count)
    """
    current = fdrm.copy()
    prev_drv: tuple | None = None
    prev_dep: tuple | None = None

    for it in range(1, max_iter + 1):
        nxt = fuzzy_multiply(current, fdrm)
        drv = tuple(np.argsort(np.argsort(-nxt.sum(axis=1))))
        dep = tuple(np.argsort(np.argsort(-nxt.sum(axis=0))))

        if drv == prev_drv and dep == prev_dep:
            return nxt, it

        prev_drv, prev_dep = drv, dep
        current = nxt

    return current, max_iter


def classify_clusters(
    driving: np.ndarray,
    dependence: np.ndarray,
    labels: List[str],
) -> Dict[str, List[str]]:
    """Classify factors into the four MICMAC strategic clusters.

    Quadrant boundaries are set at the median of each power dimension:

        Independent — high driving, low dependence  (root causes)
        Linkage     — high driving, high dependence (critical nodes)
        Dependent   — low driving,  high dependence (visible outcomes)
        Autonomous  — low driving,  low dependence  (isolated factors)

    Args:
        driving:    Driving power array (row sums of stabilized matrix).
        dependence: Dependence power array (column sums of stabilized matrix).
        labels:     Factor label strings, same order as driving/dependence.

    Returns:
        Dict mapping cluster name to list of factor labels in that cluster.
    """
    med_drv = np.median(driving)
    med_dep = np.median(dependence)

    clusters: Dict[str, List[str]] = {
        "Independent": [],
        "Linkage": [],
        "Dependent": [],
        "Autonomous": [],
    }
    for label, drv, dep in zip(labels, driving, dependence):
        hi_drv = drv >= med_drv
        hi_dep = dep >= med_dep
        if hi_drv and not hi_dep:
            clusters["Independent"].append(label)
        elif hi_drv and hi_dep:
            clusters["Linkage"].append(label)
        elif not hi_drv and hi_dep:
            clusters["Dependent"].append(label)
        else:
            clusters["Autonomous"].append(label)

    return clusters
