# Flash serving cookbook

Status: local draft, based on the October 5, 2026 isolated campaign. Production wasn't changed. Commands and values below describe measurement and reproduction boundaries, not a qualified deployment.

## 1. Freeze the reproduction target

The reproduction download contains `reproduction.json`, the reviewed model-file hashes, `measured-exl-settings.json` and `measured-exl-environment.json`. The settings file is an exact subset of the tested config, using its real key names. Supply your own paths, network/authentication and the remaining pinned defaults; it isn't a complete launch config.

| Component | Tested identity |
|---|---|
| TabbyAPI | `53da7919d4e45c63f4acbcbbc00cbe0f60a1ce65` |
| Dual-5090 recipe and overlays | `af2c4b841678a996632bf8e6bbd719aea66b823d` |
| EXL tree, before recipe patches | `5783a9360b749a1d5bde6862dc35e7766e542ca1` (v1.5.2 source) |
| EXL base wheel | `1.5.0+cu128.torch2.9.0`, Python 3.12 Linux x86-64 |
| EXL wheel SHA-256 | `d8f5b483ca882c52d79a73c059b508c666663a68b4c60e420ca489e654e8104a` |
| Model repository | `r0b0tlab/Qwen3.8-Flash-Next-EXL3-2.50bpw` |
| Model revision | `61a1a139ef2411ed6ed5717acfaff288511a1b08` |
| Strata comparison pin | `6f32ec070f23ced9f50e704d854d775da52591ab` |

The model revision is not an EXL source commit. The runtime installed the wheel, prepared the recipe's `rebase-dev-r3` tree from the pinned EXL dev source plus `ported-vs-dev.patch`, replaced the installed EXL tree, rebuilt its extension and installed the recipe overlays. A bare wheel install doesn't reproduce it. The retained setup script and log establish that sequence; this download doesn't include weights or the built runtime.

Read the [pinned dual-5090 recipe](https://github.com/adrienbrault/qwen3.8-flash-next-2x-rtx5090/tree/af2c4b841678a996632bf8e6bbd719aea66b823d), [pinned TabbyAPI](https://github.com/theroyallab/tabbyAPI/tree/53da7919d4e45c63f4acbcbbc00cbe0f60a1ce65) and [pinned model artifact](https://huggingface.co/r0b0tlab/Qwen3.8-Flash-Next-EXL3-2.50bpw/tree/61a1a139ef2411ed6ed5717acfaff288511a1b08). These public identities were checked on October 6, 2026; historical performance belongs to the October 5 campaign. Don't substitute current upstream defaults. Record CUDA, driver, Torch, GPU topology, CPU, RAM and power limit before a new run.

Measured tuned EXL settings, expressed as an inventory rather than an unverified YAML schema:

| Setting | Tested value |
|---|---|
| Model artifact | EXL3 2.50bpw Flash Next |
| KV precision | Quant8 K / Quant8 V |
| GPU cache pool | 819,200 tokens |
| Maximum sequence | 262,144 tokens |
| Maximum batch | 5 |
| MTP draft depth | 4 |
| GPU placement | 28.5 / 31.5 GiB split values |
| Host KV tier | 32,768 MiB |
| Recurrent host tier | 8,192 MiB |

Do not copy inventory names into a server config without checking the pinned schema. Host pools and GPU split values are hardware-dependent. Fully warmed observed free VRAM was about 1,994 / 1,030MiB in the stated short/mixed cells; this isn't a guaranteed worst-case reserve.

## 2. Check the server in isolation

Before each arm, verify the exact preceding engine process and its descendants have stopped. Inspect the GPU process inventory. Refuse the next arm if an old engine remains.

```sh
nvidia-smi --query-gpu=index,memory.free,utilization.gpu,power.draw --format=csv
nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv
```

Use the engine's actual ready endpoint. A model-list response can precede usable inference. Run a bounded smoke request before timing. Keep builds, downloads and correctness tests outside measured cells.

## 3. Fit the actual token budget

Use the server tokenizer and rendered template. Count system text, tool schema, messages and reasoning history. Reserve native end positions and generation tokens before admitting the request.

```text
actual rendered prompt + requested total generation + native reserve <= context limit
```

Measured full-window arithmetic:

- EXL: 253952 + 8192 = 262144.
- Strata serial: 253943 + 8192 + 8 = 262143, one unused position.
- Stock/Bee: 253950 + 8192 + 2 = 262144.

Keep automatic truncation disabled for full-budget qualification. Rejection is a result. Record actual output and finish reason; an early EOS doesn't count as reaching the requested cap.

## 4. Preserve returning history

Replay exact assistant content, reasoning fields and template markers. Don't strip an empty thinking block because the next request has thinking disabled. Compare the actual rendered history across cold and returning requests.

Timing profile: temperature 0. Mixed sampled profile: temperature 1.0, top_p 0.95, top_k 20, min_p 0, repetition penalty 1, presence/frequency penalty 0. Medium thinking was tested separately where supported. The total 8192-token output budget includes reasoning; a separate reasoning budget is another feature to verify.

## 5. Capture a row readers can compare

```json
{
  "context_limit": 262144,
  "actual_prompt_tokens": 253952,
  "requested_output_tokens": 8192,
  "actual_output_tokens": 8192,
  "finish_reason": "length",
  "completed_requests": 1,
  "requested_concurrency": 1,
  "observed_decode_overlap": 1,
  "cache_state": "cold",
  "wall_seconds": 59.94,
  "wall_output_tok_s": 136.68,
  "ttft_seconds": 38.53
}
```

Example values are rounded from a measured tuned EXL C1 cell. Add source/config/model hashes, sampler, reasoning count, cache hits, memory minima, raw request/SSE references and failures to the internal record. Publish only reviewed, privacy-safe fields.

Wall throughput = completed actual output tokens / entire wave duration. Decode-only throughput uses a different interval. Don't put both under an unlabeled "tok/s" column. Queued clients don't establish simultaneous decode capacity.

## 6. Qualify the selected configuration

Test actual tools, tool-result follow-up, schema objects and thinking replay. Then short, 100K, 128K and full-window requests, cold/warm history, code and fictional operations, concurrency beyond five, churn, overload, cancellation and recovery.

Keep PASS, FAIL, PARTIAL, INVALID and NOT RUN separate. Refine concurrency around a measured plateau. A latency threshold may end a service-profile search without proving the maximum possible throughput.

This campaign's tuned EXL failed the overload fairness probe: a 4K request waited 226.34 seconds behind twelve long requests. No admission policy is supplied as a verified fix.

## 7. Recompute the public data locally

Unzip the download, then run:

```sh
python3 verify_data.py full-window.csv
```

This standard-library check requires nine completed C1 rows, verifies each 8,192-token output and recomputes output divided by wall time. It also checks each prompt budget against the profile's native reserve. It verifies the published arithmetic; the private raw archive isn't in the download, so this isn't an independent rerun of the campaign.

For an authorized experiment, collect the row fields in section 5 from actual API usage and client wall timing. Check tools and history before timing, then compare cold, exact returning-prefix and overload rows separately. No queue-policy fix or new GPU run was tested for this package.

## 8. Prepare a reversible canary

A production canary requires separate approval. Capture the existing production image, model hashes, config, consumer history and routing before changing anything. Qualify long/short admission and queue deadlines with the same overload workload. Recheck the actual rig's power, memory margin and consumer behavior.

Rollback plan: stop new experimental admission, drain or cancel its owned requests, restore the captured baseline target and configuration, then run the baseline consumer checks. An experimental rental's frozen EXL configuration isn't automatically the production baseline.

The production rig remains unchanged. Rental destruction and verified evidence preservation were completed separately.
