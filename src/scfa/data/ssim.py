"""
Structural Self-Interaction Matrix (SSIM) — upper triangle only (i < j, 0-indexed).

Encoded from section 4.4 of the project report. Entries marked with
'O' for pairs not explicitly stated in the source table.

Symbols:
    V  — factor i influences factor j
    A  — factor j influences factor i
    X  — mutual influence
    O  — no relationship
"""

# Keys are (i, j) with i < j using 0-based indices (F1=0, ..., F11=10)
SSIM: dict[tuple[int, int], str] = {
    # F1 row
    (0, 1): "X",   # F1-F2
    (0, 2): "A",   # F1-F3: F3 drives F1
    (0, 3): "A",   # F1-F4: F4 drives F1
    (0, 4): "A",   # F1-F5: F5 drives F1
    (0, 5): "X",   # F1-F6
    (0, 6): "O",   # F1-F7
    (0, 7): "O",   # F1-F8
    (0, 8): "A",   # F1-F9: F9 drives F1
    (0, 9): "X",   # F1-F10
    (0, 10): "O",  # F1-F11 (inferred)

    # F2 row
    (1, 2): "X",   # F2-F3
    (1, 3): "A",   # F2-F4: F4 drives F2
    (1, 4): "A",   # F2-F5: F5 drives F2
    (1, 5): "X",   # F2-F6
    (1, 6): "A",   # F2-F7: F7 drives F2
    (1, 7): "A",   # F2-F8: F8 drives F2
    (1, 8): "A",   # F2-F9: F9 drives F2
    (1, 9): "O",   # F2-F10 (inferred)
    (1, 10): "O",  # F2-F11 (inferred)

    # F3 row
    (2, 3): "O",   # F3-F4
    (2, 4): "O",   # F3-F5
    (2, 5): "V",   # F3-F6: F3 drives F6
    (2, 6): "V",   # F3-F7: F3 drives F7
    (2, 7): "V",   # F3-F8: F3 drives F8
    (2, 8): "V",   # F3-F9: F3 drives F9
    (2, 9): "O",   # F3-F10
    (2, 10): "V",  # F3-F11: F3 drives F11

    # F4 row
    (3, 4): "X",   # F4-F5
    (3, 5): "V",   # F4-F6: F4 drives F6
    (3, 6): "V",   # F4-F7: F4 drives F7
    (3, 7): "X",   # F4-F8
    (3, 8): "V",   # F4-F9: F4 drives F9
    (3, 9): "V",   # F4-F10: F4 drives F10
    (3, 10): "V",  # F4-F11: F4 drives F11

    # F5 row
    (4, 5): "X",   # F5-F6
    (4, 6): "X",   # F5-F7
    (4, 7): "X",   # F5-F8
    (4, 8): "O",   # F5-F9
    (4, 9): "O",   # F5-F10 (inferred)
    (4, 10): "O",  # F5-F11 (inferred)

    # F6 row
    (5, 6): "A",   # F6-F7: F7 drives F6
    (5, 7): "O",   # F6-F8 (inferred)
    (5, 8): "O",   # F6-F9 (inferred)
    (5, 9): "O",   # F6-F10 (inferred)
    (5, 10): "O",  # F6-F11 (inferred)

    # F7 row
    (6, 7): "O",   # F7-F8 (inferred)
    (6, 8): "O",   # F7-F9 (inferred)
    (6, 9): "O",   # F7-F10 (inferred)
    (6, 10): "O",  # F7-F11 (inferred)

    # F8 row
    (7, 8): "O",   # F8-F9 (inferred)
    (7, 9): "O",   # F8-F10 (inferred)
    (7, 10): "O",  # F8-F11 (inferred)

    # F9 row
    (8, 9): "O",   # F9-F10 (inferred)
    (8, 10): "O",  # F9-F11 (inferred)

    # F10 row
    (9, 10): "A",  # F10-F11: F11 drives F10
}
