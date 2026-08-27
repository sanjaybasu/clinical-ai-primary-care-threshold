# Clinical AI Primary Care Threshold

Reproducible code for:

**How Much Benefit Would Clinical Artificial Intelligence Need to Match the Mortality Cost of Primary Care Loss, Without Widening Inequality? A Decision-Analytic Threshold Analysis**

Sanjay Basu, Ishani Ganguli, Asaf Bitton, Robert L. Phillips Jr., Zirui Song, Russell S. Phillips, Bruce E. Landon. Submitted to *Medical Decision Making*.

## What this is

A decision-analytic threshold model. Given the excess mortality associated with the loss of primary care physicians (as a calibration benchmark, not a causal target), the model derives:

1. **The required effect** — the per-patient hazard ratio clinical AI would need to demonstrate, at a given reach, to match that benchmark (the quality pathway).
2. **The required throughput** — the per-physician patient-throughput increase clinical AI would need to deliver to add equivalent physician capacity (the capacity pathway), formalizing a capacity-discount factor (φ) for the uncertain mortality value of throughput-derived versus hiring-derived capacity.
3. **The equity condition** — the reach clinical AI needs in high-vulnerability communities so that deploying AI does not widen the mortality difference between high- and low-vulnerability communities.

All three are evaluated with probabilistic sensitivity analysis and compared against evidence for six clinical AI types (disease-specific, generalist chatbot, previsit, remote patient monitoring, gap-closure, provider-facing).

## Repository contents

```
code/
  threshold_model.py   Model: reads code/inputs.json, writes every value in results/
  inputs.json           All model inputs (base case, range, source), single source of truth
make_figures.py         Regenerates figures/figure1-4 from results/
results/                 Pre-computed model outputs (CSV/JSON/NPY), one file per analysis
figures/                 Pre-generated figures (PNG), matching the manuscript
requirements.txt
LICENSE                  MIT
```

## Reproducing the results

```bash
pip install -r requirements.txt
python3 code/threshold_model.py   # regenerates every file in results/
python3 make_figures.py           # regenerates every file in figures/
```

The model is deterministic under a fixed random seed (`inputs.json`, `psa.seed`). Every reported value in the manuscript and appendix is generated from `results/`; `results/rederived_threshold_provenance.json` records the input hash, seed, and software versions for the run that produced the committed outputs.

## Data

No restricted or individual-level data are used. All inputs are drawn from published, cited sources or public surveillance data (CDC WONDER; CDC Social Vulnerability Index), listed with source and evidence grade in `code/inputs.json` and in the manuscript's Table 1 and Supplementary Appendix eTable S1. This repository contains code and derived (non-patient) analysis outputs only.

## License

MIT License (see `LICENSE`).
