# Clinical AI Primary Care Threshold

Reproducible code for:

**How Much Benefit and Reach Would Clinical Artificial Intelligence Need to Offset the Increased Mortality Associated With Primary Care Loss? A Decision-Analytic Threshold Analysis**

Sanjay Basu, Ishani Ganguli, Asaf Bitton, Robert L. Phillips Jr., Zirui Song, Russell S. Phillips, Bruce E. Landon. Submitted to *Medical Decision Making*.

## What this is

A closed-form threshold model. Using the excess mortality associated with the loss of primary care physicians as a calibration benchmark (not a causal target), the model derives:

1. **The required effect**: the per-patient all-cause mortality hazard ratio clinical AI would need, at a given reach, to match the benchmark, and equivalently the reach a given effect would need.
2. **The AI effect**: the blood pressure effect of AI-based mobile health (meta-analysis of randomized trials) transmitted to all-cause mortality through cardiovascular death (base case) or through the trial all-cause association (sensitivity), plus a hypothetical hazard ratio of 0.83.
3. **The required throughput**: the per-physician throughput increase that would add equivalent physician capacity, with a capacity-discount factor (φ).
4. **The equity condition**: the reach AI needs in high-vulnerability communities so that the mortality difference between high- and low-vulnerability communities is no larger than before the supply loss.

Both supply-loss scenarios (realized 2005-2015 decline; shortfall projected through 2038) are evaluated with probabilistic sensitivity analysis (20,000 samples, fixed seed).

## Repository contents

```
code/
  threshold_model.py   Model: reads code/inputs.json, writes every file in results/
  inputs.json          All model inputs (base case, range, source), single source of truth
make_figures.py        Regenerates figures/ from results/
results/
  threshold_canonical.json          All reported values, input hash, seed, software versions
  threshold_deterministic.csv       Point results by scenario and AI effect
  threshold_reach_grid.csv          Required hazard ratio by reach (Figure 1)
  threshold_equity_heterogeneity.csv  Equity threshold across low-vulnerability reach
  threshold_acceptability.csv       Probability the AI effect meets the requirement, by reach (Figure 3)
  threshold_capacity.csv            Required throughput across φ
  threshold_psa_*.npy               Probabilistic draws
figures/               Figures 1-3 (PNG), matching the manuscript
requirements.txt
LICENSE                MIT
```

## Reproducing the results

```bash
pip install -r requirements.txt
python3 code/threshold_model.py   # regenerates every file in results/
python3 make_figures.py           # regenerates every file in figures/
```

The model is deterministic under a fixed random seed (`inputs.json`, `psa.seed`). Every reported value in the manuscript and appendix comes from `results/threshold_canonical.json` and the CSV files beside it.

## Data

No restricted or individual-level data are used. All inputs are drawn from published, cited sources or public surveillance data (CDC WONDER; CDC Social Vulnerability Index), listed with source and evidence grade in `code/inputs.json` and in the manuscript's Table 1 and Supplementary Appendix eTable S1. This repository contains code and derived (non-patient) analysis outputs only.

## License

MIT License (see `LICENSE`).
