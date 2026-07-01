import numpy as np
import pytest

from scfa.ism import (
    driving_dependence,
    level_partition,
    ssim_to_reachability,
    transitive_closure,
)


# --- ssim_to_reachability ---

def test_v_symbol():
    R = ssim_to_reachability({(0, 1): "V"}, n=2)
    assert R[0, 1] == 1 and R[1, 0] == 0


def test_a_symbol():
    R = ssim_to_reachability({(0, 1): "A"}, n=2)
    assert R[0, 1] == 0 and R[1, 0] == 1


def test_x_symbol():
    R = ssim_to_reachability({(0, 1): "X"}, n=2)
    assert R[0, 1] == 1 and R[1, 0] == 1


def test_o_symbol():
    R = ssim_to_reachability({(0, 1): "O"}, n=2)
    assert R[0, 1] == 0 and R[1, 0] == 0


def test_diagonal_always_one():
    R = ssim_to_reachability({}, n=4)
    assert np.all(np.diag(R) == 1)


def test_unknown_symbol_raises():
    with pytest.raises(ValueError, match="Unknown SSIM symbol"):
        ssim_to_reachability({(0, 1): "Z"}, n=2)


# --- transitive_closure ---

def test_transitivity_infers_indirect_link():
    # 0 → 1 → 2, so closure must give 0 → 2
    R = np.array([[1, 1, 0],
                  [0, 1, 1],
                  [0, 0, 1]])
    assert transitive_closure(R)[0, 2] == 1


def test_transitivity_preserves_existing():
    R = np.array([[1, 1, 1],
                  [0, 1, 1],
                  [0, 0, 1]])
    Rt = transitive_closure(R)
    assert Rt[0, 1] == 1 and Rt[0, 2] == 1


def test_transitivity_idempotent():
    R = np.array([[1, 1, 0, 0],
                  [0, 1, 1, 0],
                  [0, 0, 1, 1],
                  [0, 0, 0, 1]])
    R1 = transitive_closure(R)
    R2 = transitive_closure(R1)
    assert np.array_equal(R1, R2)


def test_transitivity_no_change_when_already_closed():
    R = np.eye(3, dtype=int)  # no off-diagonal links
    assert np.array_equal(transitive_closure(R), R)


# --- level_partition ---

def test_level_partition_linear_chain():
    # 0 → 1 → 2 (after closure: 0 reaches 1,2; 1 reaches 2; 2 reaches only itself)
    R = np.array([[1, 1, 1],
                  [0, 1, 1],
                  [0, 0, 1]])
    levels = level_partition(R)
    assert 2 in levels[1]   # node 2 is the top (most dependent)
    assert 1 in levels[2]
    assert 0 in levels[3]


def test_level_partition_all_isolated():
    R = np.eye(3, dtype=int)
    levels = level_partition(R)
    # all factors have same reach=ante intersection, so all land in level 1
    assert set(levels[1]) == {0, 1, 2}


def test_level_partition_covers_all_factors():
    R = np.array([[1, 1, 0],
                  [0, 1, 1],
                  [0, 0, 1]])
    levels = level_partition(R)
    all_factors = {f for factors in levels.values() for f in factors}
    assert all_factors == {0, 1, 2}


# --- driving_dependence ---

def test_driving_power_is_row_sum():
    R = np.array([[1, 1, 0],
                  [0, 1, 1],
                  [1, 0, 1]])
    drv, _ = driving_dependence(R)
    np.testing.assert_array_equal(drv, [2, 2, 2])


def test_dependence_power_is_col_sum():
    R = np.array([[1, 1, 0],
                  [0, 1, 1],
                  [1, 0, 1]])
    _, dep = driving_dependence(R)
    np.testing.assert_array_equal(dep, [2, 2, 2])


# --- integration: SSIM → closure → partition ---

def test_full_pipeline_bdrm():
    """ssim_to_reachability + transitive_closure should reproduce the BDRM."""
    from scfa.data.bdrm import BDRM
    from scfa.data.ssim import SSIM

    R_init = ssim_to_reachability(SSIM, n=11)
    R_final = transitive_closure(R_init)

    # Every 1 in BDRM must be reachable in the final matrix
    rows, cols = np.where(BDRM == 1)
    for i, j in zip(rows, cols):
        assert R_final[i, j] == 1, (
            f"BDRM has F{i+1}→F{j+1}=1 but transitive closure gives 0"
        )
