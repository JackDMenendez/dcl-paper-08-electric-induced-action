# The electric induced-action block: derivation plan + result

**Status:** DERIVED + ENGINE-CONFIRMED (2026-07-16). Method (a) succeeds; `eps=P` is
extracted off the real engine coupling by `exp_01` (mirror of `exp_04`). Birefringence
verdict = CANCELS **conditionally** (airtight given `eps=P`, now engine-verified). Rows:
electric block + covariant completion PASS; verdict PART (speed-anisotropy + Paper IV
large-N remain). Referee-reviewed 2026-07-16.
**Purpose:** Record the problem, the E/B asymmetry that forces new theory, the two
candidate derivation methods, the consistency anchor, and now **the result** — so a
focused session can start without re-deriving the context.
**Verifier:** `src/utilities/electric_induced_action.py` (all checks PASS).
**Cited by:** `paper/sections/audit_table.tex` (electric-block rows); `CLAUDE.md`.

---

## RESULT (2026-07-16) — method (a) succeeded

Method (a) worked; the pessimistic prior in the "asymmetry" section below was too strong.
The on-site phase advance `delta_phi = omega + V(x)` (dcl-core `PhaseOscillator`,
`H = omega + V(x)`) **is itself the temporal link** (a site joined to itself at the next
tick), so a **temporal plaquette** spanned by one hop vector `V_a` and the tick direction
*does* close on the bipartite lattice. Its uniform-field holonomy is `(V_a . E) * a_t`
(with a static uniform potential `V(x) = -E . x`, `V(x) - V(x+V_a) = E . V_a`), where `a_t`
is the tick's temporal extent — **not unit weight**. There **is** an electric loop; it just
uses one spatial direction, where the magnetic loop uses a pair.

**Electric block (permittivity structure).** Summing the temporal-plaquette flux over the
three hop directions:

- `epsilon = a_t^2 * P`, with `P = sum_a V_a V_a^T = [[3,-1,1],[-1,3,1],[1,1,3]]`,
- eigenvalues `{1, 4, 4}`, optical axis `(1,1,-1)` **SUPPRESSED** to 1 (perp plane at 4).

This is the exact mirror of the magnetic `{4,4,16}` (axis **enhanced**; the magnetic
plaquette instead carries the spatial area `~a^2`), and its axis-suppression sign
reproduces Paper IV `exp_03a`. **The overall electric-vs-magnetic normalization carries an
undetermined lattice-anisotropy factor `~(a_t/a^2)^2` and the open `1/g^2` prefactor** — it
sets the common photon speed but, per the verdict, does not affect birefringence. We set
`a_t = 1` to display the structure `P`.

**Engine-confirmed (closed 2026-07-16).** The mirror of `exp_04` now exists **in this
paper** — `src/experiments/exp_01_electric_permittivity_extraction.py` — importing
`dcl_core.core3d` as the engine. It reads `P = {1,4,4}` (axis suppressed) off the engine's
**real `HopOperator.step` output**: seeding a uniform real probe state, the on-site term
`i sin(delta_phi/2) psi_R` is purely imaginary while the kinetic hop is real, so
`Im(psi_R_new)/psi_R = sin(delta_phi/2)` recovers `delta_phi = omega + V(x)` (to 1e-19)
straight from the tick evolution — a sign error or dropped `external_potential` would break
it. From that it reads `P`, confirms `P`,`Q_B` (same engine, `exp_04` route) commute + are
reciprocally ordered (adjugate structure), confirms `omega` cancels in the loop (`P`
mass-independent), and verifies the tick weight `a_t=1` (measured via the fidelity check,
not assumed). This is why the electric-block and covariant-completion rows are PASS.
*(Referee-audited: an earlier draft computed `P` off a synthetic field and only looked like
an engine test; it was rewritten to genuinely read `hop.step`.)* *(The experiment lives
here, not in dcl-core: it backs this paper's audit row, so it belongs with the paper — the
same reason the magnetic `Q` is re-derived in-repo. dcl-core needs no new engine work; a
`uniform_E_potential` sibling for `core3d.gauge` is an optional upstream tidy-up, currently
local to `exp_01`.)*

**Covariant completion — the adjugate theorem.** The two blocks are not independent. For
*any* three hop vectors,

    Q_B = sum_{a<b}(V_a x V_b)(V_a x V_b)^T = adj( sum_a V_a V_a^T ) = adj(P).

The magnetic inverse-permeability tensor **is the adjugate of the electric permittivity
tensor**: `mu^{-1} = adj(epsilon)`. (Proven symbolically for general vectors in the
verifier — it is the identity `sum(V_a x V_b)(V_a x V_b)^T = adj(sum V_a V_a^T)`.)
Consequently, for every principal axis `i`,

    epsilon_i * (mu^{-1})_i = epsilon_i * (adj epsilon)_i = det(epsilon),

so the **impedance product is isotropic** even though each block is anisotropic (opposite
senses about the same axis).

**Birefringence verdict — CANCELS (conditional; airtight given the identification).**
IF the macroscopic response tensors are `(epsilon, mu^{-1}) = (P, Q_B)`, the photon
dispersion `det(K mu^{-1} K + w^2 epsilon) = 0` factors (for general `k`) as a
**double transverse root**

    w^2 = k^T epsilon k     (both polarizations),

so the polarization split is `Delta(w^2) proportional to |epsilon_a mu_a - epsilon_p mu_p|
= |1*16 - 4*4| = 0`. **Gauge-sector vacuum birefringence cancels.** The split formula
depends only on the *anisotropy ratios* (fixed by geometry via the adjugate relation) and
not on the overall block scales, so the verdict is **invariant under independent rescaling
of `epsilon` and `mu^{-1}`** — immune to the undetermined `a_t` / `1/g^2` factors — and
holds for any hop vectors. (Referee-checked: the perfect-square factorization holds for a
general symmetric `epsilon` with `mu^{-1} = adj(epsilon)`; it does not even require the two
blocks to share eigenvectors.) This **conditional** is the load-bearing theorem. What is
*not* yet earned is the **unconditional** physical verdict, because it rides on `epsilon=P`
(analytic-only; see Outstanding above).

**Caveat — a LARGE effect, foregrounded (referee point E).** The shared dispersion
`w^2 = k^T epsilon k` is direction-dependent: `v^2(k)` ranges over `epsilon`'s eigenvalues
`[1,4]` — an **order-unity (factor ~2 in speed) directional anisotropy of the vacuum `c`**,
affecting both polarizations equally. This is a speed anisotropy, *not* birefringence, but
it is not small. Note the tension: the standard `O_h` average that would remove it
(`Tr(P)/3 . I` and `Tr(Q_B)/3 . I` are both isotropic) also makes the birefringence
cancellation **trivial**; the non-trivial, averaging-independent cancellation lives at the
un-averaged operator level, where this speed anisotropy is also present. So the result must
**not** be sold as a clean "positive null consistent with polarimetry" — the same order
predicts an order-unity directional `c`-anisotropy that itself needs an isotropy-restoration
story. That story is a separate open question, out of scope for the birefringence verdict.

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

## Equations are generated, not transcribed

When the electric block and the covariant `(epsilon, mu^{-1})` form are derived, emit their
LaTeX straight from the verified SymPy expressions (`sympy.latex()`) into
`paper/sections/generated/*.tex` and `\input` them from the section files -- so the paper's
equations are provably identical to what the verification script computed. The magnetic `Q`
already does this (`write_latex_fragments()` -> `generated/magnetic_Q.tex`); the electric
results follow the same route. See `CLAUDE.md` "SymPy-generated equations".

## Open questions — status

1. **Does a gauge-invariant electric loop exist?** YES — analytically (the on-site phase
   advance is the temporal link; the temporal plaquette closes) **and engine-verified**:
   `exp_01` reads `P` off `HopOperator.step`, confirms the recovered `delta_phi` reproduces
   `omega + V(x)` (coupling fidelity) and that `omega` cancels in the loop. (Gauge
   invariance of `V(x)-V(x+v_a)` under a global shift is trivial and is not separately
   tested.) Resolved.
2. **Does the residual anisotropy sit on the same `(1,1,-1)` axis as the magnetic block?**
   YES — `epsilon = P` and `mu^{-1} = Q_B` commute (share the eigenbasis): common axis
   `(1,1,-1)`, both isotropic (degenerate) in the perpendicular plane. **Still open:** the
   `O_h`-averaged isotropy of the *common photon speed* — the factor-~2 directional
   `c`-anisotropy (caveat above) needs its own isotropy-restoration story. Separate from the
   birefringence verdict.
3. **Does the axis contrast cancel in the photon action (not just the density)?** YES
   (conditional on `epsilon=P`). The photon dispersion has a double transverse root; the
   polarization split vanishes exactly via the adjugate relation. This is the paper's
   verdict — earned as a conditional theorem, pending the engine cross-check for the
   unconditional form.

## Pointers

- Magnetic anchor: Paper I App. B; dcl-core `exp_04` / `data/exp_04_induced_gauge_Q_tensor.log`.
- Closest existing derivation to extend: Paper II
  `notes/induced_gauge_action_nonabelian.py` / `notes/induced_gauge_action_nonabelian.md`.
- Downstream consumer + screen finding: Paper IV
  `notes/exp_03_R4_cancellation_screen_spec.md` (§4a/§7); screen prototype `exp_03a`
  (paper-04 commit `a238896`).
