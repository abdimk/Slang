import aiohttp
import asyncio
import json
import os
from slang.config.blackbox_config import(
    BLACKBOX_HEADERS,
    get_blackbox_payload,
    get_claude_headers,get_claude_payload,
    LIGHTROOM,
    get_gemini_headers,
    get_geminiPro_payload,
    get_llama_headers,
    get_llama_payload,
    dbrx_headers,
    dbrx_payload,
    gpt4_headers,
    gpt4_payload
)
from slang.log.logformat import CustomLogger
from abc import ABC,abstractmethod


logger = CustomLogger()


BASEURL = "https://www.blackbox.ai/api/chat"
class BlackBox(ABC):
    # @abstractmethod
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    # @abstractmethod
    async def __aexit__(self, exc_type,exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get_response(self):
        if not self.session:
            raise RuntimeError("Client session not initialized. Use async context manager.")
        
        try:
            async with self.session.post(BASEURL, headers=self.headers, json=self.payload) as response:
                if response.status != 200:
                    logger.__ERROR__(f"HTTP request failed with status {response.status}")
                    return ""
                
                response_text = await response.text()
                return self.format_response(response_text)
        
        except aiohttp.ClientError as client_error:
            logger.__ERROR__(f"Client connection error: {client_error}")
            return ""
        except Exception as unexpected_error:
            logger.__ERROR__(f"Unexpected error during request: {unexpected_error}")
            return ""

    def format_response(self, response_text):
        parts = response_text.split('$~~~$')
        
        search_results = ""
        try:
            results = json.loads(parts[1])
            search_results = "Search Results:\n"
            for result in results[:5]:  # Limit to top 5 results
                search_results += f"- {result['title']}\n  URL: {result['link']}\n  Snippet: {result['snippet']}\n\n"
        except:
            search_results = "Could not parse search results.\n"

        
        ai_response = parts[2].strip() if len(parts) > 2 else "No AI response"

        # Combine and format the full response
        # formatted_response = f"""{search_results} AI Response:{ai_response}"""
        formatted_response = f"{ai_response}"
        return formatted_response

    


class BlackboxAI:
    def __init__(self, query: str):
        self.query = query
        self.url = ''
        self.headers = BLACKBOX_HEADERS
        self.payload = get_blackbox_payload(query)
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
            async with self.session.post(BASEURL, headers=self.headers, json=self.payload) as response:
                if response.status != 200:
                    logger.__ERROR__(f"HTTP request failed with status {response.status}")
                    return ""
                
                response_text = await response.text()
                return self.format_response(response_text)
        
        except aiohttp.ClientError as client_error:
            logger.__ERROR__(f"Client connection error: {client_error}")
            return ""
        except Exception as unexpected_error:
            logger.__ERROR__(f"Unexpected error during request: {unexpected_error}")
            return ""

    def format_response(self, response_text):
        
        parts = response_text.split('$~~~$')
        
        search_results = ""
        try:
            results = json.loads(parts[1])
            search_results = "Search Results:\n"
            for result in results[:5]:  # Limit to top 5 results
                search_results += f"- {result['title']}\n  URL: {result['link']}\n  Snippet: {result['snippet']}\n\n"
        except:
            search_results = "Could not parse search results.\n"

        
        ai_response = parts[2].strip() if len(parts) > 2 else "No AI response"

        # Combine and format the full response
        # formatted_response = f"""{search_results} AI Response:{ai_response}"""
        formatted_response = f"{ai_response}"
        return formatted_response
    
class ClaudeAI:
    def __init__(self, query: str, system_prompt: str = None,
                 role: str = "user",
                 previewToken: bool = False,
                 userSystemPrompt: bool = False,
                 maxTokens: int = 1024,
                 codeModelMode: bool = False,
                 memory_file: str = None
                 ):
        # Initialize memory based on memory file
        self.memory_file = memory_file
        self.memory = self.load_memory() if memory_file else []

        
        if memory_file:
            self.save_memory(query)

        # Log memory for debugging
        # logger.__INFO__(self.memory)

        
        system_prompt = f"This is your memory don't mention it in chat just use it as a reference {self.memory}"
        
        self.headers = get_claude_headers()
        self.payload = get_claude_payload(f"{query}, {system_prompt}")
        self.session = None

        
        self.role = role
        self.previewToken = previewToken
        self.userSystemPrompt = True  
        self.maxTokens = maxTokens
        self.codeModelMode = codeModelMode

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get_response(self, system_prompt: str = None):
        if not self.session:
            raise RuntimeError("Client session not initialized. Use async context manager.")
        
        try:
            async with self.session.post(BASEURL, headers=self.headers, json=self.payload) as response:
                if response.status != 200:
                    print(f"HTTP request failed with status {response.status}")
                    return ""
                
                response_text = await response.text()
                
                # Save response to memory file if specified
                if self.memory_file:
                    self.save_memory(response_text)
                
                return response_text
        
        except aiohttp.ClientError as client_error:
            print(f"Client connection error: {client_error}")
            return ""
        except Exception as unexpected_error:
            print(f"Unexpected error during request: {unexpected_error}")
            return ""

    def load_memory(self):
        """Load previous interactions from a JSON file."""
        try:
            if self.memory_file and os.path.exists(self.memory_file):
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading memory file: {e}")
        return []

    def save_memory(self, query):
        """Save the current query to the JSON file."""
        if self.memory_file:
            try:
                self.memory.append(query)
                with open(self.memory_file, 'w') as f:
                    json.dump(self.memory, f, indent=2)
            except IOError as e:
                print(f"Error saving memory file: {e}")



class GeminiPro(BlackboxAI):
    def __init__(self, query: str,system_prompt:str=None,
                 role:str = "user",
                 previewToken:bool=False,
                 userSystemPrompt:bool=False,
                 maxTokens:int=1024,
                 codeModelMode:bool=False)->None:
        self.url = "https://www.blackbox.ai/api/chat"
        self.headers = get_gemini_headers()
        self.payload = get_blackbox_payload(query)
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
            async with self.session.post(BASEURL, headers=self.headers, json=self.payload) as response:
                if response.status != 200:
                    logger.__ERROR__(f"HTTP request failed with status {response.status}")
                    return ""
                
                response_text = await response.text()
                return super().format_response(response_text)
        
        except aiohttp.ClientError as client_error:
            logger.__ERROR__(f"Client connection error: {client_error}")
            return ""
        except Exception as unexpected_error:
            logger.__ERROR__(f"Unexpected error during request: {unexpected_error}")
            return ""


class GPT4:
    def __init__(self,query:str):
        self.headers = gpt4_headers()
        self.payload = gpt4_payload(query)
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
            async with self.session.post(BASEURL, headers=self.headers, json=self.payload) as response:
                if response.status != 200:
                    logger.__ERROR__(f"HTTP request failed with status {response.status}")
                    return ""
                
                response_text = await response.text()
                return response_text
        
        except aiohttp.ClientError as client_error:
            logger.__ERROR__(f"Client connection error: {client_error}")
            return ""
        except Exception as unexpected_error:
            logger.__ERROR__nt(f"Unexpected error during request: {unexpected_error}")
            return ""


class DBRX:
    def __init__(self,query:str):
        self.headers = dbrx_headers()
        self.payload = dbrx_payload(query)
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
            async with self.session.post(BASEURL, headers=self.headers, json=self.payload) as response:
                if response.status != 200:
                    logger.__ERROR__(f"HTTP request failed with status {response.status}")
                    return ""
                
                response_text = await response.text()
                return response_text
        
        except aiohttp.ClientError as client_error:
            logger.__ERROR__(f"Client connection error: {client_error}")
            return ""
        except Exception as unexpected_error:
            logger.__ERROR__(f"Unexpected error during request: {unexpected_error}")
            return ""


#@Meta-Llama-3.3-70B-Instruct-Turbo hello

class MetaLlama3InstructTurbo:
    def __init__(self,query:str):
        self.headers = get_llama_headers()
        self.payload = get_llama_payload(query)
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
            async with self.session.post(BASEURL, headers=self.headers, json=self.payload) as response:
                if response.status != 200:
                    logger.__ERROR__(f"HTTP request failed with status {response.status}")
                    return ""
                
                response_text = await response.text()
                return response_text
        
        except aiohttp.ClientError as client_error:
            logger.__ERROR__(f"Client connection error: {client_error}")
            return ""
        except Exception as unexpected_error:
            logger.__ERROR__(f"Unexpected error during request: {unexpected_error}")
            return ""


