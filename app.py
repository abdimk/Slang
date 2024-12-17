# app.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse,HTMLResponse
from fastapi.staticfiles import StaticFiles
from slang.api import Llama  
from slang.api import DuckChat,model_type
from slang.api import ClaudeAI,Imagine
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

M = model_type.DuckModelType
app = FastAPI()

@app.get("/")
async def index(request: Request):
    client_ip = request.client.host  
    server_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  

    return {
        "response": "I think the server is running !",
        "ip_address": client_ip,
        "server_time": server_time
    }


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/about", response_class=HTMLResponse)
async def index():
    with open("static/index.html", "r") as file:
        content = file.read()
    return HTMLResponse(content=content)


@app.post('/gpt4')
async def claude(request: Request):
    try:
        data = await request.json()
        query = data.get('query', '')

        if not query:
            return JSONResponse(
                status_code=400, 
                content={"error": "No query provided"}
            )

        async with ClaudeAI(query) as d1:
            response = await d1.get_response()

        return JSONResponse(content={"response": response})

    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={"error": str(e)}
        )


@app.post('/imagine')
async def image(request: Request):
    try:
        data = await request.json()
        query = data.get('query', '')

        if not query:
            return JSONResponse(
                status_code=400, 
                content={"error": "No query provided"}
            )

        async with Imagine(query) as m1:
            response = await m1.get_response()

        return JSONResponse(content={
            "model":"lightroomv1",
            "temperature":None,
            "response": response
            })

    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={"error": str(e)}
        )
    
@app.post('/claude')
async def claude(request: Request):
    try:
        data = await request.json()
        query = data.get('query', '')

        if not query:
            return JSONResponse(
                status_code=400, 
                content={"error": "No query provided"}
            )

        async with ClaudeAI(query) as d1:
            response = await d1.get_response()

        return JSONResponse(content={"response": response})

    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={"error": str(e)}
        )


@app.post('/claude3')
async def gpt40(request: Request):
    try:
        data = await request.json()
        query = data.get('query', '')

        if not query:
            return JSONResponse(
                status_code=400, 
                content={"error": "No query provided"}
            )

        async with DuckChat(M.Claude) as d1:
            response = await d1.ask_question(query)

        return JSONResponse(content={"response": response})

    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={"error": str(e)}
        )



@app.post('/llama3')
async def gpt40(request: Request):
    try:
        data = await request.json()
        query = data.get('query', '')

        if not query:
            return JSONResponse(
                status_code=400, 
                content={"error": "No query provided"}
            )

        async with DuckChat(M.Llama3o1) as d1:
            response = await d1.ask_question(query)

        return JSONResponse(content={"response": response})

    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={"error": str(e)}
        )


@app.post('/gptmini')
async def gpt40(request: Request):
    try:
        data = await request.json()
        query = data.get('query', '')

        if not query:
            return JSONResponse(
                status_code=400, 
                content={"error": "No query provided"}
            )

        async with DuckChat(M.GPT4o_Mini) as d1:
            response = await d1.ask_question(query)

        return JSONResponse(content={"response": response})

    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={"error": str(e)}
        )

@app.post("/llama")
async def llama(request: Request):
    try:
        data = await request.json()
        query = data.get('query', '')

        if not query:
            return JSONResponse(
                status_code=400, 
                content={"error": "No query provided"}
            )

        async with Llama(query) as l1:
            response = await l1.get_response()

        return JSONResponse(content={"response": response})

    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={"error": str(e)}
        )

# Optional: Additional error handling and configuration
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "An unexpected error occurred",
            "detail": str(exc)
        }
    )