"""BM25 (keyword search) and Reciprocal Rank Fusion, shared by the app and the evaluation.

This module never opens Chroma: the evaluation imports it without touching
the app's real chroma_db/ database.
"""
import re

from langchain_community.retrievers import BM25Retriever
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# Usual RRF constant: a high value gives less weight to the first ranks
RRF_K = 60
# Number of chunks taken from each retriever before the fusion
HYBRID_CANDIDATES = 10


def words(text):
    """Lowercase words, keeping identifiers like _success or mappartitions."""
    return re.findall(r"\w+", text.lower())


def words_without_stopwords(text):
    """Same as words(), without common English words (what, is, the, how...)."""
    return [w for w in words(text) if w not in ENGLISH_STOP_WORDS]


def bm25_index(chunks, remove_stopwords=True):
    """Keyword index: scores chunks by the rare words they share with the question.

    Slides contain few full sentences, so words like "what" or "is" are rare in
    the corpus and BM25 gives them a high weight: removing stopwords fixes that.
    """
    preprocess = words_without_stopwords if remove_stopwords else words
    return BM25Retriever.from_documents(chunks, preprocess_func=preprocess)


def reciprocal_rank_fusion(result_lists, key, k):
    """Merge several ranked lists of chunks and return the k best.

    Each chunk gets 1 / (RRF_K + rank) in each list; the scores are added, so a
    chunk ranked well by every retriever comes first. `key(doc)` identifies the
    same chunk in different lists.
    """
    scores, chunks = {}, {}
    for docs in result_lists:
        for rank, doc in enumerate(docs, start=1):
            doc_key = key(doc)
            scores[doc_key] = scores.get(doc_key, 0) + 1 / (RRF_K + rank)
            chunks[doc_key] = doc
    best = sorted(scores, key=scores.get, reverse=True)[:k]
    return [chunks[doc_key] for doc_key in best]
