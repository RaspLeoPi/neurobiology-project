# Neurobiology team project: brain-wide map

This repository supports a **three-member team's project for the Neurobiology course**, combining
paper reproduction with a D3 + D8 study of decision-speed signals in VISp and MOs.
It is a personal fork of [IBL's analysis repository](https://github.com/int-brain-lab/paper-brain-wide-map),
with a uv-managed environment and a guided route into reproducing the main paper:

International Brain Laboratory, Angelaki, D., Benson, B. et al. **A brain-wide map of neural activity
during complex behaviour.** Nature 645, 177–191 (2025).
[Paper](https://doi.org/10.1038/s41586-025-09235-0) ·
[Upstream figure and LaTeX sources](https://github.com/int-brain-lab/Brainwide-Map-Paper)

The repository also contains analyses relevant to Findling, C., Hubert, F., International Brain
Laboratory et al. **Brain-wide representations of prior information in mouse decision-making.**
Nature 645, 192–200 (2025). [Companion paper](https://doi.org/10.1038/s41586-025-09226-1).
The first reproduction notebook targets the main paper.

## Install with uv

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and Git, then:

```sh
git clone https://github.com/RaspLeoPi/paper-brain-wide-map.git
cd paper-brain-wide-map
uv python install 3.10
uv sync --locked --group notebook
uv run --locked --group notebook jupyter lab notebooks/reproduce_bwm.ipynb
```

The `.python-version` file selects Python 3.10. uv creates `.venv`, installs this checkout in editable
mode, and uses the committed `uv.lock`. Select `.venv/bin/python` in your editor's notebook kernel
picker. From JupyterLab launched above, use its Python 3 kernel. No Conda activation or global package
installation is needed. Linux x86_64 CPU execution is the initial validation target.

The dependency declaration is `pyproject.toml`; update it with `uv add` / `uv add --group NAME`, then
review the updated lockfile. Use `--locked` for reproduction so stale metadata fails explicitly.
The archived `requirements_frozen.txt` describes an older upstream environment, not this lockfile.
`requirements.txt` is a generated export of the **base dependencies only** for pip interoperability;
`uv sync` remains the supported reproduction workflow.

## Fetch online project data

Download the public historical unit and trial tables across regions (about 110 MiB):

```sh
uv run --locked python scripts/fetch_project_data.py tables
```

No account is required for these tables. For processed spikes, wheel, passive or widefield data,
see the [access guide](docs/data_access.md). It includes session discovery, authentication,
proxy handling, checksums, and commands that list availability before downloading.

## Start reproducing

Open [the reproduction notebook](notebooks/reproduce_bwm.ipynb) for:

- A guide to the code, identifiers, and analysis data flow.
- A checklist mapping paper results to entrypoints, inputs, outputs, and outstanding prerequisites.
- Frozen cohort checks: 699 probe insertions, 459 sessions, and 139 subjects.
- One probe's QC, five units' stimulus-selectivity shuffle tests, and event-aligned firing-rate plots.

The notebook disables proxies before importing networking libraries, downloads processed data through
ONE, and saves figures, tables, and provenance under `results/single_probe/`. Data are cached under
`data/one/`. Set `BWM_ONE_TOKEN` before launch to use a personal OpenAlyx API token; the
shared demo account currently works but ONE warns that it will be retired. Both directories are
ignored by Git. Set `BWM_CACHE_DIR` or `BWM_RESULTS_DIR` before launching Jupyter to use different storage. This is a small reproducible analysis, not full-paper
figure reproduction.

Read [the reproduction guide](docs/reproduction.md) for the code map, dependency groups, full-cohort
workflows, release caveats, and validation status. Further data-loading examples are in
[`data_loading_examples.py`](data_loading_examples.py).

## Neurobiology course project

The team selected D3 + D8 from the [broader project options report](docs/neurobiology_project_options_draft.md).
The [dedicated decision-speed plan](docs/d3_d8_decision_speed_plan.md) combines pre-stimulus and early
stimulus activity in a VISp–MOs comparison, with five provisional lab-matched session pairs, a shared
analysis protocol, three-person responsibilities, and a 28–36 person-hour budget. It is a plan;
the project analyses have not been run. The Chinese companion Word document is shared separately;
DOCX files are ignored by Git.

## Analysis environments

Groups are opt-in. Include the same groups with both `uv sync` and `uv run`; a later sync/run can
remove packages from groups that were not selected.

| Group | Additional capabilities | Example |
|---|---|---|
| Base (no group) | ONE data loading, frozen cohort, single-cell tests | `uv sync --locked` |
| `notebook` | JupyterLab, kernel, notebook validation/execution | `uv sync --locked --group notebook` |
| `dev` | pytest, flake8, package builds | `uv sync --locked --group dev` |
| `decoding` | Legacy behavioral models, CPU PyTorch on Linux x86_64, OpenTURNS | `uv sync --locked --group decoding` |
| `encoding` | neurencoding and regression tools | `uv sync --locked --group encoding` |
| `manifold` | Population analysis and statistical plotting dependencies | `uv sync --locked --group manifold` |
| `cluster` | Dask/distributed and SLURM jobqueue support | `uv sync --locked --group encoding --group cluster` |

For example, launch the legacy encoding example with:

```sh
uv run --locked --group encoding --group notebook jupyter lab brainwidemap/encoding/scripts/fit_example_session.ipynb
```

See the [decoding](brainwidemap/decoding/README.md), [encoding](brainwidemap/encoding/README.md), and
[manifold](brainwidemap/manifold/README.md) READMEs before executing their pipelines. Optional groups
provide dependencies; they do not supply precomputed results, local path configuration, external
figure utilities, or cluster infrastructure.

## Python data fetching without proxies

Run this before importing ONE, requests, boto3, or analysis modules that connect during import:

```python
import os

for key in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
    os.environ.pop(key, None)
os.environ["NO_PROXY"] = "*"
os.environ["no_proxy"] = "*"

from one.api import ONE
from brainwidemap import bwm_query

auth = ({"token": os.environ["BWM_ONE_TOKEN"]} if os.environ.get("BWM_ONE_TOKEN")
        else {"username": "intbrainlab", "password": "international"})
one = ONE(base_url="https://openalyx.internationalbrainlab.org", silent=True, **auth)
bwm_df = bwm_query(freeze="2023_12_bwm_release")
```

This changes only the current Python process. ONE uses its own cache and may create connection
settings in your user configuration directory on first use.

**Release caveat:** the current aggregate downloader defaults to `2026_Q2_IBL_et_al_BWM`, whose
checksum manifest has no trials entry. Existing aggregate-dependent callers such as `bwm_units()`
therefore require release reconciliation before paper reproduction. The new notebook uses direct
probe/trial loading and the frozen cohort instead. See the guide before requesting aggregate tables.
