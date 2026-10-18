"""Index a PDF from the command line.

Run from the ESILV_Tutor folder:
    python -m scripts.ingest data/machine_manual.pdf
"""
import logging
import sys

from app.ingestion import compute_file_hash, is_already_indexed, index_pdf

logging.basicConfig(level=logging.INFO)

DEFAULT_PDF_PATH = "data/machine_manual.pdf"


def main():
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PDF_PATH

    with open(pdf_path, "rb") as f:
        file_hash = compute_file_hash(f.read())

    if is_already_indexed(file_hash):
        print(f"{pdf_path} has already been indexed.")
        return

    chunks_indexed = index_pdf(pdf_path, pdf_path, file_hash)
    print(f"Indexed {chunks_indexed} chunks successfully.")


if __name__ == "__main__":
    main()
