#import streamlit as st
#from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain_tavily import TavilySearchResults
#from langgraph.prebuilt import create_react_agent

import streamlit as st
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent


# --- UI SETUP ---
st.set_page_config(page_title="Analyst AI Job Scout", page_icon="💼")
st.title("💼Analyst AI Job Scout: 2026 Edition")
st.markdown("Enter your details to find 5 current openings in your area.")

# --- INPUTS ---
col1, col2, col3 = st.columns(3)
with col1:
    role = st.text_input("Job Role", placeholder="e.g. Data Scientist")
with col2:
    state = st.text_input("State", placeholder="e.g. Lagos")
with col3:
    country = st.text_input("Country", placeholder="e.g. Nigeria")

if st.button("Find Jobs"):
    if not role or not state:
        st.error("Please provide both a role and a state!")
    else:
        try:
            # 1. Initialize Gemini 2.0 (Great for extracting structured data)
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash", 
                google_api_key=st.secrets["GOOGLE_API_KEY"]
            )

            # 2. Setup Tavily with a focus on Job Boards
            search = TavilySearchResults(api_key=st.secrets["TAVILY_API_KEY"], max_results=10)
            agent = create_react_agent(llm, tools=[search])

            with st.spinner(f"Searching for {role} roles in {state}..."):
                # Constructing a precise 2026 prompt
                prompt = f"""Find 5 current and active job openings for '{role}' in '{state}, {country}'. 
                Provide the results in a clean list including: 
                1. Job Title 
                2. Company Name 
                3. Location 
                4. A brief snippet of requirements 
                5. Link to apply.
                Ensure the jobs were posted recently."""

                result = agent.invoke({"messages": [("human", prompt)]})
                
                st.success("Scouting Complete!")
                st.markdown(result["messages"][-1].content)

        except Exception as e:
            st.error(f"Error: {e}")
