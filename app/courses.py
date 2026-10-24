"""Course filter: list the indexed courses and search inside a single course.

Each chunk stores the PDF filename in its "source" metadata (see ingestion.py),
so a course is identified by its filename.
"""
from app.config import TOP_K
from app.retriever import vectorstore, retrieve_documents, bm25_search, hybrid_search


def list_courses():
    """Return the sorted list of course filenames stored in Chroma."""
    data = vectorstore.get(include=["metadatas"])
    return sorted({m["source"] for m in data["metadatas"] if m.get("source")})


def retrieve_documents_for_course(question, course=None, mode="dense"):
    """Search in one course only, or in every course when course is None.

    mode: "dense" (embeddings), "bm25" (keywords) or "hybrid" (both, merged with RRF).
    """
    if mode == "bm25":
        return bm25_search(question, TOP_K, course)
    if mode == "hybrid":
        return hybrid_search(question, TOP_K, course)

    if not course:
        return retrieve_documents(question)

    return vectorstore.similarity_search(
        question,
        k=TOP_K,
        filter={"source": course}
    )
