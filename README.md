# 🚀 AI Financial Intelligence Platform (RAG + GenAI)

## 📌 Overview

This project is an industry-level AI system that analyzes financial documents and provides intelligent insights using **Retrieval-Augmented Generation (RAG)**.

Unlike basic stock apps, this system focuses on:

* Understanding financial reports
* Providing explainable insights
* Answering investment-related queries

---

## 🧠 Key Features

* 📄 Financial Document Analysis (PDF/TXT)
* 🔍 RAG-based intelligent retrieval
* 📊 Risk assessment (Low / Medium / High)
* 💬 Conversational AI assistant
* 📚 Source-backed responses (no hallucination)
* ⚡ FastAPI backend (production-ready)
* 🎯 Streamlit frontend (interactive UI)

---

## 🏗️ Architecture

```
Streamlit (Frontend)
        ↓
FastAPI (Backend API)
        ↓
LangChain RAG Pipeline
        ↓
FAISS Vector Database
        ↓
Financial Reports / Data
```

---

## 📁 Project Structure

```
ai-finance-rag/
│
├── backend/
│   ├── api/
│   ├── services/
│   ├── core/
│   ├── models/
│   ├── utils/
│
├── frontend/
│   └── app.py
│
├── data/
│   ├── reports/
│   ├── news/
│
├── vector_db/
├── logs/
├── .env
├── requirements.txt
├── Dockerfile
├── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```
git clone https://github.com/your-username/ai-finance-rag.git
cd ai-finance-rag
```

---

### 2️⃣ Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 4️⃣ Add Environment Variables

Create `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

---

### 5️⃣ Add Data

Place your files inside:

```
data/reports/
```

Example:

* financial reports
* company analysis documents

---

### 6️⃣ Run Data Pipeline (Create Vector DB)

```
python -m backend.services.pipeline
```

---

### 7️⃣ Start Backend

```
uvicorn backend.api.main:app --reload
```

---

### 8️⃣ Start Frontend

```
streamlit run frontend/app.py
```

---

## 🎯 Example Queries

* "Summarize the financial report"
* "What are the risks in this company?"
* "Should I invest in this company?"
* "Give investment insights based on report"

---

## 🧠 How It Works

1. Documents are loaded and split into chunks
2. Embeddings are created using OpenAI
3. Stored in FAISS vector database
4. User query → retrieves relevant chunks
5. LLM generates answer with context

---

## 🚀 Future Enhancements

* 📈 Real-time stock data integration (`yfinance`)
* 📰 News sentiment analysis
* 📊 Portfolio analysis dashboard
* 🔐 User authentication
* ☁️ Deployment (AWS / Docker / CI-CD)

---

## 💡 Tech Stack

* Python
* FastAPI
* Streamlit
* LangChain
* FAISS (Vector DB)
* OpenAI API
* Docker

---

## 📌 Resume Description

> Built an AI-powered Financial Intelligence Platform using LangChain, RAG, FastAPI, and Streamlit to analyze financial documents and generate explainable investment insights with vector database retrieval.

---

## 👨‍💻 Author

Your Name
GitHub: https://github.com/your-username

---
