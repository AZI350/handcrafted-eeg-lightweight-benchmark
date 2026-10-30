# Handcrafted EEG Lightweight Benchmark

Reproduction code for **“When Do Handcrafted Features Help Lightweight EEG Networks? Evidence From Five Emotion Recognition Datasets.”**

The repository evaluates lightweight one-dimensional EEG models on DREAMER, FACED, SEED, SEED-IV, and SEED-V. It compares EEG-only, feature-only, direct-fusion, and feature-based auxiliary-supervision configurations under within-subject and cross-subject protocols. The seven experiment groups cover participation mode, early stopping, multidomain feature combinations, auxiliary-loss weight, lightweight backbone, window duration, channel reduction, perturbation behaviour, and deployment cost.

## Repository name

Recommended GitHub repository name: **`handcrafted-eeg-lightweight-benchmark`**

Recommended description:

> Reproduction code for a five-dataset benchmark of handcrafted features in lightweight EEG emotion recognition.

## Important scope

- Dataset files are **not** redistributed. Obtain each dataset from its official source and comply with its licence or data-use agreement.
- DREAMER/FACED and the SEED series use separate preprocessing/training adapters because their labels and released formats differ.
- Raw Macro-F1 values are not pooled across binary, three-class, four-class, and five-class tasks.
- The complete formal study is computationally expensive. Run the syntax check and one-fold smoke tests before launching all five folds and five seeds.
- The source-data CSV files in `analysis/data/` are real archived outputs used for manuscript figures; they are not simulated examples.

## Layout

```text
configs/                   fixed paper protocol and seed lists
data/                      ignored dataset mount points (no data committed)
preprocessing/             DREAMER, FACED, and window-length preparation
pipelines/dimensional/     DREAMER/FACED binary valence/arousal experiments
pipelines/seed_series/     SEED/SEED-IV/SEED-V multiclass experiments
analysis/                  figure scripts and manuscript source-data CSV files
docs/                      data access, experiment matrix, and Origin notes
tests/                     repository-level static verification
reproduce.py               small common entry point
```

## Environment

The archived server runs used Ubuntu 22.04, Python 3.10, PyTorch 2.1.2, and CUDA 11.8. Install PyTorch for your CUDA/CPU platform first, then install the remaining packages:

```bash
python -m pip install -r requirements.txt
python -m pip install torch==2.1.2 --index-url https://download.pytorch.org/whl/cu118
```

Record the resolved environment before formal training:

```bash
python -m pip freeze > environment_freeze.txt
python tests/verify_repository.py
```

## Data preparation

See [`docs/DATASETS.md`](docs/DATASETS.md). The expected prepared layout is:

```text
data/
  dimensional_1s/DREAMER/*.npz
  dimensional_1s/FACED/*.npz
  dimensional_windows/window_1s/{DREAMER,FACED}/*.npz
  dimensional_windows/window_2s/{DREAMER,FACED}/*.npz
  dimensional_windows/window_4s/{DREAMER,FACED}/*.npz
  seed_prepared/w1/{SEED,SEED_IV,SEED_V}/*.npz
  seed_prepared/w2/{SEED,SEED_IV,SEED_V}/*.npz
  seed_prepared/w4/{SEED,SEED_IV,SEED_V}/*.npz
```

Examples:

```bash
python preprocessing/preprocess_dreamer.py --source /path/to/DREAMER.mat --output-root data/dimensional_1s
python preprocessing/preprocess.py --dataset FACED --archive /path/to/Data.zip --output-root data/dimensional_1s
python preprocessing/prepare_windows.py --input-root data/dimensional_1s --output-root data/dimensional_windows

python pipelines/seed_series/prepare.py --dataset SEED --archive /path/to/SEED.zip --output data/seed_prepared --scratch scratch
python pipelines/seed_series/prepare.py --dataset SEED_IV --archive /path/to/SEED_IV.zip --output data/seed_prepared --scratch scratch
python pipelines/seed_series/prepare.py --dataset SEED_V --archive /path/to/SEED-V.zip --output data/seed_prepared --scratch scratch
```

## Smoke tests

Static and synthetic checks:

```bash
python tests/verify_repository.py
python reproduce.py check --family dimensional
python reproduce.py check --family seed
```

One-fold, one-seed, one-epoch checks using prepared data:

```bash
python reproduce.py smoke --family dimensional --data-root data/dimensional_windows
python reproduce.py smoke --family seed --data-root data/seed_prepared
```

## Formal seven-experiment runs

Both suites print their complete plans without training unless `--execute` is supplied.

```bash
python pipelines/dimensional/suite.py --windows-root data/dimensional_windows
python pipelines/seed_series/suite.py --data-root data/seed_prepared
```

After checking `last_plan.json`, launch the formal runs:

```bash
python -u pipelines/dimensional/suite.py --windows-root data/dimensional_windows --execute
python -u pipelines/seed_series/suite.py --data-root data/seed_prepared --execute
```

Use `tmux` or `screen` on a remote server. Completed configurations are retained in separate output folders; do not mix smoke and formal results.

## Regenerate manuscript figures

The Matplotlib path is cross-platform and does not require Origin:

```bash
python analysis/make_figures.py
```

It writes PDF/SVG vector files and PNG previews to `analysis/figures/`. The optional Origin workflow is documented in [`docs/ORIGIN_FIGURES_zh.md`](docs/ORIGIN_FIGURES_zh.md) and requires a licensed local Origin installation.

## Reproducibility boundary

The repository fixes folds, split seed, training seeds, feature definitions, and experiment grids. GPU kernels and dependency builds can still introduce small numerical differences. Five-seed intervals quantify training randomness under fixed splits; they are not confidence intervals over all possible participants. See [`docs/EXPERIMENTS.md`](docs/EXPERIMENTS.md) for the exact matrix and interpretation limits.

## Citation

Use `CITATION.cff` after replacing the publication-status fields with the final journal citation and DOI.

## Licence

The source-code licence has intentionally not been assumed. Choose and add a licence before making the GitHub repository public; see `LICENSE_TO_CHOOSE.md`. Dataset licences remain separate in all cases.
