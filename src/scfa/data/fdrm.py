"""
Fuzzy Direct Reachability Matrix (FDRM) — section 5.5 of project report.

Binary relationships from the BDRM are replaced with fuzzy possibility
values based on each factor's driving power:

    0   = No possibility
    0.1 = Very low
    0.3 = Low
    0.5 = Medium
    0.7 = High
    0.9 = Very high
    1.0 = Complete

Note: some cell values in the original report were embedded in figures
and could not be extracted from the PDF. Cells marked with a comment
are inferred from the published row/column driving-power constraints.
"""

import numpy as np

FDRM = np.array(
    [
        #   F1    F2    F3    F4    F5    F6    F7    F8    F9   F10   F11
        [0.0,  1.0,  0.9,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0],  # F1
        [1.0,  0.0,  0.0,  0.0,  0.0,  0.3,  0.0,  0.0,  1.0,  1.0,  1.0],  # F2
        [0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.3,  1.0,  1.0,  0.3],  # F3
        [0.0,  0.9,  0.0,  0.0,  0.9,  1.0,  0.0,  0.0,  0.9,  0.0,  0.0],  # F4
        [0.0,  0.0,  0.9,  0.0,  0.0,  1.0,  1.0,  0.0,  0.7,  0.0,  0.0],  # F5
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.9,  0.0,  0.0,  0.0,  0.0,  0.0],  # F6
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.7,  0.0,  0.0,  0.0,  0.9],  # F7
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.5,  0.0,  1.0,  1.0],  # F8
        [0.9,  0.5,  0.0,  0.0,  0.7,  0.9,  0.0,  0.0,  0.0,  0.0,  0.0],  # F9
        [0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.9,  0.0,  0.0,  0.0,  0.0],  # F10
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.3,  0.0],  # F11
    ],
    dtype=float,
)
