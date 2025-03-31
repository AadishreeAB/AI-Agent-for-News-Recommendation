from crewai import Agent, Task, Crew, LLM
from tools import NewsFetcherTool, StoreLikeTool, FindSimilarTool
import os
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ensure API key exists
if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY! Please set it in the .env file.")

# Initialize OpenAI LLM
openai_llm = LLM(
    
    api_key=OPENAI_API_KEY,
    model="openai/gpt-3.5-turbo",
    temperature=0.7 
)




# Initialize tools
fetch_news_tool = NewsFetcherTool()
store_like_tool = StoreLikeTool()
find_similar_tool = FindSimilarTool()

# Define the Agent
news_agent = Agent(
    role="Specialized News Recommender",
    goal="Provide a mix of personalized and fresh news recommendations.",
    backstory="You are a smart assistant that understands user preferences from liked articles, "
        "and combines them with the latest headlines using NewsAPI. You ensure the user "
        "gets a 90 percent match to their taste and 10 percent diverse new stories.",
    tools=[ fetch_news_tool, find_similar_tool, store_like_tool],
    verbose=True,
    allow_delegation=False,
    memory=False,  # disable ChromaDB
    llm=openai_llm  # assign openai llm
)

# # Define the Task
# news_task = Task(
#     description=(
#         f"Based on the following liked article titles: {st.session_state.liked_articles}, "
#         "Make sure 90 percent are highly relevant and 10 percent offer new perspectives. Don't repeat old articles."
#     ),
#     expected_output="A list of recommended articles with reasoning.",
#     agent=news_agent
# )

# # Setup the Crew
# news_crew = Crew(
#     agents=[news_agent],
#     tasks=[news_task],
#     verbose=True
# )

# # Run the Agent Crew
# if __name__ == "__main__":
#     print("\n Running News Recommendation Agent...\n")
#     result = news_crew.kickoff()

#     if result:
#         print("\n📰 Recommended News:\n")
#         print(result)
#     else:
#         print("\n⚠ No recommendations found.")


