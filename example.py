import asyncio
import sys
import re 

from slang.api import DuckChat,model_type,Llama_Models
from slang.api import AskChat,Chatx,NextChat,Morphic

from slang.api import Llama,QwenCoder
from slang.api import ClaudeAI
from slang.api import ChatLlama
# from scripts.execute import execute_command
from scripts.typeffect import typeeffect
M = model_type.DuckModelType
Lm = Llama_Models.Meta_Llama_3_2_1_70B_Instruct.value



# async def Llamalight():
#     async with ChatLlama("what is your model",Lm) as lm1:
#         response = await lm1.get_response()
#         print(response)



# async def main():
#     async with Morphic("what do you know about clerk authentication") as l1:
#         response = await l1.make_request()
#         await typeeffect(response,0.0001)


# async def main()->str: [Need to sign in to access the service]
#     async with ClaudeAI("Define a tesseract")as l1:
#         response = await l1.get_response()
#         await typeeffect(response)



#Llama QewnCoder parameters [Service has been deprecated]
# async def main():
#     async with QwenCoder("write a simple hello world in go") as l1:
#         response = await l1.get_response()
#         await typeeffect(response,0.03)



# Llama 405B parameters [Service has been deprecated]
# async def main():
#     async with Llama("john the ripper") as l1:
#         response = await l1.get_response()
#         print(response)
#         await typeeffect(response,0.03)

# from langchain_experimental.tools import PythonREPLTool
# code_exec_tool = PythonREPLTool()



# async def main() -> str:
#     async with DuckChat(M.o3Mini) as d1:
#         response = await d1.ask_question("Write a Python function to calculate the factorial of a number OUTPUT ONLY THE CODE")
#         result = code_exec_tool.run(response)
#         exec(result)
#         await typeeffect(response,0.02)

#         factorial_result = eval("factorial(5)") 
#         print(factorial_result)


# query = "what is your model"
# async def main()->str:
#     chat_instance = AskChat(query)
#     answer = await chat_instance.get_answer()
#     print(answer)
    

# query = "what is your model"
# async def main()->str:
#    chat_instance = NextChat(query)
#    answer = await chat_instance.fetch_chat()
#    print(answer)
   


#Chat X

# query = input("Your question:")
# async def main(query: str)->str:
#     chat_instance = Chatx(query)
#     answer = await chat_instance.fetch_chat()
#     #translated = Lesan(answer).translate("am")
#     await typeeffect(answer, 0.02)


# from slang.deepseek import DeepSeek
# from slang.models import model_type





# deepseekR1 = model_type.DeepSeek.Deep_Seek_R1.value

# # query = input("write your prompt:")
# async def main():
#     async with DeepSeek(f"{query}",deepseekR1) as m:
#         await m.get_response()



# if __name__ == "__main__":
#     asyncio.run(main())

