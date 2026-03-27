# from fastapi import FastAPI, HTTPException, UploadFile, File
# from backend.models.schema import QueryRequest
# from backend.services.rag_service import RAGService
# import logging
# import shutil
# import os

# # -------------------------------
# # LOGGING CONFIG (INDUSTRY)
# # -------------------------------
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )

# # -------------------------------
# # APP INIT
# # -------------------------------
# app = FastAPI(title="AI Financial Intelligence API")

# rag_service = RAGService()

# # -------------------------------
# # HEALTH CHECK
# # -------------------------------
# @app.get("/health")
# def health():
#     return {"status": "ok"}

# # -------------------------------
# # QUERY ENDPOINT
# # -------------------------------
# @app.post("/query")
# def query(request: QueryRequest):
#     try:
#         if not request.question or not request.question.strip():
#             raise HTTPException(
#                 status_code=400,
#                 detail="Question cannot be empty"
#             )

#         result = rag_service.query(
#             request.question,
#             request.history
#         )

#         return {
#             "status": "success",
#             "data": result
#         }

#     except HTTPException as e:
#         raise e

#     except Exception as e:
#         logging.error(f"Error in /query: {str(e)}")

#         raise HTTPException(
#             status_code=500,
#             detail="Internal Server Error"
#         )

# # -------------------------------
# # 📂 UPLOAD ENDPOINT
# # -------------------------------
# @app.post("/upload")
# def upload_file(file: UploadFile = File(...)):
#     try:
#         # -------------------------------
#         # ✅ VALIDATE FILE TYPE
#         # -------------------------------
#         allowed_types = ["application/pdf", "text/plain"]

#         if file.content_type not in allowed_types:
#             raise HTTPException(
#                 status_code=400,
#                 detail="Only PDF and TXT files are allowed"
#             )

#         # -------------------------------
#         # ✅ CREATE DIRECTORY
#         # -------------------------------
#         upload_dir = "data/reports"
#         os.makedirs(upload_dir, exist_ok=True)

#         file_path = os.path.join(upload_dir, file.filename)

#         # -------------------------------
#         # ✅ SAVE FILE
#         # -------------------------------
#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         logging.info(f"File uploaded: {file.filename}")

#         # -------------------------------
#         # 🔥 REBUILD VECTOR DB
#         # -------------------------------
#         from backend.services.pipeline import run_pipeline
#         run_pipeline()

#         logging.info("Vector DB updated after upload")

#         return {
#             "status": "success",
#             "message": f"{file.filename} uploaded and processed successfully"
#         }

#     except HTTPException as e:
#         raise e

#     except Exception as e:
#         logging.error(f"Upload error: {str(e)}")

#         raise HTTPException(
#             status_code=500,
#             detail="Upload failed. Check logs."
#         )
from fastapi import FastAPI, HTTPException, UploadFile, File
from backend.models.schema import QueryRequest
from backend.services.rag_service import RAGService
from backend.utils.logger import logger
import shutil
import os

# -------------------------------
# APP INIT
# -------------------------------
app = FastAPI(title="AI Financial Intelligence API")

rag_service = RAGService()

# -------------------------------
# STARTUP LOG
# -------------------------------
@app.on_event("startup")
def startup_event():
    logger.info("🚀 Backend started")

# -------------------------------
# HEALTH CHECK
# -------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -------------------------------
# QUERY ENDPOINT
# -------------------------------
@app.post("/query")
def query(request: QueryRequest):
    try:
        if not request.question or not request.question.strip():
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty"
            )

        logger.info(f"🧠 Query: {request.question}")

        result = rag_service.query(
            request.question,
            request.history
        )

        return {
            "status": "success",
            "data": result
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"❌ Error in /query: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

# -------------------------------
# 📂 UPLOAD ENDPOINT
# -------------------------------
@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    try:
        allowed_types = ["application/pdf", "text/plain"]

        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail="Only PDF and TXT files are allowed"
            )

        upload_dir = "data/reports"
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"📄 File uploaded: {file.filename}")

        from backend.services.pipeline import run_pipeline
        run_pipeline()

        logger.info("✅ Vector DB updated after upload")

        return {
            "status": "success",
            "message": f"{file.filename} uploaded and processed successfully"
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"❌ Upload error: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Upload failed. Check logs."
        )