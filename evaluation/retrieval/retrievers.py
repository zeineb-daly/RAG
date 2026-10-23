"""The two retrievers compared in the evaluation.

Both have the same two methods:
    index(chunks)        : prepare the retriever with all the chunks of the corpus
    search(question, k)  : return the k best chunks, best first
"""
import re

from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever as LangchainBM25
from langchain_core.embeddings import Embeddings
from langchain_ollama import OllamaEmbeddings
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

from app.config import OLLAMA_BASE_URL, EMBEDDING_MODEL, EMBEDDING_QUERY_PREFIX, EMBEDDING_DOC_PREFIX


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


def words(text):
    """Lowercase words, keeping identifiers like _success or mappartitions."""
    return re.findall(r"\w+", text.lower())


def words_without_stopwords(text):
    """Same as words(), without common English words (what, is, the, how...)."""
    return [w for w in words(text) if w not in ENGLISH_STOP_WORDS]


class BM25Retriever:
    """Keyword search: scores chunks by the rare words they share with the question.

    Slides contain few full sentences, so words like "what" or "is" are rare in
    the corpus and BM25 gives them a high weight: removing stopwords fixes that.
    """

    def __init__(self, remove_stopwords):
        self.remove_stopwords = remove_stopwords
        self.name = "BM25 + stopwords" if remove_stopwords else "BM25 (raw)"

    def index(self, chunks):
        preprocess = words_without_stopwords if self.remove_stopwords else words
        self.bm25 = LangchainBM25.from_documents(chunks, preprocess_func=preprocess)

    def search(self, question, k):
        self.bm25.k = k
        return self.bm25.invoke(question)


class HybridRetriever:
    """Combine Dense and BM25 with Reciprocal Rank Fusion (RRF).

    Each chunk gets 1 / (60 + rank) in each list; the scores are added, so a
    chunk ranked well by both retrievers comes first. 60 is the usual RRF constant.
    """
    name = "Hybrid"

    def __init__(self, dense, bm25, candidates=10):
        self.retrievers = [dense, bm25]
        self.candidates = candidates

    def index(self, chunks):
        pass  # uses the two retrievers, already indexed

    def search(self, question, k):
        scores, chunks = {}, {}
        for retriever in self.retrievers:
            for rank, doc in enumerate(retriever.search(question, self.candidates), start=1):
                key = (doc.metadata["file"], doc.metadata["page"], doc.page_content)
                scores[key] = scores.get(key, 0) + 1 / (60 + rank)
                chunks[key] = doc
        best = sorted(scores, key=scores.get, reverse=True)[:k]
        return [chunks[key] for key in best]
