# Second-model availability amendment

Recorded before any second-model generation. The Mistral Q4 download at pinned revision 61fd4167fff3ab01ee1cfe0da183fa27a944db48 repeatedly timed out over ordinary HTTP; an Xet retry remained stalled. A bounded 1 MB range probe transferred only 554,439 bytes in 30 seconds. This is an availability-driven substitution, not selection on model outcomes.

Use cached microsoft/Phi-3.5-mini-instruct, snapshot 2fe192450127e6a83f7441aef6e3ca586c338b77, as the second family. Convert locally with llama.cpp source commit 5266f24da and quantize Q4_K_M with the installed matching binary. Preserve conversion/source hashes and native chat template. Task cases, controls, intervention texts, gates, decoding and analysis remain the V2 design. No Mistral outcomes exist or are being dropped. Phi is smaller (~3.8B); this is not a model-size-matched or pure training comparison. Qwen main runs were already underway when availability forced the substitution.
