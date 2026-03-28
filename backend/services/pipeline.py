from backend.services.ingestion_service import IngestionService
from backend.services.embedding_service import EmbeddingService
from langchain_text_splitters import RecursiveCharacterTextSplitter


def run_pipeline():
    print("🚀 Starting ingestion pipeline...")

    # -------------------------------
    # LOAD DOCUMENTS
    # -------------------------------
    ingestor = IngestionService()
    docs = ingestor.load_documents("data/reports")

    if not docs:
        print("❌ No documents found. Check your folder.")
        return

    print(f"📄 Loaded {len(docs)} documents")

    # -------------------------------
    # SPLIT DOCUMENTS (FIXED 🔥)
    # -------------------------------
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,        # ✅ better context
        chunk_overlap=150      # ✅ preserves meaning
    )

    chunks = splitter.split_documents(docs)

    if not chunks:
        print("❌ No chunks created.")
        return

    print(f"🔹 Created {len(chunks)} chunks")

    # -------------------------------
    # EMBEDDING + VECTOR DB
    # -------------------------------
    embedder = EmbeddingService()
    embedder.create_vector_db(chunks)

    print("✅ Vector DB created successfully!")


if __name__ == "__main__":
    run_pipeline()