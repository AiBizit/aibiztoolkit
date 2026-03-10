import streamlit as st
from dotenv import load_dotenv
import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

load_dotenv()

st.set_page_config(page_title="AI Business Toolkit", page_icon="🚀", layout="wide")
st.title("🚀 AI Business Toolkit")
st.caption("Your 5 AI Agents — Ready in Your Browser")

# Password protection (you set this once in Streamlit Secrets)
PASSWORD = st.secrets.get("PASSWORD", "demo123")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    pw = st.text_input("Enter your access code (from Lemon Squeezy receipt)", type="password")
    if st.button("Unlock Toolkit"):
        if pw == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect code. Please check your purchase email.")
    st.stop()

# Sidebar
agent_choice = st.sidebar.radio(
    "Choose Your AI Agent",
    ["Social Media Manager", "Email Marketer", "SEO Auditor", "Content Calendar", "Customer Support"]
)

niche = st.text_input("Your business niche or details", placeholder="e.g. local plumbing service in Texas")

if st.button("🚀 Run This Agent Now", type="primary"):
    with st.spinner("AI is working... watch the live steps below"):
        llm = ChatOpenAI(
            model="grok-4-fast-reasoning",
            base_url="https://api.x.ai/v1",
            api_key=os.getenv("GROK_API_KEY")
        )

        if agent_choice == "Social Media Manager":
            agent = Agent(role="Viral Social Media Manager", goal="Create 30 days of high-engagement posts", backstory="Top social media manager who grew 50 accounts to 100k+", llm=llm)
            task = Task(description=f"Create 30 days of Instagram + LinkedIn posts for a {niche} business. Include captions, hashtags, posting times.", agent=agent, expected_output="Full 30-day calendar")
        elif agent_choice == "Email Marketer":
            agent = Agent(role="Expert Email Marketer", goal="Create high-converting email sequences", backstory="Top marketer who doubles open rates", llm=llm)
            task = Task(description=f"Create a 5-email funnel for a {niche} business that drives sales.", agent=agent, expected_output="Full email sequence")
        elif agent_choice == "SEO Auditor":
            agent = Agent(role="SEO Auditor", goal="Audit websites for improvements", backstory="Top SEO expert who helps businesses rank #1", llm=llm)
            task = Task(description=f"Audit the SEO of a website for a {niche} business. Check keywords, speed, mobile, and give fixes.", agent=agent, expected_output="Detailed SEO audit report")
        elif agent_choice == "Content Calendar":
            agent = Agent(role="Content Planner", goal="Build content calendars", backstory="Top content strategist who boosts traffic by 5x", llm=llm)
            task = Task(description=f"Build a 30-day content calendar for a {niche} business with topics and platforms.", agent=agent, expected_output="Detailed 30-day calendar")
        else:  # Customer Support
            agent = Agent(role="Support Rep", goal="Handle customer queries", backstory="Friendly support expert who builds loyalty", llm=llm)
            task = Task(description=f"Handle a common customer query for a {niche} business with empathetic solutions.", agent=agent, expected_output="Full response thread")

        crew = Crew(agents=[agent], tasks=[task], process=Process.sequential)
        result = crew.kickoff(inputs={"niche": niche})

        st.success("✅ Done!")
        st.subheader("Live Output")
        st.code(result, language=None)
        st.download_button("Download as TXT", result, file_name=f"{agent_choice.lower().replace(' ', '_')}.txt")
