# 🤖 AI Financial Assistant

An end-to-end AI-powered financial assistant that combines Retrieval-Augmented Generation (RAG), real-time stock analysis, and financial news sentiment analysis into a single intelligent system.

---

## 🚀 Features

### 📄 Financial Report Analysis (RAG)
- Upload PDF/TXT financial reports
- Extract insights using LLM + vector database
- Provides:
  - Summary
  - Key insights
  - Risks
  - Investment recommendation

---

### 📊 Real-Time Stock Analysis
- Fetches live stock data using yfinance
- Supports Indian stocks (e.g., INFY.NS, TCS.NS)
- Outputs:
  - Current price
  - Monthly trend
  - Key metrics (PE, Market Cap, Sector)
  - Investment signal (Strong / Moderate / Weak)

---

### 📰 Financial News Sentiment Analysis
- Fetches latest finance-related news using News API
- Filters relevant business/economic articles
- Generates:
  - Sentiment (Positive / Negative / Neutral)
  - Highlights
  - Investment impact
  - Overall market sentiment

---

### 🧠 Intelligent Query Routing
- Automatically detects user intent:
  - Stock queries → Stock module
  - Report queries → RAG pipeline
  - News queries → News service
- Ensures accurate and relevant responses

---

## 🏗️ Tech Stack

Backend:
- FastAPI
- LangChain
- FAISS (Vector Database)
- OpenAI API

Frontend:
- Streamlit

Data Sources:
- yfinance (Stock data)
- NewsAPI (Financial news)

---

## 📂 Project Structure

ai_project/

backend/
- api/
- services/
- pipeline/
- config/

frontend/
- app.py

data/
- reports/

requirements.txt
README.md

---

## ⚙️ Installation

git clone https://github.com/your-username/ai-financial-assistant.git  
cd ai-financial-assistant  

python -m venv venv  
venv\Scripts\activate  

pip install -r requirements.txt  

---

## 🔑 Environment Variables

Create a .env file and add:

OPENAI_API_KEY=your_openai_key  
NEWS_API_KEY=your_news_api_key  

---

## ▶️ Run Locally

Backend:

uvicorn backend.api.main:app --reload  

Frontend:

streamlit run frontend/app.py  

---

## 🌐 Deployment

Backend:
- Render  

Frontend:
- Streamlit Cloud  

---

## 🧪 Example Queries

- Analyze INFY.NS  
- Should I invest in TCS.NS?  
- Summarize this report  
- What are the risks?  
- Show latest news  

---

## 🧠 Key Highlights

- Multi-modal AI system (RAG + API + LLM)
- Real-time financial data integration
- Explainable investment insights
- Clean and interactive UI

---

## 📌 Future Improvements

- Stock comparison (INFY vs TCS)
- Advanced financial ratios
- Portfolio recommendations
- Trend prediction using ML


