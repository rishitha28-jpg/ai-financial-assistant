from fastapi import FastAPI, HTTPException, UploadFile, File
from backend.models.schema import QueryRequest
from backend.services.rag_service import RAGService
from backend.utils.logger import logger
import shutil
import os
import threading

app = FastAPI(title="AI Financial Intelligence API")

rag_service = None


# -------------------------------
# STARTUP
# -------------------------------
@app.on_event("startup")
def startup_event():
    global rag_service
    print("🚀 Backend starting...")
    rag_service = RAGService()
    logger.info("🚀 Backend started")


# -------------------------------
# ROOT
# -------------------------------
@app.get("/")
def root():
    return {"message": "AI Financial API running"}


# -------------------------------
# HEALTH
# -------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# -------------------------------
# QUERY
# -------------------------------
@app.post("/query")
def query(request: QueryRequest):
    try:
        if rag_service is None:
            raise HTTPException(500, "Service not initialized")

        if not request.question or not request.question.strip():
            raise HTTPException(400, "Question cannot be empty")

        logger.info(f"🧠 Query: {request.question}")

        result = rag_service.query(
            request.question,
            request.history
        ) or {}

        answer = result.get("answer") or "⚠️ No response generated"
        sources = result.get("sources") or []

        return {
            "status": "success",
            "data": {
                "answer": answer,
                "sources": sources
            }
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        raise HTTPException(500, "Internal Server Error")


# -------------------------------
# UPLOAD
# -------------------------------
@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    try:
        if file.content_type not in ["application/pdf", "text/plain"]:
            raise HTTPException(400, "Only PDF and TXT allowed")

        os.makedirs("data/reports", exist_ok=True)
        file_path = os.path.join("data/reports", file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"📄 Uploaded: {file.filename}")

        # ✅ Run pipeline in background
        from backend.services.pipeline import run_pipeline
        threading.Thread(target=run_pipeline).start()

        logger.info("✅ Vector DB update started")

        return {
            "status": "success",
            "message": f"{file.filename} uploaded successfully"
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"❌ Upload error: {str(e)}")
        raise HTTPException(500, "Upload failed")