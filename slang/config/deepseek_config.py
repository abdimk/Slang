DEEPSEEK_HEADERS = {
        "Accept": "text/event-stream",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }




def DeepSeek_Payload(query:str, model:str)->None:
    return  {
        "model":model,  # Options: deepseek-ai/DeepSeek-V3, deepseek-ai/DeepSeek-R1-Distill-Llama-70B
        "messages": [
            {"role": "user", "content": query}
        ],
        "frequency_penalty": 0,
        "max_tokens": 800,
        "stream": True,
        "temperature": 0.7,
        "min_p": 0,
        "presence_penalty": 0,
        "repetition_penalty": 1,
        "seed": None,
        "top_k": 0,
        "top_p": 0.9,
        "user": None
    }