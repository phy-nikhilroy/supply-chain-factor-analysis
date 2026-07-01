"""
Binary Direct Reachability Matrix (BDRM) — section 5.4 of project report.

This is the Final Reachability Matrix (transitivity already applied) used
as input to the Fuzzy MICMAC stage. Rows and columns are ordered F1–F11.
"""

import numpy as np

BDRM = np.array(
    [
        #  F1  F2  F3  F4  F5  F6  F7  F8  F9  F10 F11
        [1,  1,  0,  0,  0,  0,  0,  0,  0,  1,  1],  # F1   driving=4
        [1,  1,  1,  0,  0,  1,  0,  0,  1,  1,  0],  # F2   driving=6
        [1,  1,  1,  1,  0,  0,  1,  1,  1,  0,  0],  # F3   driving=7
        [1,  0,  0,  1,  0,  1,  1,  1,  0,  0,  1],  # F4   driving=6
        [0,  0,  0,  1,  1,  1,  1,  1,  0,  0,  1],  # F5   driving=6
        [0,  0,  0,  0,  0,  1,  0,  0,  0,  1,  1],  # F6   driving=3
        [0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  1],  # F7   driving=2
        [0,  0,  0,  0,  0,  0,  0,  1,  0,  1,  1],  # F8   driving=3
        [1,  1,  0,  0,  1,  1,  0,  0,  1,  0,  0],  # F9   driving=5
        [0,  1,  0,  0,  0,  0,  0,  0,  0,  1,  0],  # F10  driving=2
        [1,  1,  1,  1,  1,  1,  1,  1,  1,  0,  1],  # F11  driving=10
    ],
    dtype=int,
)
