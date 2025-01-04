import aiohttp
import asyncio
import json
import base64

from slang.log.logformat import CustomLogger
from slang.config.autonomus_config import (
    ANON_LLAMA_HEADERS,
    anonLlamaPayload,
    ANON_QWEN_HEADERS,
    anonQwenPayload
)


logger = CustomLogger()

class Llama:
    def __init__(self, query: str):
        self.query = query
        self.url = "https://chatgpt.autonomous.ai/api/v1/ai/chat"
        
        self.headers = ANON_LLAMA_HEADERS
        
        system_msg = "You are Llama 3.1, a highly capable 405-billion-parameter conversational AI assistant. Your primary goal is to deliver precise, relevant, and engaging responses tailored to each conversation. Maintain a friendly, conversational tone for casual interactions, ensuring a natural, fluid dialogue. Avoid empty or irrelevant responses. When unable to perform a function call due to missing or incorrect arguments, provide a thoughtful response based on your current knowledge. Focus on enhancing the user's understanding and satisfaction in every interaction. Use bullet points or numbered lists to organize information clearly and concisely for easy reading."
        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": self.query}
        ]
        encoded_messages = base64.b64encode(json.dumps(messages).encode()).decode()
        self.payload = anonLlamaPayload(encoded_messages)
        
        self.session = None

    async def __aenter__(self):
        
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
    
        if self.session:
            await self.session.close()

    async def get_response(self):
        if not self.session:
            raise RuntimeError("Client session not initialized. Use async context manager.")
        
        async with self.session.post(self.url, headers=self.headers, json=self.payload) as response:
            logger.__INFO__(f"Status: {response.status}")
            
            full_response = ""
            async for line in response.content:
                line_str = line.decode('utf-8').strip()
                if line_str.startswith('data:'):
                    try:
                        
                        json_data = json.loads(line_str[5:])
                        
                        
                        if 'choices' in json_data and json_data['choices']:
                            delta = json_data['choices'][0].get('delta', {})
                            content = delta.get('content', '')
                            
                            
                            full_response += content
                    except json.JSONDecodeError:
                       logger.__ERROR__(f"Eror decoding JSON: {line_str}")
                       pass
                    except Exception as e:
                        logger.__ERROR__(f"Unexpected error: {e}")
                        pass 

                    #i am not going too pass them but put them in a logger 
                    # passing an exception is bad practice 
            
            return full_response



class QwenCoder:
    def __init__(self, query: str):
        self.query = query
        self.url = "https://chatgpt.autonomous.ai/api/v1/ai/chat"
        
        self.headers = ANON_QWEN_HEADERS
        
        # System message for Qwen
        system_msg = "You are Qwen 2.5-Coder, an advanced code assistant designed to help with a wide range of coding tasks. Provide precise, clear, and efficient solutions to programming challenges across various languages and domains."
        
        
        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": self.query}
        ]
        
        
        encoded_messages = base64.b64encode(json.dumps(messages).encode()).decode()
        self.payload = anonQwenPayload(encoded_messages)
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get_response(self):
        if not self.session:
            raise RuntimeError("Client session not initialized. Use async context manager.")
        
        try:
            async with self.session.post(self.url, headers=self.headers, json=self.payload) as response:
                if response.status != 200:
                    return ""
                full_response = ""
                async for line in response.content:
                    try:
                        line_str = line.decode('utf-8').strip()
                        if line_str.startswith('data:'):
                            try:
                                json_data = json.loads(line_str[5:])
                                
                                if 'choices' in json_data and json_data['choices']:
                                    delta = json_data['choices'][0].get('delta', {})
                                    content = delta.get('content', '')
                                    
                                    full_response += content
                            
                            except json.JSONDecodeError:
                                # logger.__ERROR__(f"Failed to decode JSON: {line_str}")
                                pass 
                            except Exception as json_error:
                                logger.__ERROR__(f"Unexpected error processing JSON: {json_error}")
                    
                    except UnicodeDecodeError:
                        logger.__ERROR__("Failed to decode line")
                    except Exception as line_error:
                        logger.__ERROR__("Unexpected error processing line: {line_error}")
                
                return full_response.strip()
        
        except aiohttp.ClientError as client_error:
            logger.__ERROR__(f"Client connection error: {client_error}")
            return ""
        except Exception as unexpected_error:
            logger.__ERROR__(f"Unexpected error during request: {unexpected_error}")
            return ""
