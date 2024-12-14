import aiohttp
import asyncio
import aiohttp
import asyncio
import json
from slang.config.blackbox_config import(
    BLACKBOX_HEADERS,
    get_blackbox_payload,
    get_claude_headers,get_claude_payload
)


class BlackboxAI:
    def __init__(self, query: str):
        self.query = query
        self.url = 'https://www.blackbox.ai/api/chat'
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
            async with self.session.post(self.url, headers=self.headers, json=self.payload) as response:
                if response.status != 200:
                    print(f"HTTP request failed with status {response.status}")
                    return ""
                
                response_text = await response.text()
                return self.format_response(response_text)
        
        except aiohttp.ClientError as client_error:
            print(f"Client connection error: {client_error}")
            return ""
        except Exception as unexpected_error:
            print(f"Unexpected error during request: {unexpected_error}")
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
    def __init__(self, query: str):
        self.query = query
        self.url = 'https://www.blackbox.ai/api/chat'
        self.headers = get_claude_headers()
        self.payload = get_claude_payload(query)
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
                    print(f"HTTP request failed with status {response.status}")
                    return ""
                
                response_text = await response.text()
                return response_text
        
        except aiohttp.ClientError as client_error:
            print(f"Client connection error: {client_error}")
            return ""
        except Exception as unexpected_error:
            print(f"Unexpected error during request: {unexpected_error}")
            return ""

