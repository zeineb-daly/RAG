# Generation Evaluation — LLMs

- Date: 2026-10-18
- Retrieval: `nomic-embed-text` + prefix, collection `school_courses_v2`, k = 3 (same context for every model)
- Course filter: `1.1-comparison-NoSql-DB-vs-standard-DB.pdf`
- Questions: 31 in-scope + 2 out-of-scope
- Temperature: 0
- Machine: x86_64 (CPU only)

| LLM | Keyword Coverage ↑ | False Refusal ↓ | Correct Refusal ↑ | Forbidden Phrases ↓ | Latency (s) ↓ | Avg words |
|---|---:|---:|---:|---:|---:|---:|
| llama3.2:3b | 64% | 3% | 100% | 0 | 18.4 | 121 |
| qwen2.5:7b | 62% | 39% | 100% | 0 | 31.4 | 97 |

↑ higher is better, ↓ lower is better. Side-by-side answers: `generation_answers.md`.
