# Evaluation datasets

Annotated questions used to evaluate the retrieval (and later the generation) of ESILV Tutor.

## Corpus

All 9 PDFs in `data/courses/` are indexed together, like in the app when no course filter is selected (592 pages, 613 chunks).

| Role | Course | Questions |
|---|---|---:|
| Annotated | `1.1-comparison-NoSql-DB-vs-standard-DB.pdf` | 40 |
| Annotated | `4-hadoop-ecosystem.pdf` | 36 |
| Annotated | `1-Introduction-Spark-Distributed-Dataset-Operations.pdf` | 36 |
| TD | `TD1-spark-shell.pdf`, `TD2-part1-spark-read-write.pdf`, `TD2-part2-spark-read-write.pdf` | 12 (`td_questions.json`) |
| Distractor | `intro.pdf` | — |
| Distractor | `2-brief-history-distributed-computing.pdf` | — |
| Distractor | `3-failure-and-resiliency-pinciples-distributed-computing.pdf` | — |
| — | `out_of_scope.json` (answer in none of the 9 PDFs) | 10 |
| | **Total** | **134** |

**Annotated** courses have questions with their expected pages. **TD** questions come from the teacher's exercises; their answer can be in a TD or in a course. **Distractor** courses have no questions: they are only indexed to make retrieval harder, since they cover the same domain (Big Data).

The retrieval evaluation (`evaluation/retrieval/run.py`) uses **124** questions: the 10 `out_of_scope` questions are removed, since they have no relevant page.

## Files

| File | Content |
|---|---|
| `nosql_vs_oltp.json` | Questions on the NoSQL vs OLTP course |
| `hadoop_ecosystem.json` | Questions on the Hadoop ecosystem course |
| `spark_intro.json` | Questions on the Spark introduction course |
| `td_questions.json` | Questions taken from the TD exercises (`course` is `null`, ids start with `td-`) |
| `out_of_scope.json` | Questions whose answer is in no course (used to test refusals) |
| `validate.py` | Checks the datasets against the PDFs |

## Question format

```json
{
  "id": "hadoop-lex-01",
  "course": "4-hadoop-ecosystem.pdf",
  "question": "What is an EphemeralZNode?",
  "type": "lexical",
  "relevant": [
    { "file": "4-hadoop-ecosystem.pdf", "page": 12 },
    { "file": "3-failure-and-resiliency-pinciples-distributed-computing.pdf", "page": 48 }
  ],
  "keywords": [],
  "notes": "code identifier"
}
```

| Field | Required | Description |
|---|---|---|
| `id` | yes | Unique id: `<course>-<type>-<number>` |
| `course` | yes | Course the question was written for (`null` for `out_of_scope`) |
| `question` | yes | The question, in English like the slides |
| `type` | yes | One of the 5 types below |
| `relevant` | yes | Every page (file + 1-based page number) that contains the answer, in any course. Empty for `out_of_scope` |
| `keywords` | no | Words expected in the LLM answer (generation evaluation) |
| `notes` | no | Free comment: lexical sub-category, why the question is hard... |

## Question types

| Type | What it tests | Writing rule | Count |
|---|---|---|---:|
| `factual` | Find a definition or a simple fact | Short answer, usually one page | 29 |
| `conceptual` | Understand a *why* / *how* | The answer is an explanation | 31 |
| `paraphrased` | Understand the meaning without the slide wording | **Must not** reuse the key words of the slide | 34 |
| `lexical` | Find an exact, rare term | **Must** contain an exact term of the slide | 30 |
| `out_of_scope` | Refuse when the answer is not in the courses | Topic absent from all 9 PDFs | 10 |

`paraphrased` and `lexical` are opposites on purpose: the first favours semantic search (embeddings), the second favours keyword search (BM25).

`lexical` sub-categories (in `notes`): acronym (`WAL`, `SPOF`), tool / proper name (`etcd`, `Volcano`), code identifier (`_SUCCESS`, `mapPartitions()`), number (`RF = 3`, `2^32 - 1`).

## Annotation rules

1. Questions were written **before** running any retrieval test, and none were removed after seeing results.
2. One question = one idea.
3. No question targets an **empty page** (less than 30 characters of extracted text, i.e. an image-only slide). These pages are kept for a future OCR evaluation.
4. `relevant` lists **every** page that answers the question, including pages of other courses. A page that only *mentions* the term without answering is not relevant.
5. **Near-duplicate slides**: `intro.pdf` and `3-failure-...` contain copies of 8 slides of `4-hadoop-ecosystem.pdf` (86–100% word overlap). Both copies are listed in `relevant`, so a retriever is not penalised for returning the copy.

> **Known bias:** candidate pages from other courses were found by shared rare words (step 3 of `validate.py`), which is close to how BM25 works. Each candidate was read by hand before being added, and near-duplicates were detected by whole-slide similarity, but the extra pages are still mostly lexically close to the question.

## Validation

`validate.py` reads the 9 PDFs and checks:

1. **Format**: required fields, unique ids, valid types
2. **Pages**: every relevant page exists and is not an empty page
3. **Cross-course**: pages outside `relevant` that share the question's rare words, to review by hand
4. **Out-of-scope**: `out_of_scope` questions must have no matching page

It never modifies the datasets. Run it after any change to a question or to `data/courses/`:

```bash
docker compose run --rm evaluation python evaluation/datasets/validate.py
```

Expected result: `0 error(s)`. The candidate pages listed in steps 3 and 4 are suggestions: the remaining ones were reviewed and judged not relevant (the page mentions the term but does not answer the question).
