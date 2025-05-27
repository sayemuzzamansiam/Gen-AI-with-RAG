# Phase2: Backend using FastAPI

# 1. Set up Pydantic Model (Schema Validation)
# 2. Set up AI Agent from FrontEnd Request
# 3. Run app & Explore Swagger UI Docs

"""now we have to install few things -
   pip install fastapi pydantic uvicorn  
"""

from pydantic import BaseModel
from typing import List

# data contract for the request using pydantic
class RequestState(BaseModel):
    model_name: str
    messages: str
    allow_search: bool
    system_prompt: str
    model_provider: str

    
# now let's start FastAPI

from fastapi import FastAPI, HTTPException
from main import get_response_from_ai_agent

ALLOWED_MODEL_NAMES = ["llama3-70b-8192", "mixtral-8x7b-32768", "llama-3.3-70b-versatile", "gpt-4o-mini"]
   
app = FastAPI(title = "Langgraph AI Agent")

@app.post("/chat")
def chat(request: RequestState):
    """
    API endpoint to interact with the chatbot using Langgraph and search tool.
    It dynamically selects the model based on the request.
    """
    if request.model_name not in ALLOWED_MODEL_NAMES:
        raise HTTPException(status_code=400, detail="Invalid model name provided.")
    llm_id = request.model_name
    query = request.messages
    allow_search = request.allow_search
    system_prompt = request.system_prompt
    provider = request.model_provider
    
    # Create AI Agent and get response from it
    response = get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider)
    return response
        

# 3. Run app & Explore Swagger UI Docs
if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 9999))  
    uvicorn.run(app, host="0.0.0.0", port=port)
            