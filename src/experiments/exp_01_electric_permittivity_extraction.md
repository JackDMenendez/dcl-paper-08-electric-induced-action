# exp_01 — electric permittivity block from the engine's on-site coupling

**Backs audit rows:** "Electric induced-action block (permittivity `eps = P =
{1,4,4}`, axis suppressed)" and the covariant-completion / birefringence-verdict
rows it feeds (`paper/sections/audit_table.tex`).
**Script:** `src/experiments/exp_01_electric_permittivity_extraction.py`
**Output:** `data/exp_01_electric_permittivity_extraction.{log,npy}`

## What it is

The engine-level counterpart of the analytic derivation in
`src/utilities/electric_induced_action.py`. It is to the **electric** block what
dcl-core `exp_04` is to the **magnetic** block: it reads the induced-action tensor
off the engine's *actual* gauge coupling rather than re-asserting the algebra.

The A=1 engine (`dcl_core.core3d`) couples the electric field **on-site**: the
hop's `external_potential` IS the temporal potential `A_0`, entering the tick rule
as `delta_phi = omega + V(x)` (see dcl-core `hop.py`, `HopOperator.step`). A
static, spatially varying `V(x)` IS a background electric field (`E = -grad A_0`).

**How `P` is read off the actual engine (not a synthetic field).** We seed a
uniform, *real* probe state (`psi_R` uniform real) and run one real `hop.step`.
The on-site term `i sin(delta_phi/2) psi_R` is purely **imaginary** while the
kinetic hop is purely real, so

```
Im(psi_R_new) / psi_R = sin(delta_phi/2)   =>   delta_phi(x) = omega + V(x)
```

is recovered *directly from the engine's step output*. A sign error or a dropped
`external_potential` inside `hop.step` would corrupt it — the number is not
computable without exercising the tick operator. The temporal-plaquette holonomy
is then read off the **engine-recovered** `delta_phi`:

```
Theta_a(x) = delta_phi(x) - delta_phi(x+V_a) = V(x) - V(x+V_a) = V_a . E
```

(the `omega` mass term cancels around the loop). Summed over the three RGB
directions, `density_E = sum_a Theta_a^2 = E^T P E`, and `P` is extracted linearly
in `E` exactly as `exp_04` extracts `Q_B` linearly in `B`.

## What "PASS" means

All of the following, from the **same engine**:

1. **Structure.** `P` (read off `hop.step`) has eigenvalues proportional to
   `{1, 4, 4}`, and the optical axis `(1,1,-1)` is the **suppressed** (eigenvalue-1)
   eigenvector — the mirror of the magnetic `{4,4,16}` (axis enhanced). Sign
   matches Paper IV `exp_03a`.
2. **Adjugate structure.** `P` and `Q_B` (same engine; `Q_B` via the `exp_04`
   route through `uniform_B_potential`) **commute** (`[P,Q_B]=0` to round-off) and
   are **reciprocally ordered** — `P`'s suppressed axis is `Q_B`'s enhanced axis.
   The engine-level fingerprint of `Q_B = adj(P)`.
3. **Engine coupling fidelity.** The recovered `delta_phi` reproduces `omega+V(x)`
   to round-off — i.e. `hop.step` applies the electric potential with **unit tick
   weight `a_t = 1`**. This is the check that actually exercises `hop.step`.
4. **Mass-term cancellation.** `P` is independent of `omega` (extracted at `omega=0`
   and `omega=0.3` to round-off) — the mass phase cancels around the temporal loop,
   so the extraction reads `E`, not the mass.

Observed: `P = [[3,-1,1],[-1,3,1],[1,1,3]]`, eigenvalues `[1,4,4]`, suppressed axis
`(1,1,-1)`; `[P,Q_B] ~ 4e-15`; coupling fidelity `~4e-19`; mass-cancellation
`~2e-14`.

## What it deliberately does NOT settle

- **Relative electric/magnetic scale.** The tick weight `a_t = 1` IS pinned above
  (the fidelity check), but the *absolute* magnetic normalisation is not — the
  electric-vs-magnetic ratio still carries the undetermined `1/g^2` coupling that
  Paper I left open. This is immaterial to the birefringence verdict (invariant
  under independent rescaling of `eps` and `mu^{-1}`) but is not a prediction of `c`.
- **The factor-~2 common-mode speed anisotropy** (`v^2(k) in [1,4]`) is a separate,
  un-resolved isotropy-restoration question — not birefringence.

Both are documented in `src/utilities/electric_induced_action.py` and
`notes/electric_block_derivation.md`.

## Relation to `exp_04`

`exp_04` (dcl-core) extracts `Q_B` from `uniform_B_potential` + the Peierls link
convention. This experiment reuses that exact route for `Q_B` (the magnetic
cross-check) and adds the temporal-sector analogue for `P`, so both tensors — and
the adjugate relation between them — come from one engine.
