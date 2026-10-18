"""Compare LLMs on answer quality.

Every model receives exactly the same context for each question: the
retrieval is done once with the app's real pipeline (app.retriever), then
the app's prompt (app.generation) is sent to each LLM. Only the LLM changes.

Metrics (no LLM judge):
    Keyword Coverage     : share of expected keywords found in the answer (in-scope questions)
    False Refusal Rate   : % of in-scope questions answered with the refusal sentence
    Correct Refusal Rate : % of out-of-scope questions answered with the refusal sentence
    Forbidden Phrases    : number of known wrong statements found in the answers
    Latency              : average seconds per answer (model already loaded)

Run from the ESILV_Tutor folder (inside Docker, see README):
    python -m evaluation.evaluate_generation            # ask every model
    python -m evaluation.evaluate_generation --rescore  # recompute metrics from saved answers
"""
import csv
import json
import platform
import re
import sys
import time
from datetime import date
from pathlib import Path

from langchain_ollama import ChatOllama

from app.config import OLLAMA_BASE_URL, TOP_K, COLLECTION_NAME, EMBEDDING_MODEL
from app.generation import prompt
from app.retriever import format_docs
from app.courses import retrieve_documents_for_course

EVAL_DIR = Path(__file__).parent
QUESTIONS_PATH = EVAL_DIR / "eval_questions.json"
RESULTS_DIR = EVAL_DIR / "results"

LLM_MODELS = ["llama3.2:3b", "qwen2.5:7b"]

# Matches the prompt's refusal sentence and close variants,
# e.g. "I could not find information about MongoDB"
REFUSAL_PATTERN = re.compile(r"could not find (this |any )?information", re.IGNORECASE)


def is_refusal(answer):
    return bool(REFUSAL_PATTERN.search(answer))


def keyword_coverage(answer, keywords):
    if not keywords:
        return None
    text = answer.lower()
    return sum(1 for k in keywords if k.lower() in text) / len(keywords)


def forbidden_found(answer, phrases):
    text = answer.lower()
    return [p for p in phrases if p.lower() in text]


def evaluate_model(model, questions, contexts):
    llm = ChatOllama(model=model, base_url=OLLAMA_BASE_URL, temperature=0)
    chain = prompt | llm

    # Warm-up: load the model into memory so it does not count in the latency
    llm.invoke("Hello")

    details = []
    for q in questions:
        start = time.perf_counter()
        answer = chain.invoke({
            "context": contexts[q["id"]],
            "question": q["question"]
        }).content
        latency = time.perf_counter() - start

        details.append({
            "model": model,
            "id": q["id"],
            "type": q["type"],
            "question": q["question"],
            "answer": answer,
            "refused": is_refusal(answer),
            "keyword_coverage": keyword_coverage(answer, q["expected_keywords"]),
            "forbidden_found": forbidden_found(answer, q["forbidden_phrases"]),
            "latency": latency,
            "words": len(answer.split()),
        })
        print(f"   {q['id']}  {latency:5.1f}s  refused={details[-1]['refused']}")

    return details


def summarize(model, details):
    in_scope = [d for d in details if d["type"] != "out_of_scope"]
    out_scope = [d for d in details if d["type"] == "out_of_scope"]

    return {
        "model": model,
        "keyword_coverage": sum(d["keyword_coverage"] for d in in_scope) / len(in_scope),
        "false_refusal_rate": sum(d["refused"] for d in in_scope) / len(in_scope),
        "correct_refusal_rate": (
            sum(d["refused"] for d in out_scope) / len(out_scope) if out_scope else None
        ),
        "forbidden": sum(len(d["forbidden_found"]) for d in details),
        "latency": sum(d["latency"] for d in details) / len(details),
        "words": sum(d["words"] for d in details) / len(details),
        "n_in_scope": len(in_scope),
        "n_out_scope": len(out_scope),
    }


def write_results(summaries, all_details, questions, contexts_pages, course):
    RESULTS_DIR.mkdir(exist_ok=True)
    s0 = summaries[0]

    lines = [
        "# Generation Evaluation — LLMs",
        "",
        f"- Date: {date.today().isoformat()}",
        f"- Retrieval: `{EMBEDDING_MODEL}` + prefix, collection `{COLLECTION_NAME}`, k = {TOP_K} (same context for every model)",
        f"- Course filter: `{course}`",
        f"- Questions: {s0['n_in_scope']} in-scope + {s0['n_out_scope']} out-of-scope",
        "- Temperature: 0",
        f"- Machine: {platform.processor() or platform.machine()} (CPU only)",
        "",
        "| LLM | Keyword Coverage ↑ | False Refusal ↓ | Correct Refusal ↑ "
        "| Forbidden Phrases ↓ | Latency (s) ↓ | Avg words |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for s in summaries:
        correct = f"{s['correct_refusal_rate']:.0%}" if s["correct_refusal_rate"] is not None else "-"
        lines.append(
            f"| {s['model']} | {s['keyword_coverage']:.0%} | {s['false_refusal_rate']:.0%} "
            f"| {correct} | {s['forbidden']} | {s['latency']:.1f} | {s['words']:.0f} |"
        )
    lines += [
        "",
        "↑ higher is better, ↓ lower is better. Side-by-side answers: `generation_answers.md`.",
    ]
    (RESULTS_DIR / "generation_results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Side-by-side answers, for human review
    by_key = {(d["model"], d["id"]): d for d in all_details}
    answers = ["# Generation Evaluation — Answers side by side", ""]
    for q in questions:
        answers += [
            f"## {q['id']} ({q['type']}) — {q['question']}",
            "",
            f"Retrieved pages: {contexts_pages[q['id']]} · Expected pages: {q['relevant_pages'] or 'none (out of scope)'}",
            "",
        ]
        for s in summaries:
            d = by_key[(s["model"], q["id"])]
            cov = f"{d['keyword_coverage']:.0%}" if d["keyword_coverage"] is not None else "-"
            answers += [
                f"### {s['model']}  (keywords {cov}, refused={d['refused']}, {d['latency']:.0f}s)",
                "",
                d["answer"],
                "",
            ]
    (RESULTS_DIR / "generation_answers.md").write_text("\n".join(answers) + "\n", encoding="utf-8")

    with open(RESULTS_DIR / "generation_details.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(all_details[0].keys()))
        writer.writeheader()
        writer.writerows(all_details)


def rescore(questions):
    """Recompute every metric from the answers saved in generation_details.csv."""
    by_id = {q["id"]: q for q in questions}
    all_details = []

    with open(RESULTS_DIR / "generation_details.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            q = by_id[row["id"]]
            answer = row["answer"]
            all_details.append({
                "model": row["model"],
                "id": q["id"],
                "type": q["type"],
                "question": q["question"],
                "answer": answer,
                "refused": is_refusal(answer),
                "keyword_coverage": keyword_coverage(answer, q["expected_keywords"]),
                "forbidden_found": forbidden_found(answer, q["forbidden_phrases"]),
                "latency": float(row["latency"]),
                "words": len(answer.split()),
            })

    models = list(dict.fromkeys(d["model"] for d in all_details))
    summaries = [
        summarize(m, [d for d in all_details if d["model"] == m]) for m in models
    ]
    return summaries, all_details


def main():
    data = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))
    questions = data["questions"]

    # 1. Retrieval once, shared by every model.
    # Filtered on the course the questions are about, so that other uploaded
    # courses do not change the context (results stay comparable over time).
    course = data["course"]
    contexts, contexts_pages = {}, {}
    for q in questions:
        docs = retrieve_documents_for_course(q["question"], course)
        contexts[q["id"]] = format_docs(docs)
        contexts_pages[q["id"]] = [d.metadata.get("page", 0) + 1 for d in docs]
    print(f"Retrieved contexts for {len(questions)} questions from '{course}'\n")

    if "--rescore" in sys.argv:
        summaries, all_details = rescore(questions)
    else:
        # 2. Generation with each model
        summaries, all_details = [], []
        for model in LLM_MODELS:
            print(f"-> {model}")
            details = evaluate_model(model, questions, contexts)
            all_details.extend(details)
            summaries.append(summarize(model, details))

    write_results(summaries, all_details, questions, contexts_pages, course)

    print()
    for s in summaries:
        print(
            f"{s['model']:<14} coverage={s['keyword_coverage']:.0%}  "
            f"false_refusal={s['false_refusal_rate']:.0%}  "
            f"correct_refusal={s['correct_refusal_rate']:.0%}  "
            f"forbidden={s['forbidden']}  latency={s['latency']:.1f}s"
        )
    print(f"\nResults written to {RESULTS_DIR}")


if __name__ == "__main__":
    main()
