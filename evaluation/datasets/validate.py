"""Validate the evaluation datasets against the course PDFs.

Checks:
  1. Format        : required fields, unique ids, valid types
  2. Pages         : every relevant page exists and is not an empty page
  3. Cross-course  : pages OUTSIDE `relevant` (any course) that share the
                     question's rare terms -> candidates to review by hand
  4. Out-of-scope  : out_of_scope questions must have no matching page

Run from the ESILV_Tutor folder (inside Docker, see evaluation/datasets/README.md):
    python evaluation/datasets/validate.py
"""
import json
import math
import re
from collections import Counter
from pathlib import Path

from pypdf import PdfReader

TYPES = {"factual", "conceptual", "paraphrased", "lexical", "out_of_scope"}
FIELDS = {"id", "course", "question", "type", "relevant", "keywords", "notes"}
EMPTY_THRESHOLD = 30   # chars, same as the corpus inventory
RARE_MAX_PAGES = 15    # a term is "rare" if it appears on at most 15 pages of the corpus
MAX_CANDIDATES = 4

DATASETS_DIR = Path(__file__).parent
COURSES_DIR = DATASETS_DIR.parent.parent / "data" / "courses"

STOPWORDS = set("""
a an the is are was were be been of in on at to for from by with and or not no what which who
why how when where does do did can could should would will it its this that these those there
than then into about as if so i my me you your we our they their between used use using mean
means main default kind more most other some several whole each also very many much
""".split())


def tokens(text):
    return re.findall(r"[a-z0-9_.\-]+[a-z0-9_]|[a-z0-9]", text.lower())


def load_corpus(courses_dir):
    pages = {}
    for pdf in sorted(courses_dir.glob("*.pdf")):
        for i, page in enumerate(PdfReader(pdf).pages, 1):
            pages[(pdf.name, i)] = (page.extract_text() or "")
    return pages


def main():
    pages = load_corpus(COURSES_DIR)
    page_tokens = {k: set(tokens(v)) for k, v in pages.items()}
    df = Counter(t for toks in page_tokens.values() for t in toks)
    files = {f for f, _ in pages}

    questions = []
    for path in sorted(DATASETS_DIR.glob("*.json")):
        for q in json.loads(path.read_text(encoding="utf-8")):
            questions.append((path.name, q))

    errors, report = [], []

    # 1. Format
    ids = Counter(q.get("id") for _, q in questions)
    for name, q in questions:
        missing = FIELDS - q.keys()
        if missing:
            errors.append(f"{name} {q.get('id')}: missing fields {sorted(missing)}")
        if q.get("type") not in TYPES:
            errors.append(f"{name} {q.get('id')}: invalid type {q.get('type')!r}")
        if ids[q.get("id")] > 1:
            errors.append(f"{name} {q.get('id')}: duplicate id")
        if q.get("type") == "out_of_scope" and q.get("relevant"):
            errors.append(f"{q['id']}: out_of_scope question must have relevant = []")
        if q.get("type") != "out_of_scope" and not q.get("relevant"):
            errors.append(f"{q['id']}: in-scope question has no relevant page")

    # 2. Pages
    for _, q in questions:
        for r in q.get("relevant", []):
            key = (r["file"], r["page"])
            if r["file"] not in files:
                errors.append(f"{q['id']}: unknown file {r['file']}")
            elif key not in pages:
                errors.append(f"{q['id']}: page {r['page']} does not exist in {r['file']}")
            elif len(pages[key].strip()) < EMPTY_THRESHOLD:
                errors.append(f"{q['id']}: page {r['page']} of {r['file']} is an empty page")

    # 3 + 4. Candidate pages sharing the question's rare terms
    n_pages = len(pages)
    for _, q in questions:
        rare = [t for t in dict.fromkeys(tokens(q["question"]))
                if t not in STOPWORDS and len(t) > 1 and 0 < df[t] <= RARE_MAX_PAGES]
        if not rare:
            continue
        relevant = {(r["file"], r["page"]) for r in q["relevant"]}
        needed = max(1, math.ceil(0.6 * len(rare)))
        candidates = []
        for key, toks in page_tokens.items():
            if key in relevant:
                continue
            matched = [t for t in rare if t in toks]
            if len(matched) >= needed:
                candidates.append((len(matched), key, matched))
        candidates.sort(key=lambda c: (-c[0], c[1]))
        if candidates:
            report.append((q, rare, candidates[:MAX_CANDIDATES], len(candidates)))

    # Output
    print(f"Corpus: {len(files)} PDFs, {n_pages} pages | Questions: {len(questions)}\n")
    print(f"== Format + pages: {len(errors)} error(s)")
    for e in errors:
        print("  ERROR", e)

    oos = [r for r in report if r[0]["type"] == "out_of_scope"]
    print(f"\n== Out-of-scope with matching pages: {len(oos)}")
    for q, rare, cands, total in oos:
        print(f"  {q['id']} {q['question']}  rare={rare}")
        for score, (f, p), matched in cands:
            print(f"      -> {f} p{p}  matched={matched}")

    inscope = [r for r in report if r[0]["type"] != "out_of_scope"]
    cross = [r for r in inscope if any(f != r[0]["course"] for _, (f, _), _ in r[2])]
    print(f"\n== In-scope questions with candidate pages outside `relevant`: {len(inscope)}"
          f" ({len(cross)} with another course)")
    for q, rare, cands, total in inscope:
        print(f"  {q['id']} [{q['type']}] {q['question']}")
        print(f"      relevant={[r['page'] for r in q['relevant']]}  rare terms={rare}  ({total} candidate pages)")
        for score, (f, p), matched in cands:
            where = "SAME course " if f == q["course"] else "OTHER course"
            print(f"      -> {where} {f} p{p}  matched={matched}")


if __name__ == "__main__":
    main()
