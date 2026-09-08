"""Write a tiny random-weight llama-architecture GGUF for backend self-tests.

The file carries no trained knowledge. Its only purpose is to exercise the
inference backend with the same request shapes the experiments use, so that
numerical repeatability (KV-cache reuse, batch splitting, thread count) can be
checked mechanically without any released checkpoint. Decisions produced with
it are meaningless and must never be counted as behavioral observations.

Dimensions are multiples of 256 so the same file can be quantized to Q4_K_M with
llama-quantize, matching the quantization type of the study checkpoints.
"""
import argparse
import pathlib

import numpy as np
import gguf


def build(path, seed=0, n_embd=256, n_ff=512, n_layer=2, n_head=4, n_ctx=4096):
    rng = np.random.default_rng(seed)
    # Byte-fallback vocabulary: 3 specials, 256 byte tokens, and a few whole words that appear in the prompts.
    words = ['▁the', '▁own', '▁peer', '▁action', '▁status', '▁check', '▁only', '▁work', '▁credit', '{', '}', '"', ':', ',', '▁']
    tokens = ['<unk>', '<s>', '</s>'] + [f'<0x{i:02X}>' for i in range(256)] + words
    types = [gguf.TokenType.UNKNOWN, gguf.TokenType.CONTROL, gguf.TokenType.CONTROL] + [gguf.TokenType.BYTE] * 256 + [gguf.TokenType.NORMAL] * len(words)
    # Pad to a multiple of 256 so output projections quantize cleanly.
    while len(tokens) % 256:
        tokens.append(f'<pad{len(tokens)}>')
        types.append(gguf.TokenType.UNUSED)
    n_vocab = len(tokens)
    w = gguf.GGUFWriter(str(path), 'llama')
    w.add_name('tiny-random-llama-selftest')
    w.add_context_length(n_ctx)
    w.add_embedding_length(n_embd)
    w.add_block_count(n_layer)
    w.add_feed_forward_length(n_ff)
    w.add_head_count(n_head)
    w.add_head_count_kv(n_head)
    w.add_layer_norm_rms_eps(1e-5)
    w.add_rope_freq_base(10000.0)
    w.add_vocab_size(n_vocab)
    w.add_file_type(gguf.LlamaFileType.MOSTLY_F16)
    w.add_tokenizer_model('llama')
    w.add_tokenizer_pre('default')
    w.add_token_list(tokens)
    w.add_token_scores([0.0] * n_vocab)
    w.add_token_types(types)
    w.add_bos_token_id(1)
    w.add_eos_token_id(2)
    w.add_unk_token_id(0)
    w.add_add_bos_token(True)
    w.add_chat_template("{% for m in messages %}<s>{{ m['role'] }}: {{ m['content'] }}</s>\n{% endfor %}assistant: ")

    def t(name, shape, scale):
        # 1-D norm weights stay F32, as the reference converter keeps them; matrices are F16.
        dtype = np.float32 if len(shape) == 1 else np.float16
        w.add_tensor(name, (rng.standard_normal(shape) * scale).astype(dtype))

    t('token_embd.weight', (n_vocab, n_embd), 0.02)
    t('output_norm.weight', (n_embd,), 1.0)
    t('output.weight', (n_vocab, n_embd), 0.02)
    for i in range(n_layer):
        t(f'blk.{i}.attn_norm.weight', (n_embd,), 1.0)
        t(f'blk.{i}.attn_q.weight', (n_embd, n_embd), 0.02)
        t(f'blk.{i}.attn_k.weight', (n_embd, n_embd), 0.02)
        t(f'blk.{i}.attn_v.weight', (n_embd, n_embd), 0.02)
        t(f'blk.{i}.attn_output.weight', (n_embd, n_embd), 0.02)
        t(f'blk.{i}.ffn_norm.weight', (n_embd,), 1.0)
        t(f'blk.{i}.ffn_gate.weight', (n_ff, n_embd), 0.02)
        t(f'blk.{i}.ffn_up.weight', (n_ff, n_embd), 0.02)
        t(f'blk.{i}.ffn_down.weight', (n_embd, n_ff), 0.02)
    w.write_header_to_file()
    w.write_kv_data_to_file()
    w.write_tensors_to_file()
    w.close()
    return n_vocab


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--seed', type=int, default=0)
    a = ap.parse_args()
    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    print('vocab', build(out, a.seed), 'bytes', out.stat().st_size)
