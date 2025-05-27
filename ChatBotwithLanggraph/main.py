#Step 1: Set up API keys - GROQ, TAVILY, and OpenAI

from dotenv import load_dotenv
load_dotenv()

import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
"""
Now Install -
pip install python-dotenv
"""



# Step 2: LLMs and TOOLS
"""NOW we have to install few things -
pip install langchain_groq
pip install langchain_openai
pip install langchain_community
"""

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

openai_llm = ChatOpenAI(
    model="gpt-4o-mini"
)

groq_llm = ChatGroq(
    model = "llama-3.3-70b-versatile"   
)

# LLM setup done; now Tools setup
search_tool = TavilySearch(
    max_results=2 #internet search consider only fist 2 results
)
# Step 2: Complete



# Step 3: Set up AI Agent with search functionality
""" Now we have to install few things again -
pip install langgraph
"""
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    # Select LLM
    if provider == "Groq":
        llm = ChatGroq(model=llm_id)
    elif provider == "OpenAI":
        llm = ChatOpenAI(model=llm_id)
    else:
        raise ValueError("Unsupported provider")

    # Optionally add search tool
    tools = [TavilySearchResults(max_results=2)] if allow_search else []

    # Create agent
    agent = create_react_agent(
        model=llm,
        tools=tools
    )

    # Build the `state` input (system + user)
    state = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    }

    # Invoke the agent
    response = agent.invoke(state)
    messages = response.get("messages")

    # Extract AI response
    ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]
    return ai_messages[-1] if ai_messages else "No response from agent."

 
 # This works fine.
 # End of Phase 1; Now we will work on Phase 2: Backend Building.
 