import sys
import os
import random
import streamlit as st

# Ensure root folder access
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.news_fetcher import NewsFetcherTool
from tools.vector_db import StoreLikeTool
#from agents.news_agent import news_crew  # Agent logic import
from crewai import Agent, Task, Crew
from agents.news_agent import news_agent  # Make sure this is defined in news_agent.py


# Set page config
st.set_page_config(page_title="AI News Recommender", layout="centered")

# Initialize tools
fetch_tool = NewsFetcherTool()
like_tool = StoreLikeTool()

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "category"
if "liked_articles" not in st.session_state:
    st.session_state.liked_articles = []
if "selected_categories" not in st.session_state:
    st.session_state.selected_categories = []

# PAGE 1: Category Selection

if st.session_state.page == "category":
    st.title("🧠 Personalized News Recommendation Agent")

    st.subheader("Step 1: Choose Your News Interests")

    selected = st.multiselect(
        "Pick 3 categories you’re most interested in:",
        ["sports", "politics", "entertainment", "health", "technology", "business", "science"],
        default=st.session_state.selected_categories,
        max_selections=3,
    )

    if len(selected) == 3:
        if st.button("Continue to News Feed"):
            st.session_state.selected_categories = selected
            st.session_state.page = "feed"
            st.rerun()

    elif len(selected) > 3:
        st.error("Please select only 3 categories.")


# PAGE 2: News Feed

# elif st.session_state.page == "feed":
#     st.title("\U0001F5DE️ Your News Feed")
#     st.subheader("Click ❤️ to like articles")

#     for category in st.session_state.selected_categories:
#         st.markdown(f"### 🔍 {category.title()} News")
#         results = fetch_tool._run(category)

#         if not results:
#             st.warning(f"No articles found for {category}.")
#             continue

#         for article in random.sample(results, min(2, len(results))):
#             with st.container():
#                 st.markdown(f"**{article['title']}**")
#                 if article["image"]:
#                  st.image(article["image"], use_container_width=True)
#                  st.markdown(article["description"])
#                  st.markdown(f"[\U0001F517 Read more]({article['url']})")

#                 if st.button("❤️ Like", key=f"like_{article['url']}"):
#                     article_id = hash(article["url"]) % 10**8
#                     like_tool._run(
#                         article_id=article_id,
#                         title=article["title"],
#                         description=article["description"],
#                         url=article["url"]
#                     )
#                     st.success("Article liked!")
                    
#                     st.session_state.liked_articles.append(article["title"])

#                     st.write("DEBUG: Article liked:", article["title"])

#                     st.rerun()

#     if st.button("✨ Get AI Recommendations"):
#         st.session_state.page = "recommendations"
#         st.rerun()

elif st.session_state.page == "feed":
    st.title("\U0001F5DE️ Your News Feed")
    st.subheader("Click ❤️ to like articles")

    for category in st.session_state.selected_categories:
        st.markdown(f"### 🔍 {category.title()} News")
        results = fetch_tool._run(category)

        if not results:
            st.warning(f"No articles found for {category}.")
            continue

        # ✅ NEW: Cache articles per category to avoid re-randomizing on rerun
        if f"{category}_articles" not in st.session_state:
            st.session_state[f"{category}_articles"] = random.sample(results, min(2, len(results)))

        # ✅ Use cached article list
        for article in st.session_state[f"{category}_articles"]:
            with st.container():
                st.markdown(f"**{article['title']}**")
                if article["image"]:
                    st.image(article["image"], use_container_width=True)
                st.markdown(article["description"])
                st.markdown(f"[\U0001F517 Read more]({article['url']})")

                if st.button("❤️ Like", key=f"like_{article['url']}"):
                    article_id = hash(article["url"]) % 10**8
                    like_tool._run(
                        article_id=article_id,
                        title=article["title"],
                        description=article["description"],
                        url=article["url"]
                    )
                    st.success("Article liked!")

                    st.session_state.liked_articles.append(article["title"])
                    st.write("DEBUG: Article liked:", article["title"])
                    st.rerun()

    if st.button("✨ Get AI Recommendations"):
        st.session_state.page = "recommendations"
        st.rerun()


# PAGE 3: AI Recommendations

elif st.session_state.page == "recommendations":
    st.title("🤖 AI News Recommendations")
    st.subheader("Based on your likes, here’s what our AI recommends:")

    st.write("DEBUG: Liked Articles")
    st.json(st.session_state.liked_articles)  # Debug display

    if len(st.session_state.liked_articles) < 1:
        st.warning("Like some articles first to get recommendations!")
        if st.button("⬅️ Go back to News Feed"):
            st.session_state.page = "feed"
            st.rerun()
    else:
        with st.spinner("Analyzing your preferences and generating recommendations..."):
            try:
                # ✅ 1. Create dynamic task here
                task = Task(
                    description=(
                       f"The user liked the following articles: {st.session_state.liked_articles}. "
                        "Your job is to infer the common topics or themes from these titles. "
                         
                        "Using the `news_fetcher` tool, fetch fresh news articles that match these inferred common topics. "
                        "Recommend only new articles that are relevant, interesting according to the user's preferences. "
                        "Avoid duplicates and articles the user already liked."
                    ),
                    expected_output= "Return a markdown list of 5 recommended news articles. "
                                     "Each recommendation should include a title, 1 to 2 sentence summary, image URL (if available), and a link to the article.",
                    agent=news_agent
                )

                # ✅ 2. Create and run crew
                crew = Crew(agents=[news_agent], tasks=[task], verbose=True)
                result = crew.kickoff()

                # ✅ 3. Display result
                st.success("Here are your personalized recommendations!")
                st.markdown(result)

            except Exception as e:
                st.error(f" Error while fetching recommendations: {str(e)}")




