from langchain_core.embeddings import Embeddings
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
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
