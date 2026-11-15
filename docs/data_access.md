# Fetching online BWM data

The BWM data remain online through the public AWS bucket and OpenAlyx/ONE. This repository now includes `scripts/fetch_project_data.py` to fetch data without running a project analysis. Run the commands below from the repository root. The script removes uppercase and lowercase HTTP/HTTPS/ALL proxy variables before networking imports.

## One command for the cohort-wide tables

```sh
uv run --locked python scripts/fetch_project_data.py tables
```

This downloads **clusters.pqt and trials.pqt from 2024_Q2_IBL_et_al_BWM**, approximately **110.4 MiB combined**. The tables describe the cohort across regions; they do not contain all spike trains, raw ephys, or videos. No OpenAlyx login or AWS credentials are needed for this command.

Files are stored under `data/aggregates/2024_Q2_IBL_et_al_BWM/`. Downloads use the release MD5 checksums recorded in this repository, write through a temporary `.part` file, and retain an already-valid local file. Different releases have separate directories. A checksum failure stops the download rather than silently accepting changed upstream data.

To check availability and sizes without downloading file contents:

```sh
uv run --locked python scripts/fetch_project_data.py tables --check-only
```

If uv itself needs to install packages and your shell proxy is unavailable, prefix the command with `HTTP_PROXY= HTTPS_PROXY= ALL_PROXY= http_proxy= https_proxy= all_proxy=`. The Python script independently disables proxies for data fetching.

## Files confirmed online

All six URLs returned HTTP 200 on 2026-11-15. Sizes are the live server's Content-Length, not estimates. Full large-file checksums are verified when the user downloads them; the 1,152-byte ACG time-bin file was downloaded and checksum-verified during implementation.

| Release | File | Bytes |
|---|---|---:|
| 2024_Q2_IBL_et_al_BWM | trials.pqt | 24,212,510 |
| 2024_Q2_IBL_et_al_BWM | clusters.pqt | 91,555,529 |
| 2026_Q2_IBL_et_al_BWM | clusters.pqt | 112,325,731 |
| 2026_Q2_IBL_et_al_BWM | clusters.waveforms_peak.npy | 159,163,776 |
| 2026_Q2_IBL_et_al_BWM | clusters.acgs_log.npy | 159,163,776 |
| 2026_Q2_IBL_et_al_BWM | acgs_log.times.npy | 1,152 |

The anonymous HTTPS URL pattern is `https://ibl-brain-wide-map-public.s3.amazonaws.com/aggregates/<release>/<filename>`. The bucket is documented in the [AWS Open Data registry](https://registry.opendata.aws/ibl-brain-wide-map/).

For the newer unit table, waveforms and ACGs together (approximately **410.7 MiB**):

```sh
uv run --locked python scripts/fetch_project_data.py tables --release 2026
```

For just its small ACG time-bin file:

```sh
uv run --locked python scripts/fetch_project_data.py tables --release 2026 --files acgs_log.times
```

There is no trials checksum entry for the 2026 release in this checkout, so the script deliberately offers no 2026 trials download. Keep waveform/ACG rows matched to the unit table from the same release. These downloads do not repair existing `bwm_units()` callers or change their default release.

## ONE authentication and cache

ONE session downloads use the public OpenAlyx endpoint. The shared `intbrainlab` demo account still worked during verification, but the server warns that it will be retired. To use your own account, set `BWM_ONE_TOKEN` locally before running the command. Alternatively, set both `BWM_ONE_USERNAME` and `BWM_ONE_PASSWORD`. Credentials are never included in this script's manifests.

ONE caches session files under `data/one/`; its small connection/token configuration uses the usual user-level ONE directory. `BWM_CACHE_DIR` overrides the ONE session cache, consistently with the reproduction notebook. The global `--cache-dir /path/to/data` option changes the script's aggregate/manifest root and its default ONE cache; place it before the subcommand. Data and manifests are ignored by Git.

## Fetch one processed probe and its trials

```sh
uv run --locked python scripts/fetch_project_data.py probe
```

The default is the existing example probe `3675290c-8134-4598-b924-83edb7940269` in session `15f742e1-1043-45c9-9504-f1e8a53c1744`. It caches good-unit spikes, cluster information and trials. It does not run the shuffle test, a decoder, or other scientific analyses. Use `probe --pid YOUR_PROBE_UUID` for another insertion in the frozen cohort. This path retains the reproduction loader's historical revisions.

Regional recording counts in the report do not identify a specific suitable probe. Use the unit table's atlas assignments with the Beryl mapping and the frozen cohort's probe/session metadata when choosing region-specific recordings; eligibility still depends on each project's QC and trial counts.

## Fetch selected session modalities

Inspect the available filenames first:

```sh
uv run --locked python scripts/fetch_project_data.py session --profile trials --list-only
```

Fetch the example session's trial data or wheel data:

```sh
uv run --locked python scripts/fetch_project_data.py session --profile trials
uv run --locked python scripts/fetch_project_data.py session --profile wheel
```

Use another session with `--eid YOUR_SESSION_UUID`. Profiles are `trials`, `wheel`, `pose`, `passive`, and `widefield`. These profiles fetch processed files and supporting timestamps; they do not automatically download raw video, raw ephys, or the raw receptive-field movie. Pose profiles cover common processed pose/motion files; inspect filenames before selecting newer or less common products. The passive profile includes intervals, task-replay tables and RF timestamps; full receptive-field mapping also needs its stimulus file.

Unlike the historical `probe` mode, these session profiles choose ONE's default dataset revisions, falling back to the latest revision when metadata does not identify a unique default. Mixed revision dates across different attributes are recorded as exact paths in the manifest. Do not assume they are identical to the historical reproduction inputs.

## Discover passive and widefield sessions

These modalities are not present in every electrophysiology session. The default example session had no matching passive datasets when checked. Dataset searches require the **exact filename, including its namespace**:

```sh
uv run --locked python scripts/fetch_project_data.py find --dataset _ibl_passiveGabor.table.csv --bwm-only
uv run --locked python scripts/fetch_project_data.py find --dataset widefieldU.images.npy
```

The exact passive filename search matched **398 frozen BWM sessions** during verification.

`find` prints up to five session IDs and saves all matches. A search hit does not establish analysis QC. `--bwm-only` restricts results to the frozen electrophysiology cohort; omit it for the separate widefield collection.

A passive example confirmed to have online dataset metadata is `4ecb5d24-f5cc-402c-be28-9d0f7cb14b3a`:

```sh
uv run --locked python scripts/fetch_project_data.py session --eid 4ecb5d24-f5cc-402c-be28-9d0f7cb14b3a --profile passive --list-only
```

Remove `--list-only` to fetch those processed passive files. For widefield, take a session ID from `find`, inspect `session --eid YOUR_SESSION_UUID --profile widefield --list-only`, then remove `--list-only` to download its processed components. The live exact-name widefield search returned **50 matching sessions** during verification. This is a current dataset-search count, distinct from the companion paper's 51 analyzed sessions; the difference has not been reconciled and should not be interpreted as confirmed data loss.

For a dataset outside the profiles, list all registered filenames, then request an exact filename or a narrow glob:

```sh
uv run --locked python scripts/fetch_project_data.py session --eid YOUR_SESSION_UUID --list-only --include '*'
uv run --locked python scripts/fetch_project_data.py session --eid YOUR_SESSION_UUID --include EXACT_FILENAME
```

Repeat `--include` for multiple patterns. Filename patterns match the file basename; patterns containing `/` match the relative path. Inspect large-file metadata before selecting raw recordings or videos. Empty selections fail explicitly rather than being reported as successful downloads. Each successful listing or fetch writes a manifest under `data/manifests/`, including dataset IDs and exact relative paths for session files.

Official references: [release documentation](https://docs.internationalbrainlab.org/notebooks_external/2025_data_release_brainwidemap.html), [passive protocols](https://docs.internationalbrainlab.org/notebooks_external/loading_passive_data.html), [widefield loading](https://docs.internationalbrainlab.org/notebooks_external/loading_widefield_data.html), and [data explorer](https://viz.internationalbrainlab.org).
