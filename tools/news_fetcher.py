from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import requests
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

class NewsFetcherInput(BaseModel):
    """Input schema for NewsFetcherTool."""
    query: str = Field(..., description="Topic or keyword for fetching news articles.")

class NewsFetcherTool(BaseTool):
    name: str = "news_fetcher"
    description: str = "Fetches news articles from NewsAPI based on a given query."
    args_schema: Type[BaseModel] = NewsFetcherInput

    def _run(self, query: str):
        """Fetches news articles related to the given query."""
        if not NEWS_API_KEY:
            raise ValueError(" Missing NEWS_API_KEY! Please set it in the .env file.")

        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}"
        response = requests.get(url)

        if response.status_code != 200:
            return f"Error fetching news: {response.text}"

        articles = response.json().get("articles", [])

        return [
            {
                "title": article["title"],
                "url": article["url"],
                "description": article.get("description", "No description available."),
                "image": article.get("urlToImage", ""),
            }
            for article in articles
        ]



#curl "https://newsapi.org/v2/everything?q=AI&apiKey=66ec8ada30374e78b5822eaa38d72473" ---- debugging ignore
