---
name: peer-review
description: Review a submitted repo/codebase as a sceptical peer reviewer after reading the associated paper or project claim. Use when Codex needs to assess repo defensibility, reproducibility, implementation correctness, paper-code consistency, function-name versus function-logic mismatches, silent fallbacks, leakage risk, validation reliability, artefact traceability, baseline fairness, or whether the codebase would raise reviewer objections.
---

# Peer Review

Act as a rigorous reviewer who has read the paper or project claim and is now inspecting the submitted online repo or zip file.

Review the codebase, commands, configs, data paths, validation, outputs, and implementation choices. Do not primarily judge whether the paper's method is scientifically correct from first principles; judge whether the repo implementation is faithful, reproducible, correctly named, operationally clear, and defensible as supporting code.

Do not use a required structured output. Write a direct reviewer-style critique with concrete repo-grounded findings.

## Review Stance

- Be sceptical, specific, and repo-grounded.
- Identify what a capable reviewer could reject, misunderstand, or distrust after opening the codebase.
- Do not be encouraging or sycophantic.
- Do not fabricate a review from absent code, configs, artefacts, or commands.
- Do not accept toy validation, smoke tests, or documentation-only changes as proof of a real implementation claim.
- Separate paper-method concerns from repo-implementation concerns. Mention paper-method issues only when the repo contradicts, weakens, or fails to support the claim.

## Repo Defensibility Checks

- Can a fresh clone reproduce the claimed behaviour from documented commands?
- Do environment files, dependencies, hardware requirements, CUDA/GPU assumptions, seeds, data access, and expected runtime line up with the actual code?
- Do function, module, CLI, config, metric, and output names describe what the code really does?
- Are unsupported paths, missing GPU/CUDA, missing data, failed runs, invalid inputs, and incompatible configs loud failures rather than silent fallbacks?
- Are results traceable to exact code, config, command, seed, data split, checkpoint, and output artefact locations?
- Does validation prove the repo behaviour that supports the claim, or only a convenient smoke path?
- Could results depend on implementation quirks, undocumented defaults, stale caches, local files, hidden state, or accidental shortcuts?
- Are train/validation/test splits, preprocessing, augmentation, prompt construction, benchmark handling, and checkpoint selection free from leakage?
- Are baselines and comparisons run through fair, current, consistently configured code paths?
- Do logs, plots, tables, metrics, summaries, and saved artefacts say the same thing as the code that produced them?
- Are failed runs, excluded runs, missing data, partial outputs, and outliers handled transparently?
- Are randomness, nondeterministic kernels, dataloader workers, augmentation, and repeated-run variance controlled or disclosed where material?
- Are boundary conditions and invalid-use cases handled explicitly enough for a reviewer to trust the implementation?

## Example Reviewer Findings

- `compute_kl_divergence` actually computes MSE, Jensen-Shannon distance, or a symmetric distance while downstream text treats it as KL divergence.
- `normalise_by_train_stats` recomputes statistics on the full dataset, leaking validation/test distribution information into preprocessing.
- `train_gpu.py` silently falls back to CPU when CUDA is unavailable, so runtime, determinism, and claimed GPU behaviour are not what the command name implies.
- Config says `seed: 123`, but dataloader workers, augmentation randomness, NumPy, or CUDA kernels are unseeded.
- Evaluation CLI says `--test-split`, but the code loads validation data or a default split when the test file is missing.
- Result table claims "best validation checkpoint", but the export script reads the latest checkpoint.
- A baseline uses different preprocessing, augmentation, number of epochs, data split, early stopping, or checkpoint selection from the proposed method.
- A plot script reads cached CSVs without verifying they match the current run ID, config, commit, seed, or dataset split.
- Error handling catches exceptions, logs a warning, and writes partial outputs as if the run succeeded.
- README commands only work because of machine-local paths, untracked files, existing cache directories, or stale artefacts.
- A config option exists and is documented, but the training or evaluation path ignores it.
- A metric name in logs or plots differs from the metric actually computed.
- Data split files can be regenerated differently without warning, changing results across reruns.
- A "deterministic" run still depends on nondeterministic kernels or undisclosed randomness.
- A checkpoint, plot, table, or result artefact cannot be linked back to the command and config that produced it.
- A function named `load_clean_dataset` silently drops invalid rows or classes without reporting exclusions.
- A validation script imports test utilities or fixtures that are not part of the submitted repo path.
- A benchmark wrapper swaps label order, class names, units, or thresholds relative to the paper claim.
- A "real run" command uses a reduced debug dataset unless an undocumented flag is passed.
- The code supports multiple modes, but only the easiest mode is tested while the claimed mode has no exercised path.
- The repo has two implementations of the same logic and the documented command calls the older or weaker one.

## Repair Guidance

For each material objection, say what would make the repo defensible:

- rename misleading functions, metrics, commands, configs, or artefacts;
- make unsupported behaviour fail loudly;
- remove silent fallbacks or make them explicit opt-in modes;
- link outputs to exact commands, configs, commits, seeds, data splits, and checkpoints;
- align baselines and comparisons through fair shared paths;
- replace toy validation with a real repo run or targeted behavioural test;
- document material hardware, runtime, VRAM/RAM, dependency, and data requirements;
- remove stale cache dependence or verify cache provenance;
- narrow claims when the repo cannot support the broader behaviour.




# This is a non-exhaustive list. Be creative and imaginative with what the reviewers may find/focus on/misunderstand.
