# D3 + D8: decision-speed signals in VISp and MOs

Dedicated Neurobiology course project plan · 15 November 2026 · three students

**Status: protocol and metadata feasibility assessment only.** No neural feature extraction, model fitting, hypothesis testing, or new spike downloads have been performed for this plan. The broader [project options report](neurobiology_project_options_draft.md) is retained unchanged. Its original D3 and D8 ideas are combined here with a larger, explicitly budgeted regional comparison. The Chinese companion is `docs/d3_d8_decision_speed_plan_zh.docx`, distributed separately from Git.

## 1. Research question and scope

**Do pre-stimulus activity and early stimulus responses contribute differently to predicting decision speed in primary visual cortex (VISp) and secondary motor cortex (MOs)?**

| Component | Operational question | Main session-level measure |
|---|---|---|
| D8: pre-stimulus state | Does activity before the stimulus improve reaction-time prediction beyond stimulus, block and recent behavioral history? | Error reduction when adding pre-stimulus features to a behavioral baseline |
| D3: early stimulus response | Does early activity improve prediction beyond the behavioral baseline and pre-stimulus activity? | Additional error reduction when adding early post-stimulus features |
| Primary project comparison | How do those two contributions differ between MOs and VISp? | Lab-paired MOs minus VISp differences, reported separately for D8 and D3 |

Reaction time (RT) is **firstMovement_times − stimOn_times**, in seconds. It indexes the timing of action initiation in this task, including sensory, decision and motor contributions. It is not a pure measure of internal decision duration. Pre-stimulus firing is a measured neural state, not an identified arousal variable. Results will be observational associations; neither causal effects nor communication between regions can be inferred.

Regional differences are the main project focus. We will analyze five sessions per region, one VISp session and one separate MOs session from each of five laboratories. These are **not simultaneous VISp–MOs recordings**, and the two sessions in a lab are not repeated measurements from the same animal. Lab matching reduces one source of heterogeneity but cannot remove differences in animals, behavior, recording depth, or sampled cell types. A small or unstable regional difference is a valid project outcome.

## 2. Data and a provisional cohort

### Available inputs and what is still needed

The local historical aggregate release is `data/aggregates/2024_Q2_IBL_et_al_BWM/`. Its trial table has 295,920 rows from 459 sessions, including 196,574 rows marked `bwm_include`. Its cluster table has 621,733 rows, including 75,708 units with `label >= 1`. These are cohort-wide inventory counts, not the sample size of this project. The frozen `2023_12_bwm_release.csv` contains 699 probe insertions, 459 sessions and 139 subjects.

The tables provide stimulus conditions, choice, first movement, feedback, block probability, QC/saturation flags, and unit/region identifiers. They do **not** supply all spike times. Session-specific processed spikes and cluster metadata still need downloading. Wheel data are optional for a motion-control extension; video, raw ephys, passive stimuli and widefield recordings are not required for the core project.

### Outcome-independent selection rule

1. Use the 2024 aggregate tables and the frozen cohort above. Map cluster atlas IDs to **Beryl** regions. Require `label >= 1` and at least **10 good units** in the session-region, combining probes from the same session if necessary.
2. Construct histories using the original within-session trial order **before filtering**. Apply the trial rules in Section 3. A contrast-magnitude × stimulus-side stratum must initially contain at least **20 eligible trials**. Retain sessions with at least **150 eligible trials across those strata** and at least **two nonzero contrast magnitudes**.
3. Match one VISp and one MOs session within each shared lab. For each candidate pair, intersect its eligible contrast-side strata and sum the smaller count in each shared stratum. Require common capacity of at least **150**, spanning at least two contrast magnitudes. A given contrast need not have both stimulus sides if a side fails QC; disclose the resulting coverage.
4. Within each lab, inspect VISp candidates by session date then EID, and MOs candidates by date then EID for each VISp candidate. Take the first admissible pair, independently of neural activity or any modeled effect. Require five distinct mice per region. Keep the same ten sessions for D3 and D8.
5. Allocate **150 trials to each session** using identical contrast-side quotas within its lab pair. Starting at zero, cycle through shared strata in ascending contrast then side (L before R), adding one trial while below each stratum's common capacity, until 150 are allocated. Select trials uniformly without replacement with seed 0, then restore original order. Some selected strata therefore have fewer than 20 trials; the 20-trial rule is an initial availability screen.

The metadata-only screen on 15 November 2026 found **14 eligible VISp sessions and 21 eligible MOs sessions** before pairing. Five shared labs support the matching rule: churchlandlab, cortexlab, danlab, mainenlab and zadorlab. The candidate list below yields **750 trials per region / 1,500 total** and **10 sampled neurons per session / 100 session-specific neurons** for the main analysis. Trials and neurons are not independent regional replicates: there are five lab pairs.

### Candidate appendix: identifiers and counts

Counts below are after the metadata rules, before taking the common 150-trial quota. They establish feasibility only. Actual spike/trial alignment and downloaded-unit QC may change eligibility.

| Lab | Region | Subject / date | Session EID | Good units / eligible trials |
|---|---|---|---|---|
| churchlandlab | VISp | CSHL052 / 2020-02-18 | 85dc2ebd-8aaf-46b0-9284-a197aee8b16f | 49 / 157 |
| churchlandlab | MOs | CSHL049 / 2020-01-10 | d2918f52-8280-43c0-924b-029b2317e62c | 54 / 347 |
| cortexlab | VISp | KS014 / 2019-12-05 | e1931de1-cf7b-49af-af33-2ade15e8abe7 | 11 / 441 |
| cortexlab | MOs | KS023 / 2019-12-06 | a4000c2f-fa75-4b3e-8f06-a7cf599b87ad | 22 / 378 |
| danlab | VISp | DY_009 / 2020-03-05 | 413a6825-2144-4a50-b3fc-cf38ddd6fd1a | 19 / 208 |
| danlab | MOs | DY_014 / 2020-07-18 | ee8b36de-779f-4dea-901f-e0141c95722b | 44 / 225 |
| mainenlab | VISp | ZFM-01577 / 2020-10-28 | 09b2c4d1-058d-4c84-9fd4-97530f85baf6 | 51 / 185 |
| mainenlab | MOs | ZM_2245 / 2020-01-21 | cb2ad999-a6cb-42ff-bf71-1774c57e5308 | 36 / 523 |
| zadorlab | VISp | CSH_ZAD_025 / 2020-07-30 | 6274dda8-3a59-4aa1-95f8-a8a549c46a26 | 62 / 216 |
| zadorlab | MOs | CSH_ZAD_024 / 2020-06-08 | 8207abc6-6b23-4762-92b4-82e05bed5143 | 51 / 291 |

Each candidate currently has one contributing probe in the selected region:

| Lab | VISp PID | MOs PID |
|---|---|---|
| churchlandlab | df07180e-268e-489c-826e-40cb6f63d3a5 | 2564dc27-4eda-4fc3-a151-c13475796ee1 |
| cortexlab | 9150758e-1390-41d1-b426-96675e60dbea | adca9242-0725-41d4-8eb1-5655a464431d |
| danlab | b9b101cf-24d3-4c2a-8464-bc91b9f0c767 | b375a0ee-4c5a-4a53-9cea-d753f206e5c5 |
| mainenlab | b78b3c42-eee5-47c6-9717-743b78c0b721 | 8f4fd564-7e34-4113-a6e4-ae40faa64f7a |
| zadorlab | 1bd85dab-7a53-49d1-acd4-e82f9fd07cf6 | 9bd71ac6-c455-41f3-8c56-59987a649ac4 |

Here, L/R denotes the **stimulus side**, not the sign convention of the animal's choice. Contrast is expressed as a fraction (0.0625 = 6.25%). Quotas are identical in both members of a pair:

| Lab | Common capacity | Contrast-side quotas totaling 150 |
|---|---:|---|
| churchlandlab | 157 | 0.0625L:24, 0.0625R:25, 0.125L:31, 0.125R:28, 0.25L:22, 1R:20 |
| cortexlab | 344 | 0.0625L:19, 0.0625R:19, 0.125L:19, 0.125R:19, 0.25L:19, 0.25R:19, 1L:18, 1R:18 |
| danlab | 193 | 0.0625L:22, 0.0625R:22, 0.125L:20, 0.125R:22, 0.25L:22, 0.25R:21, 1R:21 |
| mainenlab | 185 | 0.125L:25, 0.125R:25, 0.25L:25, 0.25R:25, 1L:25, 1R:25 |
| zadorlab | 191 | 0.0625L:25, 0.125L:25, 0.125R:25, 0.25L:25, 0.25R:25, 1R:25 |

Different labs have different condition mixtures. Match within each pair and adjust for conditions in the models; do not pool all trials as exchangeable observations. Disclose residual confounding and the restricted contrast-side support.

### Download route and acceptance gate

From the repository root, use the existing tools; these commands are instructions for future execution, not downloads performed for this plan:

```sh
uv sync --locked --group notebook --group manifold
uv run --locked python scripts/fetch_project_data.py tables
# Pilot VISp and MOs pair (cortexlab):
uv run --locked python scripts/fetch_project_data.py probe --pid 9150758e-1390-41d1-b426-96675e60dbea
uv run --locked python scripts/fetch_project_data.py probe --pid adca9242-0725-41d4-8eb1-5655a464431d
```

Repeat `probe --pid PID` for the other eight candidates after pilot validation. See [data access](data_access.md) for authentication, checksums, historical versus default revisions and optional wheel downloads. The script imports `os` and disables proxies before networking. Any additional Python fetching code must start with:

```python
import os
for key in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
    os.environ.pop(key, None)
os.environ["NO_PROXY"] = os.environ["no_proxy"] = "*"
```

Before extracting features, record release hashes, dataset paths/revisions and loader settings. Match clusters by **PID and cluster UUID**, verify sorter cluster IDs and Beryl assignments, and check that downloaded units satisfy the aggregate QC rule. Never use aggregate row number as a spike-cluster ID. Verify session, original trial count/order and stimulus, movement and feedback timestamps against the aggregate table, with an explicit tight timestamp tolerance (e.g. 1 ms). Check spike times share the trial clock. Never join a filtered trial table by row position alone.

**Go/no-go:** proceed only with verified unit identities, aligned trials and at least 150 common eligible trials per pair. If a candidate fails, record the reason and examine the next candidate under the same metadata-only ordering, before looking at neural effects. If five lab pairs or five distinct mice per region cannot be retained, report the shortfall and revise scope explicitly before fitting the project models. Do not relax filters to obtain an interesting difference.

## 3. Trial definitions, timing and exclusions

Use original zero-based within-session trial indices, retaining a stable `(eid, original_trial_index)` key. Verify chronological order; do not silently reorder ambiguous trials. Compute previous choice, outcome, RT and feedback time on the original sequence, then filter. The preceding trial means the preceding original trial, not the preceding retained trial.

| Item | Fixed primary rule |
|---|---|
| Starting mask | `bwm_include == True` |
| Valid response and stimulus | Choice ±1; positive nonzero contrast; retain correct and error trials |
| RT | Finite first-movement RT in **[0.15, 2.0] s** |
| Current/history fields | Finite stimulus time, block probability, previous feedback time, previous positive RT; previous choice ±1 and previous feedbackType ±1 |
| Pre-stimulus window P | **[−0.4, −0.1) s** relative to stimulus onset |
| Early window E | **[0, 0.1) s** relative to stimulus onset |
| Previous-trial separation | `stimOn_times − 0.4 >= previous_feedback_times + 0.5` |
| Saturation | Both `saturation_stim_minus04_minus01` and `saturation_stim_plus01` must be False; missing flags are not accepted as False |
| Trial matching | Section 2's contrast-side rules; seed 0; identical rows for all three models |

The early window ends at least 50 ms before the first detected movement in every retained trial. This prevents overlap with that detected movement, but does not guarantee freedom from small undetected movements or motor preparation. The pre-window separation reduces immediate feedback contamination without establishing a pure intrinsic state. The first trial, invalid-history trials and missing-value trials are excluded. Report exclusions step by step, including overlaps and the final retained count. Do not fabricate history values.

Exclude 0% contrast trials from the core project so stimulus side is defined and condition matching stays manageable. Findings will not generalize automatically to 0% trials, RT below 150 ms or above 2 s, excluded conditions, or all mice in the paper.

## 4. Shared features and models

### Feature contract

One shared trial table contains `eid`, `subject`, `lab`, `region`, `original_trial_index`, stimulus time, RT, log RT, contrast magnitude, stimulus side, probabilityLeft, normalized original trial position, previous choice, previous feedbackType, previous log RT and `stimOn_times − previous_feedback_times`. Include matching stratum, exclusion flags, selected status and fixed outer-fold assignment. A provenance manifest records the exact selection seed and IDs.

A companion unit table records PID, cluster UUID, sorter cluster ID, atlas ID, Beryl region and QC label. Sort eligible units by PID then UUID and draw **10 units without replacement, seed 0**, independently of firing rates or RT effects. For each retained trial and chosen unit, compute spike count divided by window duration in P and E. Use the same units in both windows. Save features with the trial key and ordered unit IDs so array-column identity is checkable. If multiple probes contribute, merge by identity and clock, not concatenated numeric cluster IDs.

Use raw firing rates in P and E separately in the primary joint model. **Do not subtract P from E**: that would mathematically couple the early feature to the pre-stimulus feature and complicate their incremental interpretation. Descriptive baseline-subtracted plots, if made, must be labeled and must not replace the raw primary features.

### Three nested models per session

Target: **log(RT in seconds)**, using the natural logarithm. Fit ridge regression separately in each session-region:

| Model | Predictors | Purpose |
|---|---|---|
| B | Contrast magnitude, stimulus side, block probability, trial position, previous choice, previous outcome, previous log RT, intertrial timing | Behavioral/task/history baseline |
| B+P | B plus 10 pre-stimulus unit rates | D8 contribution |
| B+P+E | B+P plus the same 10 units' early rates | D3 contribution conditional on P |

Encode contrast magnitude and stimulus side categorically, retaining additive main effects; encode block probability categorically. Standardize continuous predictors and neural rates on training data. Use a single documented encoder/scaler/ridge pipeline for all models, with consistent handling of categories absent from a training fold. Remove any zero-variance columns based on training data alone. Do not add current choice, correctness, feedback, reward or post-movement features as predictors: they are not available at the early prediction time.

Use **five chronological outer test blocks** on the retained trials, without shuffling. Around each held-out block, remove training trials within **five original trial indices** of the block's index interval. Tune alpha over **[0.1, 1, 10, 100]** with three chronological inner validation blocks, applying the same original-index gap within outer training data. Every transform and hyperparameter choice is fitted inside the relevant training split. Use identical outer/inner splits for the three models. The evaluation estimates prediction within an already sampled session using other session periods; it does not establish generalization to new animals or a prospective future session.

Pool the outer out-of-fold squared errors across all 150 trials to obtain each model's MSE. Do not average in-sample scores or select a favorable fold. Let those errors be MSE_B, MSE_BP and MSE_BPE:

- **D8 = (MSE_B − MSE_BP) / MSE_B**.
- **D3 = (MSE_BP − MSE_BPE) / MSE_B**.

Both use the same baseline denominator, so D8 + D3 equals the total normalized error reduction. Positive values indicate improved held-out prediction; negative values must remain visible. Report raw MSE as well. D3 is incremental information conditional on measured P and B, not all information carried by early responses; correlated features make these contributions model-dependent.

### Regional comparison and interpretation

For each lab, compute **MOs minus VISp** for D8 and for D3. Plot all five lab-pair differences, plus their unweighted mean. Also display each session's three MSEs and both contributions. For descriptive uncertainty, resample the five whole lab pairs with replacement 10,000 times (seed 0), and show percentile 95% intervals for the mean difference. Preserve the two region records together in each resampled pair.

Five lab pairs give limited precision and limited control of recording/animal confounds. A two-sided exact paired sign-flip test with five nonzero differences has minimum attainable p = 2/32 = 0.0625; a conventional 0.05 threshold is therefore unsuitable as a success criterion. Emphasize effect size, direction, pair consistency and sensitivity, with two regional endpoints reported side by side. Neurons, trials and CV folds must not be treated as independent regional sample units. Bootstrap intervals are descriptive and do not make the study confirmatory.

For an intuitive D3 display, split retained trials at the RT median **within each session's contrast-side condition**; omit exact median ties from that display only. Plot mean raw early rate and a short stimulus-aligned population trace for fast versus slow trials. Standardize/average units consistently and show session-level summaries. This is a descriptive companion, not a replacement for the baseline-adjusted model or a reason to choose sessions.

## 5. Controls, risks and stopping rules

Complete these within the core budget:

- Repeat the early analysis with **[0, 0.08) s**, using the same cohort, trials, units and folds. This tests sensitivity to early-window placement.
- Repeat 10-neuron selection with seeds **1–4**, keeping trials/folds fixed. Show how regional estimates change across unit samples; never choose the best seed.
- Use **20 circular within-session shifts of the full joint neural-feature matrix**, with offsets at least 20 retained trials from zero in either circular direction (e.g. a fixed seed-0 selection from offsets 20–130). Refit the same nested pipeline for each shift, retaining B and target order. Shifts preserve P/E correspondence while disturbing neural–trial alignment. They are a diagnostic for temporal structure, not a calibrated permutation p-value; task and slow-state nonstationarity violate simple exchangeability.
- Review trial identities, timing windows, gap indices and training-only preprocessing together before interpreting effects. Save an example fold diagram and a table of the latest early-window end versus movement onset.

Optional only after the core analysis is stable: add pre-stimulus wheel movement summaries to B, using verified wheel timestamps, and rerun the same comparisons (**+3–6 team hours**). It can reduce one measured motion confound; it cannot establish an arousal mechanism or eliminate all movement effects. Do not add this extension by silently exceeding the core budget.

The study does not require full-brain modeling, raw spike sorting, deep networks or cluster computing. Main risks are revision mismatches, an alignment failure that shrinks the matched cohort, a narrow trial distribution, and unstable estimates from five pairs. If downloading/alignment consumes the first week's allocation, stop scope growth and document the issue. Do not replace the target question with significance hunting.

## 6. Three-person work plan and schedule

**Core budget: 28–36 team person-hours**, approximately 9–12 hours per student across two weeks. Waiting for downloads is additional elapsed time, not assumed hands-on analysis time. The estimate includes routine loading problems and controls, but not repairing unavailable/reprocessed datasets or adding wheel analysis.

| Owner | Responsibilities and handoff | Person-hours |
|---|---|---:|
| A: data and cohort | Validate releases/identities; pilot downloads; construct original-order histories, exclusions, lab pairs, quotas and shared trial/unit tables; maintain provenance and candidate ledger | 9–11 |
| B: D3 and visualization | Extract/check early features against A's identities; make matched fast/slow displays; use the shared pipeline for D3; perform 80-ms sensitivity; prepare regional figures | 9–12 |
| C: D8 and model evaluation | Extract/check pre-stimulus features; implement shared B/B+P/B+P+E pipeline, nested folds and metrics; coordinate regional pairing, subsampling/shift controls and leakage review | 10–13 |

A supplies frozen row/unit keys before B or C constructs arrays. B and C use the same fitting function and fold manifest; they should not implement independent versions of the baseline. Each person reviews one other's outputs. Joint discussion and writing time is included in the allocations above.

| Stage | Work and acceptance checkpoint |
|---|---|
| Week 1, start | All: read the task/data definitions and freeze this protocol. A validates one pilot per region (the cortexlab pair); B/C check one set of window features and a dummy model run for mechanics only. |
| Week 1, end | A: complete ten-session identity/alignment checks, exclusion ledger and 150-trial quotas. B/C: agree on one table/feature contract and fold implementation. Gate: all five pairs pass or the shortfall is explicitly reported before effects are reviewed. |
| Week 2, first half | B/C: run the shared nested models and fixed controls; A audits inputs and keeps manifests. Do not alter the cohort based on apparent regional effects. |
| Week 2, second half | All: review five pair differences, sensitivity and uncertainty; prepare figures, a concise report and presentation. State limitations and null/negative results clearly. |

## 7. Planned files and completion criteria

The following are **future deliverables**, not files created or analyses run by this planning task:

| Location | Contents |
|---|---|
| `data/d3_d8/cohort_manifest.csv` | Candidate/accepted EIDs, PIDs, mice, labs, dates, counts, selection order and paired IDs |
| `data/d3_d8/exclusions.csv` | Original trial keys, flags/reasons, condition quotas and counts before/after each step |
| `data/d3_d8/provenance.json` | Release hashes, exact dataset revisions, software versions, parameters and seeds |
| `results/d3_d8/trials.parquet`, `units.parquet`, `features.npz` | Shared keyed trial/unit tables and ordered P/E arrays |
| `results/d3_d8/folds.csv`, `predictions.parquet` | Original trial indices, outer/inner membership/gaps and out-of-fold predictions for each model |
| `results/d3_d8/session_metrics.csv`, `regional_pairs.csv`, `controls.csv` | MSEs, D3/D8 values, five lab-pair differences and fixed sensitivity outputs |
| `results/d3_d8/figures/` | QC/exclusion and fold displays; descriptive fast/slow traces; five-pair regional comparison; sensitivity plot |
| Proposed `notebooks/d3_d8_decision_speed.ipynb` and a small shared helper module | Reproducible orchestration and one feature/model implementation, created when analysis starts |
| Proposed `docs/d3_d8_findings.md` | Short methods/results/limitations report with an explicit distinction between observations and interpretation |

`data/` and `results/` remain ignored; share compact manifests and figures deliberately when the team decides how to distribute results. Commit source analysis code and final prose when created, not large datasets or credentials. Word files are distributed separately and remain ignored.

The project is complete when identities and exclusions are auditable, the shared pipeline produces held-out predictions for every retained trial, both regional endpoints show all five pair differences, fixed controls are reported, and the three students can explain the methods and limits. A statistically significant difference is not required. This planning document itself does not answer D3 or D8.

## 8. Reading and implementation references

- [IBL: A brain-wide map of neural activity during complex behaviour (Nature, 2025)](https://doi.org/10.1038/s41586-025-09235-0): task, cohort and anatomical context. This course protocol is an extension, not a claim to reproduce a published D3/D8 result.
- [IBL trial-data loading and field definitions](https://docs.internationalbrainlab.org/notebooks_external/loading_trials_data.html): events, contrasts and behavior; verify choice coding against these definitions before plotting labels.
- [Repository reproduction guide](reproduction.md) and [data access guide](data_access.md): environment, release caveats, entrypoints and commands.
- [scikit-learn Ridge](https://scikit-learn.org/1.5/modules/generated/sklearn.linear_model.Ridge.html) and [preprocessing/leakage guidance](https://scikit-learn.org/1.5/common_pitfalls.html): use training-only pipelines with the repository's locked dependencies.
