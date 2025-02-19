from slang.api import (DuckChat,model_type)
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
import asyncio


class Prompt(BaseModel):
    query: str
    system_prompt: str | None = None



model = model_type.DuckModelType

app = FastAPI()

@app.get("/")
async def index():
    return {"Hello":"World"}


@app.post("/o3mini")
def query(prompt: Prompt):
    p = prompt.query
    sp = prompt.system_prompt
    message_response = ""
    async def send_request(q1: str, sp):
        async with DuckChat(model.o3Mini) as o3:
            message_response = await o3.ask_question(q1)
            return {
                "query": q1,
                "system prompt": sp,
                "response":message_response
                }
        
    return asyncio.run(send_request(p, sp))
    

    

