# dcl-paper-08-electric-induced-action — ARCHIVED (merged into Paper IV)

> **⚰️ TOMBSTONE (2026-07-17).** This repository is **archived, read-only**. Paper VIII
> (the electric induced-action block) has been **merged into Paper IV**, homed in
> **[`dcl-paper-04-optical-axis-birefringence`](https://github.com/JackDMenendez/dcl-paper-04-optical-axis-birefringence)**.
> The shared optical axis $(1,1,-1)$ is the natural unity of the two effects, so the
> gauge-sector electric block now lives alongside the kinematic dispersion channel in a
> single paper:
>
> *Optical-Axis Anisotropy on the A=1 Discrete Causal Lattice: Kinematic Dispersion and
> the Gauge-Sector Birefringence Cancellation.*
>
> **Where the content went.** VIII's SymPy-verified derivation was folded into paper-04
> with full history via `git subtree` (paper-04 merge commit `bdc7bf3`):
> - derivation section → paper-04 `paper/sections/gauge_sector.tex` (unified);
> - verification scripts → paper-04 `src/utilities/` (`electric_induced_action.py`,
>   `trlnT_prescription.py`, `ward_safe_diagnosis.py`) and
>   `src/experiments/exp_04_electric_permittivity_extraction.py`;
> - generated equation fragments → paper-04 `paper/sections/generated/`;
> - derivation notes → paper-04 `notes/`.
>
> **Why merged (external review, 2026-07-17).** The review returned Paper VIII =
> major-revision and preferred a single stronger paper; the author chose to merge. The
> review's corrections (induced-action → geometric candidate; `det(ε)` prefactor;
> proportional closure `μ⁻¹ = γ·adj(ε)`; the `O_h`-average / exact-adjugate fix;
> "constitutive closure"; the three-way audit split) were applied in the merged paper.
>
> **Do not develop here.** New work belongs on Paper IV (board issue #13). This repo is
> retained only for provenance; its history is also preserved inside paper-04.

---

*(Original README below, for the record.)*

# dcl-paper-08-electric-induced-action

**Paper VIII of the A=1 Discrete Causal Lattice series.**

Derives the **electric (permittivity) block of the lattice's induced gauge action** — the
permittivity tensor and the covariant completion of the gauge response — so that the
gauge-sector photon dispersion (and the birefringence verdict) becomes computable. See the
merged Paper IV for the current, review-corrected treatment.
