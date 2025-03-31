import faiss
import numpy as np
from together import Together
import os
from dotenv import load_dotenv
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

# Load API keys from .env
load_dotenv()
TOGETHER_AI_API_KEY = os.getenv("TOGETHER_AI_API_KEY")

# Ensure API key exists
if not TOGETHER_AI_API_KEY:
    raise ValueError(" Missing TOGETHER_AI_API_KEY! Set it in the .env file.")

# Initialize TogetherAI client
client = Together(api_key=TOGETHER_AI_API_KEY)

# Embedding model from TogetherAI
EMBEDDING_MODEL = "togethercomputer/m2-bert-80M-32k-retrieval"

# FAISS setup
dimension = 768
index = faiss.IndexFlatL2(dimension)
article_store = {}

class StoreLikeInput(BaseModel):
    """Input schema for storing liked articles."""
    article_id: int = Field(..., description="Unique identifier of the article.")
    title: str = Field(..., description="Title of the liked article.")
    description: str = Field(..., description="Short description of the article.")
    url: str = Field(..., description="URL of the article.")

class FindSimilarInput(BaseModel):
    """Input schema for finding similar articles."""
    query_text: str = Field(..., description="Query text for finding similar articles.")
    top_k: int = Field(5, description="Number of similar articles to fetch.")

class StoreLikeTool(BaseTool):
    name: str = "store_like"
    description: str = "Stores liked articles into FAISS for similarity matching."
    args_schema: Type[BaseModel] = StoreLikeInput

    def _run(self, article_id: int, title: str, description: str, url: str):
        embedding = self.get_embedding(title + " " + description)

        if embedding.shape[0] != dimension:
            raise ValueError(f"Embedding size mismatch: Expected {dimension}, got {embedding.shape[0]}")

        index.add(np.array([embedding]))
        article_store[len(article_store)] = {"id": article_id, "title": title, "description": description,"url": url}
        print("🔒 Stored article:", title)

        return f"Article {title} stored successfully!"

    def get_embedding(self, text):
        response = client.embeddings.create(input=[text], model=EMBEDDING_MODEL)
        return np.array(response.data[0].embedding, dtype=np.float32)

class FindSimilarTool(BaseTool):
    name: str = "find_similar"
    description: str = "Finds articles similar to the provided query."
    args_schema: Type[BaseModel] = FindSimilarInput

    def _run(self, query_text: str, top_k: int = 5):
        if index.ntotal == 0:
            return []

        query_embedding = self.get_embedding(query_text)
        _, similar_indices = index.search(np.array([query_embedding]), top_k)

        return [
            {
        "title": article_store[i]["title"],
        "description": article_store[i]["description"],
        "url": article_store[i]["url"]
            }
            for i in similar_indices[0] if i in article_store
        ] 


    def get_embedding(self, text):
        response = client.embeddings.create(input=[text], model=EMBEDDING_MODEL)
        return np.array(response.data[0].embedding, dtype=np.float32)

