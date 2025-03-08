
<div>
    <h1 align="center"> Slang <img src="slang/assets/elmo-logo.png" width="60px" height="60px"></h1> 
</div>

<p align="center"><em>A simple LLM collection for development/CLI</em></p>
<!-- <p align="center"> </p> -->

## About
<p>Slang alows you to send and customize your LLM form terminal [No Tokens Required]</p>


## Features

- **Easy to Use**: Simple commands to interact with various LLMs.
- **Customizable**: Modify prompts and parameters as needed.
- **Versatile**: Use as a CLI tool or integrate into your Python projects.

## Requirements

- Python 3.6 or higher

## Getting Started

### Prerequisites

Ensure you have Python 3.6 or higher installed. You can download it from [python.org](https://www.python.org/).

### Installation

1. **Create a virtual environment**:
    ```bash
    python3 -m venv myenv && source myenv/bin/activate
    ```

2. **Clone the repository and install the build**:
    ```bash
    git clone https://github.com/abdimk/Slang && cd Slang && pip install dist/slang-1.0.4-py3-none-any.whl 
    ```

    **or**

    **Install the dependencies**:
    ```bash
    cd Slang && pip install -U . && clear
    ```

## Usage

### CLI Usage

To use the LLM:
```bash
[GPT4,Claude3,Morphic,Llama,O3Mini]
python -m claude -c "prompt"
```

For Llama, specify the parameters:
```bash
[1B, 3B, 8B, 70B, 405B]
python -m claude -c "prompt" -m "8B"
```

### Python Package Usage

#### Using ClaudeAI From DuckDuckChat

```python
import asyncio
from slang.api import ClaudeAI
from scripts.typeffect import typeeffect

M = model_type.DuckModelType

async def main() -> str:
    async with DuckChat(M.Claude) as d1:
        response = await d1.ask_question("Tell me a fun fact about the moon")
        await typeeffect(response,0.02)


if __name__ == "__main__":
    asyncio.run(main())
```

#### Using Llama Models

```python
from slang.api import Llama_Models, ChatLlama, Llama

Lm = Llama_Models.Meta_Llama_3_2_1_70B_Instruct.value

async def Lamalight() -> None:
    async with ChatLlama("Tell me a joke", Lm) as lm1:
        response = await lm1.get_response()
        print(response)

async def LlamaBig() -> None:
    async with Llama("Tell me a Joke", Lm) as lm1:
        response = await lm1.get_response()
        print(response)

if __name__ == "__main__":
    asyncio.run(Llamalight())
    asyncio.run(LlamaBig())
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please open an issue or contact the repository owner.
