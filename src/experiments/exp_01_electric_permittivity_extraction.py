"""
exp_01_electric_permittivity_extraction.py

Engine-level extraction of the ELECTRIC induced-action block eps = P -- the
mirror of dcl-core `exp_04` (which extracts the magnetic Q_B off the engine's
Peierls links). This is the cross-check the analytic derivation
(`src/utilities/electric_induced_action.py`) lacks: it reads P off the engine's
ACTUAL tick evolution, not by re-asserting the algebra.

How it genuinely reads the engine (not a synthetic field)
---------------------------------------------------------
The A=1 engine (`dcl_core.core3d`) couples the electric field on-site: the hop's
`external_potential` IS the temporal gauge potential A_0, entering the tick rule
as `delta_phi = omega + V(x)` (dcl-core `hop.py`, `HopOperator.step`; a static,
spatially varying V(x) IS a background E field, E = -grad A_0).

We seed a uniform, REAL probe state (`psi_R` uniform real). Then in one real
`hop.step`, the on-site term `i sin(delta_phi/2) psi_R` is purely IMAGINARY while
the kinetic hop is purely real, so

    Im(psi_R_new) / psi_R = sin(delta_phi/2)  =>  delta_phi(x) = omega + V(x)

is recovered DIRECTLY from the engine's step output. A sign error or a dropped
`external_potential` inside `hop.step` would corrupt this -- the result is NOT
computable without exercising the tick operator's actual coupling. The temporal-
plaquette holonomy is then read off the engine-recovered delta_phi:

    Theta_a(x) = delta_phi(x) - delta_phi(x + V_a) = V(x) - V(x+V_a) = V_a . E,

and `density_E = sum_a Theta_a^2 = E^T P E` gives P linearly in E (like exp_04).

Claims checked (all convention-independent unless noted):
  1. STRUCTURE: P (read off hop.step) has eigenvalues proportional to {1, 4, 4};
     the optical axis (1,1,-1) is the SUPPRESSED eigenvector -- the mirror of the
     magnetic Q_B = {4,4,16} (axis enhanced). Matches Paper IV exp_03a's sign.
  2. ADJUGATE STRUCTURE: P and Q_B (same engine) COMMUTE (share the optical axis +
     degenerate perpendicular plane) and are reciprocally ordered -- the
     fingerprint of Q_B = adj(P).
  3. ENGINE COUPLING FIDELITY: the recovered delta_phi reproduces omega + V(x) to
     round-off -- the tick operator applies the electric potential with unit tick
     weight (a_t = 1). This is the check that actually exercises hop.step.
  4. MASS-TERM CANCELLATION: P is independent of omega (extracted at omega=0 and
     omega=0.3 to round-off) -- the mass phase cancels around the temporal loop,
     so the extraction reads E, not the mass.

What this does NOT settle (kept honest, per referee): the electric-vs-magnetic
RELATIVE coupling (the 1/g^2 factor; the tick weight a_t=1 IS pinned above, but
the absolute magnetic scale is not) and the residual factor-~2 common-mode
vacuum-speed anisotropy. Both are separate from the STRUCTURE this experiment
confirms. See src/utilities/electric_induced_action.py and
notes/electric_block_derivation.md.

Audit row (paper/sections/audit_table.tex):
  "Electric induced-action block (permittivity eps = P = {1,4,4}, axis suppressed)"
  and the covariant-completion / birefringence-verdict rows it feeds.
Companion doc:
  src/experiments/exp_01_electric_permittivity_extraction.md

Run: python -u src/experiments/exp_01_electric_permittivity_extraction.py
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

# The engine under test.
from dcl_core.core3d import (
    BipartiteLattice,
    DiscreteCausalSession,
    HopOperator,
    uniform_B_potential,
)
from dcl_core.core3d.lattice import RGB_VECTORS

# n_units per site (both chiralities) for the seeded uniform probe state.
_SEED_UNITS_PER_SITE = 2

RUNTIME_BUDGET_SECONDS = 5

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"
EXP_ID = "exp_01_electric_permittivity_extraction"

SHAPE = (16, 16, 16)
MARGIN = 3       # interior margin, excluding the symmetric-gauge wrap layer
EPS = 1e-3       # small probe field; extraction is linear, so value-independent

# B -> F map (F12,F13,F23) basis, matching exp_04, for the magnetic cross-check.
_B_FROM_F = np.array([[0.0, 0.0, 1.0], [0.0, -1.0, 0.0], [1.0, 0.0, 0.0]])
_RGB_PLANES = [(0, 1), (0, 2), (1, 2)]
# Reference structures (up to the out-of-scope prefactor).
_P_EIGS = np.array([1.0, 4.0, 4.0])       # electric: axis suppressed
_QB_EIGS = np.array([4.0, 4.0, 16.0])     # magnetic: axis enhanced
_AXIS = np.array([1.0, 1.0, -1.0])


def uniform_E_potential(
    shape: tuple[int, int, int],
    E_vec: np.ndarray,
    origin: np.ndarray | None = None,
) -> np.ndarray:
    """Scalar potential of a constant electric field: ``V(x) = -E . (x - origin)``.

    This IS the temporal gauge potential A_0 the hop consumes as
    ``external_potential`` (``delta_phi = omega + V(x)``); ``E = -grad V`` is the
    uniform background electric field. The sibling of dcl-core
    ``uniform_B_potential`` for the temporal/electric sector (defined here rather
    than in the engine so the paper's evidence is self-contained; it is a
    candidate to upstream into ``core3d.gauge``)."""
    E = np.asarray(E_vec, dtype=np.float64)
    if origin is None:
        origin = np.asarray([(s - 1) / 2.0 for s in shape], dtype=np.float64)
    coords = np.indices(shape, dtype=np.float64)          # (3, *shape)
    r = coords - origin.reshape(3, 1, 1, 1)
    return -(E[0] * r[0] + E[1] * r[1] + E[2] * r[2])     # -E . (x - origin)


def _roll_to(field: np.ndarray, disp: tuple[int, int, int]) -> np.ndarray:
    """``field`` evaluated at ``x + disp`` but indexed at ``x`` (periodic)."""
    return np.roll(field, shift=tuple(-int(d) for d in disp), axis=(0, 1, 2))


def _temporal_holonomy(dphi: np.ndarray, va: tuple[int, int, int]) -> np.ndarray:
    """Temporal-plaquette holonomy for hop ``va``: ``dphi(x) - dphi(x + va)``.

    Evaluated on the ENGINE-recovered on-site phase ``dphi = omega + V(x)``; the
    ``omega`` mass term cancels around the loop, leaving ``V(x) - V(x+va)``, which
    for a uniform static E is ``V_a . E`` in the bulk."""
    return dphi - _roll_to(dphi, va)


def _seed_uniform_session(shape: tuple[int, int, int], omega: float):
    """A uniform, real, unit-per-site probe state (both chiralities), matching
    dcl-core ``test_hop``'s seeding. ``psi_R`` is then uniform and real, so the
    engine's on-site term ``i sin(delta_phi/2) psi_R`` is purely IMAGINARY and the
    kinetic hop is purely real -- letting us read ``delta_phi`` off the step."""
    lattice = BipartiteLattice(shape=shape)
    n = _SEED_UNITS_PER_SITE * int(np.prod(shape))
    session = DiscreteCausalSession(lattice=lattice, n_units=n, omega=omega)
    session.N_RGB[...] = 1
    session.N_CMY[...] = 1
    session.phi_RGB[...] = 0.0
    session.phi_CMY[...] = 0.0
    return lattice, session, HopOperator(lattice=lattice)


def _engine_delta_phi(hop, session, psi_R: np.ndarray, V: np.ndarray) -> np.ndarray:
    """Recover the engine's on-site phase ``delta_phi = omega + V(x)`` from a real
    ``HopOperator.step``: ``Im(psi_R_new) / psi_R = sin(delta_phi/2)`` (the kinetic
    hop is real, so the imaginary part isolates the on-site coupling term).

    This EXERCISES the tick operator's actual coupling -- a sign error or a
    dropped ``external_potential`` in ``hop.step`` would corrupt the result."""
    psi_R_new, _ = hop.step(session, "even", external_potential=V, vector_potential=None)
    ratio = np.asarray(psi_R_new).imag / psi_R.real
    return 2.0 * np.arcsin(np.clip(ratio, -1.0, 1.0))


def extract_P(shape: tuple[int, int, int], margin: int = MARGIN,
              omega: float = 0.0) -> tuple[np.ndarray, float]:
    """Electric induced-action coefficient ``P`` (density = E^T P E), read off the
    engine's real ``HopOperator.step`` output, in the E basis. The genuine mirror
    of exp_04's extract_Q. Returns ``(P, coupling_fidelity)`` where the fidelity is
    ``max|delta_phi_engine - (omega + V)|`` -- the check that the engine's coupling
    reproduces the applied potential with unit tick weight (a_t = 1)."""
    lattice, session, hop = _seed_uniform_session(shape, omega)
    psi_R = np.asarray(session.amplitude("R"))
    V_hops = [tuple(v) for v in RGB_VECTORS]
    interior = (slice(margin, -margin),) * 3
    G = np.zeros((3, 3))
    fidelity = 0.0
    for a in range(3):
        for k in range(3):
            E = np.zeros(3); E[k] = EPS
            Vpot = uniform_E_potential(shape, E)
            dphi = _engine_delta_phi(hop, session, psi_R, Vpot)   # engine read-off
            fidelity = max(fidelity,
                           float(np.abs(dphi - (omega + Vpot))[interior].max()))
            # Holonomy on the ENGINE-recovered delta_phi (omega cancels in the loop).
            G[a, k] = float(_temporal_holonomy(dphi, V_hops[a])[interior].mean()) / EPS
    return G.T @ G, fidelity


def _plaquette_phase(A, va, vb):
    """Spatial bipartite-plaquette holonomy (uniform B => (V_a x V_b).B).
    Reproduced from dcl-core exp_04 for the same-engine magnetic cross-check."""
    def link(Av, v):
        th = np.zeros(Av.shape[1:], dtype=np.float64)
        for d in range(3):
            th = th + v[d] * 0.5 * (Av[d] + _roll_to(Av[d], v))
        return th
    nva = tuple(-c for c in va); nvb = tuple(-c for c in vb)
    step2 = tuple(va[i] - vb[i] for i in range(3))
    return (link(A, va)
            + _roll_to(link(A, nvb), va)
            + _roll_to(link(A, nva), step2)
            + _roll_to(link(A, vb), nvb))


def extract_QB(shape: tuple[int, int, int], margin: int = MARGIN) -> np.ndarray:
    """Magnetic Q_B off the engine's Peierls links (F12,F13,F23 basis). exp_04."""
    V = [tuple(v) for v in RGB_VECTORS]
    interior = (slice(margin, -margin),) * 3
    G = np.zeros((3, 3))
    for r, (a, b) in enumerate(_RGB_PLANES):
        for k in range(3):
            B = np.zeros(3); B[k] = EPS
            A = uniform_B_potential(shape, B)
            G[r, k] = float(_plaquette_phase(A, V[a], V[b])[interior].mean()) / EPS
    return _B_FROM_F.T @ (G.T @ G) @ _B_FROM_F


def _sorted_eigs(M: np.ndarray) -> np.ndarray:
    return np.sort(np.linalg.eigvalsh(M))


def _axis_eigenvector(M: np.ndarray, want_min: bool) -> np.ndarray:
    """Return the (min or max) eigenvector, normalised so max|component| = 1."""
    vals, vecs = np.linalg.eigh(M)
    idx = int(np.argmin(vals) if want_min else np.argmax(vals))
    v = vecs[:, idx]
    return v / np.abs(v).max()


def run() -> str:
    DATA_DIR.mkdir(exist_ok=True)

    # P read off the engine's real step output, at two masses: omega must cancel
    # in the temporal loop, so both must give the same P (a genuine engine check).
    P, fidelity = extract_P(SHAPE, omega=0.0)
    P_massive, _ = extract_P(SHAPE, omega=0.3)
    QB = extract_QB(SHAPE)
    P_eig = _sorted_eigs(P)
    QB_eig = _sorted_eigs(QB)

    # 1. STRUCTURE: P ~ {1,4,4}, axis suppressed (ratios are convention-independent).
    P_struct_ok = np.allclose(P_eig / P_eig.max(), _P_EIGS / _P_EIGS.max(), atol=1e-6)
    axis_vec = _axis_eigenvector(P, want_min=True)     # suppressed eigenvector
    axis_ok = np.allclose(np.abs(axis_vec), np.abs(_AXIS), atol=1e-6)

    # 2. ADJUGATE STRUCTURE: commute + reciprocal ordering (both engine-sourced).
    commute = np.abs(P @ QB - QB @ P).max()
    commute_ok = commute < 1e-6
    P_axis = _axis_eigenvector(P, want_min=True)
    QB_axis = _axis_eigenvector(QB, want_min=False)
    reciprocal_ok = np.allclose(np.abs(P_axis), np.abs(QB_axis), atol=1e-6)

    # 3. ENGINE COUPLING: delta_phi recovered from hop.step reproduces omega+V to
    # round-off -> the tick operator applies the electric potential with unit tick
    # weight (a_t = 1). This is the check that actually exercises hop.step.
    coupling_ok = fidelity < 1e-9

    # 4. MASS-TERM CANCELLATION: P is omega-independent (the omega phase cancels
    # around the temporal loop) -> the extraction reads E, not the mass.
    omega_cancels = float(np.abs(P - P_massive).max())
    omega_ok = omega_cancels < 1e-6

    all_ok = (P_struct_ok and axis_ok and commute_ok and reciprocal_ok
              and coupling_ok and omega_ok)
    status = "PASS" if all_ok else "FAIL"

    lines = [
        f"{EXP_ID} -- electric permittivity block P read off HopOperator.step",
        f"generated: {datetime.now(timezone.utc).isoformat()}",
        f"SHAPE={SHAPE}  MARGIN={MARGIN}  EPS={EPS}",
        "",
        "P (density = E^T P E, E basis), from engine-recovered delta_phi=omega+V(x):",
        np.array2string(P, precision=4, suppress_small=True),
        f"  eigenvalues: {np.round(P_eig, 4).tolist()}   (structure {{1,4,4}}: "
        f"{'OK' if P_struct_ok else 'MISMATCH'})",
        f"  suppressed axis (-> optical axis): {np.round(axis_vec, 4).tolist()}"
        f"   (expect (1,1,-1): {'OK' if axis_ok else 'MISMATCH'})",
        "",
        "Q_B (same engine, exp_04 route via uniform_B_potential, F basis):",
        f"  eigenvalues: {np.round(QB_eig, 4).tolist()}   (Paper I {{4,4,16}})",
        "",
        "Adjugate structure (Q_B = adj(P)):",
        f"  [P,Q_B] max = {commute:.2e}  (commute -> shared eigenbasis: "
        f"{'OK' if commute_ok else 'MISMATCH'})",
        f"  P-suppressed axis == Q_B-enhanced axis (reciprocal): "
        f"{'OK' if reciprocal_ok else 'MISMATCH'}",
        "",
        f"Engine coupling: max|delta_phi_engine - (omega+V)| = {fidelity:.2e}  "
        f"(hop.step reproduces the applied potential, tick weight a_t=1: "
        f"{'OK' if coupling_ok else 'BROKEN'})",
        f"Mass-term cancellation: max|P(omega=0) - P(omega=0.3)| = {omega_cancels:.2e}"
        f"  (omega cancels in the loop: {'OK' if omega_ok else 'BROKEN'})",
        "",
        "Confirmed AT ENGINE LEVEL (read off HopOperator.step, not re-asserted):",
        "the electric block STRUCTURE {1,4,4} (axis suppressed), unit tick weight",
        "a_t=1, and the adjugate relation to Q_B. NOT settled here (separate): the",
        "electric-vs-magnetic 1/g^2 relative coupling and the residual factor-~2",
        "common-mode speed anisotropy -- see src/utilities/electric_induced_action.py.",
        "",
        f"{EXP_ID} {status}",
    ]
    report = "\n".join(lines) + "\n"
    (DATA_DIR / f"{EXP_ID}.log").write_text(report, encoding="utf-8")
    np.save(DATA_DIR / f"{EXP_ID}_P.npy", P)
    print(report)
    if not all_ok:
        raise AssertionError(f"{EXP_ID} FAIL: a structural check did not pass.")
    return status


if __name__ == "__main__":
    try:
        run()
    except AssertionError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    sys.exit(0)
