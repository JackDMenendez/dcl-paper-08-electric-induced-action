# dcl-paper-08-electric-induced-action

**Paper VIII of the A=1 Discrete Causal Lattice series.**

Derives the **electric (permittivity) block of the lattice's induced gauge action** — the
covariant completion the magnetic `{4,4,16}` Wilson-loop lacks — so that Paper IV's
gauge-sector photon-dispersion birefringence *verdict* becomes computable. A sympy-verified
symbolic derivation.

## Why this paper exists

The A=1 lattice couples the two electromagnetic fields **asymmetrically**:

- **Magnetic `B`** is a spatial link phase → a clean Wilson-loop holonomy → the exact
  magnetic induced-action `Q`-tensor (eigenvalues `{4,4,16}`, optical axis `(1,1,-1)`;
  Paper I Appendix B, reproduced by dcl-core `exp_04`).
- **Electric `E`** enters as an **on-site, mass-like** phase advance `δφ = ω + V(x)` — so
  there is **no electric Wilson-loop analog**.

The covariant electric action block (the permittivity `ε`) appears in **neither Paper I nor
Paper II**, and there is **no symmetry shortcut**: the framework establishes only the spatial
point group `O_h`, not the Lorentz boosts that would fix `ε` from the magnetic `μ⁻¹`. So the
electric block is genuinely new theory — this paper supplies it.

The physical stake is binary: completing the response to a covariant `(ε, μ⁻¹)` pair decides
whether the lattice's vacuum birefringence about `(1,1,-1)` **cancels** (framework consistent
— predicts no gauge-sector birefringence) or **persists** (a real tension). A static screen in
Paper IV (`exp_03a`) already hints at cancellation — magnetic axis-enhanced vs electric
axis-suppressed — but density response is not the photon action, so the verdict waits on this
derivation.

## Method (TBD)

- **(a)** Paper I Appendix B's magnetic plaquette approach extended to the electric/temporal
  plaquette sector.
- **(b)** an action-level spectral (`Tr ln T`) probe.

## Status

`v0.1-DRAFT` — scaffolded; derivation not started. Start at
[`notes/electric_block_derivation.md`](notes/electric_block_derivation.md) and
[`src/utilities/electric_induced_action.py`](src/utilities/electric_induced_action.py) (which
carries the magnetic `{4,4,16}` consistency anchor). Audit rows: magnetic anchor `PASS`;
electric block, covariant completion, and birefringence verdict `STUB`.

## Series context

- **Paper I** (`dcl`) — the magnetic `Q`-tensor anchor (App. B).
- **Paper II** (`dcl-paper-02-sm-derivation`) — gauge structure; closest existing derivation
  to extend (`notes/induced_gauge_action_nonabelian.py`).
- **Paper IV** (`dcl-paper-04-optical-axis-birefringence`) — the downstream consumer; its
  gauge verdict (and, by decision, its v1.0) gates on this paper. Board issue **#23** (project 6).

## Build / test

```sh
setup.cmd            # create .venv + install sympy/numpy/scipy/pytest + dcl_core@v0.3.0
build.cmd tests      # pytest
python -u src/utilities/electric_induced_action.py   # magnetic anchor check + electric stub
python audit_universe.py                             # PASS/STUB/FAIL roll-up
build.cmd paper      # pdflatex 3-pass + bibtex
```

## License

Paper text and figures: CC BY 4.0. Source (scripts and infrastructure): MIT (see `LICENSE`).
