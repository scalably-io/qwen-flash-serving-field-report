# Startup playbook

These are recorded launch recipes from the October 5, 2026 campaign. Use the pinned sources in `sources.json`, compatible artifacts and an isolated experiment root. Never apply the settings to an existing production server by default.

## Selected profiles

| Profile | Recipe under `startup/` | Prerequisite and observed boundary |
|---|---|---|
| Frozen EXL | `frozen-final-repeat-process-config.json` | Pinned patched Tabby/EXL tree; final frozen repeat, distinct from tuned settings |
| Tuned EXL | `tuned-exl-b5-p819-process-config.json` | Pinned patched tree; measured settings and environment subsets supplied; fairness FAIL |
| Strata serial | `strata-mmap-serial-process-config.json` | Pinned Strata plus `strata-mmap-serial-settings.json`; native batch profiles remain failed alternatives |
| NInfer | `ninfer-small-fp8-d3-process-config.json` | Custom 3.5-bit NInfer binary pack; single GPU; named-tool/schema unsupported |
| FreeToken | `free-single-ready-process-config.json` | NVFP4 offload artifact; single GPU; actual-ready health gate, schema unsupported |
| Stock llama.cpp | `llama-slots2-clean-process-config.json` | Compatible GSQ IQ3_XXS GGUF; clean two-slot profile |
| BeeLlama | `bee-slots2-clean-process-config.json` | Compatible GSQ IQ3_XXS GGUF; clean two-slot profile |
| IK | `ik-lossless-slots1-process-config.json` | Expanded lossless-storage GGUF, not the original unsupported artifact; full-window completion incomplete |

The index includes other recorded variants. A process-config file records an intended startup, not proof of admission. Consult `COVERAGE.md` and the report before comparing any result.

## Render, then inspect

```sh
python3 render_startup.py startup/tuned-exl-b5-p819-process-config.json \
  --bench-root /path/to/new/isolated-lab
```

This new standard-library helper prints the recorded cwd, environment and argv with substituted paths. It doesn't execute anything. Only its path substitution and command rendering were checked locally; no new engine or GPU run was performed. If you use the output, supply the exact installed build and config first. The same root layout is expected; a portable installer is not supplied.

For TabbyAPI, place the selected config in its checkout's config file before starting `main.py`. The measured settings files are subsets; they don't replace its complete defaults or specify model paths, network authentication and TLS. The frozen rollback profile is separate and is not the production baseline.

For Strata, substitute paths in its recorded settings file and use the serial recipe's config argument. Keep the tested source pin separate from K8V4 pull-request builds. For NInfer and the GGUF paths, build and artifact conversion are prerequisites; launch arguments alone can't create the required model pack.

## Admit an arm before timing it

1. Confirm the previous owned process and descendants are gone; inspect GPU compute processes.
2. Wait for actual inference readiness and run a bounded smoke request. FreeToken's model-list HTTP 200 wasn't sufficient.
3. Validate actual tool arguments, tool-result follow-up, schema objects and history replay.
4. Use actual rendered prompt counts and each engine's reserve. Keep sampler/output caps fixed for the named comparison.
5. Record complete, partial, failed and invalid rows separately. Capture wall time, actual tokens and observed decode overlap.
6. Run the same long-request overload plus arriving-short-request probe before considering promotion.

The tested tuned EXL profile failed step 6. This playbook supplies no qualified queue fix or production cutover.
