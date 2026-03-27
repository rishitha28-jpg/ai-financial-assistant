from backend.services.ingestion_service import IngestionService
from backend.services.embedding_service import EmbeddingService
from langchain_text_splitters import RecursiveCharacterTextSplitter


def run_pipeline():
    ingestor = IngestionService()

    docs = ingestor.load_documents("data/reports")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,   # optimized for your system
        chunk_overlap=50
    )

    chunks = splitter.split_documents(docs)

    embedder = EmbeddingService()
    embedder.create_vector_db(chunks)

    print("✅ Vector DB created successfully!")


if __name__ == "__main__":
    run_pipeline()