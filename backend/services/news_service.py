from newsapi import NewsApiClient
import os
from dotenv import load_dotenv

load_dotenv()


class NewsService:

    def __init__(self):
        self.client = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

    def get_news(self, query="finance"):
        try:
            articles = self.client.get_everything(
                q="stock market OR economy OR business OR finance",
                language="en",
                sort_by="relevancy",
                page_size=10   # ✅ more articles
            )

            # ✅ FILTER RELEVANT NEWS
            filtered_articles = []
            keywords = ["stock", "market", "finance", "economy", "business", "earnings"]

            for a in articles["articles"]:
                title = (a.get("title") or "").lower()
                description = (a.get("description") or "").lower()

                if any(k in title or k in description for k in keywords):
                    # ✅ return richer content (title + description)
                    text = f"{a.get('title')} - {a.get('description')}"
                    filtered_articles.append(text)

            # ✅ fallback if nothing filtered
            if not filtered_articles:
                filtered_articles = [
                    f"{a.get('title')} - {a.get('description')}"
                    for a in articles["articles"][:5]
                ]

            return filtered_articles[:5]

        except Exception as e:
            print("News error:", e)
            return []