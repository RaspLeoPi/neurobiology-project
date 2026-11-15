# Population trajectories and manifold analysis

From the repository root, install the locked dependencies:

```sh
uv sync --locked --group manifold
uv run --locked --group manifold ipython
```

The uv group declares the imports used by `state_space_bwm.py`. The older `requirements.txt` in this
folder is retained for reference; it includes unrelated/misnamed packages and is not used by uv.
See the [root installation instructions](../../README.md) and
[reproduction notebook](../../notebooks/reproduce_bwm.ipynb) for a smaller runnable example.

**Before importing the analysis module**, run the proxy-disabling setup from the
[root README](../../README.md#python-data-fetching-without-proxies). Importing this module itself
creates ONE/atlas objects and calls `bwm_units()`. The current aggregate default has no trials
checksum entry, so reconcile the historical aggregate release before importing/running the full
analysis. See the [reproduction guide](../../docs/reproduction.md#moving-from-an-example-to-full-results).
The commands below describe the existing pipeline; they are not an end-to-end validated recipe yet.

After resolving those prerequisites, from the configured IPython session:

```python
from brainwidemap.manifold import state_space_bwm as manifold

for split in ("stim", "choice", "fback"):
    manifold.get_all_d_vars(split)
    manifold.d_var_stacked(split)

manifold.plot_all()
```

`get_all_d_vars` downloads processed recordings, computes per-insertion PETHs and distance metrics,
and saves them under `one.cache_dir/bwm_res/manifold/res`. `d_var_stacked` combines insertions and
computes final regional results, including p-values. Plotting consumes those cached outputs.
The upstream estimate was about three hours per split for per-insertion computation and under a
minute for stacking; these are historical estimates, not measurements of the locked environment.
For published figure assembly, additional pooled results and external figure tools are required.
