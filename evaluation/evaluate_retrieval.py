"""Compare embedding models on retrieval quality.

For each embedding configuration, the course PDF is indexed in a temporary
in-memory Chroma collection (the app's real database is never touched),
then every evaluation question is searched and the retrieved pages are
compared with the expected pages.

Metrics (a "context id" is a page number):
    Hit Rate@k        : % of questions where at least one relevant page is retrieved
    MRR               : average of 1 / rank of the first relevant chunk (0 if none)
    Context Recall    : RAGAS IDBasedContextRecall, share of relevant pages retrieved
    Context Precision : RAGAS IDBasedContextPrecision, share of retrieved pages that are relevant

Run from the ESILV_Tutor folder (inside Docker, see README):
    python -m evaluation.evaluate_retrieval
"""
import csv
import json
import platform
import sys
import time
import warnings
from datetime import date
from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.embeddings import Embeddings
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ragas import SingleTurnSample

with warnings.catch_warnings():
    # These metrics are moving to ragas.metrics.collections in ragas 1.0
    warnings.simplefilter("ignore", DeprecationWarning)
    from ragas.metrics import IDBasedContextPrecision, IDBasedContextRecall

from app.config import OLLAMA_BASE_URL, TOP_K, CHUNK_SIZE, CHUNK_OVERLAP

# Non-LLM RAGAS metrics: they compare retrieved ids with reference ids
context_recall = IDBasedContextRecall()
context_precision = IDBasedContextPrecision()

EVAL_DIR = Path(__file__).parent
QUESTIONS_PATH = EVAL_DIR / "eval_questions.json"
RESULTS_DIR = EVAL_DIR / "results"
DEFAULT_PDF_PATH = "data/courses/1.1-comparison-NoSql-DB-vs-standard-DB.pdf"

# Each configuration = one embedding model + the prefixes it was trained with
EMBEDDING_CONFIGS = [
    {
        "name": "nomic-embed-text",
        "model": "nomic-embed-text",
        "query_prefix": "",
        "doc_prefix": "",
    },
    {
        "name": "nomic-embed-text + prefix",
        "model": "nomic-embed-text",
        "query_prefix": "search_query: ",
        "doc_prefix": "search_document: ",
    },
    {
        "name": "mxbai-embed-large + prefix",
        "model": "mxbai-embed-large",
        "query_prefix": "Represent this sentence for searching relevant passages: ",
        "doc_prefix": "",
    },
    {
        "name": "all-minilm",
        "model": "all-minilm",
        "query_prefix": "",
        "doc_prefix": "",
    },
]


class PrefixedEmbeddings(Embeddings):
    """Add a text prefix before embedding questions and documents."""

    def __init__(self, base, query_prefix, doc_prefix):
        self.base = base
        self.query_prefix = query_prefix
        self.doc_prefix = doc_prefix

    def embed_documents(self, texts):
        return self.base.embed_documents([self.doc_prefix + t for t in texts])

    def embed_query(self, text):
        return self.base.embed_query(self.query_prefix + text)


def load_chunks(pdf_path):
    """Load and split the PDF exactly like the app does (same chunk settings)."""
    documents = PyPDFLoader(pdf_path).load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    return splitter.split_documents(documents)


def page_number(doc):
    # PyPDFLoader stores a 0-based page index
    return doc.metadata.get("page", 0) + 1


def score_question(retrieved_pages, relevant_pages):
    relevant = set(relevant_pages)

    hit = any(page in relevant for page in retrieved_pages)

    reciprocal_rank = 0.0
    for rank, page in enumerate(retrieved_pages, start=1):
        if page in relevant:
            reciprocal_rank = 1 / rank
            break

    sample = SingleTurnSample(
        retrieved_context_ids=retrieved_pages,
        reference_context_ids=relevant_pages
    )
    recall = context_recall.single_turn_score(sample)
    precision = context_precision.single_turn_score(sample)

    return hit, reciprocal_rank, recall, precision


def evaluate_config(config, chunks, questions):
    base = OllamaEmbeddings(model=config["model"], base_url=OLLAMA_BASE_URL)
    embeddings = PrefixedEmbeddings(base, config["query_prefix"], config["doc_prefix"])

    # Temporary in-memory collection (no persist_directory)
    collection_name = "eval_" + config["name"].replace(" ", "_").replace("+", "plus")
    vectorstore = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings
    )

    try:
        start = time.perf_counter()
        vectorstore.add_documents(chunks)
        index_time = time.perf_counter() - start

        details = []
        for q in questions:
            docs = vectorstore.similarity_search(q["question"], k=TOP_K)
            retrieved_pages = [page_number(doc) for doc in docs]
            hit, rr, recall, precision = score_question(
                retrieved_pages, q["relevant_pages"]
            )

            details.append({
                "config": config["name"],
                "id": q["id"],
                "type": q["type"],
                "question": q["question"],
                "relevant_pages": q["relevant_pages"],
                "retrieved_pages": retrieved_pages,
                "hit": hit,
                "reciprocal_rank": rr,
                "context_recall": recall,
                "context_precision": precision,
            })
    finally:
        vectorstore.delete_collection()

    summary = {
        "config": config["name"],
        "index_time": index_time,
        "all": summarize(details),
        "paraphrased": summarize([d for d in details if d["type"] == "paraphrased"]),
    }
    return summary, details


def summarize(details):
    n = len(details)
    if n == 0:
        return None
    return {
        "n": n,
        "hit_rate": sum(d["hit"] for d in details) / n,
        "mrr": sum(d["reciprocal_rank"] for d in details) / n,
        "context_recall": sum(d["context_recall"] for d in details) / n,
        "context_precision": sum(d["context_precision"] for d in details) / n,
    }


def markdown_table(summaries, subset, with_time):
    header = (
        f"| Embedding model | Hit Rate@{TOP_K} | MRR | Context Recall (RAGAS) "
        "| Context Precision (RAGAS) |"
    )
    separator = "|---|---:|---:|---:|---:|"
    if with_time:
        header += " Index time (s) |"
        separator += "---:|"

    lines = [header, separator]
    rows = [s for s in summaries if s[subset]]
    for s in sorted(rows, key=lambda s: (s[subset]["mrr"], s[subset]["context_recall"]), reverse=True):
        m = s[subset]
        line = (
            f"| {s['config']} | {m['hit_rate']:.0%} | {m['mrr']:.2f} "
            f"| {m['context_recall']:.0%} | {m['context_precision']:.0%} |"
        )
        if with_time:
            line += f" {s['index_time']:.1f} |"
        lines.append(line)
    return lines


def write_markdown(summaries, n_questions, n_chunks, pdf_name, skipped):
    n_paraphrased = summaries[0]["paraphrased"]["n"] if summaries[0]["paraphrased"] else 0
    lines = [
        "# Retrieval Evaluation — Embedding Models",
        "",
        f"- Date: {date.today().isoformat()}",
        f"- Course: `{pdf_name}` ({n_chunks} chunks, chunk_size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})",
        f"- Questions: {n_questions} (out-of-scope questions excluded)",
        f"- k = {TOP_K} retrieved chunks per question",
        f"- Machine: {platform.processor() or platform.machine()} (CPU only)",
        "",
        f"## All questions ({n_questions})",
        "",
        *markdown_table(summaries, "all", with_time=True),
        "",
        f"## Paraphrased questions only ({n_paraphrased})",
        "",
        "Questions written like a student would ask them, without reusing the slide wording.",
        "",
        *markdown_table(summaries, "paraphrased", with_time=False),
        "",
        "Note: the first configuration's index time includes loading the model into memory.",
    ]

    if skipped:
        lines += ["", "Skipped (model not available): " + ", ".join(skipped)]

    path = RESULTS_DIR / "retrieval_results.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_csv(all_details):
    path = RESULTS_DIR / "retrieval_details.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(all_details[0].keys()))
        writer.writeheader()
        writer.writerows(all_details)
    return path


def main():
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PDF_PATH

    data = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))
    # Out-of-scope questions have no relevant page: they are only used for the LLM evaluation
    questions = [q for q in data["questions"] if q["relevant_pages"]]

    chunks = load_chunks(pdf_path)
    print(f"Loaded {len(chunks)} chunks from {pdf_path}")
    print(f"Evaluating {len(questions)} questions with k={TOP_K}\n")

    summaries, all_details, skipped = [], [], []

    for config in EMBEDDING_CONFIGS:
        print(f"-> {config['name']} ...")
        try:
            summary, details = evaluate_config(config, chunks, questions)
        except Exception as e:
            print(f"   skipped: {e}")
            skipped.append(config["name"])
            continue

        summaries.append(summary)
        all_details.extend(details)
        for subset in ("all", "paraphrased"):
            m = summary[subset]
            if m:
                print(
                    f"   [{subset:<11}] Hit Rate={m['hit_rate']:.0%}  MRR={m['mrr']:.2f}  "
                    f"Context Recall={m['context_recall']:.0%}  "
                    f"Context Precision={m['context_precision']:.0%}"
                )
        print(f"   ({summary['index_time']:.1f}s to index)")

    if not summaries:
        print("No configuration could be evaluated.")
        return

    RESULTS_DIR.mkdir(exist_ok=True)
    md_path = write_markdown(
        summaries, len(questions), len(chunks), Path(pdf_path).name, skipped
    )
    csv_path = write_csv(all_details)

    print(f"\nResults written to {md_path} and {csv_path}")


if __name__ == "__main__":
    main()
