# Draft Decision Making Neurobiology Project Options

This report offers **12 researchable questions** about perceptual decisions, action selection, feedback-dependent adaptation and decision-related neural states. It is for three students comfortable with Python, retaining the one-to-two-week budget of two to four hours per person per week: **6–24 total person-hours**. The two previously set-aside prior-decoding questions are not the default topics.

Only the downloaded file structures, data amounts and anatomical sampling have been inspected. **No candidate question has been tested, no neural effects have been estimated, and no decoders have been fitted.** Starter regions indicate feasible data coverage, not established mechanisms. Choose one core question, pilot 3–5 suitable sessions in one region, and add a second comparison only if the pilot succeeds.

## What the downloaded data support

The downloaded 2024_Q2 files passed their download checksums. Reading them confirms:

- **trials.pqt: 295,920 trial rows across 459 sessions.** Of these, **196,574 rows** have bwm_include=True. This is an existing inclusion mask, not a final sample size for any proposed question.
- **clusters.pqt: 621,733 unit rows across 699 probe insertions and 459 sessions.** **75,708 units** have label at least 1.
- Trial columns include stimulus contrasts, choice, feedback, reward volume, block probability and event times. Unit metadata include probe/session links, unit identities, QC and atlas labels.
- **The aggregate unit table does not contain trial-wise spike times.** Behavioral pilots and sample selection can start now; every complete neural project below still requires downloading selected probe recordings.

Reaction times and outcome/choice/context labels can be constructed from the trial table. Waveforms, pose and widefield data are not prerequisites for most core questions. The existing access commands and complete 279-region inventory are retained later in this report.

## Decision making shortlist

| ID | Research question | Hours | Assessment |
| --- | --- | --- | --- |
| D1 | Stimulus coding versus choice coding | 12–18 | Recommended |
| D2 | Choice information before movement | 14–20 | Moderate |
| D3 | Early neural responses and decision speed | 8–12 | Recommended low workload |
| D4 | Post-error adjustment and neural state | 12–18 | Recommended |
| D5 | History dependent stay and switch choices | 14–20 | Moderate |
| D6 | Stimulus difficulty and feedback responses | 14–22 | Condition-count risk |
| D7 | Block context and sensory responses | 12–18 | Moderate |
| D8 | Pre-stimulus state and response readiness | 10–16 | Accessible |
| D9 | Stability of choice signals within a session | 16–24 | Upper-budget option |
| D10 | Active decisions versus passive replay | 14–22 | Extra data preparation |
| D11 | Population size and choice information | 16–24 | Computational option |
| D12 | Coordination between simultaneously recorded regions | 24–36 | Stretch beyond usual budget |

These are total team estimates including reading, preparation, checks, figures and a short report. Adding another region typically adds approximately 3–6 person-hours. Decoder, passive-protocol and paired-region preparation is less predictable. At the lower end of the budget, avoid two unrelated projects.

## Region availability from the actual unit table

The following counts use label≥1, map atlas_id to Beryl, count units within each session-region after combining probes, and link sessions to mice using the frozen cohort. The good-unit column includes all QC-passing units in each region; session and mouse columns apply the minimum of five units per session-region. This is an anatomical/unit-count screen, before error-count, trial-condition, saturation-window or revision-matching requirements.

| Region | Good units | Sessions with ≥5 units | Mice | Interpretation |
| --- | --- | --- | --- | --- |
| VISp | 880 | 35 | 28 | Before trial eligibility |
| LGd | 557 | 22 | 19 | Before trial eligibility |
| LP | 1,812 | 58 | 53 | Before trial eligibility |
| MOs | 1,293 | 36 | 29 | Before trial eligibility |
| MOp | 1,458 | 30 | 20 | Before trial eligibility |
| CP | 2,892 | 64 | 38 | Before trial eligibility |
| ACAd | 369 | 21 | 16 | Before trial eligibility |
| ACAv | 195 | 11 | 8 | Before trial eligibility |
| ACB | 340 | 19 | 13 | Before trial eligibility |
| ORBvl | 669 | 8 | 7 | Before trial eligibility |
| BLA | 150 | 10 | 9 | Before trial eligibility |
| CA1 | 1,807 | 94 | 71 | Before trial eligibility |
| DG | 1,137 | 68 | 60 | Before trial eligibility |
| SCm | 1,666 | 54 | 36 | Before trial eligibility |
| MRN | 2,678 | 99 | 64 | Before trial eligibility |

These are unique-session counts and differ from the original appendix's “recordings” column. At the ≥5-good-units-per-region threshold, **MOs and CP share 7 sessions from 7 mice; VISp and MOs share none; VISp and CP share only 1**. VISp/MOs comparisons can therefore use different sessions, but simultaneous coupling between those regions is not a suitable default project.

## Investigation plans

### D1 Stimulus coding versus choice coding

**Question:** On error trials, does pre-movement neural activity track the presented stimulus side or the animal’s actual choice?

**Decision-making relevance:** Separates sensory evidence from the action the animal selects.

**Core analysis:** Use low/medium nonzero contrasts and the four stimulus-side × choice combinations. Compare response contrasts in one region first, then repeat in another if time permits.

**Starter regions:** MOs / CP; VISp

**Data and scale:** Spikes plus contrast, choice and movement times. Pilot 3–5 sessions with enough errors in both directions.

**Key controls and interpretation:** Correct trials alone cannot separate stimulus from choice. Balance contrast/block and avoid fitting stimulus, choice and correctness as if they were independent. Choice also specifies wheel direction.

**Three-person split:**

- **Member A:** Build the four-condition trial table and QC counts.
- **Member B:** Compute aligned responses and stimulus/choice effect sizes.
- **Member C:** Check matching and session consistency; interpret the sensory/action distinction.

**Deliverable:** A four-condition response figure and per-session effect-size comparison.

**Total workload:** 12–18 person-hours; recommended.

### D2 Choice information before movement

**Question:** Can held-out choice predictions improve as neural activity is measured closer to movement onset?

**Decision-making relevance:** Examines the timing of signals associated with decision formation or action preparation.

**Core analysis:** Choose three prespecified pre-movement windows and fit a small regularized logistic decoder within sessions. Compare balanced accuracy with matched-condition label shuffles.

**Starter regions:** MOs / CP / SCm

**Data and scale:** Trial-aligned spikes; both choice directions. Start with one region and 3–5 sessions.

**Key controls and interpretation:** Use only pre-movement features; preserve stimulus/block balance, trial-wise splits and training-only preprocessing. Predictability does not establish an abstract decision signal.

**Three-person split:**

- **Member A:** Prepare windows and matched folds.
- **Member B:** Implement the decoder and control runs.
- **Member C:** Audit leakage and uncertainty; compare timing.

**Deliverable:** A decoding-versus-time plot with held-out controls.

**Total workload:** 14–20 person-hours; moderate.

### D3 Early neural responses and decision speed

**Question:** At the same stimulus contrast and side, do early neural responses differ between faster and slower choices?

**Decision-making relevance:** Links sensory processing to the time required to produce a decision-related action.

**Core analysis:** Split reaction times within matched stimulus conditions. Compare an early response measure and firing-rate curves, beginning in VISp.

**Starter regions:** VISp; MOs / LP

**Data and scale:** Spikes plus stimulus and first-movement times; 3–5 sessions can form a small pilot.

**Key controls and interpretation:** The neural window must end before movement on included trials. Report the resulting trial exclusions. Reaction time is a behavioral measure, not a direct readout of an internal decision time.

**Three-person split:**

- **Member A:** Prepare condition-matched reaction-time groups.
- **Member B:** Calculate early responses and session summaries.
- **Member C:** Check window/exclusion sensitivity and make figures.

**Deliverable:** Matched fast/slow response curves and session-level contrasts.

**Total workload:** 8–12 person-hours; recommended low workload.

### D4 Post-error adjustment and neural state

**Question:** After an error, do next-trial reaction time and pre-stimulus neural activity change together?

**Decision-making relevance:** Connects behavioral adaptation after feedback with a measurable neural state.

**Core analysis:** First summarize next-trial reaction time after correct/error outcomes using the local trial table. Add pre-stimulus firing from one region and compare matched conditions.

**Starter regions:** ACAd / MOs

**Data and scale:** Consecutive trial history, feedback and reaction times; additional regional spikes are required for the neural part.

**Key controls and interpretation:** Define the preceding trial before QC filtering; do not join nonadjacent surviving trials. Account for current difficulty, block, previous movement and different post-error timeout intervals. Association alone does not show executive control.

**Three-person split:**

- **Member A:** Build original consecutive-trial histories and behavioral summaries.
- **Member B:** Add pre-stimulus neural features.
- **Member C:** Match confounds and relate neural and behavioral contrasts.

**Deliverable:** A behavioral adaptation plot plus matched neural-state comparisons.

**Total workload:** 12–18 person-hours; recommended.

### D5 History dependent stay and switch choices

**Question:** Does pre-stimulus activity distinguish whether the next choice repeats or switches direction, beyond previous choice and outcome?

**Decision-making relevance:** Studies history-dependent action selection without fitting a subjective-prior model.

**Core analysis:** Define stay/switch from adjacent choices. Compare a small behavioral-history baseline with a model adding pre-stimulus neural features.

**Starter regions:** CP / MOs / ORBvl

**Data and scale:** Trial histories plus pre-stimulus spikes; require both stay and switch examples within history conditions.

**Key controls and interpretation:** Match current stimulus, block, previous direction and intertrial timing. Evaluate the neural increment on held-out trials; this does not establish causal intention.

**Three-person split:**

- **Member A:** Define histories and balanced labels.
- **Member B:** Fit behavioral and neural-augmented models.
- **Member C:** Audit splits and summarize the incremental prediction.

**Deliverable:** Held-out prediction improvement and a stay/switch condition table.

**Total workload:** 14–20 person-hours; moderate.

### D6 Stimulus difficulty and feedback responses

**Question:** Does the neural difference between correct and incorrect feedback depend on stimulus difficulty?

**Decision-making relevance:** Relates outcome processing to the evidence available during the decision.

**Core analysis:** Compare correct/error feedback within low/high nonzero contrast conditions and estimate their interaction at session level.

**Starter regions:** CP / ACAd; BLA

**Data and scale:** Feedback-aligned spikes, outcome and contrast. Check easy-error trial counts before choosing the topic.

**Key controls and interpretation:** Do not call a contrast-based difficulty category subjective surprise or reward prediction error. Reward, noise, licking and timeout differ between outcomes.

**Three-person split:**

- **Member A:** Count and match the four conditions.
- **Member B:** Compute feedback responses and interaction contrasts.
- **Member C:** Check sparse cells and alternative windows.

**Deliverable:** A difficulty-by-outcome response figure with session uncertainty.

**Total workload:** 14–22 person-hours; condition-count risk.

### D7 Block context and sensory responses

**Question:** For the same weak stimulus, does its early neural response differ between left-biased and right-biased blocks?

**Decision-making relevance:** Tests an association between task context and sensory processing.

**Core analysis:** Match weak nonzero contrast, stimulus side and trial timing across block contexts. Compare baseline and stimulus-evoked responses separately.

**Starter regions:** VISp / LGd / LP

**Data and scale:** Block labels, contrast and spikes; enough observations in both block contexts within each session.

**Key controls and interpretation:** The recorded block probability is objective task context, not a measured subjective belief. Check drift, choice and movement; do not equate a baseline shift with sensory gain.

**Three-person split:**

- **Member A:** Prepare matched context conditions.
- **Member B:** Separate baseline and evoked-response effects.
- **Member C:** Check session drift and behavioral confounds.

**Deliverable:** A matched-context response plot and baseline-control comparison.

**Total workload:** 12–18 person-hours; moderate.

### D8 Pre-stimulus state and response readiness

**Question:** Within the same stimulus condition, does pre-stimulus activity predict a faster or slower upcoming response?

**Decision-making relevance:** Examines trial-to-trial neural state before sensory evidence arrives.

**Core analysis:** Use pre-stimulus population rate or a few training-derived features to predict reaction time, beyond stimulus and recent-history covariates.

**Starter regions:** MOs / ACAd / MRN

**Data and scale:** Baseline spikes, movement timestamps and preceding-trial timing.

**Key controls and interpretation:** Compare within sessions; exclude contamination by previous feedback or movement. Without independent pupil/pose evidence, call it a neural state rather than measured arousal.

**Three-person split:**

- **Member A:** Prepare clean baseline windows and history covariates.
- **Member B:** Fit the small reaction-time model.
- **Member C:** Check history/timing controls and session consistency.

**Deliverable:** Observed versus predicted reaction-time summaries and baseline response plots.

**Total workload:** 10–16 person-hours; accessible.

### D9 Stability of choice signals within a session

**Question:** Does a choice decoder trained early in a session generalize to later trials?

**Decision-making relevance:** Investigates stability of decision-related representations over time.

**Core analysis:** Compare held-out early, held-out late, and early-to-late decoding with matched contrast, choice and block distributions. Keep unit identities fixed.

**Starter regions:** MOs / CP

**Data and scale:** Long sessions with enough trials and stable units; additional spike trains required.

**Key controls and interpretation:** Unequal training sizes and unit drift can mimic changing representations. A time effect alone does not identify fatigue or learning.

**Three-person split:**

- **Member A:** Check unit stability and balanced early/late samples.
- **Member B:** Implement temporal generalization.
- **Member C:** Audit training-size and drift controls.

**Deliverable:** A small early/late generalization matrix and stability controls.

**Total workload:** 16–24 person-hours; upper-budget option.

### D10 Active decisions versus passive replay

**Question:** Do the same visual stimuli evoke different responses when the animal performs the task versus during passive replay?

**Decision-making relevance:** Relates sensory responses to task engagement in a decision-making setting.

**Core analysis:** Use the same units across active and passive periods, matching contrast and stimulus side. Compare baseline-adjusted responses.

**Starter regions:** VISp / LP / LGd

**Data and scale:** Task spikes and passive Gabor tables from the same session. The earlier metadata search found 398 BWM sessions with passive Gabor files, not 398 eligible sessions for every region.

**Key controls and interpretation:** Check actual stimulus equivalence, corrected passive timestamps, recording drift and movement. Task-state differences do not isolate a decision computation.

**Three-person split:**

- **Member A:** Verify paired protocol eligibility and timestamp versions.
- **Member B:** Match stimuli and calculate active/passive contrasts.
- **Member C:** Check drift, baseline and movement controls.

**Deliverable:** Same-unit active/passive response comparisons.

**Total workload:** 14–22 person-hours; extra data preparation.

### D11 Population size and choice information

**Question:** How does held-out choice prediction change as more simultaneously recorded neurons are included?

**Decision-making relevance:** Examines the distribution of choice-related information across a neural ensemble.

**Core analysis:** Use one fixed pre-movement window and repeated random neuron subsets. Hold trial splits and class balance fixed across subset sizes.

**Starter regions:** MOs / CP

**Data and scale:** Sessions with enough good units for a shared population-size grid. Begin in one region.

**Key controls and interpretation:** Keep neuron selection and scaling inside training folds. Do not pool unmatched unit identities across sessions or infer biological information limits from one decoder.

**Three-person split:**

- **Member A:** Prepare eligible sessions and subset schedules.
- **Member B:** Run fixed-window population-size decoding.
- **Member C:** Audit selection leakage and summarize sampling uncertainty.

**Deliverable:** Choice-decoding curves versus neuron count with shuffle controls.

**Total workload:** 16–24 person-hours; computational option.

### D12 Coordination between simultaneously recorded regions

**Question:** Do trial-to-trial choice-related signals covary between MOs and CP after accounting for stimulus and block?

**Decision-making relevance:** Examines coordinated decision-related activity across cortical and striatal populations.

**Core analysis:** Build separate held-out regional readouts on identical trials, then assess residual covariation using session-aware controls.

**Starter regions:** MOs + CP in the same session

**Data and scale:** The downloaded unit metadata contain 7 sessions from 7 mice with at least 5 good units in both MOs and CP. Trial and signal eligibility remain to be checked.

**Key controls and interpretation:** Shared stimulus, movement, slow drift and readout fitting can produce covariation. Cross-fitting and time-aware nulls are necessary; correlation does not demonstrate directed communication or causality.

**Three-person split:**

- **Member A:** Verify simultaneous pairs and exact trial correspondence.
- **Member B:** Build cross-fitted regional readouts.
- **Member C:** Develop shared-input/drift controls and assess uncertainty.

**Deliverable:** Paired-session residual-covariation summaries and controls.

**Total workload:** 24–36 person-hours; stretch beyond usual budget.

## Recommended combinations and schedule

- **Most direct sensory-versus-choice story: D1.** Use error trials to distinguish sensory evidence from the selected action.
- **Lowest workload: D3.** Relate neural responses to decision speed at matched stimulus conditions; start in one region, approximately 8–12 person-hours.
- **Feedback-dependent behavioral adaptation: D4.** Begin with a behavioral pilot from the existing trial table, then add ACAd or MOs spikes.
- **For decoding: D2.** Start with one region and three fixed windows; reserve D11 as a later extension.
- **For task engagement: D10.** Confirm matched active/passive protocols from the same units before selecting the project.
- **Coherent two-question combination: D3+D8, approximately 14–20 person-hours.** Study pre-stimulus state and early sensory responses in relation to decision speed, sharing reaction-time groups and recordings.
- **Another combination: D4+D6, approximately 20–28 person-hours.** Connect outcome responses to the next decision, with greater risk of exceeding the budget.
- **D12 is a stretch direction**, not a recommended first analysis within this course schedule.

On days 1–2, choose one question, read the relevant paper sections and fix the primary measure. Member A checks whether one session has enough observations. If errors or minority classes are insufficient, reduce stratification, expand a prespecified session set or change question; do not select sessions by the observed effect. On days 3–5, Member A expands to 3–5 eligible sessions, Member B implements the core analysis, and Member C independently audits windows, matching and splits. In week 2, complete one key robustness check and jointly prepare figures, limitations and the report. For a one-week project, retain only the one-region core.

## Common analytical boundaries

- All topics are observational. Choice direction is tied to wheel-action direction; decoding or correlation alone does not isolate a pure decision-formation mechanism.
- Subjective confidence, accumulated evidence, arousal and reward prediction error are not directly recorded variables. Contrast, reaction time and block labels are related task or behavioral measures.
- Construct history and adjacency in original trial order before masking. Recount the usable observations for each proposed condition.
- Check session IDs, revisions and original trial correspondence when joining aggregate tables to downloaded spikes/trials. Do not assume different revisions or filtered rows remain positionally aligned. Check the saturation flag appropriate to each event window.
- Summarize at session/mouse level rather than treating every neuron from a mouse as an independent biological replicate. With few sessions, emphasize effect sizes and uncertainty; significance and statistical power are not guaranteed.
- For decoders, fit selection, scaling and tuning only on training data, keep complete trials in folds, and check stimulus/block confounds and slow session drift. Randomly interleaving adjacent trials alone can give optimistic performance.
- The main paper already studies choice, outcome and movement representations. These are suitable reproduction-plus-extension course questions; novelty needs a focused check after selection. See the [main paper](https://doi.org/10.1038/s41586-025-09235-0), [trial documentation](https://docs.internationalbrainlab.org/notebooks_external/loading_trials_data.html), and this repository's loading/decoding implementations.

The following sections retain the full data scope, online access instructions and complete region appendix. General anatomical themes remain as background; D1–D12 above are the decision-focused shortlist.

## Full data inventory and coverage

**Scope:** the paper-linked BWM cohort, all 279 areas in this checkout's region table, and relevant data modalities. Counts below refer to the named source snapshots, not a fresh database-wide download audit. Other IBL collections are listed separately in the [public dataset catalog](https://docs.internationalbrainlab.org/public_docs/dataset_overview.html); they are not added to this cohort's totals.

### Cohort size and inclusion levels

The frozen cohort contains **699 probe insertions, 459 sessions, 139 mice, and 12 laboratories**. Spike sorting yielded **621,733 units**, including multiunit activity; **75,708** pass unit QC. Subsequent restrictions produce different region and neuron counts. [Main paper](https://doi.org/10.1038/s41586-025-09235-0); [local inclusion stages](../brainwidemap/meta/inclusion_info.csv).

| Dataset or restriction | Amount and interpretation |
| --- | --- |
| Released cohort | 699 insertions; 459 sessions; 139 mice; 12 laboratories |
| All sorted units | 621,733 units; not all are well-isolated single neurons |
| Unit QC | 75,708 good-quality units across 268 region labels in the inclusion summary |
| Gray-matter units after QC | 65,336 good units across 266 regions |
| At least 5 units per session-region and at least 2 qualifying sessions per region | 62,990 units across 210 regions |
| Additional minimum of 20 pooled units per region for main figures | 62,857 units across 201 regions |
| Full region table in this checkout | 279 named areas; 210 rows have canonical=True; 13 areas have zero listed good units |

The regional table is a different summary view: its regional unit columns sum to **521,709 units and 65,336 good units**, and should not be substituted for the release-wide total of 621,733. The appendix preserves the source column definitions. Its canonical flag marks the 210-region stage, rather than guaranteeing membership in the final 201-region main-figure cohort. Forty-five areas have fewer than three listed recordings.

Recording counts are reported exactly as “# recordings” in the source. They are not independently recounted unique sessions or mice. A probe may traverse multiple regions, so regional recording counts must not be summed to obtain the number of experiments. Regions were sampled across sessions; arbitrary region pairs are not guaranteed to have simultaneous recordings. The dataset spans the left forebrain/midbrain and right hindbrain/cerebellum, rather than providing equivalent bilateral sampling everywhere.

### Available modalities and their amounts

| Data type | Available information | Amount or coverage | Possible use |
| --- | --- | --- | --- |
| Processed electrophysiology | Spike times, clusters, amplitudes, depths, QC and unit IDs | 699-insertion cohort; unit counts depend on filtering above | Event responses, variability, selectivity and small decoders |
| Anatomy and probe metadata | Atlas region labels, coordinates, probe/session/mouse/laboratory links | 279 named areas in the supplied regional table | Compare anatomical systems and select adequately sampled regions |
| Behavioral trials | Contrast, stimulus side, choice, feedback, block probability and event times | 295,920 downloaded rows; 196,574 pass the existing BWM mask; further project-specific filtering required | Match trial conditions and align neural activity |
| Wheel behavior | Position and timestamps; derived speed, velocity and movement timing | Session-linked; no separate complete-session count established here | Neural correlates of movement direction, speed and onset |
| Pose, motion and eye measures | Camera pose estimates, motion energy and pupil/eye-derived signals where present | Subset with camera-specific availability and QC; no claim of coverage in all 459 sessions | Movement controls and exploratory neural-behavior associations |
| Passive protocol and spontaneous activity | Spontaneous periods, receptive-field mapping, and visual/auditory task replay | Only recordings containing the relevant protocol; eligible-session count not established | Active versus passive responses, spontaneous versus evoked activity |
| Waveforms and autocorrelograms | Peak waveforms, logarithmic ACGs and shared ACG time bins | 2026_Q2 helper lists clusters.pqt plus 3 NumPy array files; array row counts not audited | Exploratory waveform/temporal-feature comparisons; not cell-type ground truth |
| Raw ephys and camera recordings | AP/LFP data and camera video through ONE where released | Session/dataset-dependent; large files; no complete file or byte census here | Optional LFP, video or spike-sorting projects outside the recommended core scope |
| Widefield calcium imaging | Cortical spatial/temporal components, timestamps and atlas alignment | Separate companion-paper cohort: 51 analyzed sessions in 6 mice; not part of the 699-insertion electrophysiology cohort | Cortical event-response comparisons; additional packages and preparation needed |
| Analysis summaries and decoder outputs | Regional analysis scores in this repo; code can generate trial-wise predictions and masks | 279-row regional summary is local; full trial-wise decoder results are not cached locally | Topic selection; trial-wise questions require suitable outputs to be obtained or generated |

The [release notes](https://docs.internationalbrainlab.org/notebooks_external/2025_data_release_brainwidemap.html) document additions including passive intervals and enhanced pose estimates, and a correction to passive Gabor alignment. Use compatible current dataset revisions for such projects. Trial, video, passive and wheel availability should be checked by session before committing to a topic. The selected historical loader revision is not an assurance that later corrections have been applied.

See [IBL loading examples](https://docs.internationalbrainlab.org/loading_examples.html), [passive data documentation](https://docs.internationalbrainlab.org/notebooks_external/loading_passive_data.html), and [widefield documentation](https://docs.internationalbrainlab.org/notebooks_external/loading_widefield_data.html). The [companion paper](https://doi.org/10.1038/s41586-025-09226-1) reports the analyzed widefield cohort; acquisition counts and counts retained for particular analyses can differ. Existing waveform/ACG array rows must be matched to the clusters table from the same aggregate release. The current aggregate default lacks a trials checksum entry, as explained in the reproduction guide.

### Coverage across all major anatomical groups

The following values are sums of the regional summary columns. A good-unit count describes listed QC-passing units, not an independently verified final analysis sample.

| Anatomical group | Areas | Table units | Good units | Examples |
| --- | --- | --- | --- | --- |
| Isocortex (Isocortex) | 43 | 97,041 | 13,002 | VISp, MOs |
| Olfactory areas (OLF) | 11 | 15,011 | 2,027 | PIR, AON |
| Hippocampal formation (HPF) | 15 | 81,295 | 7,021 | CA1, DG |
| Cortical subplate (CTXsp) | 7 | 7,149 | 873 | BLA, BMA |
| Cerebral nuclei (CNU) | 21 | 48,088 | 6,386 | CP, ACB |
| Thalamus (TH) | 44 | 62,110 | 11,222 | LGd, LP |
| Hypothalamus (HY) | 27 | 7,898 | 847 | LHA, MPO |
| Midbrain (MB) | 35 | 81,616 | 9,049 | SCm, MRN |
| Hindbrain (HB) | 56 | 69,327 | 7,871 | PRNr, GRN |
| Cerebellum (CB) | 20 | 52,174 | 7,038 | SIM, IP |

### Project themes across the full coverage

Starter-region amounts are recordings/good units. Workloads are total person-hours for a small pilot. These are proposed questions, not results or a guarantee that every region in a group is suitable.

| System | Starter regions and amounts | Possible question | Hours |
| --- | --- | --- | --- |
| Isocortex | VISp 65/880; MOs 60/1,293 | Do stimulus and movement responses differ between VISp and MOs? | 10–15 |
| Olfactory areas | PIR 33/614; AON 15/428 | Do PIR and AON show task-event responses during this visual task? | 10–16 |
| Hippocampal formation | CA1 168/1,807; DG 171/1,137 | Do CA1 and DG differ in feedback-aligned response magnitude? | 10–15 |
| Cortical subplate | BLA 15/150; BMA 16/175 | Do BLA and BMA differ in correct-versus-error feedback responses? | 12–18 |
| Cerebral nuclei | CP 83/2,892; ACB 24/340 | Do CP and ACB differ in movement- or feedback-aligned activity? | 10–15 |
| Thalamus | LGd 29/557; LP 85/1,812 | Do LGd and LP differ in stimulus-evoked response magnitude? | 10–14 |
| Hypothalamus | LHA 16/166; MPO 4/40 | Does LHA activity change around movement or feedback? | 12–18 |
| Midbrain | SCm 78/1,666; MRN 137/2,678 | Do SCm and MRN differ in movement-aligned response profiles? | 10–15 |
| Hindbrain | PRNr 28/770; GRN 17/560 | Do PRNr and GRN differ in first-movement-aligned activity? | 10–15 |
| Cerebellum | SIM 23/893; IP 31/619 | Do SIM and IP differ in movement- or feedback-related responses? | 10–16 |

Use a common three-person split for these additional themes: **Member A** handles session selection, condition counts, QC and the common spike-count table; **Member B** produces aligned responses and the agreed primary effect size; **Member C** handles condition matching, session/mouse summaries, robustness checks and interpretation. All three contribute to the final report. Responses in olfactory areas during a visual task do not demonstrate olfactory coding; hippocampal event responses alone do not establish a memory mechanism. Sparsely sampled hypothalamic areas warrant a descriptive pilot first.

Additional modalities offer these extensions:

| Extension | Data and main limitation | Hours |
| --- | --- | --- |
| Active versus passive visual responses | Same-unit task spikes and passive replay; verify protocol, matched stimuli and corrected revisions | 14–22 |
| Spontaneous versus task-evoked activity | Recordings containing both periods; account for movement and state differences | 12–18 |
| Firing rate versus wheel speed | Aligned spikes and wheel timestamps; check direction/event/speed correlations | 12–18 |
| Neural activity versus pose or motion energy | Reliable camera signals; video synchronization and QC add preparation costs | 18–30 |
| Regional waveform-width or ACG distributions | Same-release clusters and arrays; preserve row alignment and avoid cell-type claims | 16–24 |
| Cortical event responses in widefield imaging | Separate imaging cohort; wfield and atlas registration preparation | 20–35 |

These estimates include eligibility and compatibility work and are less certain than the existing spike/trial workflow. For a one-to-two-week project, prioritize standard spike analyses, or active/passive comparisons only after confirming suitable passive recordings.

The [existing reproduction notebook](../notebooks/reproduce_bwm.ipynb) remains the starting point for loading, QC, spike counting and plotting. See the [reproduction guide](reproduction.md) for environment setup and release caveats. Disable proxies before Python data fetching.

## Obtaining the data online

The public endpoints were checked on 2026-11-15. All six aggregate files below returned HTTP 200. The historical 2024 unit/trial tables have now been fully downloaded and verified by the user; the larger 2026 files have only been checked for online availability. The small ACG time-bin file was downloaded and its MD5 verified; small example-session trial files were also fetched successfully through ONE. These checks retrieve data and metadata without answering the proposed research questions.

**Run this single line from the repository root to obtain the historical cohort-wide unit and trial tables:**

```sh
uv run --locked python scripts/fetch_project_data.py tables
```

The pair totals **110.4 MiB** and is saved to `data/aggregates/2024_Q2_IBL_et_al_BWM/`. It needs no OpenAlyx login or AWS credentials. These are aggregate tables, not all 699 probe recordings. MD5 checks detect incomplete or changed downloads; existing valid files are reused, and releases are kept in separate directories.

| Release | File | Bytes |
|---|---|---:|
| 2024_Q2_IBL_et_al_BWM | trials.pqt | 24,212,510 |
| 2024_Q2_IBL_et_al_BWM | clusters.pqt | 91,555,529 |
| 2026_Q2_IBL_et_al_BWM | clusters.pqt | 112,325,731 |
| 2026_Q2_IBL_et_al_BWM | clusters.waveforms_peak.npy | 159,163,776 |
| 2026_Q2_IBL_et_al_BWM | clusters.acgs_log.npy | 159,163,776 |
| 2026_Q2_IBL_et_al_BWM | acgs_log.times.npy | 1,152 |

To check availability without downloading contents, append `--check-only`. To fetch all four newer waveform/ACG release files (410.7 MiB), use:

```sh
uv run --locked python scripts/fetch_project_data.py tables --release 2026
```

The newer set has no trials entry in the repository's checksum manifest. Match its waveform/ACG rows to its own clusters table, rather than mixing release versions. The tiny-file test is available as `tables --release 2026 --files acgs_log.times`.

**For processed spike trains and trials from one probe:**

```sh
uv run --locked python scripts/fetch_project_data.py probe
```

This uses the notebook's example probe and historical loader revisions. Specify `probe --pid YOUR_PROBE_UUID` for another insertion in the frozen cohort. No statistical analysis is performed.

**For session-specific modalities and current dataset revisions:**

```sh
uv run --locked python scripts/fetch_project_data.py session --profile trials
uv run --locked python scripts/fetch_project_data.py session --profile wheel
uv run --locked python scripts/fetch_project_data.py session --eid YOUR_SESSION_UUID --profile pose --list-only
```

Profiles include `trials`, `wheel`, `pose`, `passive`, and `widefield`. Use `--list-only` to inspect a session first; remove it to fetch matching processed files. Optional modalities are not present in every session. ONE's own revision selection is applied per dataset and exact selected paths are recorded.

**Find suitable session IDs before choosing an optional modality:**

```sh
uv run --locked python scripts/fetch_project_data.py find --dataset _ibl_passiveGabor.table.csv --bwm-only
uv run --locked python scripts/fetch_project_data.py find --dataset widefieldU.images.npy
```

The live exact-filename search found **398 sessions in the frozen BWM cohort with passive Gabor data**, and **50 sessions with widefieldU.images.npy** across the public database. These are search matches, not QC-qualified samples. The latter is distinct from the paper's 51-session widefield analysis cohort; this difference has not been reconciled. Dataset filenames must include any namespace, such as `_ibl_`.

A passive session with confirmed metadata can be inspected and then downloaded by removing `--list-only`:

```sh
uv run --locked python scripts/fetch_project_data.py session --eid 4ecb5d24-f5cc-402c-be28-9d0f7cb14b3a --profile passive --list-only
```

For widefield, substitute an ID from the search and use `session --eid YOUR_SESSION_UUID --profile widefield --list-only`; remove the listing flag to fetch its processed components. Raw video/ephys and full RF stimulus files require explicit dataset selection; profiles do not silently fetch those larger files. The [complete access guide](data_access.md) covers exact-name/glob downloads and other commands.

ONE access currently works with the shared demo login, which the server warns will be retired. Set `BWM_ONE_TOKEN` locally for your personal API token, or set `BWM_ONE_USERNAME` and `BWM_ONE_PASSWORD`. Public S3 table downloads do not use those credentials. The script disables HTTP/HTTPS/ALL proxies before networking imports. If uv itself needs a proxy-free package install, prefix the command with `HTTP_PROXY= HTTPS_PROXY= ALL_PROXY= http_proxy= https_proxy= all_proxy=`.

ONE files default to `data/one/`; `BWM_CACHE_DIR` overrides that session cache. Download/search manifests are saved under `data/manifests/`, or alongside aggregate files. The global `--cache-dir /path/to/data` option changes the script's data root and goes before the subcommand. Downloads are cached and no credentials are written into manifests. Use `session --list-only --include '*'` to inspect all filenames before selecting a less common dataset.

References: [public S3 registry](https://registry.opendata.aws/ibl-brain-wide-map/), [current BWM release](https://docs.internationalbrainlab.org/notebooks_external/2025_data_release_brainwidemap.html), and [ONE data explorer](https://viz.internationalbrainlab.org).

## Appendix Complete inventory of 279 regions

Acronyms and full English names preserve the source atlas labels for direct use with code. Proposed themes and workloads for each group are above. The last column is only the source canonical flag, not final 201-region eligibility. Areas with zero good units do not support the proposed neuron analyses using the default good-unit filter.

### Isocortex (Isocortex)

| Region | Atlas name | Recordings | Units | Good units | Flag |
| --- | --- | --- | --- | --- | --- |
| ACAd | Anterior cingulate area dorsal part | 24 | 1,960 | 369 | True |
| ACAv | Anterior cingulate area ventral part | 18 | 1,388 | 195 | True |
| AId | Agranular insular area dorsal part | 10 | 1,100 | 188 | True |
| AIp | Agranular insular area posterior part | 8 | 533 | 93 | True |
| AIv | Agranular insular area ventral part | 8 | 725 | 149 | True |
| AUDd | Dorsal auditory area | 9 | 991 | 133 | True |
| AUDp | Primary auditory area | 7 | 1,450 | 167 | True |
| AUDpo | Posterior auditory area | 6 | 439 | 46 | True |
| AUDv | Ventral auditory area | 10 | 1,061 | 253 | True |
| ECT | Ectorhinal area | 9 | 729 | 85 | True |
| FRP | Frontal pole cerebral cortex | 11 | 812 | 88 | True |
| GU | Gustatory areas | 5 | 445 | 69 | True |
| ILA | Infralimbic area | 12 | 2,008 | 314 | True |
| MOp | Primary motor area | 37 | 8,796 | 1,458 | True |
| MOs | Secondary motor area | 60 | 10,023 | 1,293 | True |
| ORBl | Orbital area lateral part | 8 | 2,164 | 199 | True |
| ORBm | Orbital area medial part | 10 | 1,856 | 313 | True |
| ORBvl | Orbital area ventrolateral part | 10 | 3,060 | 669 | True |
| PERI | Perirhinal area | 7 | 163 | 36 | False |
| PL | Prelimbic area | 21 | 2,165 | 420 | True |
| RSPagl | Retrosplenial area lateral agranular part | 36 | 2,281 | 310 | True |
| RSPd | Retrosplenial area dorsal part | 38 | 3,088 | 318 | True |
| RSPv | Retrosplenial area ventral part | 38 | 4,617 | 528 | True |
| SSp-bfd | Primary somatosensory area barrel field | 32 | 5,226 | 488 | True |
| SSp-ll | Primary somatosensory area lower limb | 13 | 1,434 | 130 | True |
| SSp-m | Primary somatosensory area mouth | 13 | 3,567 | 354 | True |
| SSp-n | Primary somatosensory area nose | 9 | 1,214 | 72 | True |
| SSp-tr | Primary somatosensory area trunk | 15 | 1,930 | 303 | True |
| SSp-ul | Primary somatosensory area upper limb | 16 | 1,761 | 196 | True |
| SSp-un | Primary somatosensory area unassigned | 8 | 600 | 67 | True |
| SSs | Supplemental somatosensory area | 15 | 3,168 | 439 | True |
| TEa | Temporal association areas | 11 | 1,040 | 166 | True |
| VISC | Visceral area | 6 | 375 | 61 | True |
| VISa | Anterior area | 56 | 6,222 | 940 | True |
| VISal | Anterolateral visual area | 5 | 697 | 95 | True |
| VISam | Anteromedial visual area | 26 | 2,581 | 374 | True |
| VISl | Lateral visual area | 14 | 1,559 | 151 | True |
| VISli | Laterointermediate area | 9 | 656 | 83 | True |
| VISp | Primary visual area | 65 | 8,559 | 880 | True |
| VISpl | Posterolateral visual area | 14 | 523 | 95 | True |
| VISpm | posteromedial visual area | 22 | 1,995 | 241 | True |
| VISpor | Postrhinal area | 8 | 889 | 99 | True |
| VISrl | Rostrolateral visual area | 10 | 1,191 | 75 | True |

### Olfactory areas (OLF)

| Region | Atlas name | Recordings | Units | Good units | Flag |
| --- | --- | --- | --- | --- | --- |
| AOB | Accessory olfactory bulb | 2 | 90 | 0 | False |
| AON | Anterior olfactory nucleus | 15 | 3,534 | 428 | True |
| COAa | Cortical amygdalar area anterior part | 4 | 113 | 17 | False |
| COAp | Cortical amygdalar area posterior part | 20 | 1,899 | 121 | True |
| DP | Dorsal peduncular area | 19 | 1,637 | 318 | True |
| MOB | Main olfactory bulb | 3 | 1,227 | 140 | True |
| PAA | Piriform-amygdalar area | 5 | 490 | 82 | True |
| PIR | Piriform area | 33 | 3,735 | 614 | True |
| TR | Postpiriform transition area | 9 | 508 | 37 | True |
| TTd | Taenia tecta dorsal part | 14 | 1,771 | 270 | True |
| TTv | Taenia tecta ventral part | 1 | 7 | 0 | False |

### Hippocampal formation (HPF)

| Region | Atlas name | Recordings | Units | Good units | Flag |
| --- | --- | --- | --- | --- | --- |
| APr | Area prostriata | 9 | 328 | 16 | True |
| CA1 | Field CA1 | 168 | 23,169 | 1,807 | True |
| CA2 | Field CA2 | 33 | 656 | 39 | True |
| CA3 | Field CA3 | 88 | 12,085 | 950 | True |
| DG | Dentate gyrus | 171 | 18,156 | 1,137 | True |
| ENTl | Entorhinal area lateral part | 22 | 4,321 | 585 | True |
| ENTm | Entorhinal area medial part dorsal zone | 20 | 4,151 | 639 | True |
| FC | Fasciola cinerea | 6 | 221 | 23 | True |
| HATA | Hippocampo-amygdalar transition area | 8 | 578 | 59 | True |
| IG | Induseum griseum | 5 | 134 | 9 | False |
| PAR | Parasubiculum | 10 | 2,119 | 117 | True |
| POST | Postsubiculum | 26 | 3,243 | 233 | True |
| PRE | Presubiculum | 11 | 1,693 | 115 | True |
| ProS | Prosubiculum | 29 | 3,095 | 378 | True |
| SUB | Subiculum | 42 | 7,346 | 914 | True |

### Cortical subplate (CTXsp)

| Region | Atlas name | Recordings | Units | Good units | Flag |
| --- | --- | --- | --- | --- | --- |
| BLA | Basolateral amygdalar nucleus | 15 | 1,565 | 150 | True |
| BMA | Basomedial amygdalar nucleus | 16 | 1,645 | 175 | True |
| CLA | Claustrum | 6 | 355 | 49 | True |
| EPd | Endopiriform nucleus dorsal part | 15 | 1,254 | 199 | True |
| EPv | Endopiriform nucleus ventral part | 12 | 822 | 124 | True |
| LA | Lateral amygdalar nucleus | 8 | 583 | 63 | True |
| PA | Posterior amygdalar nucleus | 17 | 925 | 113 | True |

### Cerebral nuclei (CNU)

| Region | Atlas name | Recordings | Units | Good units | Flag |
| --- | --- | --- | --- | --- | --- |
| AAA | Anterior amygdalar area | 3 | 265 | 25 | True |
| ACB | Nucleus accumbens | 24 | 2,655 | 340 | True |
| BST | Bed nuclei of the stria terminalis | 17 | 1,797 | 207 | True |
| CEA | Central amygdalar nucleus | 15 | 1,101 | 159 | True |
| CP | Caudoputamen | 83 | 25,339 | 2,892 | True |
| FS | Fundus of striatum | 5 | 166 | 32 | True |
| GPe | Globus pallidus external segment | 13 | 1,807 | 322 | True |
| GPi | Globus pallidus internal segment | 6 | 415 | 45 | True |
| IA | Intercalated amygdalar nucleus | 2 | 82 | 18 | True |
| LSc | Lateral septal nucleus caudal (caudodorsal) part | 12 | 749 | 111 | True |
| LSr | Lateral septal nucleus rostral (rostroventral) part | 32 | 5,686 | 1,156 | True |
| LSv | Lateral septal nucleus ventral part | 17 | 1,303 | 164 | True |
| MA | Magnocellular nucleus | 7 | 363 | 48 | True |
| MEA | Medial amygdalar nucleus | 13 | 1,435 | 184 | True |
| MS | Medial septal nucleus | 6 | 724 | 106 | True |
| NDB | Diagonal band nucleus | 5 | 347 | 50 | True |
| OT | Olfactory tubercle | 20 | 872 | 79 | True |
| SF | Septofimbrial nucleus | 12 | 751 | 115 | True |
| SH | Septohippocampal nucleus | 2 | 61 | 4 | False |
| SI | Substantia innominata | 27 | 1,592 | 256 | True |
| TRS | Triangular nucleus of septum | 8 | 578 | 73 | True |

### Thalamus (TH)

| Region | Atlas name | Recordings | Units | Good units | Flag |
| --- | --- | --- | --- | --- | --- |
| AD | Anterodorsal nucleus | 3 | 229 | 15 | True |
| AM | Anteromedial nucleus | 10 | 902 | 128 | True |
| AV | Anteroventral nucleus of thalamus | 11 | 1,418 | 203 | True |
| CL | Central lateral nucleus of the thalamus | 12 | 433 | 38 | True |
| CM | Central medial nucleus of the thalamus | 7 | 270 | 65 | True |
| Eth | Ethmoid nucleus of the thalamus | 21 | 1,673 | 366 | True |
| IAD | Interanterodorsal nucleus of the thalamus | 4 | 125 | 23 | True |
| IAM | Interanteromedial nucleus of the thalamus | 2 | 22 | 7 | False |
| IGL | Intergeniculate leaflet of the lateral geniculate complex | 4 | 179 | 16 | True |
| IMD | Intermediodorsal nucleus of the thalamus | 2 | 6 | 1 | False |
| IntG | Intermediate geniculate nucleus | 2 | 35 | 6 | False |
| LD | Lateral dorsal nucleus of thalamus | 25 | 3,062 | 581 | True |
| LGd | Dorsal part of the lateral geniculate complex | 29 | 2,925 | 557 | True |
| LGv | Ventral part of the lateral geniculate complex | 10 | 1,060 | 143 | True |
| LH | Lateral habenula | 16 | 787 | 76 | True |
| LP | Lateral posterior nucleus of the thalamus | 85 | 8,064 | 1,812 | True |
| MD | Mediodorsal nucleus of thalamus | 23 | 2,917 | 604 | True |
| MG | Medial geniculate complex | 16 | 1,557 | 332 | True |
| MH | Medial habenula | 14 | 308 | 38 | True |
| PCN | Paracentral nucleus | 12 | 389 | 84 | True |
| PF | Parafascicular nucleus | 10 | 1,055 | 150 | True |
| PIL | Posterior intralaminar thalamic nucleus | 6 | 180 | 11 | False |
| PO | Posterior complex of the thalamus | 53 | 10,659 | 2,329 | True |
| POL | Posterior limiting nucleus of the thalamus | 21 | 1,378 | 166 | True |
| PP | Peripeduncular nucleus | 4 | 105 | 13 | False |
| PR | Perireunensis nucleus | 5 | 196 | 28 | True |
| PT | Parataenial nucleus | 2 | 19 | 4 | False |
| PVT | Paraventricular nucleus of the thalamus | 12 | 515 | 84 | True |
| PoT | Posterior triangular thalamic nucleus | 21 | 1,591 | 228 | True |
| RE | Nucleus of reuniens | 3 | 148 | 8 | False |
| RH | Rhomboid nucleus | 3 | 66 | 6 | False |
| RT | Reticular nucleus of the thalamus | 25 | 3,177 | 421 | True |
| SGN | Suprageniculate nucleus | 11 | 571 | 131 | True |
| SMT | Submedial nucleus of the thalamus | 6 | 829 | 140 | True |
| SPA | Subparafascicular area | 7 | 347 | 25 | False |
| SPF | Subparafascicular nucleus | 21 | 758 | 70 | True |
| SubG | Subgeniculate nucleus | 1 | 48 | 7 | False |
| VAL | Ventral anterior-lateral complex of the thalamus | 11 | 1,544 | 295 | True |
| VM | Ventral medial nucleus of the thalamus | 19 | 790 | 118 | True |
| VPL | Ventral posterolateral nucleus of the thalamus | 24 | 2,799 | 436 | True |
| VPLpc | Ventral posterolateral nucleus of the thalamus parvicellular part | 12 | 527 | 80 | True |
| VPM | Ventral posteromedial nucleus of the thalamus | 41 | 7,984 | 1,310 | True |
| VPMpc | Ventral posteromedial nucleus of the thalamus parvicellular part | 10 | 456 | 67 | True |
| Xi | Xiphoid thalamic nucleus | 1 | 7 | 0 | False |

### Hypothalamus (HY)

| Region | Atlas name | Recordings | Units | Good units | Flag |
| --- | --- | --- | --- | --- | --- |
| ADP | Anterodorsal preoptic nucleus | 1 | 80 | 5 | False |
| AHN | Anterior hypothalamic nucleus | 4 | 180 | 10 | False |
| AVP | Anteroventral preoptic nucleus | 3 | 161 | 15 | False |
| DMH | Dorsomedial nucleus of the hypothalamus | 4 | 140 | 16 | False |
| LHA | Lateral hypothalamic area | 16 | 1,147 | 166 | True |
| LM | Lateral mammillary nucleus | 2 | 34 | 8 | False |
| LPO | Lateral preoptic area | 4 | 291 | 89 | True |
| MEPO | Median preoptic nucleus | 1 | 32 | 5 | False |
| MM | Medial mammillary nucleus | 4 | 276 | 5 | False |
| MPN | Medial preoptic nucleus | 1 | 24 | 2 | False |
| MPO | Medial preoptic area | 4 | 315 | 40 | True |
| PH | Posterior hypothalamic nucleus | 9 | 717 | 24 | True |
| PMd | Dorsal premammillary nucleus | 1 | 54 | 2 | False |
| PMv | Ventral premammillary nucleus | 1 | 64 | 0 | False |
| PS | Parastrial nucleus | 2 | 192 | 35 | True |
| PSTN | Parasubthalamic nucleus | 3 | 98 | 8 | False |
| PVH | Paraventricular hypothalamic nucleus | 2 | 67 | 5 | False |
| PVHd | Paraventricular hypothalamic nucleus descending division | 5 | 109 | 6 | False |
| PVp | Periventricular hypothalamic nucleus posterior part | 1 | 3 | 0 | False |
| PeF | Perifornical nucleus | 5 | 196 | 28 | True |
| SFO | Subfornical organ | 1 | 1 | 0 | False |
| STN | Subthalamic nucleus | 4 | 93 | 6 | False |
| SUM | Supramammillary nucleus | 5 | 242 | 10 | False |
| TU | Tuberal nucleus | 1 | 69 | 8 | False |
| VLPO | Ventrolateral preoptic nucleus | 1 | 16 | 0 | False |
| VMH | Ventromedial hypothalamic nucleus | 4 | 117 | 2 | False |
| ZI | Zona incerta | 50 | 3,180 | 352 | True |

### Midbrain (MB)

| Region | Atlas name | Recordings | Units | Good units | Flag |
| --- | --- | --- | --- | --- | --- |
| APN | Anterior pretectal nucleus | 63 | 14,098 | 1,543 | True |
| AT | Anterior tegmental nucleus | 4 | 218 | 23 | False |
| CLI | Central linear nucleus raphe | 6 | 361 | 89 | True |
| CUN | Cuneiform nucleus | 11 | 1,013 | 100 | True |
| DR | Dorsal nucleus raphe | 2 | 370 | 42 | True |
| DT | Dorsal terminal nucleus of the accessory optic tract | 3 | 54 | 9 | False |
| EW | Edinger-Westphal nucleus | 2 | 3 | 0 | False |
| IC | Inferior colliculus | 26 | 5,812 | 458 | True |
| IF | Interfascicular nucleus raphe | 1 | 127 | 18 | False |
| III | Oculomotor nucleus | 3 | 47 | 7 | False |
| IPN | Interpeduncular nucleus | 3 | 561 | 10 | False |
| MA3 | Medial accesory oculomotor nucleus | 1 | 6 | 0 | False |
| MPT | Medial pretectal area | 2 | 22 | 0 | False |
| MRN | Midbrain reticular nucleus | 137 | 23,026 | 2,678 | True |
| MT | Medial terminal nucleus of the accessory optic tract | 2 | 25 | 0 | False |
| NB | Nucleus of the brachium of the inferior colliculus | 4 | 280 | 23 | True |
| NOT | Nucleus of the optic tract | 25 | 835 | 92 | True |
| NPC | Nucleus of the posterior commissure | 12 | 804 | 71 | True |
| OP | Olivary pretectal nucleus | 5 | 146 | 39 | True |
| PAG | Periaqueductal gray | 55 | 6,968 | 733 | True |
| PBG | Parabigeminal nucleus | 3 | 146 | 14 | True |
| PPN | Pedunculopontine nucleus | 19 | 2,977 | 369 | True |
| PPT | Posterior pretectal nucleus | 13 | 411 | 70 | True |
| Pa4 | Paratrochlear nucleus | 1 | 67 | 3 | False |
| RL | Rostral linear nucleus raphe | 1 | 40 | 12 | False |
| RN | Red nucleus | 24 | 3,768 | 429 | True |
| RPF | Retroparafascicular nucleus | 4 | 377 | 42 | True |
| RR | Midbrain reticular nucleus retrorubral area | 7 | 430 | 60 | True |
| SAG | Nucleus sagulum | 4 | 253 | 51 | True |
| SCm | Superior colliculus motor related | 78 | 14,140 | 1,666 | True |
| SCs | Superior colliculus sensory related | 31 | 2,259 | 185 | True |
| SNc | Substantia nigra compact part | 9 | 163 | 36 | True |
| SNr | Substantia nigra reticular part | 21 | 1,369 | 149 | True |
| VTA | Ventral tegmental area | 8 | 310 | 17 | False |
| VTN | Ventral tegmental nucleus | 2 | 130 | 11 | False |

### Hindbrain (HB)

| Region | Atlas name | Recordings | Units | Good units | Flag |
| --- | --- | --- | --- | --- | --- |
| AMB | Nucleus ambiguus | 2 | 73 | 8 | False |
| AP | Area postrema | 1 | 183 | 3 | False |
| CS | Superior central nucleus raphe | 11 | 2,359 | 391 | True |
| CU | Cuneate nucleus | 4 | 500 | 24 | True |
| DCO | Dorsal cochlear nucleus | 16 | 1,791 | 312 | True |
| DMX | Dorsal motor nucleus of the vagus nerve | 3 | 62 | 2 | False |
| DTN | Dorsal tegmental nucleus | 3 | 164 | 21 | False |
| ECU | External cuneate nucleus | 5 | 492 | 21 | True |
| GR | Gracile nucleus | 1 | 32 | 9 | False |
| GRN | Gigantocellular reticular nucleus | 17 | 3,921 | 560 | True |
| I5 | Intertrigeminal nucleus | 4 | 366 | 42 | True |
| ICB | Infracerebellar nucleus | 8 | 249 | 65 | True |
| IO | Inferior olivary complex | 4 | 100 | 2 | False |
| IRN | Intermediate reticular nucleus | 34 | 6,481 | 744 | True |
| ISN | Inferior salivatory nucleus | 1 | 14 | 4 | False |
| LAV | Lateral vestibular nucleus | 12 | 840 | 169 | True |
| LC | Locus ceruleus | 1 | 2 | 0 | False |
| LDT | Laterodorsal tegmental nucleus | 2 | 567 | 51 | True |
| LIN | Linear nucleus of the medulla | 2 | 61 | 11 | False |
| LRN | Lateral reticular nucleus | 5 | 372 | 31 | True |
| MARN | Magnocellular reticular nucleus | 5 | 449 | 83 | True |
| MDRN | Medullary reticular nucleus | 9 | 2,310 | 180 | True |
| MV | Medial vestibular nucleus | 24 | 5,268 | 672 | True |
| NI | Nucleus incertus | 6 | 373 | 24 | False |
| NLL | Nucleus of the lateral lemniscus | 8 | 1,868 | 184 | True |
| NTS | Nucleus of the solitary tract | 21 | 1,419 | 124 | True |
| P5 | Peritrigeminal zone | 6 | 485 | 46 | True |
| PARN | Parvicellular reticular nucleus | 21 | 2,560 | 423 | True |
| PAS | Parasolitary nucleus | 2 | 6 | 1 | False |
| PB | Parabrachial nucleus | 28 | 3,464 | 306 | True |
| PC5 | Parvicellular motor 5 nucleus | 5 | 306 | 35 | True |
| PCG | Pontine central gray | 9 | 1,048 | 82 | True |
| PDTg | Posterodorsal tegmental nucleus | 2 | 194 | 12 | False |
| PG | Pontine gray | 4 | 140 | 9 | False |
| PGRN | Paragigantocellular reticular nucleus | 13 | 1,166 | 120 | True |
| PRNc | Pontine reticular nucleus caudal part | 11 | 1,985 | 280 | True |
| PRNr | Pontine reticular nucleus | 28 | 7,039 | 770 | True |
| PRP | Nucleus prepositus | 9 | 957 | 70 | True |
| PSV | Principal sensory nucleus of the trigeminal | 8 | 1,443 | 115 | True |
| Pa5 | Paratrigeminal nucleus | 2 | 75 | 4 | False |
| RM | Nucleus raphe magnus | 1 | 12 | 0 | False |
| RO | Nucleus raphe obscurus | 1 | 81 | 1 | False |
| SOC | Superior olivary complex | 9 | 1,139 | 35 | True |
| SPIV | Spinal vestibular nucleus | 19 | 2,162 | 327 | True |
| SPVC | Spinal nucleus of the trigeminal caudal part | 5 | 590 | 42 | True |
| SPVI | Spinal nucleus of the trigeminal interpolar part | 16 | 4,127 | 321 | True |
| SPVO | Spinal nucleus of the trigeminal oral part | 8 | 1,539 | 129 | True |
| SUT | Supratrigeminal nucleus | 14 | 1,430 | 103 | True |
| SUV | Superior vestibular nucleus | 13 | 1,502 | 277 | True |
| TRN | Tegmental reticular nucleus | 10 | 1,463 | 193 | True |
| V | Motor nucleus of trigeminal | 10 | 1,678 | 166 | True |
| VCO | Ventral cochlear nucleus | 6 | 850 | 141 | True |
| VII | Facial motor nucleus | 6 | 861 | 63 | True |
| XII | Hypoglossal nucleus | 2 | 347 | 12 | False |
| x | Nucleus x | 4 | 344 | 45 | True |
| y | Nucleus y | 1 | 18 | 6 | False |

### Cerebellum (CB)

| Region | Atlas name | Recordings | Units | Good units | Flag |
| --- | --- | --- | --- | --- | --- |
| ANcr1 | Crus 1 | 12 | 3,321 | 421 | True |
| ANcr2 | Crus 2 | 19 | 4,383 | 519 | True |
| CENT2 | Lobule II | 17 | 4,105 | 613 | True |
| CENT3 | Lobule III | 29 | 4,549 | 663 | True |
| COPY | Copula pyramidis | 17 | 3,287 | 284 | True |
| CUL4 5 | Lobules IV-V | 36 | 9,036 | 1,207 | True |
| DEC | Declive (VI) | 8 | 1,780 | 190 | True |
| DN | Dentate nucleus | 10 | 731 | 197 | True |
| FL | Flocculus | 5 | 469 | 39 | True |
| FN | Fastigial nucleus | 5 | 242 | 46 | False |
| FOTU | Folium-tuber vermis (VII) | 7 | 594 | 100 | True |
| IP | Interposed nucleus | 31 | 2,767 | 619 | True |
| LING | Lingula (I) | 8 | 216 | 45 | True |
| NOD | Nodulus (X) | 10 | 1,282 | 165 | True |
| PFL | Paraflocculus | 8 | 1,409 | 133 | True |
| PRM | Paramedian lobule | 19 | 3,959 | 382 | True |
| PYR | Pyramus (VIII) | 7 | 1,043 | 207 | True |
| SIM | Simple lobule | 23 | 6,301 | 893 | True |
| UVU | Uvula (IX) | 11 | 2,273 | 245 | True |
| VeCB | Vestibulocerebellar nucleus | 6 | 427 | 70 | True |

Source: [brainwidemap/meta/region_info.csv](../brainwidemap/meta/region_info.csv)

SHA256: 03f3db63aec6650a051d768b633b45cde32b854bf714e745bbacf704256c40b3
