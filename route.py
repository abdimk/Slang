import asyncio
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
