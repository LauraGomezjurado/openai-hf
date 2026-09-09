# Amendment: llama31_8b acquisition record (2026-09-09, before any inference on this model)

`models/llama31_8b.json` was frozen with `revision: null`, `gguf_sha256: null` and
`status: "not acquired"`. Its `acquisition` field instructs: "Record repository revision and
file SHA-256 at download time as an amendment; the original weights are gated, the GGUF
repository is public." This amendment supplies both. No design parameter changes; the frozen
model spec is left byte-unchanged to preserve its hash in `freeze.json`.

This is the second cross-family attempt, after `mistral7b` was excluded at the control gate
(14/20, [record](../../docs/peer_claims_v3_cross_family_gates.md) — the single-model note cited
when this amendment was written was superseded by that combined record later the same day).

## Acquisition

| Field | Value |
|---|---|
| Repository | `bartowski/Meta-Llama-3.1-8B-Instruct-GGUF` |
| **Revision resolved** | `bf5b95e96dac0462e2a09145ec66cae9a3f12067` |
| Repository `lastModified` | 2024-12-01T04:12:27Z |
| Repository `gated` | false |
| File | `Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf` |
| Local path | `data/models/peer_claims_v3/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf` |
| Size (bytes) | 4920739232 |
| **SHA-256** | `7b064f5842bf9532c91456deda288a1b672397a54fa729aa665952863033557c` |
| Downloaded (UTC) | 2026-09-09 |

Because the frozen spec carried no revision, the revision recorded here is the repository
`main` at download time, resolved via the Hugging Face model API *before* the transfer and
then used explicitly in the download URL, so the bytes hashed above are the bytes at that
commit rather than at a floating `main`. Any future re-acquisition must use this commit, not
`main`.

The quantization is third-party Q4_K_M and must not be treated as original precision, as the
frozen spec states. The original `meta-llama/Llama-3.1-8B-Instruct` weights are gated, were
not downloaded, and no conversion was performed here; the GGUF repository is public and
required no authentication.

## Backend and machine

Unchanged from the `mistral7b` run and its
[acquisition amendment](amendment_2026-09-08_mistral7b_acquisition.md): Homebrew
`llama.cpp 0.4.0`, build 10809, commit `5266f24da` — the same commit pinned as the
repository's conversion source — on Apple Silicon arm64, served CPU-only by
`scripts/serve_v3_cpu.py` (`--device none -ngl 0`). This is not the machine that produced the
V2 and opportunity-cost records, so the determinism gate recorded alongside this run is the
applicable one and the V2 machine's gate records do not transfer.

`reasoning_mode` is `scratchpad` and `system_role` is `true`, so this model needs no
rendering amendment: unlike `gemma2_9b`, its chat template accepts a system role, and the
scratchpad instruction is delivered in the system message as the protocol specifies.

## What this amendment does not do

It does not alter any factor, cell count, wording, generation parameter, gate threshold or
stopping rule. It does not promote `llama31_8b` past its gates: eligibility is decided by the
backend determinism gate and the 20/20 reason-mode control gate, and a failure of either is
recorded rather than interpreted, with no prompt adaptation.
