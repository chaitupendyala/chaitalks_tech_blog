---
title: "How Transformer Architecture Works: A Friendly, Visual Guide"
date: 2026-05-13
categories:
  - "ai"
  - "machine-learning"
tags:
  - "transformers"
  - "attention"
  - "self-attention"
  - "deep-learning"
  - "neural-networks"
  - "nlp"
  - "llm"
  - "gpt"
  - "bert"
  - "pytorch"
  - "attention-is-all-you-need"
  - "positional-encoding"
  - "multi-head-attention"
  - "encoder-decoder"
  - "ai-fundamentals"
---

Every modern Large Language Model — GPT, Claude, Gemini, Llama, you name it — is built on the same core idea introduced in a single 2017 paper called [*Attention Is All You Need*](https://arxiv.org/abs/1706.03762). That idea is the **Transformer**.

In this post I want to walk through how the Transformer actually works, in a way that is hopefully easy to follow even if you're not deep into machine learning. I'll use diagrams, small code snippets, and concrete examples wherever they help.

* * *

## Why Transformers Matter

Before Transformers, the best language models used **Recurrent Neural Networks** (RNNs) or **LSTMs**. They processed text one word at a time, left to right, remembering a little bit as they went. This worked, but it had two big problems:

1. **They were slow.** You couldn't parallelize them — word 100 had to wait for word 99.
2. **They forgot things.** Long-range relationships ("the *cat*, which had been chased through six paragraphs, finally *slept*") were hard to capture.

The Transformer threw away recurrence entirely. Instead, it lets every word look at every other word *simultaneously* using a mechanism called **self-attention**. This unlocked massive parallelism and dramatically better handling of long context — which is essentially why the LLM era happened.

* * *

## The Big Picture

The original Transformer is an **encoder–decoder** model designed for machine translation. The encoder reads the input sentence, the decoder writes the translated sentence.

Here's the high-level shape:

```
              INPUT (e.g. "I love chai")
                       |
                       v
        +--------------------------------+
        |          ENCODER STACK         |
        |  (N identical encoder layers)  |
        +--------------------------------+
                       |
                       | rich context vectors
                       v
        +--------------------------------+
        |          DECODER STACK         |
        |  (N identical decoder layers)  |
        +--------------------------------+
                       |
                       v
              OUTPUT (e.g. "Me encanta el chai")
```

Modern LLMs like GPT use only the **decoder** half. BERT-style models use only the **encoder** half. The architecture below is the same building block in all of them.

Each encoder layer contains two sub-layers:

```
                  Input embeddings
                         |
                         v
            +------------------------+
            |  Multi-Head Self-      |
            |       Attention        |
            +------------------------+
                         |
                  + residual & norm
                         |
                         v
            +------------------------+
            |   Feed-Forward Network |
            +------------------------+
                         |
                  + residual & norm
                         |
                         v
                  To next layer
```

Let's unpack each piece.

* * *

## Step 1: Turning Words into Numbers (Embeddings)

Neural networks operate on numbers, not text. So the first thing a Transformer does is convert each token (roughly: a word or subword) into a vector — a list of numbers that represents its meaning.

```
"chai"   ->  [ 0.12, -0.43, 0.88, ..., 0.05 ]   (e.g. 512 numbers)
"tea"    ->  [ 0.10, -0.41, 0.85, ..., 0.07 ]
"car"    ->  [-0.55,  0.22, 0.01, ..., 0.91 ]
```

The cool part: tokens with similar meaning tend to end up with similar vectors. These embeddings are learned during training.

In PyTorch this is just a lookup table:

```python
import torch
import torch.nn as nn

vocab_size = 30000     # how many distinct tokens we know
d_model    = 512       # size of each embedding vector

embedding = nn.Embedding(vocab_size, d_model)

# A batch of one sentence with 4 token IDs
tokens = torch.tensor([[42, 7, 1500, 99]])
x = embedding(tokens)       # shape: (1, 4, 512)
```

* * *

## Step 2: Telling the Model About Order (Positional Encoding)

Here's the catch: self-attention treats the input like a *set*, not a *sequence*. To the model, "the dog bit the man" and "the man bit the dog" look identical unless we tell it about position.

The fix is **positional encoding** — we add a small, position-dependent vector to each token embedding. The original paper used a clever pattern of sines and cosines:

```
PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

Visually, the encoding looks like a series of waves at different frequencies. Each position gets a unique fingerprint:

```
position 0:  [ sin(0), cos(0), sin(0),  cos(0),  ... ]
position 1:  [ sin(.), cos(.), sin(..), cos(..), ... ]
position 2:  [ sin(.), cos(.), sin(..), cos(..), ... ]
              ^---low freq---^^----higher freq----^
```

In code:

```python
import math
import torch

def positional_encoding(seq_len, d_model):
    pe = torch.zeros(seq_len, d_model)
    position = torch.arange(0, seq_len).unsqueeze(1).float()
    div_term = torch.exp(
        torch.arange(0, d_model, 2).float()
        * -(math.log(10000.0) / d_model)
    )
    pe[:, 0::2] = torch.sin(position * div_term)
    pe[:, 1::2] = torch.cos(position * div_term)
    return pe

x = x + positional_encoding(x.size(1), d_model)
```

Modern models often use other variants (learned positions, RoPE, ALiBi), but the goal is always the same: inject position information.

* * *

## Step 3: Self-Attention — The Heart of the Transformer

This is the idea that makes Transformers work. The intuition:

> For each word, look at *every other word* in the sentence and decide which ones are relevant to understanding it right now. Then mix in information from the relevant ones.

Take the sentence:

> *"The animal didn't cross the street because it was too tired."*

What does "it" refer to? A human reads "it" and instantly looks back at "the animal." Self-attention learns to do exactly this:

```
   The   animal   didn't   cross   the   street   because   it   was   too   tired
                                                            |
                                                            v
   attention weights when processing "it":
   The     animal   didn't   cross   the    street   because   it    was    too   tired
   0.02    0.71     0.01     0.03    0.02   0.08     0.02      0.05  0.02   0.01  0.03
            ^^^^                                                                    
       big weight on "animal"
```

### How it works: Queries, Keys, and Values

For each token, we compute three vectors by multiplying the embedding with three learned weight matrices:

- **Query (Q):** "What am I looking for?"
- **Key (K):** "What do I contain?"
- **Value (V):** "What information will I share if you pay attention to me?"

A nice analogy: imagine searching a library.

- Your **query** is the topic you want.
- Each book has a **key** (its title/spine).
- If a key matches your query, you read the book's **value** (its actual contents).

The attention formula is:

```
Attention(Q, K, V) = softmax( Q · Kᵀ / sqrt(d_k) ) · V
```

In plain English:

1. **Compare** every query with every key (`Q · Kᵀ`) → you get a matrix of similarity scores.
2. **Scale** by `sqrt(d_k)` so the numbers don't blow up.
3. **Softmax** turns scores into a probability distribution (the "attention weights").
4. **Multiply** the weights by the values to get the weighted mix.

Here's a minimal PyTorch implementation:

```python
import torch
import torch.nn.functional as F

def scaled_dot_product_attention(Q, K, V, mask=None):
    d_k = Q.size(-1)
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)

    if mask is not None:
        scores = scores.masked_fill(mask == 0, float("-inf"))

    weights = F.softmax(scores, dim=-1)   # attention probabilities
    return torch.matmul(weights, V), weights
```

A picture of the attention scores matrix is the classic Transformer visualization:

```
                Keys ->
              The animal didn't cross the street because it  was too tired
           +---------------------------------------------------------------
   Queries | .  .   .    .     .   .     .       .   .   .   .
      The  | █  .   .    .     ▓   .     .       .   .   .   .
   animal  | .  █   .    .     .   .     .       ▒   .   .   .
   didn't  | .  .   █    .     .   .     .       .   ▒   .   .
    cross  | .  .   .    █     .   ▓     .       .   .   .   .
      the  | ▓  .   .    .     █   .     .       .   .   .   .
   street  | .  .   .    ▓     .   █     .       .   .   .   .
  because  | .  .   .    .     .   .     █       .   .   .   .
       it  | .  █▓  .    .     .   .     .       █   .   .   .
      was  | .  .   ▒    .     .   .     .       .   █   .   ▓
      too  | .  .   .    .     .   .     .       .   .   █   ▓
    tired  | .  ▒   .    .     .   .     .       ▓   ▓   ▓   █
```

Each row tells you what that word was "looking at." Notice how "it" attends strongly to "animal."

* * *

## Step 4: Multi-Head Attention

One round of attention learns one *kind* of relationship. But language has many kinds — grammatical, semantic, coreference, and so on. So we run attention **in parallel** with several different Q/K/V projections, then concatenate the results. Each parallel run is called a **head**.

```
              Input
                |
   +------+------+------+------+
   |      |      |      |      |
   v      v      v      v      v
 Head 1  Head 2 Head 3 ...   Head h     <- each looks at a different "view"
   |      |      |      |      |
   +------+------+------+------+
                |
                v
            Concat
                |
                v
          Linear layer
                |
                v
            Output
```

Different heads end up specializing in different patterns — one might track subject-verb agreement, another might track which pronouns refer to which nouns. (This wasn't designed in; it just emerges.)

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        assert d_model % num_heads == 0
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)

    def forward(self, x, mask=None):
        B, T, _ = x.shape

        # Project and reshape into (B, num_heads, T, d_k)
        Q = self.W_q(x).view(B, T, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(x).view(B, T, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(x).view(B, T, self.num_heads, self.d_k).transpose(1, 2)

        out, _ = scaled_dot_product_attention(Q, K, V, mask)

        # Concatenate heads back together
        out = out.transpose(1, 2).contiguous().view(B, T, self.d_model)
        return self.W_o(out)
```

* * *

## Step 5: Feed-Forward Network

After mixing information across tokens with attention, each token is passed independently through a small fully-connected network. It's basically two linear layers with a non-linearity in between:

```
        token vector (d_model)
              |
              v
        Linear: d_model -> d_ff       (e.g. 512 -> 2048)
              |
              v
            GELU / ReLU
              |
              v
        Linear: d_ff -> d_model       (e.g. 2048 -> 512)
              |
              v
        new token vector
```

```python
class FeedForward(nn.Module):
    def __init__(self, d_model, d_ff):
        super().__init__()
        self.fc1 = nn.Linear(d_model, d_ff)
        self.fc2 = nn.Linear(d_ff, d_model)

    def forward(self, x):
        return self.fc2(F.gelu(self.fc1(x)))
```

This part gives the model extra capacity to *process* the information attention just gathered. A common intuition: **attention moves information between tokens, the feed-forward network computes on it.**

* * *

## Step 6: Residual Connections and Layer Normalization

Around each sub-layer, Transformers add two boring-looking but absolutely critical pieces:

- **Residual connection:** add the input back to the output (`x + Sublayer(x)`).
- **Layer normalization:** normalize each token's vector to have stable mean/variance.

Together they make deep stacks trainable:

```
              x
              |
        +-----+-----+
        |           |
        |           v
        |     Sub-layer (Attention or FFN)
        |           |
        +-----+-----+
              v
            Add  (residual)
              |
              v
           LayerNorm
              |
              v
           output
```

Without residual connections, training a 12+ layer Transformer would be a nightmare of vanishing gradients. With them, you can stack 100+ layers (see GPT-3 and friends).

* * *

## Step 7: The Decoder and "Masked" Attention

In the encoder, every token can attend to every other token freely. In the decoder (the part that *generates* text), there's a twist: when predicting word `t`, you must not peek at words `t+1`, `t+2`, … because those don't exist yet at inference time.

The fix is a **causal mask** — we zero out (well, set to `-inf` before the softmax) all positions to the right:

```
          Keys ->
        The  cat  sat  on   the  mat
        +---------------------------
   The  |  ok   .   .   .   .   .
   cat  |  ok   ok  .   .   .   .
   sat  |  ok   ok  ok  .   .   .
    on  |  ok   ok  ok  ok  .   .
   the  |  ok   ok  ok  ok  ok  .
   mat  |  ok   ok  ok  ok  ok  ok
```

This is exactly the mask GPT-style models use. They're decoder-only Transformers trained to predict the next token, which is why they always generate left-to-right.

The decoder also has a second attention sub-layer called **cross-attention**, where queries come from the decoder but keys and values come from the encoder. That's how a translation model "looks at" the source sentence while writing each output word.

* * *

## Step 8: From Vectors Back to Words

After the final layer, each output position is a vector of size `d_model`. To turn it into a probability distribution over the vocabulary, we apply one more linear layer plus a softmax:

```
final vector  ->  Linear (d_model -> vocab_size)  ->  Softmax  ->  probabilities
                                                                    |
                                                                    v
                                                            pick the next token
```

During training, we compare these probabilities to the true next token using cross-entropy loss. During generation, we sample (or greedily pick) the next token, append it, and feed it back in.

* * *

## Putting It All Together

A single Transformer block (the type used in GPT-style models) looks like this end to end:

```python
class TransformerBlock(nn.Module):
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super().__init__()
        self.attn = MultiHeadAttention(d_model, num_heads)
        self.ff   = FeedForward(d_model, d_ff)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.drop  = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        # Sub-layer 1: self-attention + residual + norm
        x = self.norm1(x + self.drop(self.attn(x, mask)))
        # Sub-layer 2: feed-forward + residual + norm
        x = self.norm2(x + self.drop(self.ff(x)))
        return x
```

And a tiny full model:

```python
class MiniGPT(nn.Module):
    def __init__(self, vocab_size, d_model=128, num_heads=4,
                 d_ff=512, num_layers=4, max_len=256):
        super().__init__()
        self.tok_emb = nn.Embedding(vocab_size, d_model)
        self.pos_emb = nn.Parameter(torch.zeros(1, max_len, d_model))
        self.blocks  = nn.ModuleList([
            TransformerBlock(d_model, num_heads, d_ff)
            for _ in range(num_layers)
        ])
        self.norm = nn.LayerNorm(d_model)
        self.head = nn.Linear(d_model, vocab_size, bias=False)

    def forward(self, idx):
        B, T = idx.shape
        x = self.tok_emb(idx) + self.pos_emb[:, :T]

        # Causal mask: (T, T) lower-triangular
        mask = torch.tril(torch.ones(T, T, device=idx.device)).bool()

        for block in self.blocks:
            x = block(x, mask)

        x = self.norm(x)
        return self.head(x)   # (B, T, vocab_size)
```

That's it. Fewer than 50 lines of code captures the essence of the architecture behind ChatGPT, Claude, Gemini, and Llama. Real models are vastly bigger (hundreds of billions of parameters, dozens of layers, thousands of dimensions) and use many engineering tricks (mixed precision, FlashAttention, KV caches, RoPE, MoE, etc.), but the core is exactly what you just read.

* * *

## A Mental Model You Can Keep

If you want a one-paragraph summary to walk away with:

> A Transformer turns each token into a vector, adds position information, then repeatedly mixes information between tokens (self-attention) and processes each token independently (feed-forward), wrapped in residual connections and layer norms. Stack enough of these blocks, train on enough text, and you get something that has effectively read the internet.

The "magic" isn't really magic — it's a stack of dot products, softmaxes, and linear layers, applied at enormous scale. The genius of the 2017 paper was figuring out that this particular combination, with no recurrence at all, was the right shape for learning language.

* * *

## References and Further Reading

- Vaswani et al., **["Attention Is All You Need"](https://arxiv.org/abs/1706.03762)** — the original 2017 Transformer paper. Surprisingly readable.
- Jay Alammar, **["The Illustrated Transformer"](https://jalammar.github.io/illustrated-transformer/)** — beautiful visual walkthrough; still the best intro on the internet.
- Andrej Karpathy, **["Let's build GPT: from scratch, in code, spelled out"](https://www.youtube.com/watch?v=kCc8FmEb1nY)** — two hours that will leave you understanding GPT.
- Karpathy's **[nanoGPT](https://github.com/karpathy/nanoGPT)** — a clean, minimal PyTorch implementation of GPT you can read in one sitting.
- Devlin et al., **["BERT: Pre-training of Deep Bidirectional Transformers"](https://arxiv.org/abs/1810.04805)** — the encoder-only sibling that powered a generation of NLP models.
- Radford et al., **["Language Models are Unsupervised Multitask Learners"](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)** — the GPT-2 paper; decoder-only Transformers at scale.
- Lilian Weng, **["The Transformer Family"](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/)** — great survey of variants (sparse attention, long-context tricks, RoPE, etc.).
- Dao et al., **["FlashAttention"](https://arxiv.org/abs/2205.14135)** — how modern systems make attention fast and memory-efficient.

If you implement even a tiny version of the model above and train it on a few megabytes of text, the way these pieces click together stops feeling abstract pretty quickly. Highly recommended.
