<!-- markdownlint-disable MD022 MD025 MD033 MD060 -->
# CLAUDE.md -- Working Brief for Claude Code

> Project: Paper VIII -- The Electric Induced-Action Block

This file is the project memory for Claude Code. Keep it updated so a
new conversation can continue work without the full chat history.

---

## CURRENT STATUS (2026-07-16) -- v0.1-DRAFT (derivation done, analytic; PART)

**Headline result (analytic; referee-reviewed 2026-07-16).** Method (a) succeeded. The
electric block is `epsilon = P = sum_a V_a V_a^T`, eigenvalues `{1,4,4}`, optical axis
`(1,1,-1)` **suppressed** -- the exact mirror of the magnetic `{4,4,16}` (axis enhanced),
sign-consistent with Paper IV `exp_03a`. The covariant completion is the theorem
`mu^{-1} = Q_B = adj(epsilon)` (proven for general hop vectors). Given `(eps,mu^{-1}) =
(P,Q_B)`, the photon dispersion is a **double transverse root** `w^2 = k^T eps k`, so the
polarization split `~ |eps_a mu_a - eps_p mu_p| = |1*16-4*4| = 0`: **gauge-sector vacuum
birefringence CANCELS** -- prefactor-independent and geometry-general. Verifier:
`src/utilities/electric_induced_action.py` (all conditional checks PASS) + numeric sweep
(2e4 random `k`, split `< 1e-14`).

**Status of the referee's two gaps:**
1. **CLOSED (2026-07-16).** `eps = P` is now read off the **real engine evolution**, not
   analytic-only: `src/experiments/exp_01_electric_permittivity_extraction.py` recovers
   `delta_phi = omega + V(x)` from `HopOperator.step`'s output (`Im(psi_R_new)/psi_R =
   sin(delta_phi/2)`, to 1e-19) and reads `P = {1,4,4}` (axis suppressed) off THAT — so a
   sign error or dropped `external_potential` in the tick rule would break it. It also
   confirms `P`,`Q_B` commute + reciprocal (adjugate structure), that `omega` cancels in
   the loop (P is mass-independent), and that the tick weight is `a_t=1` (measured, not
   assumed). This is why the electric-block + covariant-completion rows are PASS.
   (Referee-audited 2026-07-16: an earlier version computed `P` off a synthetic field and
   only *looked* like an engine test; this was rewritten to genuinely read `hop.step`.)
2. **SHARPENED + DECOUPLED (2026-07-16).** The shared dispersion `w^2 = k^T eps k` gives a
   **factor-~2 directional anisotropy of the vacuum `c`** (common to both polarizations --
   NOT birefringence, but not small). Analysis in
   `notes/speed_anisotropy_and_isotropy_restoration.md` (verified in the utility): the
   optical axis `(1,1,-1)` IS the 4th cube body-diagonal, absent from the 3 hop axes, so the
   lattice is trigonal `D_3d`, not `O_h`. Averaging the blocks over the four diagonal domains
   restores `O_h` exactly (`<eps>=3I`, `<mu^-1>=8I`) -- the anisotropy averages away. Crucially
   the adjugate/birefringence cancellation holds in **every single domain** AND after the
   average, so it is **decoupled** from the speed anisotropy: however the vacuum-structure
   question resolves (single trigonal domain vs `O_h`-restored), birefringence still cancels.
   The verdict row stays PART for the *vacuum-structure* question + Paper IV's large-N
   classification -- NOT for any doubt about the cancellation.

**Headline claim (to be earned):** the A=1 lattice has a well-defined *electric*
induced-action block -- a permittivity `epsilon` and the covariant completion of the
gauge response -- derivable from the tick rule, matching the already-exact *magnetic*
block. **Now derived analytically AND engine-confirmed (block + completion PASS); only the
unconditional birefringence verdict remains PART.**

**Why this paper exists.** Paper IV's gauge-sector photon-dispersion birefringence
*verdict* cannot be rendered without it. The engine couples E and B **asymmetrically**:
magnetic `B` is a spatial link phase -> clean Wilson-loop holonomy -> the exact
magnetic `Q`-tensor (eigenvalues `{4,4,16}`, optical axis `(1,1,-1)`; Paper I App. B,
reproduced by dcl-core `exp_04`). Electric `E` enters as an **on-site, mass-like**
`delta_phi = omega + V(x)` -> there is **no electric Wilson-loop analog**. The covariant
electric action block (the `epsilon`) exists in **neither Paper I nor Paper II**, and
there is **no symmetry shortcut** (the framework establishes only spatial `O_h`, not the
Lorentz boosts `K_a`, which are not in the discrete centralizer -- Paper II audit table).
So the electric block is genuinely new theory. Discovered via Paper IV `exp_03a`
(the static E+B cancellation screen, paper-04 commit `a238896`): magnetic response is
**axis-enhanced**, electric **axis-suppressed** about `(1,1,-1)` -- opposite senses,
suggestive of a cancellation, but density response is NOT the photon action, so it is
not a verdict.

**Derivation method -- TBD (two candidates):**
- **(a)** Paper I App. B's magnetic plaquette approach extended to the
  electric/temporal-plaquette sector.
- **(b)** an action-level spectral (`Tr ln T`) probe.

**Audit rows:** magnetic anchor `PASS`; electric block and covariant `(epsilon, mu^{-1})`
completion now `PASS` (analytic + symbolic + **engine-extracted**, `exp_01`); birefringence
verdict `PART` (conditional proven + `eps=P` engine-verified; unconditional pends the speed
anisotropy + Paper IV large-N). Upgraded from all-`STUB` on 2026-07-16.

**Verification code lives in THIS paper, importing dcl-core as the engine** (not in
dcl-core): `src/experiments/exp_01_...` imports `dcl_core.core3d` and reads `P` off the
engine's `external_potential`, the same way it re-derives the magnetic `Q` in-repo. dcl-core
needs no new engine work (the electric `external_potential` coupling already exists); the
only tidy-up would be upstreaming a `uniform_E_potential` sibling into `core3d.gauge` (a
5-line helper, currently local to `exp_01`) -- optional, not blocking.

**Next concrete action:** the derivation + engine cross-check are done. Remaining:
(1) the paper body is still scaffold placeholders -- write the derivation section
(hand-written prose `\input`-ing the generated fragments); (2) the factor-~2 common-mode
speed-anisotropy / `O_h` isotropy-restoration question, which gates lifting the verdict row
to PASS and feeds Paper IV's large-N dispersion classification.

**Scope gate:** this paper is HELD-upstream of Paper IV v1.0 (PM ruling 2026-07-09):
Paper IV v1.0 waits on this verdict. Board issue #23 (project 6); blocks #13/#17/#18/#19.

---

## What This Project Is

A symbolic-derivation paper (Paper VIII of the A=1 Discrete Causal Lattice series). It
derives the electric sector of the lattice's induced gauge action -- the permittivity and
the covariant `F_{mu nu} F^{mu nu}` completion -- so that the gauge-sector photon
dispersion (and hence the birefringence verdict of Paper IV) becomes computable. Every
claim is backed by a runnable sympy script under `src/utilities/` whose printed output the
audit table cites; the magnetic `{4,4,16}` result is the built-in consistency anchor.

---

## Paper Title and Theme

**Title:** The Electric Induced-Action Block: Permittivity and the Covariant Completion
of the Lattice Gauge Response.

**Core theme / framing:** the lattice gives magnetism a clean Wilson-loop but hands
electricity an on-site mass-like coupling; completing the gauge response to a covariant
`(epsilon, mu^{-1})` pair is the missing derivation that decides whether the lattice's
vacuum birefringence cancels (framework consistent) or persists (a real tension). One
derivation, a binary physical consequence.

---

## Audit Table Status

| Row | Status | What it claims |
|---|---|---|
| Magnetic induced-action `Q`-tensor `{4,4,16}` (anchor) | PASS | Paper I App. B / dcl-core `exp_04`; `max\|Q - Paper_I_Q\| = 0`; re-derived here |
| Electric induced-action block `epsilon = P = {1,4,4}`, axis suppressed | PASS | analytic + symbolic + **read off `HopOperator.step`** (`exp_01`): `delta_phi=omega+V` recovered to 1e-19, `omega` cancels in loop, `a_t=1` verified; matches `exp_03a` sign |
| Covariant completion `mu^{-1} = Q_B = adj(epsilon)` | PASS | adjugate identity proven for general vectors; `exp_01` confirms `P`,`Q_B` commute + reciprocal from one engine. Relative `eps`:`mu^{-1}` scale (`a_t`,`1/g^2`) reported not fixed |
| Gauge-sector birefringence verdict: **cancels** (conditional) | PART | double-root theorem + 2e4-`k` numeric; `eps=P` engine-verified (`exp_01`); gates Paper IV #18/#17/#19. Remaining: residual factor-~2 speed anisotropy (isotropy restoration) + Paper IV large-N dispersion |

Mirror of `paper/sections/audit_table.tex` -- update both together. The claim-auditor
agent treats `audit_table.tex` as the authority.

---

## Conventions

- **Status legend.** `PASS` / `PART` / `STUB` / `FAIL` (front-matter of `paper/main.tex`).
- **File naming.** Sections: `paper/sections/<topic>.tex`. Notes: `notes/<topic>.md`.
  Derivation/verification scripts: `src/utilities/<topic>.py`. Experiments (if any):
  `src/experiments/exp_NN_<name>.{py,md}`.
- **Cross-references.** `\label{}` + `\ref{}`/`\autoref{}`, never hard-coded numbers.
- **Bibliography.** `paper/paper-bib/references.bib`; `\bibliographystyle{unsrt}`.
- **Verification-script discipline.** Every audit row that claims a derived result names a
  `src/utilities/*.py` (or `exp_NN`) whose printed output backs it. `python audit_universe.py`
  is the roll-up. A claim without a runnable verifier cannot be `PASS`.
- **SymPy-generated equations (use when it makes sense).** When a paper equation is a
  *derived* symbolic result -- not definitional prose -- generate its LaTeX from the verifying
  SymPy expression via `sympy.latex()` rather than hand-transcribing it. Emit the fragments to
  auto-generated `paper/sections/generated/*.tex` files that the section `.tex` files
  `\input`, so the paper's equations are provably identical to what the verification script
  computed and cannot drift from it. (Same pattern the generator-zoo uses to emit its
  catalogue table.) Apply judgment: this is for the load-bearing derived equations (the
  magnetic `Q`, the electric block, the covariant `(epsilon, mu^{-1})` form), not every inline
  symbol. `src/utilities/electric_induced_action.py::write_latex_fragments` is the working
  exemplar (it emits the magnetic `Q`); the electric block follows the same route once derived.

## Documentation convention for code

Every non-trivial line of physics code says what it **is** in the theory, not just what it
does in the program: name the mathematical object, cite the section/equation, use "IS" for
exact correspondences and "approximates" for continuum limits.

---

## Release flow

See `release_notes/README.md`. Summary: CI green -> update `CITATION.cff` -> draft
`release_notes/vX.Y*.md` -> **Zenodo deposit first (DOI into `\thanks{}` + `CITATION.cff`)**
-> commit -> tag -> GitHub Release.

---

## What NOT to Change

- The magnetic `{4,4,16}` anchor values -- they are inherited from Paper I App. B and are
  the consistency check; if a derivation step breaks them, the step is wrong, not the anchor.
- The audit table's role as canonical PASS/STUB authority.

---

## Cross-references (series)

- **Paper I** (`dcl`, doi:10.5281/zenodo.20078529) -- App. B magnetic `Q`-tensor (anchor).
- **Paper II** (`dcl-paper-02-sm-derivation`, doi:10.5281/zenodo.20292158) -- gauge structure;
  `notes/induced_gauge_action_nonabelian.py` is the closest existing derivation to extend.
- **Paper IV** (`dcl-paper-04-optical-axis-birefringence`) -- the downstream consumer; its
  gauge verdict gates on this paper. See its `notes/exp_03_R4_cancellation_screen_spec.md`.
- **dcl-core** (v0.3.0) -- `exp_04` (magnetic Q holonomy) is the numerical cross-check.

---

## Notes Index

`notes/README.md` -- conventions for notes/.

- `notes/electric_block_derivation.md` -- the derivation plan + result: the E/B asymmetry,
  the temporal-plaquette electric block, the adjugate completion, and the birefringence
  verdict. Start here.
- `notes/speed_anisotropy_and_isotropy_restoration.md` -- the one open caveat, sharpened:
  the optical axis is the 4th cube body-diagonal (trigonal `D_3d`); the `O_h` domain-average
  restores isotropy; the birefringence cancellation is decoupled from the speed anisotropy.
