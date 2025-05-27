# *Phase3: Frontend
# 1. Set up UI with streamlit
# 2. Connect with backend vie URL


# 1. Set up UI with streamlit (MODEL PROVIDER,MODEL,SYSTEM PROMPT, WEB SEARCH, QUERY)


""" We have to install few things -
pip install streamlit
"""
import streamlit as st
import requests # It's good practice to put all imports at the top

st.set_page_config(page_title= "Langgraph AI Agent", layout = "centered")
st.title("AI Chatbot Agent")
st.write("Create and Interact with AI AGENTS")

system_prompt =st.text_area("Define your AI Agent:", height=70, placeholder="Type your system prompt here...")


MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile"]
MODEL_NAMES_OPENAI= ["gpt-4o-mini"]

#DROPDOWN FOR MODEL SELECTION
provider = st.radio("Select Model Provider", ["Groq", "OpenAI"])

if provider == "Groq":
    selected_model = st.selectbox("Select GROQ Model", MODEL_NAMES_GROQ)
elif provider == "OpenAI":
    selected_model = st.selectbox("Select OpenAI Model", MODEL_NAMES_OPENAI)


allow_web_search = st.checkbox("Allow Web search")


user_query =st.text_area("Enter Your Query:", height=150, placeholder="Ask Any Question")

BACKEND_API_URL_FROM_ENV = st.secrets.get("BACKEND_API_URL")

if BACKEND_API_URL_FROM_ENV:
    API_URL = BACKEND_API_URL_FROM_ENV
else:
    # Fallback for local development if BACKEND_API_URL is not set
    # This allows you to run frontend.py locally and still connect to backend.py running locally
    API_URL = "http://127.0.0.1:9999/chat"
    # Optional: Add this warning to the main area if you prefer, or keep in sidebar
    # st.sidebar.warning(f"BACKEND_API_URL not set. Using local default: {API_URL}")
    # Or, for more visibility during local testing:
    st.caption(f"Dev Mode: Connecting to backend at {API_URL}")


if st.button("Submit"):
    if user_query.strip():
        payload = {
            "model_name": selected_model,
            "messages": user_query,
            "allow_search": allow_web_search,
            "system_prompt": system_prompt,
            "model_provider": provider
        }

        st.info(f"Sending request to: {API_URL} with query: \"{user_query[:50]}...\"") # Show a snippet of query

        try:
            # Send the POST request to the backend
            http_response = requests.post(API_URL, json=payload, timeout=180) # Renamed to http_response for clarity

            # Check for HTTP errors (4xx or 5xx status codes)
            http_response.raise_for_status()

            # The backend returns the AI response directly as a string.
            # So, we use .text to get it.
            ai_response_content = http_response.text

            st.subheader("Agent Response")
            st.markdown(f"**Final Response:** {ai_response_content}")

        except requests.exceptions.HTTPError as errh:
            st.error(f"An HTTP error occurred while communicating with the backend: {errh}")
            # It's helpful to show the response text if it's an HTTP error, as it might contain error details from FastAPI
            if hasattr(http_response, 'text'):
                st.error(f"Backend error details: {http_response.text}")
        except requests.exceptions.ConnectionError as errc:
            st.error(f"A connection error occurred: {errc}. Is the backend server running at {API_URL}?")
        except requests.exceptions.Timeout as errt:
            st.error(f"The request to the backend timed out: {errt}")
        except requests.exceptions.RequestException as err:
            st.error(f"An unexpected error occurred during the request: {err}")
        except Exception as e: # Catch any other unexpected errors
            st.error(f"An unexpected error occurred: {e}")
            # If http_response was defined and has text, show it
            if 'http_response' in locals() and hasattr(http_response, 'text'):
                st.error(f"Raw response content that caused the error: {http_response.text}")
    else:
        st.warning("Please enter a query.")