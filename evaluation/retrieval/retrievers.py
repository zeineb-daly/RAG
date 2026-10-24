"""The two retrievers compared in the evaluation.

Both have the same two methods:
    index(chunks)        : prepare the retriever with all the chunks of the corpus
    search(question, k)  : return the k best chunks, best first
"""
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from langchain_ollama import OllamaEmbeddings

from app.config import OLLAMA_BASE_URL, EMBEDDING_MODEL, EMBEDDING_QUERY_PREFIX, EMBEDDING_DOC_PREFIX
# Same BM25 and fusion code as the app
from app.search import HYBRID_CANDIDATES, bm25_index, reciprocal_rank_fusion


class PrefixedEmbeddings(Embeddings):
    """Add a text prefix before embedding questions and documents.

    Copy of app/retriever.py: importing that module would open the app's real
    chroma_db/ database, which the evaluation must never touch.
    """

    def __init__(self, base, query_prefix, doc_prefix):
        self.base = base
        self.query_prefix = query_prefix
        self.doc_prefix = doc_prefix

    def embed_documents(self, texts):
        return self.base.embed_documents([self.doc_prefix + t for t in texts])

    def embed_query(self, text):
        return self.base.embed_query(self.query_prefix + text)


class DenseRetriever:
    """Semantic search with the app's embedding model (nomic-embed-text + prefix)."""
    name = "Dense"

    def index(self, chunks):
        embeddings = PrefixedEmbeddings(
            OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=OLLAMA_BASE_URL),
            EMBEDDING_QUERY_PREFIX,
            EMBEDDING_DOC_PREFIX,
        )
        # Temporary in-memory collection (no persist_directory)
        self.vectorstore = Chroma(collection_name="eval_dense", embedding_function=embeddings)
        # Small batches: Ollama's runner crashes when it receives ~600 texts at once
        for start in range(0, len(chunks), 64):
            self.vectorstore.add_documents(chunks[start:start + 64])

    def search(self, question, k):
        return self.vectorstore.similarity_search(question, k=k)


class BM25Retriever:
    """Keyword search (see app/search.py), with or without English stopwords."""

    def __init__(self, remove_stopwords):
        self.remove_stopwords = remove_stopwords
        self.name = "BM25 + stopwords" if remove_stopwords else "BM25 (raw)"

    def index(self, chunks):
        self.bm25 = bm25_index(chunks, self.remove_stopwords)

    def search(self, question, k):
        self.bm25.k = k
        return self.bm25.invoke(question)


class HybridRetriever:
    """Combine Dense and BM25 with Reciprocal Rank Fusion (see app/search.py)."""
    name = "Hybrid"

    def __init__(self, dense, bm25, candidates=HYBRID_CANDIDATES):
        self.retrievers = [dense, bm25]
        self.candidates = candidates

    def index(self, chunks):
        pass  # uses the two retrievers, already indexed

    def search(self, question, k):
        return reciprocal_rank_fusion(
            [retriever.search(question, self.candidates) for retriever in self.retrievers],
            key=lambda doc: (doc.metadata["file"], doc.metadata["page"], doc.page_content),
            k=k,
        )
