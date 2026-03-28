# 🤖 AI Financial Intelligence Platform

An **industry-grade AI-powered financial assistant** that integrates **Retrieval-Augmented Generation (RAG), real-time stock analysis, and financial news intelligence** into a unified system.

🔗 **Live Backend API:**
https://ai-financial-assistant-i3l8.onrender.com

---

## 🚀 Overview

This project is designed to simulate a **real-world financial intelligence system** used in fintech and investment firms.

It enables users to:

* Analyze financial reports (PDF/TXT)
* Evaluate stock performance
* Understand market sentiment from news
* Get structured, explainable investment insights

---

## ✨ Core Features

### 📄 Financial Report Analysis (RAG)

* Upload PDF/TXT financial documents
* Uses **vector database (FAISS) + LLM**
* Extracts structured insights:

✅ Summary
✅ Key Insights
✅ Risks
✅ Recommendation
✅ Investment Signal

---

### 📊 Real-Time Stock Analysis

* Live stock data via `yfinance`
* Supports Indian market (e.g., `INFY.NS`, `TCS.NS`)

Provides:

* 💰 Current Price
* 📉 Monthly Trend
* 📌 Key Metrics (PE, Market Cap, Sector, 52W High/Low)
* 🎯 Investment Signal (Strong / Moderate / Weak)

---

### 📰 Financial News Sentiment Analysis

* Integrated with NewsAPI
* AI-powered sentiment classification

Outputs:

* Sentiment per article
* Key highlights
* Investment impact
* Overall market sentiment

---

### 🧠 Intelligent Query Routing

Automatically detects user intent:

| Query Type     | Routed To        |
| -------------- | ---------------- |
| Stock queries  | 📊 Stock Engine  |
| Report queries | 📄 RAG Pipeline  |
| News queries   | 📰 News Analyzer |

---

## 🏗️ Architecture

```
User (Streamlit UI)
        ↓
FastAPI Backend (Router)
        ↓
-----------------------------------
| Stock | RAG | News |
-----------------------------------
        ↓
LLM (Groq - LLaMA 3)
        ↓
Response (Structured Output)
```

---

## 🛠️ Tech Stack

### Backend

* FastAPI
* LangChain
* FAISS (Vector DB)
* Groq (LLaMA 3 LLM)

### Frontend

* Streamlit

### Data Sources

* yfinance (Stock Data)
* NewsAPI (Financial News)

---

## 📂 Project Structure

```
ai-financial-assistant/

backend/
│
├── api/              # FastAPI endpoints
├── services/         # RAG, Stock, News logic
├── models/           # Request schema
├── utils/            # Logger & config
│
frontend/
├── app.py            # Streamlit UI
│
data/
├── reports/          # Uploaded documents
│
requirements.txt
README.md
```

---

## ⚙️ Installation

```bash
git clone https://github.com/rishitha28-jpg/ai-financial-assistant.git
cd ai-financial-assistant

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create `.env` file:

```
GROQ_API_KEY=your_groq_api_key
NEWS_API_KEY=your_news_api_key
```

---

## ▶️ Run Locally

### Backend

```bash
uvicorn backend.api.main:app --reload
```

### Frontend

```bash
streamlit run frontend/app.py
```

---

## 🌐 Deployment

### 🚀 Backend (Render)

* Hosted on Render
* Auto-deploy from GitHub

### 🎨 Frontend (Streamlit Cloud)

* Connect GitHub repo
* Select `frontend/app.py`

---

## 🧪 Example Queries

Try these:

```
Analyze INFY.NS
Should I invest in TCS.NS?
Summarize this report
What are the risks?
Show latest news
```

---

## 🧠 Key Highlights

✔ End-to-end GenAI system (RAG + APIs + LLM)
✔ Real-time financial data integration
✔ Structured & explainable outputs
✔ Modular microservice-like architecture
✔ Production-ready backend (FastAPI)
✔ Scalable vector search (FAISS)

---

## 📈 Future Enhancements

* 📊 Stock comparison (INFY vs TCS)
* 📉 Advanced financial ratios (ROE, EBITDA)
* 💼 Portfolio recommendation system
* 🤖 ML-based trend prediction
* 🌍 Multi-market support (US, EU)

