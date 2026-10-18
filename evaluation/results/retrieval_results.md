# Retrieval Evaluation — Embedding Models

- Date: 2026-10-18
- Course: `1.1-comparison-NoSql-DB-vs-standard-DB.pdf` (35 chunks, chunk_size=500, overlap=100)
- Questions: 31 (out-of-scope questions excluded)
- k = 3 retrieved chunks per question
- Machine: x86_64 (CPU only)

## All questions (31)

| Embedding model | Hit Rate@3 | MRR | Context Recall (RAGAS) | Context Precision (RAGAS) | Index time (s) |
|---|---:|---:|---:|---:|---:|
| mxbai-embed-large + prefix | 97% | 0.94 | 88% | 39% | 14.3 |
| all-minilm | 97% | 0.94 | 86% | 38% | 2.0 |
| nomic-embed-text + prefix | 97% | 0.92 | 88% | 39% | 6.0 |
| nomic-embed-text | 94% | 0.87 | 84% | 39% | 6.0 |

## Paraphrased questions only (14)

Questions written like a student would ask them, without reusing the slide wording.

| Embedding model | Hit Rate@3 | MRR | Context Recall (RAGAS) | Context Precision (RAGAS) |
|---|---:|---:|---:|---:|
| mxbai-embed-large + prefix | 93% | 0.89 | 86% | 36% |
| all-minilm | 93% | 0.89 | 79% | 33% |
| nomic-embed-text + prefix | 93% | 0.86 | 82% | 36% |
| nomic-embed-text | 86% | 0.77 | 79% | 36% |

Note: the first configuration's index time includes loading the model into memory.
