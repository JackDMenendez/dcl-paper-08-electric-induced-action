# The Tr ln T mode-filling prescription (method (b))

**Status:** derived (2026-07-16). Answers Paper IV's blocking question and retires
VIII's deferred "method (b)".
**Verifier:** `src/utilities/trlnT_prescription.py` (all checks PASS).
**Triggered by:** handoff `2026-07-16-paper04-to-paper08-vacuum-prescription-question`.
**Related:** [[electric_block_derivation]], [[speed_anisotropy_and_isotropy_restoration]].

---

## The question (from Paper IV)

IV is building a dynamical, k-resolved vacuum-polarization extractor: a Brillouin-zone
sum of the second-order field-induced eigenphase shift of the A=1 two-band transfer
operator `T(k)`, aiming to reproduce VIII's geometric blocks `eps = P = {1,4,4}` and
`mu^-1 = Q_B = {4,4,16}` from the dynamics. It needs the **mode-filling prescription**:
which band(s) of `T(k)` form the "sea", and with what weight. Paper I got the induced
action as a pure holonomy with **no explicit sea sum**, so the prescription is the one
that reproduces that holonomy. This is a theory choice, not a numerics knob.

## The answer

**Sum the second-order eigenphase shift of the PHYSICAL (propagating) band only, unit
weight per Brillouin-zone point.** The physical band is the eigenvalue continued from
`lambda = 1 + i*omega` at `k = 0` (`|lambda| ~ 1`; -> the light cone as `omega -> 0`);
the doubler is heavily damped (`|lambda| ~ sin^2(omega/2) -> 0`).

## Why (the proof)

From the tick rule (dcl-core `core3d/hop.py`, even then odd tick), in the `(R, L)`
basis at wavevector `k`:

    M_even = [[i s, c S_RGB(k)],[0, 1]],   M_odd = [[1, 0],[c S_CMY(k), i s]],
    T(k) = M_odd M_even,   s = sin(dphi/2), c = cos(dphi/2), dphi = omega + V(x).

Both factors are **triangular**, so `det M_even = det M_odd = i s` and

    det T(k) = - sin^2(dphi/2),

**independent of k and of the hop structure factor**. Therefore:

1. The MAGNETIC field (which enters only through the Peierls phase in `S`) is
   **invisible to `det T`**; the ELECTRIC field enters `det T` only as the on-site
   `sin^2((omega+V)/2)`. So the full **two-band** trace `Tr ln T = ln det T` has **no
   Maxwell content** -- magnetically zero, electrically only a local `V^2` mass
   renormalization (not the gradient permittivity `eps ~ (grad V)^2`).
2. Since `ln lambda_phys + ln lambda_doubler = ln det T` is field-fixed, the two bands
   respond **exactly oppositely**: `d ln lambda_phys = - d ln lambda_doubler` (verified
   to `1e-15`). The induced Maxwell action is thus a **single-band** response.
3. The doubler-only choice gives **minus** the action, so the sign/identity matters: it
   is the **physical** band. (Its `k -> 0` limit is the propagating photon-like mode.)

The **tensor structure** `{4,4,16}`/`{1,4,4}` is then guaranteed: the field enters
`S_RGB(k)` through the same hop vectors `V_a` that build VIII's geometric holonomy, so
the physical band's second-order response carries the same `V_a`-projection structure.
The **overall scale** is the one-loop `1/g^2` prefactor that Paper I / VIII already
defer. The anchor is: reproduce `{4,4,16}` magnetically (IV's acceptance test).

## How this maps method (a) <-> method (b)

Method (a) (VIII): the induced action IS the plaquette holonomy -- geometric, no sea
sum. Method (b) (IV): the induced action is the BZ eigenphase sum `-Tr ln T`. They agree
because the two bands cancel in `det T`, leaving only the physical band -- and the
physical band's second-order eigenphase shift **equals** the geometric holonomy. Paper
I's "no explicit sea sum" is exactly this cancellation: there was never a nontrivial
two-band sea; only the propagating band contributes, and it contributes the holonomy.

## Scope note (engine limitation, from IV)

core3d has no dynamical gauge field -- `external_potential` / `vector_potential` are
STATIC backgrounds. The induced action here is the second-order response of the MATTER
transfer operator to a static background; there is no literal propagating photon to
clock. IV's "dynamical" content is the A=1-survival of the induced-action anisotropy in
a matter observable + the Fresnel dispersion verdict of the `(eps, mu^-1)` tensors. VIII's
(held) intro/conclusion must not claim a literal dynamical-photon dispersion.
