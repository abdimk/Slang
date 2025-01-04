import aiohttp
import asyncio
import json

from slang.log.logformat import CustomLogger
from slang.models.model_type import LlamaModels 

from slang.config.llama_config import (
    CHATLLAMA_HEADERS,
    chat_llama_payload
)

logger = CustomLogger()

class ChatLlama:
    
    def __init__(self, query: str, model: str = "Meta-Llama-3.2-1B-Instruct") -> None:
        self.headers = CHATLLAMA_HEADERS
        self.payload = chat_llama_payload(model, query)
        self.BASEURL = 'https://chatgptgratis.eu/backend/chat.php'

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

        
    async def get_response(self):
        async with self.session.post(self.BASEURL, headers=self.headers, json=self.payload) as response:
            full_content = ""
            async for line in response.content:
                try:
                    line = line.decode('utf-8').strip()
                    if not line:
                        continue
                    if line == 'data: [DONE]':
                        break
                    if line.startswith('data: '):
                        line = line[6:]
                        
                        try:
                            data = json.loads(line)
                            
                            if 'choices' in data and data['choices']:
                                content = data['choices'][0]['delta'].get('content', '')
                                if content:
                                    full_content += content
                                    # print(content, end='', flush=True)
                        
                        except json.JSONDecodeError:
                        
                            logger.__ERROR__(f"\nError parsing JSON: {line}")
                    else:
                        
                        logger.__ERROR__(f"\nUnexpected line: {line}")
                
                except Exception as e:
                    logger.__ERROR__(f"\nError processing line: {e}")
            
            return full_content

