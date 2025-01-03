from datetime import datetime

time = datetime.now()

NEXTCHAT_HEADERS = {
    "accept": "application/json, text/event-stream",
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
}


def nextChatPayload(query:str,stream:bool,model:str,temperature:float,presence_penalty:float,frequency_penalty:float,top_p:float,max_tokens:int)->dict:
    return {
            "messages": [
                {"role": "system", 
                "content": "You are ChatGPT, a large language model trained by OpenAI.\n"
                                            "Knowledge cutoff: 2024-10\n"
                                            "Current model: gpt-4o\n"
                                            f"Current time: {time}\n"
                                            "Latex inline: \\(x^2\\)\n"
                                            "Latex block: $$e=mc^2$$\n"},
                {"role": "user", 
                "content": f"{query}"}
            ],
            "stream": stream,
            "model": model,
            "temperature": temperature,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
            "top_p": top_p,
            "max_tokens": max_tokens
        }
    


################
    
ASKCHAT_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/json",
    "Origin": "https://www.teach-anything.com",
    "Referer": "https://www.teach-anything.com/",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

def askChatPlayload(query:str)->dict:
    return {
            "prompt": f"Pretend you are GPT-4 model. Explain {query} English with a simple example.\n"
                                "Knowledge cutoff: 2024-10\n"
                                "Current model: gpt-4o\n"
                                f"Current time: \n"
                                "Latex inline: \\(x^2\\)\n"
                                "Latex block: $$e=mc^2$$\n"
    }



#################
# DUCK DUCK HEADERS
################




CHATX_HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Origin': 'https://www.pizzagpt.it',
    'Referer': 'https://www.pizzagpt.it/en',
    'x-secret': 'Marinara'
        
}


MORPHIC_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/json",
    "Cookie": "copilot:state=false; images:state=false; ph_phc_HK6KqP8mdSmxDjoZtHYi3MW8Kx5mHmlYpmgmZnGuaV5_posthog=%7B%22distinct_id%22%3A%220193be60-3f74-7aab-b7e2-59fd224fd2ed%22%2C%22%24sesid%22%3A%5B1734099588434%2C%220193c062-f1f3-7496-960e-b0a08da05057%22%2C1734099530227%5D%7D",
    "Origin": "https://www.morphic.sh",
    "Referer": "https://www.morphic.sh/",
    "Sec-CH-UA": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"Linux"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

def morphic_payload(query:str) -> dict:
    return {
         "messages": [
                {
                    "role": "user",
                    "content": f"{query}",
                    "type": "input",
                    "id": "clkCqnlbfqNTvOna",
                    "status": "done"
                }
            ]
    }