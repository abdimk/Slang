from types import TracebackType
from typing import AsyncGenerator, Self

import aiohttp
import msgspec
from fake_useragent import UserAgent
## Import the exceptions
from slang.exceptions import(
    ConversationLimitException,
    DuckChatException,
    RatelimitException
)

import asyncio
import gzip
import zlib
import brotli
import chardet
from slang.models import model_type,models

Generative_Models = model_type.ModelType


"""
To do 


Historical Data Analysis
Term selection
quick recap
"""

class AskChat:
    def __init__(self, query: str):
        self.url = "https://www.teach-anything.com/api/generate"
        self.query = query
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

        self.payload = {
            "prompt": f"{self.query}\nYou are ChatGPT, a large language model trained by OpenAI.\n"
                      "Knowledge cutoff: 2024-10\n"
                      "Current model: gpt-4o\n"
                      "Current time: Sat Dec 07 2024 13:58:28 GMT+0300 (East Africa Time)\n"
                      "Latex inline: \\(x^2\\)\n"
                      "Latex block: $$e=mc^2$$\n"
        }

        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Origin": "https://www.teach-anything.com",
            "Referer": "https://www.teach-anything.com/",
            "User-Agent": self.user_agent,
        }

    async def get_answer(self) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, headers=self.headers, json=self.payload) as response:
                if response.status == 200:
                    encoding = response.headers.get('Content-Encoding', '').lower()
                    response_data = await response.read()

                    # Handle compression
                    if 'gzip' in encoding:
                        response_data = gzip.decompress(response_data)
                    elif 'deflate' in encoding:
                        response_data = zlib.decompress(response_data)
                    elif 'br' in encoding:
                        response_data = brotli.decompress(response_data)

                    # Detect encoding and decode response
                    detected = chardet.detect(response_data)
                    detected_encoding = detected.get('encoding', 'utf-8')  # Use 'utf-8' as default if unknown
                    try:
                        response_body = response_data.decode(detected_encoding)
                    except (UnicodeDecodeError, LookupError):
                        # Fallback to Latin-1 if decoding fails
                        response_body = response_data.decode('latin1')

                    return response_body
                else:
                    return f"Request failed with status {response.status}"

    # # Standalone function for testing
    # async def send_request():
    #     question = "What is your name?"
    #     chat_instance = AskChat(query=question)
    #     response = await chat_instance.get_answer()
    #     return f"Response:, {response}"


class DuckChat:
    def __init__(self,model: model_type.ModelType = Generative_Models.GPT4o_Full,
                 session:aiohttp.ClientSession | None = None,
                 user_agent: UserAgent | str = UserAgent(min_version=120.0)) -> None:
        if type(user_agent) is str:
            self.user_agent = user_agent

        else:
            self.user_agent = user_agent.random # type: ignore

        self._session = session or aiohttp.ClientSession(
            headers={
                "Host": "duckduckgo.com",
                "Accept": "text/event-stream",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://duckduckgo.com/",
                "User-Agent": self.user_agent,
                "DNT": "1",
                "Sec-GPC": "1",
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "TE": "trailers",
            }
        )

        self.vqd: list[str] = []
        self.history = models.History(model, [])
        self.__encoder = msgspec.json.Encoder()
        self.__decoder = msgspec.json.Decoder()

    async def __aenter__(self) -> Self:
        return self
    
    async def __aexit__(
            self,
            exc_type: type[BaseException] | None = None,
            exc_value: BaseException | None = None,
            traceback: TracebackType | None = None,
    ) -> None:
        
        await self._session.__aexit__(exc_type,exc_value,traceback)

    # Generate a new x-vqd-4 Token
    async def get_vqd(self) -> None:
        """Get new x-vqd-4 token"""
        async with self._session.get(
            "https://duckduckgo.com/duckchat/v1/status", headers={"x-vqd-accept": "1"}
        ) as response:
            if response.status == 429:
                res = await response.read()
                try:
                    err_message = self.__decoder.decode(res).get("type", "")
                except Exception:
                    raise DuckChatException(res.decode())
                else:
                    raise RatelimitException(err_message)
            if "x-vqd-4" in response.headers:
                self.vqd.append(response.headers["x-vqd-4"])
            else:
                raise DuckChatException("No x-vqd-4")
            
    async def get_answer(self) -> str:
        """Get message answer from chatbot"""
        async with self._session.post(
            "https://duckduckgo.com/duckchat/v1/chat",
            headers={
                "Content-Type": "application/json",
                "x-vqd-4": self.vqd[-1],
            },
            data=self.__encoder.encode(self.history),
        ) as response:
            res = await response.read()
            if response.status == 429:
                raise RatelimitException(res.decode())
            try:
                data = self.__decoder.decode(
                    b"["
                    + b",".join(
                        res.lstrip(b"data: ").rstrip(b"\n\ndata: [DONE][LIMIT_CONVERSATION]\n").split(b"\n\ndata: ")
                    )
                    + b"]"
                )
            except Exception:
                raise DuckChatException(f"Couldn't parse body={res.decode()}")
            message = []
            for x in data:
                if x.get("action") == "error":
                    err_message = x.get("type", "") or str(x)
                    if x.get("status") == 429:
                        if err_message == "ERR_CONVERSATION_LIMIT":
                            raise ConversationLimitException(err_message)
                        raise RatelimitException(err_message)
                    raise DuckChatException(err_message)
                message.append(x.get("message", ""))
        self.vqd.append(response.headers.get("x-vqd-4", ""))
        return "".join(message)
    
    async def ask_question(self, query: str) -> str:
        """Get answer from chat AI"""
        if not self.vqd:
            await self.get_vqd()
        self.history.add_input(query)

        message = await self.get_answer()

        self.history.add_answer(message)
        return message

    async def reask_question(self, num: int) -> str:
        """Get re-answer from chat AI"""

        if num >= len(self.vqd):
            num = len(self.vqd) - 1
        self.vqd = self.vqd[:num]

        if not self.history.messages:
            return ""

        if not self.vqd:
            await self.get_vqd()
            self.history.messages = [self.history.messages[0]]
        else:
            num = min(num, len(self.vqd))
            self.history.messages = self.history.messages[: (num * 2 - 1)]
        message = await self.get_answer()
        self.history.add_answer(message)

        return message

    async def stream_answer(self) -> AsyncGenerator[str, None]:
        """Stream answer from chatbot"""
        async with self._session.post(
            "https://duckduckgo.com/duckchat/v1/chat",
            headers={
                "Content-Type": "application/json",
                "x-vqd-4": self.vqd[-1],
            },
            data=self.__encoder.encode(self.history),
        ) as response:
            if response.status == 429:
                raise RatelimitException(await response.text())
            try:
                async for line in response.content:
                    if line.startswith(b"data: "):
                        chunk = line[6:]
                        if chunk.startswith(b"[DONE]"):
                            break
                        try: 
                            data = self.__decoder.decode(chunk)
                            if "message" in data and data["message"]:
                                yield data["message"]
                        except Exception:
                            raise DuckChatException(f"Couldn't parse body={chunk.decode()}")
            except Exception as e:
                raise DuckChatException(f"Error while streaming data: {str(e)}")
        self.vqd.append(response.headers.get("x-vqd-4", ""))

    async def ask_question_stream(self, query: str) -> AsyncGenerator[str, None]:
        """Stream answer from chat AI"""
        if not self.vqd:
            await self.get_vqd()
        self.history.add_input(query)

        message_list = []
        async for message in self.stream_answer():
            yield message
            message_list.append(message)

        self.history.add_answer("".join(message_list))

    async def reask_question_stream(self, num: int) -> AsyncGenerator[str, None]:
        """Stream re-answer from chat AI"""

        if num >= len(self.vqd):
            num = len(self.vqd) - 1
        self.vqd = self.vqd[:num]

        if not self.history.messages:
            raise GeneratorExit("There is no history messages")

        if not self.vqd:
            await self.get_vqd()
            self.history.messages = [self.history.messages[0]]
        else:
            num = min(num, len(self.vqd))
            self.history.messages = self.history.messages[: (num * 2 - 1)]

        message_list = []
        async for message in self.stream_answer():
            yield message
            message_list.append(message)

        self.history.add_answer("".join(message_list))



