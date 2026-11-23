# AC-AZT: Action-Centric Agentic Zero-Trust Authorization

**Reproducibility Package — Version 1.1**

**Companion paper:** *Trustworthy Agentic AI Defense: Adaptive Zero-Trust for Cloud–Edge–IoT* (UCC 2026 Workshop)*
**Authors:** Abubakar Wakili, Sara Bakkali, and Mohammad Hammoudeh

## Overview

Cybersecurity agents can propose actions that change real systems, including isolating workloads, updating firewall rules, and rotating credentials. A correct threat alert does not automatically mean that the proposed response is authorized, proportionate, or safe to execute.

**Action-Centric Agentic Zero-Trust Authorization (AC-AZT)** is a proposed gateway architecture for checking individual cybersecurity actions before execution. It combines contextual risk assessment with mandatory safety rules, autonomy limits, human-approval decisions, and post-action checks. The objective is to distinguish actions that may proceed from those that require approval or must be denied.

This repository contains the **Python policy simulator and reproducibility records** used to study that design across cloud, edge, and Internet of Things (IoT) scenarios. The experiments evaluate authorization decisions and simulated postconditions; they do not implement a deployed AI agent or production enforcement gateway.

## Research Contribution

The package supports three contributions described in the paper:

1. **Action-level authorization design:** A proposed policy boundary that considers operational impact, required privilege, uncertainty, destructiveness, affected scope, and mandatory rules before execution.

2. **Reproducible policy evaluation:** Paired comparisons with direct execution and static authorization on 240 constructed cases, supported by ablation, threshold, weight, domain, and recovery analyses.

3. **Authorization failure analysis:** Case-level evidence of missed approval requirements and a supplementary experiment showing why authorization cannot safely depend on unverified input attributes.

The study provides an evaluated policy design and an analysis of its failure modes, rather than claiming that the complete architecture has been deployed or that it resists real-world prompt injection.

## Key Experimental Results

The benchmark contains **60 base cybersecurity actions** (30 cloud, 15 edge, and 15 IoT). Each action is evaluated under four conditions: benign operation, simulated instruction injection, scope escalation, and unsafe or stale context.

The resulting 240 constructed cases are evaluated using the same inputs for three authorization methods.

| Evaluation metric | Direct execution | Static authorization | AC-AZT |
|---|---:|---:|---:|
| Oracle-PERMIT Execution Rate (OPER) | 33/33 | 33/33 | **31/33** |
| Completed-and-Committed Rate (CCR) | 29/33 | 29/33 | **28/33** |
| Unauthorized executions (UAR numerator) | 197/207 | 139/207 | **3/207** |
| Constructed attack cases executed (ASR numerator) | 160/170 | 120/170 | **0/170** |
| Three-class oracle agreement | 43/240 | 96/240 | **234/240 (97.5%)** |

### Main Findings

AC-AZT executed only 3 of the 207 actions requiring approval or denial, corresponding to an unauthorized execution rate of **1.45%**. On this benchmark, this represents descriptive reductions of 93.72 percentage points relative to direct execution and 65.70 percentage points relative to static authorization.

All three unauthorized executions were benign requests requiring approval (`B019`, `B038`, and `B054`). No oracle-DENY case was executed (0/175).

AC-AZT executed 31 of 33 oracle-permitted cases. However, only 28 completed and committed. The other three executed actions failed simulated postcondition checks and were marked rolled back.

These results demonstrate how the specified policy controls behave on constructed cases. They are not estimates of real-world attack prevention or deployment performance.

## Trusted-Attribute Validation Probe

A supplementary experiment examined what happens when a policy violation is present but the corresponding validation flag remains permissive.

The unchanged AC-AZT gateway was evaluated using counterfactual inputs derived from the original benign actions.

| Counterfactual condition | With benchmark risk increase | Without risk increase |
|---|---:|---:|
| Scope mismatch with permissive validation flag | **28/60 executed** | 31/60 executed |
| Appended instruction text with valid typed-interface flag | **29/60 executed** | 31/60 executed |

### Interpretation

**Scope validation:** The simulator trusts the supplied `scope_within_authorization` field rather than independently deriving permission from actual requested and approved scopes.

**Instruction-text handling:** Appending instruction text does not itself alter authorization when the typed-interface flag remains valid. The gateway does not interpret the added text.

These findings expose the importance of independent attribute verification. Neither experiment demonstrates that a deployed LLM agent followed attacker-controlled instructions. The probe labels were defined by the authors rather than by independent blinded assessors.

## Evaluation Design

For each proposed action, AC-AZT defines a contextual risk score:

\[
R(a)=w_I I(a)+w_P P(a)+w_U U(a)+w_D D(a)+w_S S(a)
\]

where:

- **I — Operational impact:** Potential consequences of the action.
- **P — Required privilege:** Authority needed for execution.
- **U — Uncertainty:** Reliability of the supporting evidence.
- **D — Destructiveness:** Difficulty of reversing an action.
- **S — Affected scope:** Resources potentially affected.

The weights sum to one. The reported configuration uses equal weights and a permit threshold of 0.45. Mandatory safety checks take precedence over the numerical score.

Here, *risk-adaptive* means context-sensitive, action-level authorization. The simulator does not learn policies or update its weights online.

### What the Simulator Implements

- Mandatory authorization rules.
- Contextual risk scoring.
- Autonomy ceilings A2, A3, and A4.
- Authorization decision records.
- Simplified postcondition checks.
- Boolean-based simulated recovery.

### What Remains Part of the Proposed Architecture

- An operational LLM planning agent.
- Cloud, edge, and IoT execution adapters.
- Cryptographically issued, short-lived capabilities.
- Human-approval workflows.
- Trusted derivation of authorization attributes.
- Stateful recovery under partial failures.

The simulator trusts supplied Boolean fields for scope validity, interface type, evidence freshness, and rollback availability. This assumption is central to interpreting the experimental findings.

## Repository Contents

| File or directory | Description |
|---|---|
| `AC-AZT-Notebook.ipynb` | Original executed notebook and experimental outputs, preserved as the original record |
| `AC-AZT-Notebook-v3.ipynb` | Revised notebook with corrected methodological explanations, oracle-class breakdown, and trusted-attribute probe |
| `results/` | Base scenarios, expanded benchmark, case-level decisions, configuration, metric summaries, and additional analyses |
| `tables/` | Generated experimental tables |
| `figures/` | Experimental figures in PDF, PNG, and SVG formats |
| `scripts/make_paper_fig2.py` | Recreates the paper's Figure 2 using the recorded CSV results |
| `requirements.txt` | Python dependencies |
| `CITATION.cff` | Citation metadata |
| `SHA256SUMS.txt` | File integrity checksums |

The revised notebook preserves the original gateway, scenario-generation, and oracle logic. Its additional analyses do not change the original experimental decisions.

## Reproduce the Experiments

### Requirements

- Python 3.12 (the original experiment used Python 3.12.14).
- JupyterLab.
- Dependencies listed in `requirements.txt`.

No external dataset, cloud account, LLM API, or network emulator is required.

### Reproduction Steps

1. Clone the repository:

   `git clone https://github.com/wakili-research/AC-AZT-Agentic-Zero-Trust.git`

2. Open a terminal in the cloned repository folder.

3. Install the required dependencies:

   `python -m pip install -r requirements.txt`

4. Start JupyterLab:

   `jupyter lab`

5. Open `AC-AZT-Notebook-v3.ipynb` and select **Run All**.

6. Use the experiment configuration and random seed `20260920`.

7. Compare the generated decisions and tables with the committed files in `results/` and `tables/`.

Run the notebook in a separate working copy if you want to preserve the committed experimental outputs unchanged.

To recreate the paper's Figure 2, run:

`python scripts/make_paper_fig2.py results figures/paper_fig2`

### Metric Terminology

The original notebook uses the label `LASR` for the execution rate among oracle-PERMIT cases.

The paper and updated documentation use **Oracle-PERMIT Execution Rate (OPER)** because this measure counts execution rather than successful completion.

The **Completed-and-Committed Rate (CCR)** is reported separately. Historical CSV column names are retained to preserve the original experimental record.

## Metric Definitions

| Metric | Definition | AC-AZT |
|---|---|---:|
| OPER | Executions among 33 oracle-PERMIT cases | 31/33 |
| CCR | Oracle-PERMIT cases executed, verified, and committed | 28/33 |
| UAR | Executions among 207 approval-or-deny cases | 3/207 |
| DENY executions | Executions among 175 oracle-DENY cases | 0/175 |
| Approval-required executions | Executions among 32 approval-required cases | 3/32 |
| ASR | Executions among 170 constructed attack cases | 0/170 |
| Accuracy | Exact agreement with the three-class oracle | 234/240 |
| FER | Oracle-PERMIT cases sent for approval | 2/33 |
| Failed-effect commits | Failed effects committed among ten postcondition-failure cases | 0/10 |

Of the ten postcondition-failure cases, AC-AZT executed three and marked all three rolled back. The remaining seven were stopped before execution.

Rollback success is represented by a Boolean condition and does not establish that an operational compensation mechanism would succeed.

The direct-execution and static-authorization baselines each recorded CCR 29/33, but they also committed four failed effects in the simulated failure cases.

## Oracle and Statistical Interpretation

The reference oracle assigns each case one of three labels:

| Oracle label | Number of cases |
|---|---:|
| PERMIT | 33 |
| APPROVAL_REQUIRED | 32 |
| DENY | 175 |
| **Total** | **240** |

The authors manually assigned benign labels for each base action. Variant labels follow documented safety properties.

The oracle is **method-separated** because reference labels are produced without running the evaluated authorization methods. However, it is not an independently blinded oracle: no external annotators were used, and the constructed variant properties overlap with AC-AZT's mandatory rules.

The benchmark is purposively constructed, and the four variants of each base action share attributes.

For these reasons, the reported results are descriptive benchmark counts and paired comparisons rather than population-level estimates.

The original notebook retains exploratory Wilson intervals and exact McNemar tests for the experimental record. These are not used to support population-level conclusions in the revised manuscript.

In particular, zero executions among 170 constructed attack cases does not establish resistance against real agent-level prompt injection.

## Ablation, Threshold, and Failure Analysis

The ablation experiments examine how removing individual controls changes the simulator's decisions.

Removing mandatory rules increased unauthorized execution from 3/207 to 87/207. Removing scope bounding increased it to 31/207, while removing contextual risk or freshness checks increased it to 8/207.

Contextual risk scoring therefore prevented five additional unauthorized executions in this suite, but also withheld two oracle-PERMIT executions. It did not change the constructed attack result, which was governed by mandatory rules.

The configured threshold was 0.45. A threshold of 0.35 produced a more favorable observed execution-rate trade-off on the evaluated cases. The available experimental record does not establish independent preregistration or rule out developmental exploration when setting the default.

The experiment also identifies three approval-required requests that were permitted because the corresponding approval conditions were not encoded in the gateway's rules.

These observations inform future development of stronger attribute validation, approval enforcement, and authorization policies.

## Timing and Performance

The experiment measures local Python policy-processing time using `perf_counter_ns` over 48,000 evaluations per method.

Two timing records are preserved:

| Run | Environment | Median / p95 / p99 (µs) |
|---|---|---|
| Original experiment | Python 3.12.14, pandas 2.2.3, NumPy 2.3.5, SciPy 1.17.0, Matplotlib 3.10.8; Intel Core i5-1135G7, 32 GB RAM, Windows 11,  | 1.476 / 1.783 / 2.157 |


The original results are retained in `AC-AZT-Notebook.ipynb`. The later run is recorded in `results/metric_summary.csv` and `results/authorization_latency.csv`.

Authorization decisions and benchmark counts remain unchanged between the two runs.

These measurements exclude network communication, identity services, approval delays, external tool execution, and other deployment costs. They should not be interpreted as end-to-end cloud, edge, or IoT latency.

## Known Limitations

The experimental package supports the following observations:

- Approval requirements not represented by explicit rules may be missed.
- The gateway trusts supplied authorization attributes rather than verifying them independently.
- Simulated instruction-injection cases activate predefined flags rather than testing a real agent interpreting attacker-controlled text.
- The recovery model uses Boolean availability flags rather than actual compensation workflows.
- Invariant checks reuse attributes supplied to the gateway and therefore measure internal policy consistency.
- The benchmark has no independently labeled held-out evaluation set.
- The simulator does not implement a production execution gateway or a functioning human-approval service.

These limitations define the current evaluation boundary and identify areas requiring further implementation and testing.

## File Integrity

`SHA256SUMS.txt` contains hashes for the distributed files, excluding the checksum manifest itself.

From the repository root, the hashes can be checked using:

`sha256sum -c SHA256SUMS.txt`

This command requires `sha256sum` or a compatible tool.

The checksum manifest must be regenerated whenever any tracked file, including this README, changes.

## Citation and Reuse

If this repository supports your research, please cite the accompanying paper and the repository using the metadata in `CITATION.cff`.

GitHub provides a **Cite this repository** option based on this metadata.

No archival DOI is claimed.

**License:** No explicit open-source license has yet been granted. Public availability alone does not authorize unrestricted reuse, redistribution, or modification. License terms should be agreed by the authors before adding a `LICENSE` file.

## Scope of Claims

AC-AZT v3.4 is a reproducible, constructed, author-labeled policy-simulation benchmark. It provides case-level evidence of how the implemented authorization rules behave, how individual controls affect decisions, and where approval and trusted-attribute weaknesses arise.

The present study does not establish the security of a deployed AI agent, resistance to adaptive prompt injection, cryptographic capability enforcement, operational approval workflows, or recovery from irreversible or partially failed actions.
