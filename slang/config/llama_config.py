CHATLLAMA_HEADERS = {
    'authority': 'chatgptgratis.eu',
    'method': 'POST',
    'path': '/backend/chat.php',
    'scheme': 'https',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://chatgptgratis.eu',
    'referer': 'https://chatgptgratis.eu/chat.html',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

def chat_llama_payload(model: str, query: str) -> dict:
    return {
        "message": query,  
        "model": model     
    }