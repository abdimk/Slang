import asyncio
import sys
import re 

from slang.api import DuckChat,model_type,Llama_Models
from slang.api import AskChat,Chatx,NextChat,Morphic

from slang.api import Llama,QwenCoder
from slang.api import ClaudeAI
from slang.api import ChatLlama
from scripts.execute import execute_command

M = model_type.DuckModelType
Lm = Llama_Models.Meta_Llama_3_2_1_70B_Instruct.value

async def main():
    async with ChatLlama("what is your model",Lm) as lm1:
        response = await lm1.get_response()
        print(response)

# async def main():
#     async with Morphic("") as l1:
#         response = await l1.get_response()
#         await typeeffect(response,0.0001)


# async def main():
#     async with ClaudeAI("what is my name")as l1:
#         response = await l1.get_response()
#         print(response)

# #Llama QewnCoder parameters 
# async def main():
#     async with QwenCoder("write a simple hello world in go") as l1:
#         response = await l1.get_response()
#         await typeeffect(response,0.03)


# #Llama 405B parameters 
# async def main():
#     async with Llama("john the ripper") as l1:
#         response = await l1.get_response()
#         await typeeffect(response,0.03)




# async def main():
#     async with Morphic("john the ripper") as m1:
#         response = await m1.make_request()
#         print(response)
        # await typeeffect(response,0.03)



# query = "what is your model"
# async def main() -> str:
#     async with DuckChat(M.Claude) as d1:
#         response = await d1.ask_question(query)
#         print(response)
#         # response = remove_markdown_formatting(response)
#         # await typeeffect(response,0.02)



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
   #translated = Lesan(answer).translate("am")
#    await typeeffect(answer, 0.02)



#Chat X

# query = input("Your question:")
# async def main(query: str)->str:
#     chat_instance = Chatx(query)
#     answer = await chat_instance.fetch_chat()
#     #translated = Lesan(answer).translate("am")
#     await typeeffect(answer, 0.02)

    

if __name__ == "__main__":
    asyncio.run(main())
