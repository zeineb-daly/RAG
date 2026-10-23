"""Load the course PDFs and split them into chunks, exactly like the app."""
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import CHUNK_SIZE, CHUNK_OVERLAP

COURSES_DIR = Path(__file__).parent.parent.parent / "data" / "courses"


def load_chunks(courses_dir=COURSES_DIR):
    """Return the chunks of every PDF, with `file` and 1-based `page` metadata."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = []
    for pdf in sorted(Path(courses_dir).glob("*.pdf")):
        pages = PyPDFLoader(str(pdf)).load()
        for doc in splitter.split_documents(pages):
            # PyPDFLoader stores a 0-based page index
            doc.metadata = {"file": pdf.name, "page": doc.metadata.get("page", 0) + 1}
            chunks.append(doc)
    return chunks
