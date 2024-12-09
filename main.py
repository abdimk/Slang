import asyncio
import sys
import re 

from slang.api import DuckChat,model_type
from slang.api import AskChat
M = model_type.ModelType

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


# async def main(question: str = "") -> str:
#     print(f"Question: {question}")
#     async with DuckChat(M.GPT4o_Mini) as d1:
#         response = await d1.ask_question(question)
#         response = remove_markdown_formatting(response)
#         await typeeffect(response,0.02)

query = input("Your question:")
async def main(query:str)->str:
    chat_instance = AskChat(query)
    answer = await chat_instance.get_answer()
    print(answer)
    
    

if __name__ == "__main__":
    asyncio.run(main(query))