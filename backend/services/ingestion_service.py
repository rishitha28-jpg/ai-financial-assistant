import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader

class IngestionService:

    def load_documents(self, folder_path):
        documents = []

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)

            if file.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())

            elif file.endswith(".txt"):
                loader = TextLoader(file_path)
                documents.extend(loader.load())

        return documents