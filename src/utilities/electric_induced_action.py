"""Electric induced-action block -- derivation + magnetic consistency anchor.

Paper VIII of the A=1 Discrete Causal Lattice series.

This script has two jobs:

1. ANCHOR (PASS today): reproduce and verify the *magnetic* induced-action
   Q-tensor from Paper I Appendix B --
   Q IS the O(B^2) coefficient of the bipartite-plaquette Wilson-loop action,
   with eigenvalues {4, 4, 16} and optical axis (1, 1, -1). This is the
   consistency check every electric-block derivation step must not break.

2. ELECTRIC BLOCK (STUB): derive the electric permittivity `epsilon` and the
   covariant (epsilon, mu^-1) completion. The magnetic field enters as a
   spatial link phase (clean holonomy -> Q), but the electric field enters as
   an on-site, mass-like phase advance delta_phi = omega + V(x) -- there IS no
   electric Wilson-loop analog, so this block is genuinely new theory. See
   notes/electric_block_derivation.md for the two candidate methods.

Documentation convention: comments say what each object IS in the theory.
Run: python -u src/utilities/electric_induced_action.py
"""

from __future__ import annotations

import sympy as sp

# --- Magnetic induced-action Q-tensor (Paper I App. B) -----------------------
# Q IS the coefficient matrix of the induced magnetic action
#   1 - Re W_ab = F^T Q F   (bipartite plaquette holonomy, uniform field).
# Inherited value (reproduced exactly by dcl-core exp_04, max|Q - Paper_I_Q|=0).
Q_MAGNETIC = sp.Matrix([
    [8,  4, -4],
    [4,  8, -4],
    [-4, -4, 8],
])

# The optical axis IS the eigenvector with the enhanced eigenvalue.
OPTICAL_AXIS = sp.Matrix([1, 1, -1])
EXPECTED_EIGENVALUES = {sp.Integer(4): 2, sp.Integer(16): 1}  # value: multiplicity


def verify_magnetic_anchor() -> bool:
    """PASS iff Q reproduces {4,4,16} and the (1,1,-1) axis carries eigenvalue 16."""
    eigs = Q_MAGNETIC.eigenvals()  # {value: multiplicity}
    eig_ok = eigs == EXPECTED_EIGENVALUES
    # Q . (1,1,-1) IS 16 . (1,1,-1)  -> axis is the enhanced eigenvector.
    axis_ok = sp.simplify(Q_MAGNETIC * OPTICAL_AXIS - 16 * OPTICAL_AXIS) == sp.zeros(3, 1)
    trace_ok = sp.trace(Q_MAGNETIC) == 24  # 4 + 4 + 16
    return bool(eig_ok and axis_ok and trace_ok)


def derive_electric_block():
    """Derive the electric permittivity block. STUB -- new theory.

    Method (a): extend Paper I App. B's plaquette approach to the electric /
    temporal-plaquette sector. Method (b): action-level spectral (Tr ln T)
    probe. The obstruction to overcome: E is on-site (no spatial loop), so a
    gauge-invariant electric holonomy may not exist -- part (a)'s first task is
    to establish whether it does. See notes/electric_block_derivation.md.
    """
    raise NotImplementedError(
        "Electric induced-action block not yet derived (Paper VIII STUB). "
        "See notes/electric_block_derivation.md for methods (a) and (b)."
    )


def main() -> None:
    print("Paper VIII -- Electric Induced-Action Block")
    print("=" * 52)

    anchor = verify_magnetic_anchor()
    print(f"[ANCHOR ] magnetic Q-tensor {{4,4,16}}, axis (1,1,-1): "
          f"{'PASS' if anchor else 'FAIL'}")
    if not anchor:
        raise SystemExit("Magnetic anchor FAILED -- fix before touching the electric block.")

    print("[ELECTRIC] permittivity block: STUB (not yet derived)")
    print("           -> notes/electric_block_derivation.md (methods a/b)")


if __name__ == "__main__":
    main()
