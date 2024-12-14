import aiohttp
import asyncio
import json
import base64
import logging

class Llama:
    def __init__(self, query: str):
        self.query = query
        self.url = "https://chatgpt.autonomous.ai/api/v1/ai/chat"
        
        self.headers = {
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
        
        
        system_msg = "You are Llama 3.1, a highly capable 405-billion-parameter conversational AI assistant. Your primary goal is to deliver precise, relevant, and engaging responses tailored to each conversation. Maintain a friendly, conversational tone for casual interactions, ensuring a natural, fluid dialogue. Avoid empty or irrelevant responses. When unable to perform a function call due to missing or incorrect arguments, provide a thoughtful response based on your current knowledge. Focus on enhancing the user's understanding and satisfaction in every interaction. Use bullet points or numbered lists to organize information clearly and concisely for easy reading."
        
        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": self.query}
        ]
        
        encoded_messages = base64.b64encode(json.dumps(messages).encode()).decode()
        
        self.payload = {
            "messages": encoded_messages,
            "threadId": "0193c0f9-c006-7ff0-9a3f-0e1b5cd3ac13",
            "userId": "0193c0f9-98de-7ff0-9a3f-01d37f04bee9",
            "stream": True,
            "aiAgent": "llama",
            "useTool": False
        }
        
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
            #print(f"Status: {response.status}")
            
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
                       # print(f"Error decoding JSON: {line_str}")
                       pass
                    except Exception as e:
                        #print(f"Unexpected error: {e}")
                        pass 

                    #i am not going too pass them but put them in a logger 
                    # passing an exception is bad practice 
            
            return full_response



# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class QwenCoder:
    def __init__(self, query: str):
        self.query = query
        self.url = "https://chatgpt.autonomous.ai/api/v1/ai/chat"
        
        self.headers = {
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
        
        # System message for Qwen
        system_msg = "You are Qwen 2.5-Coder, an advanced code assistant designed to help with a wide range of coding tasks. Provide precise, clear, and efficient solutions to programming challenges across various languages and domains."
        
        # Prepare messages
        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": self.query}
        ]
        
        # Encode messages
        encoded_messages = base64.b64encode(json.dumps(messages).encode()).decode()
        
        # Prepare payload
        self.payload = {
            "messages": encoded_messages,
            "threadId": "0193c113-22f1-7777-b672-4b4690bfd431",
            "userId": "0193c0f9-98de-7ff0-9a3f-01d37f04bee9",
            "stream": True,
            "aiAgent": "qwen_coder",
            "useTool": False
        }
        
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get_response(self):
        if not self.session:
            logger.error("Client session not initialized. Use async context manager.")
            raise RuntimeError("Client session not initialized. Use async context manager.")
        
        try:
            async with self.session.post(self.url, headers=self.headers, json=self.payload) as response:
                if response.status != 200:
                    logger.error(f"HTTP request failed with status {response.status}")
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
                                logger.warning(f"Failed to decode JSON: {line_str}")
                            except Exception as json_error:
                                logger.error(f"Unexpected error processing JSON: {json_error}")
                    
                    except UnicodeDecodeError:
                        logger.warning("Failed to decode line")
                    except Exception as line_error:
                        logger.error(f"Unexpected error processing line: {line_error}")
                
                return full_response.strip()
        
        except aiohttp.ClientError as client_error:
            logger.error(f"Client connection error: {client_error}")
            return ""
        except Exception as unexpected_error:
            logger.error(f"Unexpected error during request: {unexpected_error}")
            return ""
