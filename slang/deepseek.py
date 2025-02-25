import json
import sys
import aiohttp
from slang.config.deepseek_config import(
    DEEPSEEK_HEADERS,DeepSeek_Payload
)
from slang.log.logformat import CustomLogger


logger = CustomLogger()

class DeepSeek:
    def __init__(self, query:str, model:str)->None:
        self.url = "https://api.deepinfra.com/v1/openai/chat/completions"
        self.headers = DEEPSEEK_HEADERS
        self.payload = DeepSeek_Payload(query, model)

        self.collected = []

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    
    async def get_response(self):
        if not self.session:
            raise RuntimeError("Client sesssion not initialized. Use async context manager.")
        

        try:
            async with self.session.post(self.url, headers=self.headers, json=self.payload) as response:
                if response.status != 200:
                    logger.__ERROR__(f"HTTP request failed with status {response.status}")
                    return ""

                async for line in response.content:
                    line = line.decode().strip()
                    if line.startswith("data: "):
                        try:
                            data = json.loads(line[6:])
                            if "choices" in data and data["choices"]:
                                content = data["choices"][0]["delta"].get("content", "")

                                if content.strip().startswith("```"):
                                    sys.stdout.writeline("\n")
                                    sys.stdout.flush()
                                    sys.stdout.write(content)
                                    sys.stdout.write("\n")
                                else:
                                    sys.stdout.write(content)

                                sys.stdout.flush()

                                if content:
                                    self.collected.append(content)

                        except json.JSONDecodeError:
                            continue

        except aiohttp.ClientError as client_error:
            logger.__ERROR__(f"Client connection error: {client_error}")        

        # final_response = "".join(self.collected).strip()
        # sys.stdout.write("\n\nFinal Response:\n" + final_response + "\n")
        sys.stdout.write("\n")
        sys.stdout.flush()

        
