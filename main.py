import asyncio
import sys
import re 

from slang.api import DuckChat,model_type
from slang.api import AskChat,Chatx,NextChat,Morphic
from lang.lesan import Lesan
from slang.api import Llama,QwenCoder
from slang.api import ClaudeAI

M = model_type.DuckModelType

async def typeeffect(text: str, delay: float = 0.04):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        
        await asyncio.sleep(delay)
    
    sys.stdout.write("\n")


# trying to remove the ** starts that look a annoying as hell
def remove_markdown_formatting(text: str) -> str:
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text) 
    text = re.sub(r'\*(.*?)\*', r'\1', text)   

    return text


Custom_query = {
    'prompt':'',
    "filter":"",
    "exporeHttp":'',
    "systemDate":"",
    "disabledTopics":[],
    "transformerModels":""
}


# async def main():
#     async with Morphic("") as l1:
#         response = await l1.get_response()
#         await typeeffect(response,0.0001)



async def main():
    async with ClaudeAI("what is your model") as l1:
        response = await l1.get_response()
        print(response)



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
#         await typeeffect(response,0.03)



# query = input("Your question:")
# async def main(question: str = "") -> str:
#     async with DuckChat(M.GPT4o_Mini) as d1:
#         response = await d1.ask_question(question)
#         response = remove_markdown_formatting(response)
#         await typeeffect(response,0.02)


#AskChat
# query = input("Your question:")
# async def main(query:str)->str:
#     chat_instance = AskChat(query)
#     answer = await chat_instance.get_answer()
#     await typeeffect(answer, 0.02)
    
#query = input("Your question:")
#async def main(query: str)->str:
#    chat_instance = NextChat(query)
#    answer = await chat_instance.fetch_chat()
#    #translated = Lesan(answer).translate("am")
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
