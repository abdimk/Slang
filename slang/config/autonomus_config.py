ANON_LLAMA_HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "country-code": "ET",
    "origin": "https://www.autonomous.ai",
    "priority": "u=1, i",
    "referer": "https://www.autonomous.ai/",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A_Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "socketid": "wwyzY_3cXW3tC2lhAOHG",
    "time-zone": "Africa/Addis_Ababa",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

def anonLlamaPayload(encoded_messages:str)->dict:
    return {
        "messages": encoded_messages,
        "threadId": "0193c0f9-c006-7ff0-9a3f-0e1b5cd3ac13",
        "userId": "0193c0f9-98de-7ff0-9a3f-01d37f04bee9",
        "stream": True,
        "aiAgent": "llama",
        "useTool": False
    }


# QwenCoder
ANON_QWEN_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/json",
    "Origin": "https://www.autonomous.ai",
    "Referer": "https://www.autonomous.ai/",
    "Sec-Ch-Ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Linux\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Country-Code": "ET",
    "Time-Zone": "Africa/Addis_Ababa",
    "SocketId": "DYWjcFUeMHkg3JseAgAc"
}

def anonQwenPayload(encoded_messages:str)->dict:
    return {
        "messages": encoded_messages,
        "threadId": "0193c113-22f1-7777-b672-4b4690bfd431",
        "userId": "0193c0f9-98de-7ff0-9a3f-01d37f04bee9",
        "stream": True,
        "aiAgent": "qwen_coder",
        "useTool": False
    }