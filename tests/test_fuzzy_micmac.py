import numpy as np
import pytest

from scfa.fuzzy_micmac import classify_clusters, fuzzy_multiply, stabilize


# --- fuzzy_multiply ---

def test_known_result():
    """Manually computed 2×2 max-min product."""
    A = np.array([[0.5, 0.3],
                  [0.1, 0.9]])
    B = np.array([[0.4, 0.7],
                  [0.8, 0.2]])
    # C[0,0] = max(min(0.5,0.4), min(0.3,0.8)) = max(0.4, 0.3) = 0.4
    # C[0,1] = max(min(0.5,0.7), min(0.3,0.2)) = max(0.5, 0.2) = 0.5
    # C[1,0] = max(min(0.1,0.4), min(0.9,0.8)) = max(0.1, 0.8) = 0.8
    # C[1,1] = max(min(0.1,0.7), min(0.9,0.2)) = max(0.1, 0.2) = 0.2
    expected = np.array([[0.4, 0.5],
                          [0.8, 0.2]])
    np.testing.assert_array_almost_equal(fuzzy_multiply(A, B), expected)


def test_identity_matrix_is_neutral():
    """Multiplying by true identity leaves the matrix unchanged."""
    I = np.eye(3)
    A = np.array([[0.5, 0.3, 0.0],
                  [0.0, 0.7, 0.4],
                  [0.2, 0.0, 0.9]])
    np.testing.assert_array_almost_equal(fuzzy_multiply(A, I), A)
    np.testing.assert_array_almost_equal(fuzzy_multiply(I, A), A)


def test_output_values_in_unit_interval():
    rng = np.random.default_rng(0)
    A = rng.random((6, 6))
    B = rng.random((6, 6))
    C = fuzzy_multiply(A, B)
    assert C.min() >= 0.0 and C.max() <= 1.0


def test_zero_matrix_gives_zero():
    Z = np.zeros((4, 4))
    np.testing.assert_array_equal(fuzzy_multiply(Z, Z), Z)


def test_associativity_holds():
    """(A·B)·C == A·(B·C) under max-min composition."""
    rng = np.random.default_rng(1)
    A = rng.random((4, 4))
    B = rng.random((4, 4))
    C = rng.random((4, 4))
    lhs = fuzzy_multiply(fuzzy_multiply(A, B), C)
    rhs = fuzzy_multiply(A, fuzzy_multiply(B, C))
    np.testing.assert_array_almost_equal(lhs, rhs)


# --- stabilize ---

def test_returns_correct_types():
    A = np.array([[0.0, 0.9], [0.5, 0.0]])
    result, it = stabilize(A)
    assert isinstance(result, np.ndarray)
    assert isinstance(it, int) and it >= 1


def test_max_iter_is_hard_ceiling():
    A = np.full((3, 3), 0.5)
    _, it = stabilize(A, max_iter=4)
    assert it <= 4


def test_stabilized_output_in_unit_interval():
    rng = np.random.default_rng(2)
    A = rng.random((5, 5))
    result, _ = stabilize(A)
    assert result.min() >= 0.0 and result.max() <= 1.0


def test_project_fdrm_converges_and_dimensions():
    """The project FDRM stabilizes and produces an 11×11 output."""
    from scfa.data.fdrm import FDRM
    result, it = stabilize(FDRM)
    assert result.shape == (11, 11)
    assert it < 100, "Should converge well before the 100-iteration ceiling"


def test_project_fdrm_f4_f5_highest_driving():
    """After stabilization F4 and F5 should have the highest driving power,
    consistent with section 5.8 of the project report."""
    from scfa.data.fdrm import FDRM
    stabilized, _ = stabilize(FDRM)
    driving = stabilized.sum(axis=1)
    top2 = set(np.argsort(driving)[-2:])
    assert top2 == {3, 4}, (
        f"Expected F4 (idx 3) and F5 (idx 4) as top drivers, got indices {top2}"
    )


def test_project_fdrm_f9_lowest_driving():
    """F9 (Collaborations) should have the lowest driving power — sole autonomous factor."""
    from scfa.data.fdrm import FDRM
    stabilized, _ = stabilize(FDRM)
    driving = stabilized.sum(axis=1)
    assert np.argmin(driving) == 8, "F9 (idx 8) expected to have lowest driving power"


# --- classify_clusters ---

def test_four_clean_quadrants():
    driving    = np.array([8.0, 8.0, 3.0, 3.0])
    dependence = np.array([3.0, 8.0, 3.0, 8.0])
    labels     = ["A", "B", "C", "D"]
    clusters = classify_clusters(driving, dependence, labels)
    assert "A" in clusters["Independent"]
    assert "B" in clusters["Linkage"]
    assert "C" in clusters["Autonomous"]
    assert "D" in clusters["Dependent"]


def test_all_labels_assigned():
    rng = np.random.default_rng(3)
    labels = [f"F{i}" for i in range(10)]
    drv = rng.random(10)
    dep = rng.random(10)
    clusters = classify_clusters(drv, dep, labels)
    assigned = [f for group in clusters.values() for f in group]
    assert sorted(assigned) == sorted(labels)


def test_project_fdrm_f9_is_autonomous():
    """F9 (Collaborations) should fall in the Autonomous cluster."""
    from scfa.data.factors import FACTOR_LABELS
    from scfa.data.fdrm import FDRM
    stabilized, _ = stabilize(FDRM)
    drv = stabilized.sum(axis=1)
    dep = stabilized.sum(axis=0)
    clusters = classify_clusters(drv, dep, FACTOR_LABELS)
    assert "F9-Collab" in clusters["Autonomous"], (
        f"Expected F9-Collab in Autonomous, got {clusters}"
    )
