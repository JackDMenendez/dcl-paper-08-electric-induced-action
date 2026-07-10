# The electric induced-action block: derivation plan

**Status:** DRAFT (plan; derivation not started)
**Purpose:** Record the problem, the E/B asymmetry that forces new theory, the two
candidate derivation methods, and the consistency anchor — so a focused session can start
without re-deriving the context.
**Cited by:** `paper/sections/audit_table.tex` (electric-block rows); `CLAUDE.md`.

---

## The problem in one line

Derive the lattice's **electric** induced-action block (the permittivity `epsilon`) and the
covariant completion of the gauge response, matching the already-exact **magnetic** block, so
the gauge-sector photon dispersion — and Paper IV's birefringence verdict — becomes computable.

## The asymmetry that makes this new theory

The A=1 tick rule couples the two fields on different footings:

- **Magnetic `B`** enters as a **spatial link phase** `exp(i A . v)` on the hop (Peierls
  substitution). A closed spatial plaquette gives a gauge-invariant **Wilson-loop holonomy**;
  its `O(B^2)` induced action is the magnetic `Q`-tensor
  `Q = [[8,4,-4],[4,8,-4],[-4,-4,8]]`, eigenvalues `{4,4,16}`, optical axis `(1,1,-1)`
  (Paper I App. B; reproduced exactly by dcl-core `exp_04`, `max|Q - Paper_I_Q| = 0`).
- **Electric `E`** enters as an **on-site, mass-like** phase advance
  `delta_phi(x) = omega + V(x)` (a scalar/temporal potential), **not** a spatial link phase.
  So there is **no closed electric plaquette / no electric Wilson-loop analog** to read a
  clean holonomy from.

Two consequences:
1. The electric action block (`epsilon`) is **absent from Paper I and Paper II** — Paper II
   only reuses the magnetic `Q` for the coupling ratio; it never builds the electric sector.
2. There is **no symmetry shortcut** from magnetic to electric. Relating `epsilon` to `mu^{-1}`
   would require the Lorentz boosts, but the framework establishes only the spatial point group
   `O_h`; the boosts `K_a` are **not** in the discrete per-site centralizer (Paper II audit
   table). Boost covariance is continuum-emergent, not a discrete symmetry we can lean on here.

## The physical stake (binary)

Completing the response to a covariant `(epsilon, mu^{-1})` pair decides the vacuum
birefringence about `(1,1,-1)`:
- **cancels** -> the framework *predicts the absence* of gauge-sector birefringence
  (consistent with polarimetry; a positive null); or
- **persists** -> a genuine, testable (near-falsifying) prediction.

Prior hint (not a verdict): Paper IV's static screen `exp_03a` found magnetic response
**axis-enhanced** and electric **axis-suppressed** about `(1,1,-1)` — *opposite senses*,
suggestive of cancellation — but the **density** response it measured is not the photon
**action**, so the sign of the effect on the dispersion is not yet established.

## Candidate methods

- **(a) Extend Paper I App. B to the electric/temporal-plaquette sector.** Build the
  temporal (space-time) plaquette holonomy for the on-site electric coupling and read off its
  quadratic form. Risk: because `E` is on-site (no spatial loop), the "temporal plaquette" may
  degenerate; part of the work is establishing whether a gauge-invariant loop exists at all,
  or whether the electric block must be read from the on-site sector directly.
- **(b) Action-level spectral (`Tr ln T`) probe.** Expand the one-loop effective action
  `-Tr ln T[A, A_0]` of the tick operator `T` to second order in the background and extract the
  coefficients of the electric invariants directly, bypassing the need for an explicit loop.
  Heavier, but does not presuppose an electric holonomy exists.

Start with (a) to expose the obstruction concretely; fall back to (b).

## Consistency anchor (do not break)

Any derivation must reproduce the magnetic block as the `B`-only limit: `Q = {4,4,16}`,
axis `(1,1,-1)`. `src/utilities/electric_induced_action.py` checks this first (the anchor
passes today); the electric block is the new content.

## Open questions

1. Does a gauge-invariant electric loop exist on the bipartite lattice, or is the electric
   response irreducibly on-site (method (a) degenerates -> method (b))?
2. Is the effective `(epsilon, mu^{-1})` isotropic after `O_h` averaging, and does the
   residual operator-level anisotropy sit on the same `(1,1,-1)` axis as the magnetic block?
3. Does the axis contrast **cancel** in the photon action (not just the density)?

## Pointers

- Magnetic anchor: Paper I App. B; dcl-core `exp_04` / `data/exp_04_induced_gauge_Q_tensor.log`.
- Closest existing derivation to extend: Paper II
  `notes/induced_gauge_action_nonabelian.py` / `notes/induced_gauge_action_nonabelian.md`.
- Downstream consumer + screen finding: Paper IV
  `notes/exp_03_R4_cancellation_screen_spec.md` (§4a/§7); screen prototype `exp_03a`
  (paper-04 commit `a238896`).
