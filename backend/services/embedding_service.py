from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os
from dotenv import load_dotenv

# -------------------------------
# 🔥 ADD THIS (TIMEOUT FIX)
# -------------------------------
os.environ["HF_HUB_TIMEOUT"] = "60"   # increase timeout (important)

# Load environment variables
load_dotenv()


class EmbeddingService:

    def __init__(self):
        # ✅ Use environment variable (industry practice)
        self.vector_db_path = os.getenv("VECTOR_DB_PATH", "vector_db")

    def create_vector_db(self, documents):
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-MiniLM-L3-v2",
            model_kwargs={"device": "cpu"}
        )

        db = FAISS.from_documents(documents, embeddings)

        # ✅ Save using configurable path
        db.save_local(self.vector_db_path)

    def load_vector_db(self):
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-MiniLM-L3-v2",
            model_kwargs={"device": "cpu"}
        )

        return FAISS.load_local(
            self.vector_db_path,
            embeddings,
            allow_dangerous_deserialization=True
        )