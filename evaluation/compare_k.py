"""Does k=5 give better answers than k=3? Small generation test on a sample of questions.

Same retriever (Dense, like the app) and same prompt (app.generation) for both:
only the number of chunks given to the LLM changes. The k=3 context is the
first 3 chunks of the k=5 context.

Outputs, in evaluation/results/generation_k3_vs_k5.md:
    per k: relevant page in context, false refusals, correct refusals, latency
    and the two answers side by side for each question

Run from the ESILV_Tutor folder (inside Docker, see README):
    python -m evaluation.compare_k
"""
import json
import random
import re
import time
from pathlib import Path

from langchain_ollama import ChatOllama

from app.config import OLLAMA_BASE_URL, LLM_MODEL
from app.generation import prompt
from evaluation.retrieval.corpus import load_chunks
from evaluation.retrieval.retrievers import DenseRetriever

EVAL_DIR = Path(__file__).parent
PER_TYPE = 3
REFUSAL = re.compile(r"could not find (this |any )?information", re.IGNORECASE)


def sample_questions():
    questions = []
    for path in sorted((EVAL_DIR / "datasets").glob("*.json")):
        questions += json.loads(path.read_text(encoding="utf-8"))
    rng = random.Random(0)  # fixed seed: same sample every run
    groups = {
        "factual": [q for q in questions if q["type"] == "factual" and not q["id"].startswith("td-")],
        "conceptual": [q for q in questions if q["type"] == "conceptual" and not q["id"].startswith("td-")],
        "paraphrased": [q for q in questions if q["type"] == "paraphrased"],
        "lexical": [q for q in questions if q["type"] == "lexical"],
        "TD": [q for q in questions if q["id"].startswith("td-")],
    }
    sample = [q for qs in groups.values() for q in rng.sample(qs, PER_TYPE)]
    return sample + rng.sample([q for q in questions if q["type"] == "out_of_scope"], 2)


def format_context(docs):
    # Same layout as app/retriever.py format_docs
    return "\n\n---\n\n".join(
        f"Document: {d.metadata['file']}\nSource: {d.metadata['file']}\n"
        f"Page: {d.metadata['page']}\nContent:\n{d.page_content}"
        for d in docs
    )


def main():
    questions = sample_questions()
    retriever = DenseRetriever()
    print("Indexing...")
    retriever.index(load_chunks())

    chain = prompt | ChatOllama(model=LLM_MODEL, base_url=OLLAMA_BASE_URL, temperature=0)
    chain.invoke({"context": "", "question": "Hello"})  # warm-up: load the model

    rows = []
    for n, q in enumerate(questions, 1):
        docs = retriever.search(q["question"], k=5)
        relevant = {(r["file"], r["page"]) for r in q["relevant"]}
        row = {"q": q}
        for k in (3, 5):
            start = time.perf_counter()
            answer = chain.invoke({"context": format_context(docs[:k]), "question": q["question"]}).content
            row[k] = {
                "answer": answer,
                "latency": time.perf_counter() - start,
                "refusal": bool(REFUSAL.search(answer)),
                "hit": any((d.metadata["file"], d.metadata["page"]) in relevant for d in docs[:k]),
            }
        rows.append(row)
        print(f"{n}/{len(questions)} {q['id']}  k3 {row[3]['latency']:.0f}s  k5 {row[5]['latency']:.0f}s")

    in_scope = [r for r in rows if r["q"]["type"] != "out_of_scope"]
    oos = [r for r in rows if r["q"]["type"] == "out_of_scope"]
    lines = [
        "# Generation test — k=3 vs k=5",
        "",
        f"- LLM: {LLM_MODEL}, retriever: Dense (nomic-embed-text + prefix), same prompt as the app",
        f"- {len(in_scope)} in-scope questions ({PER_TYPE} per type, random seed 0) + {len(oos)} out-of-scope",
        "",
        "| | k=3 | k=5 |",
        "|---|---:|---:|",
        "| Relevant page in context | " + " | ".join(
            f"{sum(r[k]['hit'] for r in in_scope)} / {len(in_scope)}" for k in (3, 5)) + " |",
        "| False refusals (in-scope answered with refusal) | " + " | ".join(
            f"{sum(r[k]['refusal'] for r in in_scope)} / {len(in_scope)}" for k in (3, 5)) + " |",
        "| Correct refusals (out-of-scope) | " + " | ".join(
            f"{sum(r[k]['refusal'] for r in oos)} / {len(oos)}" for k in (3, 5)) + " |",
        "| Average latency (s) | " + " | ".join(
            f"{sum(r[k]['latency'] for r in rows) / len(rows):.1f}" for k in (3, 5)) + " |",
        "",
        "## Answers side by side",
    ]
    for r in rows:
        q = r["q"]
        lines += ["", f"### {q['id']} ({q['type']}) — {q['question']}", ""]
        for k in (3, 5):
            flags = f"page in context: {'yes' if r[k]['hit'] else 'no'}, refusal: {'yes' if r[k]['refusal'] else 'no'}"
            lines += [f"**k={k}** ({flags}, {r[k]['latency']:.0f}s)", "", r[k]["answer"].strip(), ""]

    path = EVAL_DIR / "results" / "generation_k3_vs_k5.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:14]))
    print(f"\nFull results written to {path}")


if __name__ == "__main__":
    main()
