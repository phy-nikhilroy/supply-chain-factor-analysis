# Supply Chain Factor Analysis

A Python implementation of an **ISM + Fuzzy MICMAC** analysis pipeline to identify and prioritize the factors affecting sustainable supply chain performance in India's food and packaging industries.

---

## What it does

1. **Factor Analysis** (via SPSS 21) — reduces 32 candidate factors from a Likert-scale expert survey (n = 41) to 11 critical factors explaining ~77.2% of total variance
2. **Interpretive Structural Modeling (ISM)** — builds a directed hierarchy of causal relationships using a Structural Self-Interaction Matrix (SSIM), reachability matrices with transitivity closure, and iterative level partitioning
3. **Fuzzy MICMAC** (coded in Python) — replaces binary ISM relationships with fuzzy possibility values; iteratively multiplies the matrix via max-min composition until driving/dependence power rankings stabilize; classifies all factors into four strategic clusters

---

## Key results

### ISM hierarchy (3 levels)

```
Level I  — Outcomes    : Customer Awareness, Global Image, Media, Collaborations,
                         Working Conditions, Sales & Marketing
Level II — Middle tier : Lack of Expertise, Infrastructure, Governance Mechanism
Level III — Root causes: Government Policies (F3), Lack of Complete Information (F4)
```

### Fuzzy MICMAC cluster classification

| Cluster | Factors | Interpretation |
|---|---|---|
| Independent (root causes) | F4 — Lack of Info, F5 — Lack of Expertise | High driving, low dependence — fix these first |
| Linkage (critical nodes) | F1, F2, F6, F8, F10 | High driving AND dependence — volatile, cascading effects |
| Dependent (outcomes) | F3, F7 | Low driving, high dependence — visible performance metrics |
| Autonomous (isolated) | F9 — Collaborations | Low driving AND dependence — underutilized lever |

---

## Tech stack

| Tool | Role |
|---|---|
| Python 3 | Fuzzy MICMAC algorithm and visualization |
| NumPy | Matrix operations, max-min fuzzy multiplication |
| Matplotlib | Driving vs. dependence power scatter plot with quadrant classification |
| SPSS 21 | Reliability analysis (Cronbach's α) and PCA-based Factor Analysis |
| Google Forms | Expert survey instrument (n = 41 respondents, ~58% response rate) |

---

## Core algorithm — Fuzzy MICMAC

### Max-min matrix composition

```python
def fuzzy_multiply(A, B):
    """Fuzzy matrix multiplication: C[i][j] = max_k { min(A[i][k], B[k][j]) }"""
    n = A.shape[0]
    C = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            C[i][j] = np.max(np.minimum(A[i, :], B[:, j]))
    return C
```

### Iterative stabilization

```python
def stabilize_fuzzy_micmac(FDRM, max_iterations=100):
    """
    Multiply FDRM by itself until driving-power and dependence-power
    rankings no longer change between iterations.
    """
    current = FDRM.copy()
    prev_drv_rank, prev_dep_rank = None, None

    for it in range(1, max_iterations + 1):
        nxt = fuzzy_multiply(current, FDRM)
        drv_rank = np.argsort(np.argsort(-nxt.sum(axis=1)))
        dep_rank = np.argsort(np.argsort(-nxt.sum(axis=0)))

        if (prev_drv_rank is not None
                and np.array_equal(drv_rank, prev_drv_rank)
                and np.array_equal(dep_rank, prev_dep_rank)):
            return nxt, it

        prev_drv_rank, prev_dep_rank = drv_rank, dep_rank
        current = nxt

    return current, max_iterations
```

### ISM — SSIM to reachability matrix

```
Encoding rules:
  V  →  R[i][j]=1, R[j][i]=0   (i drives j)
  A  →  R[i][j]=0, R[j][i]=1   (j drives i)
  X  →  R[i][j]=1, R[j][i]=1   (mutual)
  O  →  R[i][j]=0, R[j][i]=0   (no relation)

Transitivity: if R[i][k]=1 and R[k][j]=1 then R[i][j]=1
```

---

## Validation

The Python Fuzzy MICMAC implementation was validated against the published results of **Gorane & Kant (2013)** *(Asia Pacific Journal of Marketing and Logistics, 25(2), 263–286)*. The FDRM from the paper was used as input; the generated stabilized matrix and driving/dependence powers matched the published values **exactly**, confirming correctness of the max-min composition and convergence logic.

---

## Survey data summary

| Metric | Value |
|---|---|
| Candidate factors identified | 32 |
| Experts contacted | 97 |
| Usable responses | 41 (~58% response rate) |
| Cronbach's Alpha | 0.886 ("Good") |
| Factors retained (Eigenvalue > 1) | 11 |
| Cumulative variance explained | ~77.2% |

---

## References

1. Warfield, J.N. (1974). Developing interconnection matrices in structural modeling. *IEEE Trans. Syst. Man Cybern.*
2. Gorane, S.J. & Kant, R. (2013). Modelling the SCM enablers: an integrated ISM-fuzzy MICMAC approach. *Asia Pacific Journal of Marketing and Logistics, 25(2)*, 263–286.
3. Nishikant Mishra & Akshit Singh (2017). ISM and fuzzy MICMAC for customer-centric beef supply chain. *Production Planning and Control.*
4. Seuring & Muller (2008). From a literature review to a conceptual framework for SSCM. *Journal of Cleaner Production, 16.*
