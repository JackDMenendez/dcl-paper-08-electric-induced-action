# The common-mode speed anisotropy and O_h isotropy restoration

**Status:** analysis (2026-07-16). Sharpens the one open caveat on the
birefringence verdict; **decouples** the speed anisotropy from the verdict.
**Verifier:** `src/utilities/electric_induced_action.py`
(`optical_axis_is_fourth_diagonal`, `oh_domain_average`).
**Related:** [[electric_block_derivation]].

---

## The question

The birefringence verdict left one honest caveat. Both photon polarizations share
the dispersion `w^2 = k^T epsilon k` with `epsilon = P` (eigenvalues `{1,4,4}`), so
the common phase speed is direction-dependent:

    v^2(k_hat) = k_hat^T P k_hat  ranges over [1, 4]

— a factor-~2 anisotropy of the vacuum speed of light about `(1,1,-1)`. This is a
**common-mode** effect (both polarizations equally), so it is **not** birefringence;
but it is not small, and an order-unity vacuum-`c` anisotropy is tightly bounded by
experiment. The question: is this anisotropy a real prediction, or an artifact of an
incomplete symmetry average — and either way, does it bear on the birefringence
verdict?

## The geometric origin of the optical axis

The answer starts with *why* `(1,1,-1)` is special. The three A=1 hop directions,
as axes, are **three of the four cube body-diagonals**:

    hop axes: (1,1,1), (1,-1,-1), (1,-1,1)     [= V1, V2, V3 up to sign]
    the four body-diagonals: (1,1,1), (1,1,-1), (1,-1,1), (1,-1,-1)

The optical axis `(1,1,-1)` is precisely the **fourth** body-diagonal — the one the
hop set omits. Selecting three of the four diagonals breaks the cubic point group
`O_h` down to the **trigonal** group `D_3d` about the omitted diagonal. A
`D_3d`-invariant quadratic form is exactly *uniaxial* — one eigenvalue along the
trigonal axis, a degenerate pair in the perpendicular plane — which is why both
induced tensors come out `{axis; 4, 4}` about `(1,1,-1)`. The axis is not put in by
hand; it is the diagonal the lattice leaves out. (Verified:
`optical_axis_is_fourth_diagonal()`.)

## Two levels, and the O_h average

There are four ways to choose three of the four body-diagonals — four **diagonal
domains**, each trigonal about a different body-diagonal (its own optical axis). The
actual A=1 lattice is the single domain with axis `(1,1,-1)`.

- **Single-domain (the un-averaged A=1 lattice).** `epsilon`, `mu^{-1}` are
  anisotropic (`{1,4,4}`, `{4,4,16}`), trigonal about `(1,1,-1)`. The adjugate
  relation `mu^{-1} = adj(epsilon)` holds, so there is **no birefringence** — but the
  common-mode speed anisotropy `v^2 in [1,4]` is present.
- **O_h-restored (average over the four domains).** Averaging the blocks over the
  four diagonal domains gives, exactly,

      <epsilon> = 3 I,     <mu^{-1}> = 8 I

  (verified: `oh_domain_average()`). The medium is isotropic Maxwell: **no**
  birefringence (now trivially) and **no** speed anisotropy. The factor-~2 anisotropy
  has averaged completely away.

## The decisive point: birefringence is decoupled from the anisotropy

The adjugate relation — hence the birefringence cancellation — holds **in every
single domain** (checked: `Q_B = adj(P)` for all four). So the cancellation is
present *non-trivially* before any averaging, and *trivially* after it. It therefore
does **not** depend on whether the physical vacuum is single-domain or
`O_h`-restored: **either way, gauge-sector vacuum birefringence is absent.**

The speed anisotropy is the *one* feature that distinguishes the two levels: present
in a single domain, gone under the domain average. It is thus a **separate** question
from the birefringence verdict, and however it resolves it cannot revive
birefringence. This is the resolution of the referee's tension ("if you `O_h`-average
to kill the anisotropy, the cancellation is trivial; un-averaged, the anisotropy is
present"): the cancellation is robust at *both* levels, so the tension is only
apparent.

## What remains genuinely open

Whether the physical A=1 vacuum is a single trigonal domain or an `O_h`-restored
average is a question about vacuum structure that the leading induced-action
calculation does not settle. Two honest possibilities:

1. **`O_h`-restored** (e.g. the physical continuum samples/averages the four domain
   orientations, or a coarse-graining restores cubic symmetry): the vacuum is
   isotropic, the speed anisotropy is absent, and everything is consistent — the
   `(1,1,-1)` axis survives only as the (canceling) *structure* seen by a
   birefringence probe, not as a speed anisotropy.
2. **Single-domain**: the trigonal anisotropy is physical, and the factor-~2 speed
   anisotropy is a genuine, testable prediction that must be reconciled with the tight
   experimental isotropy bounds — a potential tension, but **still with no
   birefringence**.

Deciding between these is the remaining work; it is separate from — and does not
gate — the birefringence verdict. This is why the birefringence-verdict row stays
`PART` (that status is now carried by this vacuum-structure question plus Paper IV's
large-`N` dispersion classification, **not** by any doubt about the cancellation
itself).
