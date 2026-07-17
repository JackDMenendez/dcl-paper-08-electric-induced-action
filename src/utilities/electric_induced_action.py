"""Electric induced-action block -- derivation, magnetic anchor, and the
gauge-sector birefringence verdict.

Paper VIII of the A=1 Discrete Causal Lattice series.

Result (derived + symbolically verified here)
---------------------------------------------
The lattice couples the two fields on different footings, and this is the whole
point:

* MAGNETIC ``B`` IS a spatial link phase (Peierls). A closed *spatial* plaquette
  spanned by two hop vectors ``V_a, V_b`` has flux ``(V_a x V_b) . B``, so the
  induced O(B^2) action is
      density_B = sum_{a<b} ((V_a x V_b) . B)^2 = B^T Q_B B,
  reproducing Paper I App. B: ``Q_B`` eigenvalues ``{4, 4, 16}``, optical axis
  ``(1,1,-1)`` ENHANCED (16). This is the inherited anchor.

* ELECTRIC ``E`` IS an on-site, mass-like phase advance
  ``delta_phi(x) = omega + V(x)`` (implemented in dcl-core ``PhaseOscillator``,
  ``H = omega + V(x)``). That on-site advance IS a *temporal* link (a site joined
  to itself at the next tick), so a *temporal* plaquette spanned by ONE hop
  vector ``V_a`` and the tick direction closes on the bipartite lattice. Its
  uniform-field holonomy is ``(V_a . E) * a_t`` (with a uniform static potential
  ``V(x) = -E . x``, ``V(x) - V(x + V_a) = E . V_a``), where ``a_t`` IS the tick's
  temporal extent -- NOT unit weight. Hence the induced O(E^2) action is
      density_E = sum_a ((V_a . E) a_t)^2 = a_t^2 * E^T P E,  P = sum_a V_a V_a^T,
  giving the STRUCTURE ``P`` with eigenvalues ``{1, 4, 4}``, optical axis
  ``(1,1,-1)`` SUPPRESSED (1). This is the mirror of the magnetic block (whose
  spatial plaquette instead carries the area ``~a^2``), and is the new content of
  the paper. Its axis-suppression sign matches Paper IV ``exp_03a`` (the static
  E+B screen). The overall electric-vs-magnetic normalization thus carries an
  undetermined lattice-anisotropy factor ``~(a_t/a^2)^2`` and the open ``1/g^2``
  prefactor; the code sets ``a_t = 1`` to display the STRUCTURE ``P``. Per the
  verdict below this factor is immaterial to birefringence (it only renormalizes
  the common photon speed), but it is real and is NOT fixed here.

  ENGINE-CONFIRMED: ``P`` is no longer analytic-only. The mirror of ``exp_04`` --
  ``src/experiments/exp_01_electric_permittivity_extraction.py`` -- reads ``P``
  off the engine's on-site ``external_potential`` coupling
  (``delta_phi = omega + V(x)``), recovering ``{1,4,4}`` with the axis suppressed,
  confirming ``P`` and ``Q_B`` commute + are reciprocally ordered (the adjugate
  structure) from one engine, and reporting the tick weight ``a_t`` explicitly.
  What remains reported-not-fixed is the electric-vs-magnetic RELATIVE
  normalization (``a_t``, ``1/g^2``) -- immaterial to the verdict below.

* COVARIANT COMPLETION. The two blocks are not independent: for any three hop
  vectors,
      Q_B = sum_{a<b}(V_a x V_b)(V_a x V_b)^T = adj( sum_a V_a V_a^T ) = adj(P).
  The magnetic tensor IS the adjugate of the electric tensor. So identifying the
  macroscopic response tensors as ``eps = P`` (permittivity) and
  ``mu^{-1} = Q_B = adj(P)`` (inverse permeability), every principal axis obeys
      eps_i * (mu^{-1})_i = eps_i * (adj eps)_i = det(eps),
  i.e. the impedance product is ISOTROPIC even though eps and mu^{-1} are each
  anisotropic (with opposite senses about the same axis).

* BIREFRINGENCE VERDICT (conditional -- airtight given the identification).
  IF the macroscopic response tensors are ``(eps, mu^{-1}) = (P, Q_B)``, then the
  photon dispersion ``det(K mu^{-1} K + w^2 eps) = 0`` factors as
  ``det(eps) * w^2 * (w^2 - k^T eps k)^2`` -- a DOUBLE transverse root for every
  propagation direction (proven for a general symmetric ``eps`` with
  ``mu^{-1} = adj(eps)``; it does NOT even require eps, mu^{-1} to share
  eigenvectors). Both polarizations share ``w^2 = k^T eps k``, so the split is
      Delta(w^2) proportional to |eps_a (mu^{-1})_a - eps_p (mu^{-1})_p| = 0.
  Gauge-sector vacuum birefringence CANCELS. Because the cancellation follows
  from the adjugate relation, it is invariant under INDEPENDENT rescaling of eps
  and mu^{-1} -- immune to the undetermined a_t / 1/g^2 factors -- and holds for
  any hop vectors. This CONDITIONAL is the load-bearing theorem.

  What is NOT yet earned is the UNCONDITIONAL physical verdict -- not because of
  ``eps = P`` (now engine-confirmed by exp_01) but because of the isotropy-
  restoration question for the common-mode speed anisotropy (below) and Paper IV's
  full E+B dispersion classification at large N.

* HONEST CAVEAT -- a LARGE effect the verdict does not address. The shared
  dispersion ``w^2 = k^T eps k`` is direction-dependent: ``v^2(k)`` ranges over
  eps's eigenvalues ``[1, 4]`` -- an order-unity (factor ~2 in speed) directional
  anisotropy of the vacuum ``c``, affecting BOTH polarizations equally. That is a
  speed anisotropy, NOT birefringence -- but it is not small, and the standard
  ``O_h``-average that would remove it (``Tr(P)/3 . I``, ``Tr(Q_B)/3 . I`` are both
  isotropic) also makes the birefringence cancellation TRIVIAL. The non-trivial,
  averaging-independent cancellation lives at the un-averaged operator level,
  where this speed anisotropy is also present. See
  notes/electric_block_derivation.md; this is a separate isotropy-restoration
  question and must not be sold as a clean polarimetry null.

Documentation convention: comments say what each object IS in the theory.
Run: python -u src/utilities/electric_induced_action.py
"""

from __future__ import annotations

import os

import sympy as sp

# Paper equations are GENERATED from the verified SymPy expressions (never
# hand-transcribed): this dir holds auto-generated LaTeX fragments that the
# paper section files `\input`. See CLAUDE.md "SymPy-generated equations".
_HERE = os.path.dirname(os.path.abspath(__file__))
GENERATED_TEX_DIR = os.path.normpath(
    os.path.join(_HERE, "..", "..", "paper", "sections", "generated")
)

# --- The spatial hop vectors (RGB sublattice directions) ---------------------
# These IS the three primitive hop directions of the A=1 bipartite octahedral
# lattice; the CMY partners are their negatives (V V^T is insensitive to sign,
# so only the three are needed to build the induced-action tensors).
V1 = sp.Matrix([1, 1, 1])
V2 = sp.Matrix([1, -1, -1])
V3 = sp.Matrix([-1, 1, -1])
V_HOPS = [V1, V2, V3]

# The optical axis IS the common eigenvector distinguished by both blocks.
OPTICAL_AXIS = sp.Matrix([1, 1, -1])

# Inherited magnetic anchor (Paper I App. B; dcl-core exp_04, max|Q-Q_I|=0).
Q_MAGNETIC = sp.Matrix([
    [8,  4, -4],
    [4,  8, -4],
    [-4, -4, 8],
])
EXPECTED_MAG_EIGS = {sp.Integer(4): 2, sp.Integer(16): 1}   # value: multiplicity
EXPECTED_ELE_EIGS = {sp.Integer(1): 1, sp.Integer(4): 2}    # electric mirror


def _cross(a: sp.Matrix, b: sp.Matrix) -> sp.Matrix:
    """Vector cross product ``a x b`` (the spatial-plaquette area vector)."""
    return sp.Matrix([
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    ])


def _outer(v: sp.Matrix) -> sp.Matrix:
    """Outer product ``v v^T`` (a rank-1 quadratic form)."""
    return v * v.T


# --- Magnetic block: derived from first principles (the anchor) --------------
def derive_magnetic_Q() -> sp.Matrix:
    """``Q_B = sum_{a<b} (V_a x V_b)(V_a x V_b)^T`` -- the O(B^2) induced-action
    coefficient. Its flux ``(V_a x V_b) . B`` IS the spatial-plaquette holonomy
    for a uniform field (Paper I App. B; dcl-core exp_04)."""
    pairs = [(0, 1), (0, 2), (1, 2)]
    Q = sp.zeros(3, 3)
    for a, b in pairs:
        Q += _outer(_cross(V_HOPS[a], V_HOPS[b]))
    return Q


# --- Electric block: the new derivation --------------------------------------
def derive_electric_block() -> sp.Matrix:
    """``P = sum_a V_a V_a^T`` -- the O(E^2) induced-action coefficient.

    The electric field enters on-site as ``delta_phi = omega + V(x)``; that
    on-site phase advance IS the temporal link. The temporal plaquette spanned
    by one hop ``V_a`` and the tick direction closes on the bipartite lattice,
    and for a uniform field its holonomy IS ``(V_a . E) * a_t`` (with a uniform
    static potential ``V(x) = -E . x`` one has ``V(x) - V(x + V_a) = E . V_a``);
    ``a_t`` (the tick's temporal extent) is set to 1 here to expose the STRUCTURE.
    Summed over the three hop directions this gives the permittivity STRUCTURE
    ``eps = P`` (up to the a_t^2 and 1/g^2 factors). Eigenvalues ``{1, 4, 4}``:
    optical axis ``(1,1,-1)`` SUPPRESSED to 1, the perpendicular plane at 4
    (mirror of the magnetic ``{4, 4, 16}``).

    STATUS: engine-confirmed (PASS). ``exp_01`` extracts this same ``P`` off the
    engine's on-site ``external_potential`` coupling (the mirror of dcl-core
    ``exp_04``). Only the electric-vs-magnetic relative scale (``a_t``, ``1/g^2``)
    is reported-not-fixed, and it is immaterial to the birefringence verdict."""
    P = sp.zeros(3, 3)
    for v in V_HOPS:
        P += _outer(v)
    return P


# --- Covariant completion: the adjugate theorem ------------------------------
def adjugate_relation() -> tuple[bool, sp.Expr]:
    """Verify ``Q_B = adj(P)`` (magnetic block IS the adjugate of the electric
    block), the structural fact behind covariant completion and the null
    birefringence verdict. Returns ``(holds, det P)``."""
    P = derive_electric_block()
    Q = derive_magnetic_Q()
    holds = sp.simplify(Q - P.adjugate()) == sp.zeros(3, 3)
    return bool(holds), P.det()


def adjugate_is_general() -> bool:
    """The adjugate relation holds for ANY three hop vectors (not just the
    octahedral ones): ``sum_{a<b}(A_a x A_b)(A_a x A_b)^T = adj(sum_a A_a A_a^T)``.
    This is why the birefringence cancellation is structural, not lattice-tuned."""
    a = sp.Matrix(sp.symbols("a0:3", real=True))
    b = sp.Matrix(sp.symbols("b0:3", real=True))
    c = sp.Matrix(sp.symbols("c0:3", real=True))
    Vg = [a, b, c]
    Pg = _outer(a) + _outer(b) + _outer(c)
    Qg = sp.zeros(3, 3)
    for i, j in [(0, 1), (0, 2), (1, 2)]:
        Qg += _outer(_cross(Vg[i], Vg[j]))
    return sp.simplify(Qg - Pg.adjugate()) == sp.zeros(3, 3)


# --- Origin of the optical axis + O_h isotropy restoration -------------------
# The four cube body-diagonals. The A=1 hop set (V_HOPS) is three of them, and
# the optical axis (1,1,-1) IS the fourth -- the one absent from the hop set.
# That absence breaks cubic O_h to trigonal D_3d about (1,1,-1) and is the
# geometric origin of the uniaxial induced tensors.
BODY_DIAGONALS = [sp.Matrix(d) for d in
                  [(1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1)]]


def _P_from(vs: list[sp.Matrix]) -> sp.Matrix:
    P = sp.zeros(3, 3)
    for v in vs:
        P += _outer(v)
    return P


def _QB_from(vs: list[sp.Matrix]) -> sp.Matrix:
    Q = sp.zeros(3, 3)
    for i, j in [(0, 1), (0, 2), (1, 2)]:
        Q += _outer(_cross(vs[i], vs[j]))
    return Q


def optical_axis_is_fourth_diagonal() -> bool:
    """PASS iff the actual A=1 electric block equals the diagonal-domain that
    OMITS ``(1,1,-1)`` -- i.e. the lattice's three hop axes are three of the four
    cube body-diagonals and the optical axis is the fourth, missing one."""
    omit_axis = BODY_DIAGONALS[1]                       # (1,1,-1)
    dirs = [d for d in BODY_DIAGONALS if d != omit_axis]
    same_block = sp.simplify(_P_from(dirs) - derive_electric_block()) == sp.zeros(3, 3)
    axis_is_omitted = sp.simplify(
        derive_electric_block() * omit_axis - 1 * omit_axis) == sp.zeros(3, 1)
    return bool(same_block and axis_is_omitted)


def oh_domain_average() -> tuple[sp.Matrix, sp.Matrix]:
    """Average the electric and magnetic blocks over the four 'diagonal domains'
    (the four ways to use three of the four body-diagonals as hop directions,
    each trigonal about the omitted diagonal). Returns ``(<P>, <Q_B>)``; both are
    ISOTROPIC (``3I``, ``8I``), so O_h is restored by the domain average and the
    common-mode speed anisotropy averages away. (The birefringence cancellation,
    by contrast, already holds in every single domain via the adjugate relation,
    so it is robust to whether or not this averaging is physical.)"""
    Psum = sp.zeros(3, 3)
    Qsum = sp.zeros(3, 3)
    for omit in range(4):
        dirs = [BODY_DIAGONALS[i] for i in range(4) if i != omit]
        Psum += _P_from(dirs)
        Qsum += _QB_from(dirs)
    return sp.Rational(1, 4) * Psum, sp.Rational(1, 4) * Qsum


# --- Birefringence verdict: photon dispersion --------------------------------
def _cross_matrix(k: sp.Matrix) -> sp.Matrix:
    """``[k]_x`` such that ``[k]_x v = k x v`` -- the curl operator for a plane
    wave with wavevector ``k``."""
    return sp.Matrix([
        [0, -k[2], k[1]],
        [k[2], 0, -k[0]],
        [-k[1], k[0], 0],
    ])


def birefringence_split() -> sp.Expr:
    """The polarization splitting of ``w^2`` for a uniaxial ``(eps, mu^{-1})``
    pair sharing the optical axis. Returns ``Delta(w^2)`` as a function of the
    principal values and propagation angle ``theta``; it IS proportional to
    ``|eps_a mu_a^{-1} - eps_p mu_p^{-1}|`` and so vanishes exactly when the
    axial and perpendicular impedance products agree (the adjugate condition)."""
    ea, ep, na, np_, th, w2 = sp.symbols(
        "e_a e_p n_a n_p theta w2", real=True, positive=True
    )
    eps = sp.diag(ea, ep, ep)          # electric block in principal basis (axis first)
    nu = sp.diag(na, np_, np_)         # magnetic block mu^{-1} in the same basis
    k = sp.Matrix([sp.cos(th), sp.sin(th), 0])   # WLOG in the axis-perp plane
    K = _cross_matrix(k)
    transverse = sp.factor(((K * nu * K + w2 * eps).det()) / w2)  # drop longitudinal
    roots = sp.solve(sp.Eq(transverse, 0), w2)
    return sp.simplify(roots[0] - roots[1]) if len(roots) == 2 else sp.Integer(0)


def _principal_values(M: sp.Matrix) -> tuple[sp.Expr, sp.Expr]:
    """Return ``(axial, perpendicular)`` eigenvalues of a block that is uniaxial
    about ``OPTICAL_AXIS`` -- the axial one is read off the axis, the
    (degenerate) perpendicular one from the remaining trace."""
    axial = (M * OPTICAL_AXIS)[0] / OPTICAL_AXIS[0]
    perp = (M.trace() - axial) / 2
    return sp.simplify(axial), sp.simplify(perp)


def verdict_no_birefringence() -> bool:
    """PASS iff the derived blocks satisfy the exact cancellation condition
    ``eps_a * mu_a^{-1} = eps_p * mu_p^{-1}`` -- i.e. the split formula
    ``birefringence_split`` evaluates to zero at the lattice principal values."""
    ea, ep = _principal_values(derive_electric_block())   # (1, 4)
    na, np_ = _principal_values(derive_magnetic_Q())      # (16, 4)
    return bool(sp.simplify(ea * na - ep * np_) == 0)


def photon_dispersion_double_root() -> tuple[bool, sp.Expr]:
    """Confirm the general-``k`` dispersion is a double transverse root (no
    birefringence). Returns ``(is_double_root, w^2(k))`` where ``w^2 = k^T P k``
    is the shared dispersion of both polarizations."""
    kx, ky, kz, w2 = sp.symbols("kx ky kz w2", real=True)
    k = sp.Matrix([kx, ky, kz])
    K = _cross_matrix(k)
    P = derive_electric_block()
    Q = derive_magnetic_Q()
    det = sp.expand((K * Q * K + w2 * P).det())
    # det = C * w2 * (w2 - k^T P k)^2  when the two transverse roots coincide.
    shared = sp.expand((k.T * P * k)[0])
    C = sp.Poly(det, w2).coeff_monomial(w2 ** 3)   # leading (out-of-scope) prefactor
    is_double = sp.expand(det - C * w2 * (w2 - shared) ** 2) == 0
    return bool(is_double), shared


def numeric_birefringence_sweep(n: int = 20000, seed: int = 0) -> float:
    """Independent NUMERIC guard on the symbolic double-root proof: over ``n``
    random propagation directions, return the maximum polarization split of the
    two transverse roots of ``det(K Q_B K + w^2 P) = 0``. Expected ~1e-14 (they
    coincide). Guards against a SymPy error in the symbolic proof above."""
    import numpy as _np
    P = _np.array(derive_electric_block().tolist(), dtype=float)
    Q = _np.array(derive_magnetic_Q().tolist(), dtype=float)
    rng = _np.random.default_rng(seed)
    worst = 0.0
    for _ in range(n):
        k = rng.standard_normal(3)
        k /= _np.linalg.norm(k)
        K = _np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
        # (K Q K) E = -w^2 P E  ->  eig of P^{-1}(-K Q K); top two are transverse.
        w2 = _np.sort(_np.real(_np.linalg.eigvals(_np.linalg.solve(P, -K @ Q @ K))))
        worst = max(worst, abs(w2[2] - w2[1]))
    return worst


# --- Anchor gate -------------------------------------------------------------
def verify_magnetic_anchor() -> bool:
    """PASS iff the first-principles ``Q_B`` equals the inherited anchor and
    carries ``{4,4,16}`` with the ``(1,1,-1)`` axis at eigenvalue 16."""
    Q = derive_magnetic_Q()
    matches_inherited = sp.simplify(Q - Q_MAGNETIC) == sp.zeros(3, 3)
    eig_ok = Q.eigenvals() == EXPECTED_MAG_EIGS
    axis_ok = sp.simplify(Q * OPTICAL_AXIS - 16 * OPTICAL_AXIS) == sp.zeros(3, 1)
    return bool(matches_inherited and eig_ok and axis_ok)


def verify_electric_block() -> bool:
    """PASS iff ``P`` carries ``{1,4,4}`` with the ``(1,1,-1)`` axis SUPPRESSED
    to eigenvalue 1 (the mirror of the magnetic anchor)."""
    P = derive_electric_block()
    eig_ok = P.eigenvals() == EXPECTED_ELE_EIGS
    axis_ok = sp.simplify(P * OPTICAL_AXIS - 1 * OPTICAL_AXIS) == sp.zeros(3, 1)
    return bool(eig_ok and axis_ok)


# --- Paper equations, generated (never hand-transcribed) ---------------------
def write_latex_fragments() -> list[str]:
    """Emit derived equations as LaTeX fragments for the paper to ``\\input``.

    Generated via ``sympy.latex`` from the verified expressions, so the paper's
    equations cannot drift from the math. See CLAUDE.md "SymPy-generated
    equations"."""
    os.makedirs(GENERATED_TEX_DIR, exist_ok=True)
    P = derive_electric_block()
    Q = derive_magnetic_Q()
    written: list[str] = []

    def _emit(name: str, body: str) -> None:
        path = os.path.join(GENERATED_TEX_DIR, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("% AUTO-GENERATED by src/utilities/electric_induced_action.py"
                     " -- do not edit.\n")
            fh.write(body + "\n")
        written.append(path)

    _emit("magnetic_Q.tex", "Q_B = " + sp.latex(Q, mat_delim="["))
    _emit("electric_P.tex", r"\varepsilon = P = " + sp.latex(P, mat_delim="["))
    _emit("adjugate_relation.tex",
          r"\mu^{-1} = Q_B = \operatorname{adj}(P) = \operatorname{adj}(\varepsilon)")
    _emit("birefringence_condition.tex",
          r"\Delta(\omega^2) \;\propto\; \bigl|\varepsilon_a\,\mu^{-1}_a"
          r" - \varepsilon_p\,\mu^{-1}_p\bigr| = |\det\varepsilon - \det\varepsilon| = 0")

    # Dispersion factorization -- emit the VERIFIED factored form (checked equal
    # to the raw determinant here, so the displayed equation cannot drift).
    kx, ky, kz, w2 = sp.symbols("kx ky kz w2", real=True)
    kvec = sp.Matrix([kx, ky, kz])
    K = _cross_matrix(kvec)
    det = sp.expand((K * Q * K + w2 * P).det())
    shared = sp.expand((kvec.T * P * kvec)[0])
    factored = sp.factor(P.det()) * w2 * (w2 - shared) ** 2
    assert sp.expand(det - factored) == 0, "dispersion factorization drifted"
    _emit("dispersion_factorization.tex",
          r"\det\!\bigl(K\,\mu^{-1}K + \omega^2\varepsilon\bigr) = "
          + sp.latex(sp.det(P)) + r"\,\omega^2\,\bigl(\omega^2 - k^{\!\top}\!"
          r"\varepsilon\,k\bigr)^2")
    _emit("shared_dispersion.tex",
          r"\omega^2 = k^{\!\top}\!\varepsilon\,k = " + sp.latex(shared))

    Pbar, Qbar = oh_domain_average()
    _emit("oh_average.tex",
          r"\langle\varepsilon\rangle = " + sp.latex(Pbar, mat_delim="[")
          + r",\qquad \langle\mu^{-1}\rangle = " + sp.latex(Qbar, mat_delim="["))
    return written


def main() -> None:
    print("Paper VIII -- Electric Induced-Action Block")
    print("=" * 60)

    anchor = verify_magnetic_anchor()
    print(f"[ANCHOR  ] magnetic Q_B from first principles = {{4,4,16}}, "
          f"axis (1,1,-1) ENHANCED (16): {'PASS' if anchor else 'FAIL'}")
    if not anchor:
        raise SystemExit("Magnetic anchor FAILED -- fix before the electric block.")
    print(f"           Q_B = {derive_magnetic_Q().tolist()}")

    electric = verify_electric_block()
    P = derive_electric_block()
    print(f"[ELECTRIC] permittivity P from temporal plaquette = {{1,4,4}}, "
          f"axis (1,1,-1) SUPPRESSED (1): {'PASS' if electric else 'FAIL'}")
    print(f"           P = {P.tolist()}   (matches exp_03a axis-suppression sign)")

    holds, detP = adjugate_relation()
    general = adjugate_is_general()
    print(f"[COVARIANT] mu^-1 = Q_B = adj(P): {'PASS' if holds else 'FAIL'} "
          f"(det P = {detP}); holds for ANY hop vectors: "
          f"{'PASS' if general else 'FAIL'}")

    axis_geom = optical_axis_is_fourth_diagonal()
    Pbar, Qbar = oh_domain_average()
    oh_ok = (Pbar == 3 * sp.eye(3)) and (Qbar == 8 * sp.eye(3))
    print(f"[GEOMETRY] optical axis (1,1,-1) IS the 4th cube body-diagonal, absent "
          f"from the hop set (-> trigonal D_3d): {'PASS' if axis_geom else 'FAIL'}")
    print(f"           O_h restoration -- 4-domain average <P>=3I, <Q_B>=8I "
          f"isotropic: {'PASS' if oh_ok else 'FAIL'} (speed anisotropy averages "
          f"away; birefringence already null per-domain via adj)")

    is_double, shared = photon_dispersion_double_root()
    split = birefringence_split()
    cancels = verdict_no_birefringence()
    ea, ep = _principal_values(derive_electric_block())
    na, np_ = _principal_values(derive_magnetic_Q())
    print(f"[VERDICT ] CONDITIONAL on (eps,mu^-1)=(P,Q_B): dispersion is a DOUBLE "
          f"transverse root w^2 = k^T P k: {'PASS' if is_double else 'FAIL'}")
    print(f"           shared w^2(k) = {shared}")
    print(f"           split Delta(w^2) proportional to (eps_a mu_a - eps_p mu_p) "
          f"= ({ea}*{na} - {ep}*{np_}) = {ea * na - ep * np_}")
    print(f"           => birefringence CANCELS (prefactor-independent): "
          f"{'PASS' if cancels else 'FAIL'}")
    sweep = numeric_birefringence_sweep()
    sweep_ok = sweep < 1e-10
    print(f"           numeric sweep (2e4 random k): max split = {sweep:.2e} "
          f"{'PASS' if sweep_ok else 'FAIL'}")
    print(f"           v^2(k) in [{ea}, {ep}]: common-mode speed anisotropy "
          f"remains (NOT birefringence; see notes).")
    print("           eps=P engine-verified by exp_01; unconditional verdict still "
          "pends the speed-anisotropy story + Paper IV large-N (row stays PART).")

    for path in write_latex_fragments():
        print(f"[LATEX   ] generated "
              f"{os.path.relpath(path, os.path.join(_HERE, '..', '..'))}")

    ok = (anchor and electric and holds and general and is_double and cancels
          and sweep_ok and axis_geom and oh_ok)
    print("=" * 60)
    print(f"CONDITIONAL CHECKS: {'ALL PASS' if ok else 'CHECK FAILED'}  "
          f"(eps=P engine-confirmed by exp_01; verdict conditional on the "
          f"eps,mu^-1 identification)")
    if not ok:
        raise SystemExit("A derivation check failed.")


if __name__ == "__main__":
    main()
