#import streamlit as st
#from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain_tavily import TavilySearchResults
#from langgraph.prebuilt import create_react_agent

import streamlit as st
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent

# --- 1. OPTIMIZED UI SETUP ---
st.set_page_config(page_title="AI Job Scout 2.0", page_icon="💼", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0f1116; color: #ffffff; }
    .job-card { background: #1b1e26; padding: 15px; border-radius: 8px; border-left: 4px solid #00ff88; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ AI Job Scout: Ultra-Fast")
st.caption("2026 High-Performance Engine")

# --- 2. INPUTS ---
col1, col2 = st.columns(2)
with col1:
    role = st.text_input("Role", placeholder="e.g. UX Designer")
with col2:
    location = st.text_input("Location", placeholder="e.g. Seattle, WA")

# --- 3. THE ENGINE ---
try:
    # Use Gemini 1.5 Flash for the fastest initial 'reasoning'
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-latest", 
        google_api_key=st.secrets["GOOGLE_API_KEY"],
        temperature=0.1 # Low temperature = faster, more focused output
    )

    # SPEED HACK: Use 'basic' search depth and limit results to 3 for raw speed
    search_tool = TavilySearch(
        api_key=st.secrets["TAVILY_API_KEY"],
        max_results=3, 
        search_depth="basic" 
    )

    agent_executor = create_react_agent(llm, tools=[search_tool])

    if st.button("Find Jobs Now"):
        if role and location:
            # We use a container to stream the response so it feels instant
            with st.chat_message("assistant"):
                status_placeholder = st.empty()
                response_placeholder = st.empty()
                
                status_placeholder.status("🔍 Scouting live job boards...", expanded=True)
                
                # SPEED HACK: Streaming chunks instead of waiting for the whole response
                full_response = ""
                # We limit the agent to a very specific set of instructions to avoid 'looping'
                prompt = f"Find 3 active {role} jobs in {location}. Output: Job Title, Company, and Link. Be extremely concise."
                
                for chunk in agent_executor.stream({"messages": [("human", prompt)]}):
                    if "messages" in chunk:
                        content = chunk["messages"][-1].content
                        full_response += content
                        response_placeholder.markdown(full_response)
                
                status_placeholder.empty()
                st.success("Scout Complete!")
        else:
            st.warning("Please fill in both fields.")

except Exception as e:
    st.error(f"Engine Error: {e}")
