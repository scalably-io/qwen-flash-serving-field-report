# Qwen Flash serving field report

Privacy-safe companion to Scalably's October 5, 2026 isolated dual-RTX-5090 campaign. [Canonical field report](https://scalably.io/blog/qwen-flash-next-dual-rtx-5090-serving-benchmark).

Tuned EXL led the completed warm 256K C1 comparison at 371.98 wall tok/s. Strata serial led cold at 147.98. The short-code C5 result was 1,071.12 aggregate wall tok/s. A short overload probe waited 226.34 seconds. No production-qualified winner, equal-quality comparison or complete per-engine matrix.

## Start here

- [Field report](FIELD-REPORT.md): the measured cells and what they mean.
- [Cookbook](COOKBOOK.md): pins, setup boundary, history replay, isolation, row contract and reversible canary gates.
- [Results](full-window.csv): nine completed 8,192-output C1 aggregate rows.
- [Source identities](sources.json): recipe, runtime, model and all six challenger repository commits.
- [Startup inventory](startup/INDEX.json): all retained process-launch recipes, including unsupported and failed alternatives. Config files can be prepared before admission; inclusion is not proof that a configuration ever served successfully.
- [Coverage](COVERAGE.md): PASS, FAIL, PARTIAL, INVALID and NOT RUN remain separate.

## Recompute without a GPU

```sh
python3 verify_data.py full-window.csv
```

Python's standard library is sufficient. This checks the published arithmetic and token budgets. It does not rerun inference or authenticate private raw evidence.

## Reproduction boundary

The startup JSON preserves recorded argument arrays, working directories and relevant environment variables. `<BENCH_ROOT>` and `<CUDA_ROOT>` replace private machine paths. Substitute a new isolated experiment root and the appropriate installed toolchain. Treat argv as an array, never shell-evaluate it. The files don't install models or validate your paths.

EXL's config/environment subsets use the tested keys. TabbyAPI loaded `main.py` from its checkout; the config was supplied through that checkout's config file. Reproduction also needs the pinned recipe's tree preparation, extension rebuild and overlays. A model revision isn't an EXL code revision, and a bare EXL wheel doesn't reproduce the run. Challenger launch recipes require the exact compatible artifacts, hashes, builds and tokenizer/templates; this package doesn't supply weights, binary packs or a rebuilt runtime. NInfer's custom binary pack and IK's converted GGUF are distinct prerequisites, not interchangeable upstream downloads.

No newly adapted launcher, queue fix or inference run was validated for this publication package. Follow the cookbook's admission and consumer checks before timing or promotion. Every API limitation describes the tested historical build.

## What's public

Reviewed aggregate results, chart SVG/PNG, model-file hashes, source identities, settings and sanitized launch recipes. No raw request/output traces, operational receipts, account identifiers, credentials, private implementations or weight files. Upstream code is linked at exact commits and isn't vendored.
