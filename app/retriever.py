import logging

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from app.search import HYBRID_CANDIDATES, bm25_index, reciprocal_rank_fusion
from app.config import (
    OLLAMA_BASE_URL,
    EMBEDDING_MODEL,
    TOP_K,
    CHROMA_DIR,
    COLLECTION_NAME,
    EMBEDDING_QUERY_PREFIX,
    EMBEDDING_DOC_PREFIX,
)


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


embeddings = PrefixedEmbeddings(
    OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=OLLAMA_BASE_URL),
    query_prefix=EMBEDDING_QUERY_PREFIX,
    doc_prefix=EMBEDDING_DOC_PREFIX,
)

vectorstore = Chroma(
    persist_directory=CHROMA_DIR,
    embedding_function=embeddings,
    collection_name=COLLECTION_NAME
)

retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})


def retrieve_documents(question):
    return retriever.invoke(question)


# -------------------------
# BM25 (keywords) and Hybrid (Dense + BM25)
# -------------------------

logger = logging.getLogger(__name__)

# Built from the chunks already stored in Chroma (see build_bm25_index)
bm25 = None


def build_bm25_index():
    """(Re)build the BM25 index from every chunk in Chroma. Chroma itself is only read."""
    global bm25
    data = vectorstore.get(include=["documents", "metadatas"])
    chunks = [
        Document(page_content=text, metadata=metadata)
        for text, metadata in zip(data["documents"], data["metadatas"])
    ]
    # Same order as the evaluation corpus (file, then page): only changes how ties are broken
    chunks.sort(key=lambda c: (c.metadata.get("source", ""), c.metadata.get("page", 0)))
    # rank_bm25 cannot index an empty corpus
    bm25 = bm25_index(chunks) if chunks else None
    logger.info("BM25 index built with %d chunks", len(chunks))


def bm25_search(question, k, course=None):
    """The k best chunks by keywords, in one course or in every course."""
    index = bm25  # local copy: an upload can replace the index during the search
    if index is None:
        return []
    # Rank every chunk with the index of all courses, then keep the course's chunks
    ranked = index.vectorizer.get_top_n(index.preprocess_func(question), index.docs, n=len(index.docs))
    if course:
        ranked = [doc for doc in ranked if doc.metadata.get("source") == course]
    return ranked[:k]


def hybrid_search(question, k, course=None):
    """Dense + BM25 merged with Reciprocal Rank Fusion (same as the evaluation)."""
    dense_docs = vectorstore.similarity_search(
        question,
        k=HYBRID_CANDIDATES,
        filter={"source": course} if course else None
    )
    bm25_docs = bm25_search(question, HYBRID_CANDIDATES, course)
    return reciprocal_rank_fusion(
        [dense_docs, bm25_docs],
        key=lambda doc: (doc.metadata.get("source"), doc.metadata.get("page"), doc.page_content),
        k=k,
    )


def format_docs(docs):
    formatted_chunks = []

    for doc in docs:
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page_label", "Unknown")
        title = doc.metadata.get("document_title", source)

        formatted_chunks.append(
            f"Document: {title}\n"
            f"Source: {source}\n"
            f"Page: {page}\n"
            f"Content:\n{doc.page_content}"
        )

    return "\n\n---\n\n".join(formatted_chunks)

def extract_sources(docs):
    sources = []
    for doc in docs:
        source = {
            "file": doc.metadata.get("source", "Unknown"),
            "page": doc.metadata.get("page_label", doc.metadata.get("page", 0) + 1)
        }
        if source not in sources:
            sources.append(source)
    return sources
