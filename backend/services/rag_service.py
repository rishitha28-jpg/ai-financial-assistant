from langchain_groq import ChatGroq
from backend.services.embedding_service import EmbeddingService
from backend.services.news_service import NewsService
import os
from dotenv import load_dotenv
import logging
import yfinance as yf
import re

load_dotenv()


class RAGService:
    def __init__(self):
        try:
            self.db = EmbeddingService().load_vector_db()
            self.retriever = self.db.as_retriever(search_kwargs={"k": 5})
        except Exception as e:
            logging.error(f"Vector DB load failed: {str(e)}")
            self.db = None
            self.retriever = None

        self.news_service = NewsService()

        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-8b-instant",
            temperature=0
        )

        logging.info("✅ RAG Service initialized")

    # -------------------------------
    # 🔍 TICKER EXTRACTION (FIXED)
    # -------------------------------
    def extract_ticker(self, question):
        question = question.upper()

        # ✅ Indian stocks
        match = re.search(r"\b[A-Z]{2,}\.NS\b", question)
        if match:
            return match.group()

        # ✅ Optional US stocks (strict)
        match = re.search(r"\b[A-Z]{2,5}\b", question)
        if match:
            ticker = match.group()

            blacklist = {
                "WHAT", "THIS", "THAT", "SHOULD",
                "INVEST", "ANALYZE", "SHOW", "NEWS",
                "LATEST", "PRICE", "TREND", "RISKS",
                "SUMMARY", "SUMMARIZE", "REPORT",
                "THE", "AND", "FOR", "WITH"
            }

            if ticker in blacklist:
                return None

            # Only allow if clearly stock intent
            if ".NS" not in question and "stock" not in question.lower():
                return None

            return ticker

        return None

    # -------------------------------
    # 📊 STOCK ANALYSIS
    # -------------------------------
    def analyze_stock(self, question):
        try:
            ticker = self.extract_ticker(question)

            if not ticker:
                return {"answer": "⚠️ Mention stock like INFY.NS", "sources": []}

            stock = yf.Ticker(ticker)
            hist = stock.history(period="1mo")

            if hist is None or hist.empty:
                return {"answer": f"⚠️ No stock data for {ticker}", "sources": ["yfinance"]}

            close = hist["Close"].dropna()

            current_price = close.iloc[-1]
            change = current_price - close.iloc[0]

            if change > 20:
                trend = "Strong Uptrend 📈"
                signal = "Strong 📈"
            elif change > 0:
                trend = "Mild Uptrend 📊"
                signal = "Moderate 📊"
            elif change > -20:
                trend = "Mild Downtrend 📊"
                signal = "Moderate 📊"
            else:
                trend = "Strong Downtrend 📉"
                signal = "Weak 📉"

            info = stock.info

            market_cap = info.get("marketCap")
            if market_cap:
                market_cap = f"₹{market_cap/1e7:.2f} Cr"
            else:
                market_cap = "N/A"

            return {
                "answer": f"""
📊 Stock Analysis: {ticker}

Current Price: ₹{current_price:.2f}
Change (1 Month): ₹{change:.2f}
Trend: {trend}

📌 Key Metrics:
- Market Cap: {market_cap}
- PE Ratio: {info.get("trailingPE", "N/A")}
- Sector: {info.get("sector", "N/A")}

🎯 Investment Signal: {signal}

⚠️ Not financial advice.
""",
                "sources": ["yfinance"]
            }

        except Exception as e:
            logging.error(f"Stock error: {str(e)}")
            return {"answer": "⚠️ Stock error", "sources": []}

    # -------------------------------
    # 📰 NEWS
    # -------------------------------
    def analyze_news(self, question):
        try:
            news = self.news_service.get_news("finance")

            if not news:
                return {"answer": "⚠️ No news found", "sources": []}

            response = self.llm.invoke(f"""
Analyze sentiment:

{news}

Give:
1. Sentiment
2. Highlights
3. Investment impact
""")

            return {"answer": response.content, "sources": news}

        except Exception as e:
            logging.error(f"News error: {str(e)}")
            return {"answer": "⚠️ News error", "sources": []}

    # -------------------------------
    # 🧠 RAG
    # -------------------------------
    def handle_rag(self, question, history):
        try:
            if not self.retriever:
                return {"answer": "⚠️ Upload documents first", "sources": []}

            docs = self.retriever.invoke(question)

            context = "\n".join(set([doc.page_content for doc in docs]))

            prompt = f"""
You are a STRICT financial analyst.

Rules:
- Use ONLY the given context
- Do NOT hallucinate
- If not present → say "Not mentioned in report"

Context:
{context}

Question:
{question}

Answer format:
1. Summary
2. Key Insights
3. Risks
4. Recommendation
5. Investment Signal (Strong/Moderate/Weak)
"""

            response = self.llm.invoke(prompt)

            return {
                "answer": response.content,
                "sources": list({
                    doc.metadata.get("source"): doc.metadata
                    for doc in docs
                }.values())
            }

        except Exception as e:
            logging.error(f"RAG error: {str(e)}")
            return {"answer": "⚠️ RAG error", "sources": []}

    # -------------------------------
    # 🚦 ROUTER
    # -------------------------------
    def query(self, question, history=None):
        try:
            q = question.lower()

            ticker = self.extract_ticker(question)

            if ticker:
                return self.analyze_stock(question)

            if "news" in q:
                return self.analyze_news(question)

            return self.handle_rag(question, history)

        except Exception as e:
            logging.error(f"Query error: {str(e)}")
            return {"answer": "⚠️ Internal error", "sources": []}