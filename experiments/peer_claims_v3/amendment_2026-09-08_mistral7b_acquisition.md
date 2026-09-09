# Amendment: mistral7b acquisition record (2026-09-08, before any checkpoint inference)

`models/mistral7b.json` was frozen with `gguf_sha256: null` and
`status: "not on the study machine as of 2026-09-08"`, because protocol gate 1 permits the
file hash to be "recorded as an amendment at download time for files not yet acquired".
This amendment supplies that record. No design parameter changes; the frozen model spec
file is left byte-unchanged to preserve its hash in `freeze.json`.

## Acquisition

The file was downloaded on a second machine, not the machine that produced the V2 and
opportunity-cost records. `qwen3_think` and `phi35mini` are **not** present here: both were
locally converted from cached Hugging Face weights that are not part of the repository
(`data/models/` is gitignored), so they cannot be reconstructed on this machine. This
amendment therefore covers `mistral7b` only, and any stage run recorded here is a
first-family-of-record run rather than a continuation of the V2 machine's series.

| Field | Value |
|---|---|
| Repository | `bartowski/Mistral-7B-Instruct-v0.3-GGUF` |
| Revision requested | `61fd4167fff3ab01ee1cfe0da183fa27a944db48` (as frozen) |
| File | `Mistral-7B-Instruct-v0.3-Q4_K_M.gguf` |
| Local path | `data/models/peer_claims_v3/Mistral-7B-Instruct-v0.3-Q4_K_M.gguf` |
| Size (bytes) | 4372812000 |
| **SHA-256** | `1270d22c0fbb3d092fb725d4d96c457b7b687a5f5a715abe1e818da303e562b6` |
| Downloaded (UTC) | 2026-09-08 |

The quantization is third-party Q4_K_M and must not be treated as original precision, as
the frozen spec already states. The original `mistralai/Mistral-7B-Instruct-v0.3` weights
were not downloaded and no conversion was performed here.

The September workflow-obligations failure recorded in
`experiments/workflow_obligations/v2/model_availability_amendment.md` (HTTP timeouts, failed
Xet transfer) did not recur: the transfer completed in one pass over plain HTTPS at the
pinned revision.

## Backend

`llama-server` was not present on this machine and was installed from Homebrew
(`llama.cpp 0.4.0`). It reports:

```
version: 0.4.0 (build 10809, commit 5266f24da)
built with AppleClang 21.0.0.21000101 for Darwin arm64
```

`5266f24da` is the same llama.cpp commit already pinned in the repository as the conversion
source (`data/external/llama_conversion_source/llama.cpp-5266f24da`, and the
`quantization` field of `models/qwen3_think.json` and `models/phi35mini.json`). The backend
generating inference here is therefore the commit the frozen records name, not a newer one.
This is a fortunate coincidence of the Homebrew bottle, not something the protocol
guaranteed; if a future bottle moves off this commit, that must be recorded as a further
amendment, because the determinism diagnosis in `protocol.md` is backend-specific.

All flags used by `scripts/serve_v3_cpu.py` were confirmed present in this build:
`--device`, `--no-op-offload`, `--no-kv-offload`, `--fit`, `--jinja`,
`--chat-template-kwargs`, `-np`, `-ub`.

Hardware differs from the V2 machine (Apple Silicon, arm64, CPU-only by the serve script's
`--device none -ngl 0`). Because the determinism gate is run per model path on the machine
that serves it, the gate result recorded alongside this run is the applicable one; the V2
machine's gate records do not transfer.

## What this amendment does not do

It does not alter any factor, cell count, wording, generation parameter, gate threshold or
stopping rule. It does not promote `mistral7b` past its gates: eligibility is still decided
by the backend determinism gate and the 20/20 reason-mode control gate, and a failure of
either is recorded rather than interpreted.
