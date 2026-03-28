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
        self.db = None
        self.retriever = None

        self.news_service = NewsService()

        if not os.getenv("GROQ_API_KEY"):
            raise ValueError("❌ GROQ_API_KEY missing in .env")

        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-8b-instant",
            temperature=0
        )

        logging.info("✅ RAG initialized")

    # -------------------------------
    # RETRIEVER
    # -------------------------------
    def load_retriever(self):
        try:
            if self.retriever is None:
                self.db = EmbeddingService().load_vector_db()

                self.retriever = self.db.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": 5}
                )

                logging.info("✅ Retriever ready")

        except Exception as e:
            logging.error(f"Vector DB error: {str(e)}")
            self.retriever = None

    # -------------------------------
    # STOCK
    # -------------------------------
    def extract_ticker(self, question):
        match = re.search(r"\b[A-Z]{2,}\.NS\b", question.upper())
        return match.group() if match else None

    def analyze_stock(self, question):
        try:
            ticker = self.extract_ticker(question)

            if not ticker:
                return {"answer": "⚠️ Use format like INFY.NS", "sources": []}

            stock = yf.Ticker(ticker)
            hist = stock.history(period="1mo")

            if hist is None or hist.empty:
                return {"answer": "⚠️ No stock data", "sources": []}

            close = hist["Close"]
            current = close.iloc[-1]
            change = current - close.iloc[0]

            if change > 20:
                trend, signal = "Strong Uptrend 📈", "Strong"
            elif change > 0:
                trend, signal = "Uptrend 📊", "Moderate"
            elif change > -20:
                trend, signal = "Downtrend 📊", "Moderate"
            else:
                trend, signal = "Strong Downtrend 📉", "Weak"

            info = stock.info or {}

            market_cap = info.get("marketCap")
            market_cap = f"₹{market_cap/1e7:.2f} Cr" if market_cap else "N/A"

            return {
                "answer": f"""
📊 Stock Analysis: {ticker}

Current Price: ₹{current:.2f}
Change (1 Month): ₹{change:.2f}
Trend: {trend}

📌 Key Metrics:
- Market Cap: {market_cap}
- PE Ratio: {info.get("trailingPE", "N/A")}
- Sector: {info.get("sector", "N/A")}
- 52W High: {info.get("fiftyTwoWeekHigh", "N/A")}
- 52W Low: {info.get("fiftyTwoWeekLow", "N/A")}

🎯 Investment Signal: {signal}

Reason:
- Based on price trend and momentum
- Market behavior over last 1 month

⚠️ Not financial advice
""",
                "sources": ["yfinance"]
            }

        except Exception as e:
            return {"answer": f"⚠️ Stock error: {str(e)}", "sources": []}

    # -------------------------------
    # NEWS
    # -------------------------------
    def analyze_news(self, question):
        try:
            news = self.news_service.get_news("finance")

            if not news:
                return {"answer": "⚠️ No news found", "sources": []}

            prompt = f"""
Analyze financial news.

News:
{news}

Give:
1. Sentiment per article
2. Key highlights
3. Investment impact
4. Overall sentiment
"""

            response = self.llm.invoke(prompt)
            answer = response.content if hasattr(response, "content") else str(response)

            return {
                "answer": answer,
                "sources": news
            }

        except Exception as e:
            return {"answer": f"⚠️ News error: {str(e)}", "sources": []}

    # -------------------------------
    # RAG (FINAL FIXED)
    # -------------------------------
    def handle_rag(self, question, history):
        try:
            self.load_retriever()

            if not self.retriever:
                return {"answer": "⚠️ Upload documents first", "sources": []}

            docs = self.retriever.invoke(question)

            if not docs:
                return {"answer": "⚠️ No relevant content found", "sources": []}

            if not isinstance(docs, list):
                docs = [docs]

            context = "\n\n".join(doc.page_content for doc in docs)

            if not context.strip():
                return {"answer": "⚠️ Empty document content", "sources": []}

            prompt = f"""
You are a financial analyst.

Answer ONLY from the provided context.

Always follow this structure:

1. Summary
2. Key Insights
3. Risks
4. Recommendation
5. Investment Signal (Strong / Moderate / Weak)

Rules:
- Do NOT skip sections
- Do NOT hallucinate
- Extract as much information as possible from context
- Do NOT say "Not mentioned" unless absolutely no information exists
- Always try to infer insights from numbers (revenue, profit, EPS, growth)
- Investment Signal must ALWAYS be given based on analysis

Context:
{context}

Question:
{question}
"""
            response = self.llm.invoke([
                {
                    "role": "system",
                    "content": "You are a strict financial analyst. Always return full structured output."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ])

            answer = response.content if hasattr(response, "content") else str(response)

            sources = list(set(
                doc.metadata.get("source", "unknown")
                for doc in docs
            ))

            return {
                "answer": answer,
                "sources": sources
            }

        except Exception as e:
            logging.error(f"RAG error: {str(e)}")
            return {"answer": f"⚠️ RAG error: {str(e)}", "sources": []}

    # -------------------------------
    # ROUTER
    # -------------------------------
    def query(self, question, history=None):
        try:
            if not question:
                return {"answer": "⚠️ Empty question", "sources": []}

            if re.search(r"\b[A-Z]{2,}\.NS\b", question.upper()):
                return self.analyze_stock(question)

            if "news" in question.lower():
                return self.analyze_news(question)

            return self.handle_rag(question, history)

        except Exception as e:
            return {"answer": f"⚠️ Internal error: {str(e)}", "sources": []}