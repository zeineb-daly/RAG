import hashlib
import logging
import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import CHUNK_SIZE, CHUNK_OVERLAP
from app.retriever import vectorstore

logger = logging.getLogger(__name__)


def compute_file_hash(content):
    return hashlib.sha256(content).hexdigest()


def is_already_indexed(file_hash):
    existing = vectorstore.get(
        where={"file_hash": file_hash},
        limit=1
    )
    return bool(existing["ids"])


def extract_document_title(documents, filename):
    if not documents:
        return filename

    first_page = documents[0].page_content

    for line in first_page.splitlines():
        title = line.strip()

        if title:
            return title[:150]

    return filename


def index_pdf(pdf_path, filename, file_hash):
    """Load a PDF, split it into chunks and store them in Chroma.

    Returns the number of chunks indexed.
    Raises ValueError if the PDF contains no readable text.
    """
    # 1. Load PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    if not documents:
        raise ValueError("No readable pages found.")

    document_title = extract_document_title(documents, filename)
    logger.info("Extracted document title: %s", document_title)

    # Keep the original filename in metadata
    for doc in documents:
        doc.metadata["source"] = os.path.basename(filename)

    # 2. Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(documents)

    if not chunks:
        raise ValueError("No readable text found.")

    for chunk in chunks:
        chunk.metadata["file_hash"] = file_hash

    # 3. Generate embeddings and store in Chroma
    vectorstore.add_documents(chunks)

    logger.info("Indexed %d chunks from %s", len(chunks), filename)

    return len(chunks)
