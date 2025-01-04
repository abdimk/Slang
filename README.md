<div>
    <h1 align="center"> Slang <img src="slang/assets/elmo-logo.png" width="60px" height="60px"></h1> 
</div>

<p align="center"><em>A simple LLM Wrapper/CLI</em></p>
<!-- <p align="center"> </p> -->

## About
<p>Slang alows you to send and customize your LLM form terminal [No Tokens Required]</p>


- This is in the early stages, so you might experience some issues.
- This is not for commercial use and barely works!
- A lot of refactoring is still expected as this is part of my final year project.

<h2>Installation</h2>

### Create a virtual python enviroment
```bash
python3 -m venv myenv && source myenv/bin/activate
```

### Clone the repository
```bash
git clone https://github.com/abdimk/Slang && pip install dist/slang-0.6-py3-none-any.whl 
```

### Install the dependencies
```bash
cd Slang && pip install -U . && clear
```

<h2>Usage</h2>

### To use the LLM
```bash
[claude,morphic,qwen]
python -m claude -c "prompt"
```

### For Llama you need to specify the paramters
```bash
[1B, 3B, 8B, 70B]
python -m claude -c "prompt" -m "8B"
```


<h3>Use as a package</h3>

```python
import asyncio
from slang.api import AskChat,Chatx,NextChat,Morphic
from slang.api import Llama,QwenCoder
from slang.api import ClaudeAI
from slang.api import ChatLlama
from scripts.typeffect import typeeffect


#To use ClaudeAI
async def main()->None:
    async with ClaudeAI("prompt",system_prompt="",maxTokens=1024) as cld:
        response = await cld.get_response()
        print(response)
        #for typer effect
        await typeeffect(response)

if __name__ =="__main__":
    asyncio.run(main())
```

<h3> Using Llama Models </h3>

```python
from slang.api import Llama_Models
from slang.api import ChatLlama
from slang.api import Llama # 405B
"""
You can choose between [1B, 3B, 8B, 70B, 405B] parameters
"""
Lm = Llama_Models.Meta_Llama_3_2_1_70B_Instruct.value #Choose from the given models 


async def Lamalight()->None:
    async with ChatLlama("Tell me a joke",Lm) as lm1:
        response = await lm1.get_response()
        print(response)


# To use 405B parameters
async def LlamaBig()->None:
    async with Llama("Tell me a Joke",Lm) as lm1:
        response = await lm1.get_response()
        print(response)


if __name__ =="__main__":
    asyncio.run(Lamalight())
    asyncio.run(LlamaBig())

```
