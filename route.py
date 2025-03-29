import asyncio
import aiohttp
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from slang.api import (DuckChat,model_type,Llama_Models)
from slang.api import ChatLlama
from fastapi.middleware.cors import CORSMiddleware

class Prompt(BaseModel):
    query: str
    system_prompt: str | None = None



model = model_type.DuckModelType
llamaModel = Llama_Models.Meta_Llama_3_2_1_8B_Instruct

app = FastAPI()


# simple gemini pro
# This function sends a request to Gemini, extracts, and returns the text content.
async def send_request_togemini(query: str, sp: str) -> str:
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-2.0-flash:generateContent?key=AIzaSyD0THDIxQLdYpvz07ht12I13OgtHFrkL8k"
    )
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": query}
                ]
            }
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 200:
                json_response = await response.json()
                candidates = json_response.get("candidates", [])
                # Return the first candidate's text, if available.
                for candidate in candidates:
                    content = candidate.get("content", {})
                    parts = content.get("parts", [])
                    for part in parts:
                        text = part.get("text", "")
                        return text
                return "No content found in response."
            else:
                text_response = await response.text()
                return f"Error {response.status}: {text_response}"

@app.get("/")
async def index():
    return {"Hello":"World"}


@app.post("/o3mini")
def query(prompt: Prompt):
    p = prompt.query
    sp = prompt.system_prompt
    message_response = ""
    # print(f'{p}\n{sp}')
    async def send_request(q1: str, sp):
        async with DuckChat(model.o3Mini) as o3:
            message_response = await o3.ask_question(q1)
            return {
                "query": q1,
                "system prompt": sp,
                "response":message_response
                }
        
    return asyncio.run(send_request(p, sp))

# Define the FastAPI POST endpoint.
@app.post("/gemini")
async def query(prompt: Prompt):
    response_text = await send_request_togemini(prompt.query, prompt.system_prompt)
    return {
        "query": prompt.query,
        "system_prompt": prompt.system_prompt,
        "response": response_text
    }

    

#using llama model 
@app.post("/llama")
def llamaRequest(prompt: Prompt):
    p = prompt.query
    sp = prompt.system_prompt

    message_response = ""
    # print(f'{p}\n{sp}')
    async def send_request(q1:str, sp):
        async with ChatLlama(p,llamaModel.value) as llama:
            message_response = await llama.get_response()
            return {
                "query": q1,
                "system prompt": sp,
                "response": message_response
            }
    return asyncio.run(send_request(p, sp))



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_methods=["*"],
    allow_headers=["*"],
)
