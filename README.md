# AI Agent for News Recommendation

This project is a personalized news recommendation system powered by a single AI agent built using the [CrewAI](https://github.com/joaomdmoura/crewai) framework. The agent analyses user preferences and recommends relevant news articles based on liked content.

---

# What It Does

- Fetches real-time news via NewsAPI
- Stores liked articles using FAISS vector similarity
- Recommends similar articles based on embeddings
- Uses GPT-3.5 Turbo from OpenAI for reasoning
- Embeddings generated using TogetherAI

---

##  Structure

NewsRecommenderAI/
├── agents/ # AI agent logic
├── tools/ # News fetcher and vector DB
├── ui/ # (Optional) Streamlit UI
├── .env # API keys (gitignored)
└── app.py # Main script


---

# Features

- ✅ Real-time news retrieval
- ✅ Vector-based article matching
- ✅ Like-based preference learning
- ✅ Human-like recommendations using LLMs
- ✅ Simple and modular agent structure

---

# Environment Variables

To run this project, create a `.env` file in the root directory with the following keys:

```env
NEWS_API_KEY=your_newsapi_key
TOGETHER_AI_API_KEY=your_togetherai_key
OPENAI_API_KEY=your_openai_key

These are automatically loaded via dotenv.

# Future Improvements

-Build a full UI with Streamlit
-Implement feedback-based reinforcement learning
-Upgrade to multi-agent setup for richer capabilities
-Test different embedding models and news sources

👩‍🏫 Academic Note
This project was developed as part of an academic case study to explore AI agents and real-world applications of autonomous systems in personalised content delivery.




