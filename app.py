#import streamlit as st
#from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain_tavily import TavilySearchResults
#from langgraph.prebuilt import create_react_agent

import streamlit as st
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch  # The 2026 standard
from langgraph.prebuilt import create_react_agent

# --- 1. PAGE CONFIG & STYLING ---
st.set_page_config(page_title="AI Job Scout", page_icon="💼", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; color: #1c1c1c; }
    h1 { color: #0e1117 !important; font-weight: 800; }
    .job-card { 
        background-color: white; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 5px solid #2e7d32;
        margin-bottom: 15px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HEADER & INPUTS ---
st.title("💼 AI Job Scout")
st.write("Finding your next role with real-time AI web intelligence.")

col1, col2 = st.columns(2)
with col1:
    role = st.text_input("What role are you looking for?", placeholder="e.g. Data Analyst")
with col2:
    location = st.text_input("City and State/Country", placeholder="e.g. Austin, Texas")

# --- 3. CORE LOGIC ---
if st.button("Search Current Openings"):
    if not role or not location:
        st.warning("Please enter both a role and a location.")
    else:
        try:
            # Initialize 2026 Stable Model
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash", 
                google_api_key=st.secrets["GOOGLE_API_KEY"]
            )

            # Initialize Tavily (Partner Package version)
            search_tool = TavilySearch(
                api_key=st.secrets["TAVILY_API_KEY"],
                max_results=5
            )

            # Create the ReAct Agent
            agent = create_react_agent(llm, tools=[search_tool])

            with st.spinner(f"Scouring the web for {role} jobs in {location}..."):
                # Agent reasoning path
                query = f"Find 5 current and active job openings for {role} in {location}. Provide the Job Title, Company, Location, and a direct URL to apply for each."
                
                # Streaming for better UX
                result = agent.invoke({"messages": [("human", query)]})
                
                st.subheader("Latest Openings Found:")
                st.markdown(result["messages"][-1].content)

        except Exception as e:
            if "429" in str(e):
                st.error("API Limit reached. Please wait 60 seconds.")
            else:
                st.error(f"An error occurred: {e}")

# --- 4. FOOTER ---
st.divider()
st.caption("Powered by Gemini 2.0 & Tavily Search (2026 Edition)")
