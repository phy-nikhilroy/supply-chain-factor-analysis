"""Interpretive Structural Modeling (ISM) algorithms."""

from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np


def ssim_to_reachability(ssim: Dict[Tuple[int, int], str], n: int) -> np.ndarray:
    """Build initial binary reachability matrix from upper-triangle SSIM entries.

    Args:
        ssim: Dict mapping (i, j) with i < j to one of {'V', 'A', 'X', 'O'}.
        n:    Number of factors.

    Returns:
        (n, n) integer array with diagonal = 1 and off-diagonal from SSIM rules:
            V → R[i,j]=1, R[j,i]=0
            A → R[i,j]=0, R[j,i]=1
            X → R[i,j]=1, R[j,i]=1
            O → R[i,j]=0, R[j,i]=0
    """
    R = np.eye(n, dtype=int)
    for (i, j), sym in ssim.items():
        if sym == "V":
            R[i, j] = 1
        elif sym == "A":
            R[j, i] = 1
        elif sym == "X":
            R[i, j] = R[j, i] = 1
        elif sym != "O":
            raise ValueError(f"Unknown SSIM symbol: {sym!r}")
    return R


def transitive_closure(R: np.ndarray) -> np.ndarray:
    """Apply transitivity to produce the Final Reachability Matrix.

    Uses Floyd-Warshall: if R[i,k]=1 and R[k,j]=1 then R[i,j]=1.
    """
    R = R.copy().astype(bool)
    n = R.shape[0]
    for k in range(n):
        R |= np.outer(R[:, k], R[k, :])
    return R.astype(int)


def level_partition(R: np.ndarray) -> Dict[int, List[int]]:
    """Assign factors to ISM hierarchy levels by iterative elimination.

    A factor is assigned to the current level when its reachability set
    equals the intersection of its reachability and antecedent sets.
    Level I (top) contains the most dependent factors (visible outcomes);
    the bottom level contains the root driving factors.

    Args:
        R: Final Reachability Matrix (after transitive closure), shape (n, n).

    Returns:
        Dict mapping level number (1 = top) to list of 0-based factor indices.
    """
    remaining = list(range(R.shape[0]))
    levels: Dict[int, List[int]] = {}
    level = 1

    while remaining:
        level_factors = []
        for i in remaining:
            reach = {j for j in remaining if R[i, j] == 1}
            ante  = {j for j in remaining if R[j, i] == 1}
            if reach == reach & ante:
                level_factors.append(i)

        if not level_factors:
            # Cycle or malformed matrix — assign all remaining to current level
            levels[level] = remaining[:]
            break

        levels[level] = level_factors
        remaining = [f for f in remaining if f not in level_factors]
        level += 1

    return levels


def driving_dependence(R: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Compute driving power (row sums) and dependence power (column sums)."""
    return R.sum(axis=1), R.sum(axis=0)
