# Reproducing the main BWM paper

Start with [`notebooks/reproduce_bwm.ipynb`](../notebooks/reproduce_bwm.ipynb). It contains the results
checklist and an executable five-unit stimulus example. The target is
[IBL et al., Nature (2025)](https://doi.org/10.1038/s41586-025-09235-0); the prior-information companion
paper is outside this first reproduction slice.

## Code map

| Layer | Location | Role |
|---|---|---|
| Shared data access | `brainwidemap/bwm_loading.py` | Cohort queries; spike/trial loading; aggregate downloads; session/unit/region QC |
| Cohort snapshots | `brainwidemap/fixtures/` | Packaged CSV freezes from 2022 and 2023 |
| Single-cell statistics | `brainwidemap/single_cell_stats/` | Condition-combined Mann–Whitney/shuffle tests for stimulus, choice, feedback, and block |
| Population decoding | `brainwidemap/decoding/` | Numbered cache, fit, format, and summary stages; functions separate inputs, targets, nulls, fits, and outputs |
| Single-neuron encoding | `brainwidemap/encoding/` | Design matrix, cross-validation, leave-one-out fits, predictions; `pipelines/01`–`04` scale these up |
| Population trajectories | `brainwidemap/manifold/` | Per-insertion PETHs, pooled distances/latencies, region plots |
| Integration and figures | `brainwidemap/meta/` | Combines analysis outputs and assembles manuscript panels |
| Aggregate generation | `scripts/create_*_table.py` | Legacy staging scripts with machine-specific paths; not needed for the first example |
| Existing checks | `brainwidemap/test/` | Cohort hashes, QC, aggregate consistency, and seeded single-cell reference results |

An `eid` identifies a session; a `pid` identifies a probe insertion. Unit `uuids` are stable identifiers.
After `load_good_units`, spike cluster indices address the returned cluster table; its `cluster_id`
column is the original sorter ID. Do not join reindexed IDs across different probes.

The main analysis flow is **frozen cohort → processed recordings → QC/trial masks → analysis-specific
results → pooled regional summaries → figure assembly**. Figure 4 is stimulus, Figure 5 choice,
Figure 6 feedback, and Figure 7 wheel movement, as explicitly named in `meta/bwm_figs.py`. The notebook
catalog distinguishes confirmed labels from thematic or unverified panel mappings.

## Environments and dependency policy

`pyproject.toml` declares dependencies and package metadata, `.python-version` selects 3.10, and
`uv.lock` records resolved versions and Git revisions. The runtime is installed editable from this
fork. Dependency groups follow [uv's project model](https://docs.astral.sh/uv/concepts/projects/dependencies/).

```sh
uv sync --locked --group notebook --group dev
uv run --locked --group notebook jupyter lab notebooks/reproduce_bwm.ipynb
```

For an editor, select `.venv/bin/python`. If a named kernel is needed, install it explicitly:

```sh
uv run --locked --group notebook python -m ipykernel install --user --name brainwidemap --display-name "Brainwide map (.venv)"
```

Kernel registration is optional and writes a small user-level kernelspec. No kernel registration is
needed for the documented JupyterLab launch. See [uv's Jupyter integration](https://docs.astral.sh/uv/guides/integration/jupyter/).

The `decoding`, `encoding`, `manifold`, and `cluster` groups are selectable independently; repeat
selected groups on `uv run`, or use `--all-groups` when intentionally installing the entire stack.
On Linux x86_64, PyTorch comes from the explicit CPU wheel index. CUDA RAPIDS utilities in
`encoding/scripts/embed_saved_weights.py` are outside these CPU groups. External figure utilities
and precomputed results are also outside the locked analysis environment.

The behavioral-model dependency uses a fixed upstream revision with the legacy model namespace
expected by this code. Do not replace it with an unpinned upstream branch. Numerical compatibility
bounds are part of this fork's environment, rather than a claim to recover the authors' exact
historical environment. `requirements_frozen.txt` is preserved unchanged as historical evidence.

Regenerate the pip-compatible base export after dependency changes:

```sh
uv export --locked --no-default-groups --no-dev --no-emit-project --no-hashes --output-file requirements.txt
```

The export contains only base dependencies. To install the checkout using pip, use `pip install -e .`;
analysis groups are managed by uv. Keep the current environment and this export consistent through
`uv.lock`, rather than editing the export manually.

## What the first notebook executes

The notebook verifies the frozen cohort locally, then fetches the existing test example:

- `eid`: `15f742e1-1043-45c9-9504-f1e8a53c1744`
- `pid`: `3675290c-8134-4598-b924-83edb7940269` (`probe00`)
- QC: good units; 0.08–2.0 s reaction times; required-event checks; existing performance truncation.
- Unit selection: first five eligible units sorted by original cluster ID, chosen before testing.
- Statistic: existing `get_stim_time_shuffle`, 0–100 ms post-stimulus, 3,000 shuffles, NumPy seed 0.
- Plots: left/right positive-contrast stimulus PETHs, mean ± SEM. These descriptive curves do not
  condition on choice and block, whereas the statistical test does.

The small subset does not reproduce a brain-wide selectivity fraction or significance map. No
brain-wide multiple-testing correction or pooled-region filter is inferred from these five cells.

`BWM_CACHE_DIR` defaults to `data/one`; `BWM_RESULTS_DIR` defaults to `results/single_probe`.
The notebook removes uppercase/lowercase HTTP/HTTPS/ALL proxy settings and sets both NO_PROXY
variants to `*` before network-capable imports. Use that same first-cell setup in other Python
fetching scripts. The public demo account worked during validation, but ONE warns that it will be
retired. Set `BWM_ONE_TOKEN` before launching the new notebook to use a personal API token instead;
tokens are not written to its result/provenance files. Changing proxy environment variables after
importing a module that already connects can be too late.

Outputs are `stimulus_selectivity.csv`, `trial_conditions.csv`, `stimulus_peth.png`,
`stimulus_peth.pdf`, and `provenance.json`. The JSON records package versions, source/lock hashes,
cohort and loader revisions, chosen units, p-values, and timings. Cache contents and output files
are ignored by Git; the source notebook is committed without outputs.

To save an executed notebook from a fresh kernel:

```sh
uv run --locked --group notebook jupyter nbconvert --to notebook --execute notebooks/reproduce_bwm.ipynb --ExecutePreprocessor.timeout=3600 --output executed_reproduce_bwm.ipynb --output-dir results
```

## Fetching additional online data

Use `uv run --locked python scripts/fetch_project_data.py tables` for the anonymous public
historical unit/trial tables. Releases are cached separately and validated with MD5 checksums.
The [data access guide](data_access.md) documents live sizes, session/probe downloads,
passive and widefield discovery, authentication, and metadata-only listing. This helper
provides an explicit access path; it does not change the legacy aggregate defaults below.

## Moving from an example to full results

**Cohort and aggregates.** The frozen query and aggregate release are separate choices. The current
downloader defaults to `2026_Q2_IBL_et_al_BWM`; its checksum manifest lists clusters, waveforms,
and ACG arrays, but no trials table. `bwm_units()` and several existing tests request trials without
specifying a tag. Reconcile those callers before attempting historical canonical unit counts.
`2024_Q2_IBL_et_al_BWM` has both trials and clusters checksums. It can be requested explicitly with
`download_aggregate_tables(one, type="trials", tag="2024_Q2_IBL_et_al_BWM")`, and similarly for clusters.
Use one release for both and isolate release-specific cache directories: the downloader currently
uses untagged local filenames. The new notebook bypasses this mismatch without changing public APIs.

**Decoding.** Select `--group decoding`, configure `decoding/settings.py` from its template, then
cache data, assemble sessions/null targets, run fits, format outputs, and build summaries. See the
[decoding README](../brainwidemap/decoding/README.md). Inter-individual model modes additionally
refer to external `braindelphi` artifacts; they are not part of the default environment.

**Encoding.** Select `--group encoding`; inspect the legacy single-session notebook, configure
`GLM_CACHE` / `GLM_FIT_PATH`, and follow the four stages. Cluster execution additionally needs
`--group cluster`, SLURM, and adapted paths/container commands. The existing Dockerfile,
`environment.yaml`, and Singularity pipeline assumptions are retained as legacy resources; uv does
not rebuild or validate those images.

**Manifold.** Select `--group manifold`. Importing `state_space_bwm.py` initializes ONE, an atlas,
and the aggregate-dependent canonical unit table. Resolve the aggregate issue before importing it.
Then `get_all_d_vars` computes per-insertion results, `d_var_stacked` pools them, and plotting
functions consume those results. The upstream README's multi-hour estimates are not measurements
from this environment. The old manifold requirements file includes unrelated/misnamed packages;
the uv group instead declares imports used by the population-analysis script.

**Paper figures.** `meta/bwm_figs.py` expects pooled decoding, trajectory, single-cell, and GLM
files under `one.cache_dir/bwm_res/bwm_figs_data/`. It also forces `Qt5Agg`, imports utilities from
other repositories (`reproducible_ephys_functions`, `ibl_style`, etc.), and imports `GLMPredictor`,
which is absent from this checkout's `glm_predict.py`. Other figure scripts reference `dmn_bwm`.
Several output paths are hardcoded. In addition, the ED Fig. 9 assembly explicitly warns that
placeholder data must be replaced. These are documented blockers, not repaired or validated
publication outputs.

## Validation status

Validated on Linux x86_64 with Python 3.10.20 on 2026-11-15:

| Check | Result |
|---|---|
| Locked install with every dependency group | Passed |
| Decoding/model-settings, encoding/design/fit/prediction, manifold dependencies, Dask/jobqueue imports | Passed; full analysis jobs not executed |
| Existing `TestBWMLoading.test_data_freeze` assertions | Passed for all four fixtures, invoked without its network-dependent `setUp` |
| Notebook schema, Python syntax, cleared source outputs | Passed |
| Fresh-kernel execution with only the `notebook` group | Passed, all 19 cells, no cell errors |
| Wheel and source distribution | Built successfully; all four cohort CSVs packaged; analysis modules present in wheel |

The data run loaded **1,385,557 spikes and 27 good units**. Of 826 loaded trials, **494** passed the
mask; no performance truncation was required. The five selected original sorter IDs were
**55, 100, 124, 134, 154**. Their stimulus p-values were approximately
**0.343719, 0.400533, 0.068144, 0.585971, 0.398700**. No significance is inferred from this example.
Loading/QC took **48.9 s**, the 3,000-shuffle test **7.0 s**, and the notebook's timed analysis
**58.9 s** in total (excluding kernel startup/imports). Download/runtime will vary across machines.

The initial run used `ibllib 4.1.1`, `ONE-api 3.6.2`, NumPy 1.26.4, pandas 2.3.3, and SciPy 1.15.3.
The all-groups import check additionally used `neurencoding 0.1.8`, the pinned
`behavior-models 0.1.0` revision, and `torch 2.14.1+cpu`. The exact environment is in `uv.lock`.

A final cached run after an exact notebook-only sync took **20.3 s**, reproduced the same five
p-values, and embedded the PETH figure in the executed notebook. The local executed notebook is
`results/executed_reproduce_bwm.ipynb`; per-unit results and the
full run record are under `results/single_probe/`. These artifacts are ignored by Git. The committed
notebook remains cleared so another run starts from its documented inputs.

Full-cohort analysis, the complete remote test suite, and legacy SLURM/container execution remain
separate validation tasks.
