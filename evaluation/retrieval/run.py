"""Compare Dense (embeddings) and BM25 (keywords) retrieval on the evaluation dataset.

Outputs, in evaluation/results/retrieval_dense_vs_bm25_k{TOP_K}.md:
    1. Hit Rate and MRR per question type, for each retriever
    2. Complementarity between Dense and BM25 + stopwords
    3. The questions found by only one of them, and by none (concrete examples)

Run from the ESILV_Tutor folder (inside Docker, see README):
    python -m evaluation.retrieval.run
"""
import json
from pathlib import Path

from app.config import TOP_K
from evaluation.retrieval.corpus import load_chunks
from evaluation.retrieval.metrics import hit_rate, mrr
from evaluation.retrieval.retrievers import BM25Retriever, DenseRetriever, HybridRetriever

EVAL_DIR = Path(__file__).parent.parent
TYPES = ["factual", "conceptual", "paraphrased", "lexical"]


def load_questions():
    questions = []
    for path in sorted((EVAL_DIR / "datasets").glob("*.json")):
        questions += json.loads(path.read_text(encoding="utf-8"))
    # Out-of-scope questions have no relevant page: they are only used for the LLM evaluation
    return [q for q in questions if q["type"] != "out_of_scope"]


def evaluate(retriever, chunks, questions):
    """For each question id: the retrieved (file, page) list, its hit and its reciprocal rank."""
    print(f"Indexing {len(chunks)} chunks with {retriever.name}...")
    retriever.index(chunks)

    results = {}
    for q in questions:
        docs = retriever.search(q["question"], k=TOP_K)
        retrieved = [(d.metadata["file"], d.metadata["page"]) for d in docs]
        relevant = {(r["file"], r["page"]) for r in q["relevant"]}
        results[q["id"]] = {
            "retrieved": retrieved,
            "hit": hit_rate(retrieved, relevant),
            "rr": mrr(retrieved, relevant),
        }
    return results


def average(values):
    return sum(values) / len(values)


def pages(ids):
    return ", ".join(f"{f[:12]} p{p}" for f, p in ids)


def main():
    questions = load_questions()
    chunks = load_chunks()
    dense, bm25 = DenseRetriever(), BM25Retriever(remove_stopwords=True)
    retrievers = [dense, BM25Retriever(remove_stopwords=False), bm25, HybridRetriever(dense, bm25)]
    results = {r.name: evaluate(r, chunks, questions) for r in retrievers}

    lines = [
        "# Retrieval Evaluation — Dense vs BM25",
        "",
        f"- Corpus: {len({c.metadata['file'] for c in chunks})} PDFs, {len(chunks)} chunks",
        f"- Questions: {len(questions)} (out-of-scope excluded)",
        # The app's own k is TOP_K in .env (3 by default): this run may override it (-e TOP_K=5)
        f"- k = {TOP_K} retrieved chunks per question (the app uses TOP_K from .env, 3 by default)",
        "- Dense = nomic-embed-text + prefix (the app's retriever)",
        "- BM25 (raw) = keyword search on lowercase words",
        "- BM25 + stopwords = same, without common English words (scikit-learn ENGLISH_STOP_WORDS)",
        "- Hybrid = Dense + BM25 + stopwords, top 10 of each merged with Reciprocal Rank Fusion",
        "",
        "## 1. Results per question type",
        "",
        "| Type | Questions | " + " | ".join(f"{name} Hit@{TOP_K} | {name} MRR" for name in results) + " |",
        "|---|---:|" + "---:|---:|" * len(results),
    ]
    groups_by_row = {qtype: [q["id"] for q in questions if q["type"] == qtype] for qtype in TYPES}
    # Questions taken from the teacher's TD exercises (realistic wording, not written from the slides)
    groups_by_row["TD questions"] = [q["id"] for q in questions if q["id"].startswith("td-")]
    groups_by_row["**All**"] = [q["id"] for q in questions]
    for label, ids in groups_by_row.items():
        cells = [
            f"{average([res[i]['hit'] for i in ids]):.0%} | {average([res[i]['rr'] for i in ids]):.2f}"
            for res in results.values()
        ]
        lines.append(f"| {label} | {len(ids)} | " + " | ".join(cells) + " |")

    # Complementarity between the app's retriever and the best BM25
    dense, bm25 = results["Dense"], results["BM25 + stopwords"]
    groups = {
        "Found by both": [q for q in questions if dense[q["id"]]["hit"] and bm25[q["id"]]["hit"]],
        "Missed by Dense, found by BM25": [q for q in questions if not dense[q["id"]]["hit"] and bm25[q["id"]]["hit"]],
        "Missed by BM25, found by Dense": [q for q in questions if dense[q["id"]]["hit"] and not bm25[q["id"]]["hit"]],
        "Missed by both": [q for q in questions if not dense[q["id"]]["hit"] and not bm25[q["id"]]["hit"]],
    }
    found = len(questions) - len(groups["Missed by both"])

    lines += [
        "",
        "## 2. Complementarity (Dense vs BM25 + stopwords)",
        "",
        "| | Questions |",
        "|---|---:|",
        *[f"| {title} | {len(qs)} |" for title, qs in groups.items()],
        f"| **Found by at least one** | **{found} / {len(questions)} ({found / len(questions):.0%})** |",
    ]

    for number, title in enumerate(list(groups)[1:], start=3):
        lines += ["", f"## {number}. {title}", "",
                  "| id | Type | Question | Expected pages | Dense retrieved | BM25 retrieved |",
                  "|---|---|---|---|---|---|"]
        for q in groups[title]:
            expected = [(r["file"], r["page"]) for r in q["relevant"]]
            lines.append(
                f"| {q['id']} | {q['type']} | {q['question']} | {pages(expected)} "
                f"| {pages(dense[q['id']]['retrieved'])} | {pages(bm25[q['id']]['retrieved'])} |"
            )

    # Wins/losses: what Hybrid changes compared with Dense, question by question
    hybrid = results["Hybrid"]
    wins = [q for q in questions if not dense[q["id"]]["hit"] and hybrid[q["id"]]["hit"]]
    losses = [q for q in questions if dense[q["id"]]["hit"] and not hybrid[q["id"]]["hit"]]
    lines += [
        "", "## 6. Wins / losses (Hybrid vs Dense)", "",
        "| | Questions |", "|---|---:|",
        f"| Wins (missed by Dense, found by Hybrid) | {len(wins)} |",
        f"| Losses (found by Dense, missed by Hybrid) | {len(losses)} |",
        f"| Unchanged | {len(questions) - len(wins) - len(losses)} |",
    ]
    for title, subset in [("Wins", wins), ("Losses", losses)]:
        lines += ["", f"### {title}", "",
                  "| id | Type | Question | Expected pages | Dense retrieved | Hybrid retrieved |",
                  "|---|---|---|---|---|---|"]
        for q in subset:
            expected = [(r["file"], r["page"]) for r in q["relevant"]]
            lines.append(
                f"| {q['id']} | {q['type']} | {q['question']} | {pages(expected)} "
                f"| {pages(dense[q['id']]['retrieved'])} | {pages(hybrid[q['id']]['retrieved'])} |"
            )

    path = EVAL_DIR / "results" / f"retrieval_dense_vs_bm25_k{TOP_K}.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:30]))
    print(f"\nFull results written to {path}")


if __name__ == "__main__":
    main()
