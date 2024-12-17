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

class Imagine:
    def __init__(self, query: str):
        self.query = query
        self.url = 'https://www.blackbox.ai/api/chat'
        self.headers = self.get_imagine_headers()
        self.payload = self.get_imagine_payload(query)
        self.session = None

    def get_imagine_headers(self):
        return {
            'authority': 'www.blackbox.ai',
            'method': 'POST',
            'path': '/api/chat',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'cookie': 'sessionId=0430adb7-09af-4b69-a2bf-1e0ced8892fd; __Host-authjs.csrf-token=a6cf92e74e6466942ac9c7d7f4db259a773d3c3841617a8b55f74e74a00add43%7Cf4eac72fc5a8462de9e1cac4ce947ff32bc4f748482c707f37c1b0b762a91867; __Secure-authjs.callback-url=https%3A%2F%2Fwww.blackbox.ai',
            'origin': 'https://www.blackbox.ai',
            'priority': 'u=1, i',
            'referer': 'https://www.blackbox.ai/',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }

    def get_imagine_payload(self, query):
        return {
            "messages": [
                {"id": "zIIqFWX", "content": query, "role": "user"}
            ],
            "id": "zIIqFWX",
            "previewToken": None,
            "userId": None,
            "codeModelMode": True,
            "agentMode": {},
            "trendingAgentMode": {},
            "isMicMode": False,
            "userSystemPrompt": None,
            "maxTokens": 1024,
            "playgroundTopP": None,
            "playgroundTemperature": None,
            "isChromeExt": False,
            "githubToken": "",
            "clickedAnswer2": False,
            "clickedAnswer3": False,
            "clickedForceWebSearch": False,
            "visitFromDelta": False,
            "mobileClient": False,
            "userSelectedModel": None,
            "validated": "00f37b34-a166-4efb-bce5-1312d87f2f94",
            "imageGenerationMode": True,
            "webSearchModePrompt": False
        }

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
