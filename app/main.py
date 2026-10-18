from fastapi import FastAPI, HTTPException, UploadFile, File
import os
import logging
import tempfile

from app.schemas import QuestionRequest
from app.ingestion import compute_file_hash, is_already_indexed, index_pdf
from app.retriever import format_docs, extract_sources
from app.courses import list_courses, retrieve_documents_for_course
from app.conversation import condense_question
from app.generation import generate_answer


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

app = FastAPI()


# -------------------------
# API endpoints
# -------------------------

@app.get("/")
def home():
    return {"message": "RAG API is running"}


@app.get("/courses")
def get_courses():
    return {"courses": list_courses()}



@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    temp_path = None

    try:
        # 1. Read uploaded file
        content = await file.read()
        file_hash = compute_file_hash(content)

        if is_already_indexed(file_hash):
            return {
                "filename": file.filename,
                "message": "This PDF has already been indexed.",
                "chunks_indexed": 0
            }
        if not content.startswith(b"%PDF-"):
            raise HTTPException(
                status_code=400,
                detail="Invalid PDF file."
            )

        # 2. Save temporarily so PyPDFLoader can read it
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name

        # 3. Load, split and store in Chroma
        chunks_indexed = index_pdf(temp_path, file.filename, file_hash)

        return {
            "filename": file.filename,
            "chunks_indexed": chunks_indexed,
            "message": "Document indexed successfully."
        }

    except HTTPException:
        raise

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception:
        logger.exception("Document upload failed")
        raise HTTPException(
            status_code=500,
            detail="Document processing failed."
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        await file.close()


@app.post("/ask")
def ask_question(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )
    try:
        logger.info("Received a question (course: %s)", request.course or "all")

        # 0. Follow-up questions are rewritten using the conversation history
        standalone_question = condense_question(question, request.history)
        if standalone_question != question:
            logger.info("Standalone question: %s", standalone_question)

        # 1. Retrieval: find the most relevant chunks (in one course or in all)
        retrieved_docs = retrieve_documents_for_course(standalone_question, request.course)
        logger.info("Retrieved %d documents", len(retrieved_docs))

        # 2. Build the context for the LLM
        context = format_docs(retrieved_docs)
        logger.info("Context sent to LLM:\n%s", context)

        # 3. Generation: ask the LLM to answer
        answer = generate_answer(context, standalone_question)
        sources = extract_sources(retrieved_docs)

        logger.info("Generated RAG response")

        return {
            "question": question,
            "standalone_question": standalone_question,
            "answer": answer,
            "sources": sources
        }
    except Exception:
        logger.exception("RAG request failed")

        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the question."
        )
