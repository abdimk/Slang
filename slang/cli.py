import typer
import asyncio
import sys
from typing import Optional
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
from rich.markdown import Markdown
from rich.spinner import Spinner
from rich.live import Live
from rich.table import Table
from rich import box

from slang.api import ClaudeAI,GeminiPro
from slang.api import QwenCoder,Llama,Morphic,GPT4,ChatLlama
from slang.api import DuckChat,model_type,Llama_Models


M = model_type.DuckModelType


console = Console()

app = typer.Typer()



@app.command()
def main() -> None:
    """Default command."""
    try:
        message = Text("Slang CLI: https://github.com/abdimk/Slang\n Abdisa Merga 2024", style="bold green")
        panel = Panel(message, title="Welcome", subtitle="Powered by Rich CLI", expand=False)
        console.print(panel)
    
    except Exception as e:
        error_message = Text(f"An error occurred: {str(e)}", style="bold red")
        error_panel = Panel(
            error_message, 
            title="Error", 
            border_style="red", 
            expand=False
        )
        console.print(error_panel)
        console.print_exception()
@app.command()
def about(all: Optional[bool] = typer.Option(False, "-all", help="Shows details about the CLI")) -> None:
    """
    Display detailed information about Slang CLI and its models.
    """
    console.print(Panel(
        Text("Slang CLI - LLM CLI Wrapper", style="bold green"),
        title="About",
        border_style="green"
    ))

    table = Table(
        title="Slang AI Models Overview",
        show_header=True,
        header_style="bold magenta",
        box=box.DOUBLE
    )

    table.add_column("Model", style="cyan")
    table.add_column("Description", style="green")
    table.add_column("Capabilities", style="yellow")
    table.add_column("Status", style="bold")

    table.add_row(
        "Claude 3 Haiku", 
        "Advanced AI by Anthropic", 
        "Conversational, Code, Analysis", 
        "[green]Active[/green]"
    )
    table.add_row(
        "Llama 3.1", 
        "Open-source LLM by Meta", 
        "General Purpose, Multilingual", 
        "[green]Active[/green]"
    )
    table.add_row(
        "o3Mini", 
        "Large Language Model by Open AI", 
        "Multilingual, Coding", 
        "[green]Active[/green]"
    )
    table.add_row(
        "Morphic", 
        "Specialized AI Model", 
        "Research, Specific Domains", 
        "[yellow]Limited Access[/yellow]"
    )

    console.print(table)

    # Additional details if -all flag is used
    if all:
        console.print(Panel(
            Text(
                "Slang CLI provides a unified interface to interact with multiple AI models. "
                "Each model offers unique capabilities and strengths for different use cases.",
                style="italic"
            ),
            title="Additional Information",
            border_style="blue"
        ))
            



@app.command()
def morphic(query: str = typer.Option(..., "-c", "--command",help="The query to send to Morphic")) -> None:
    """
    Send a query to Morphic search engine 
    """

    async def run_query():
        try:
            with console.status("[bold white] Morphic[/bold white]", spinner="dots"):
                async with Morphic(query) as m1:
                    response = await m1.make_request()

                markdown_content = Markdown(response)
                panel = Panel(
                    markdown_content,
                    title="Morphic",
                    border_style="red",
                    expand=True
                )

                console.print(panel)
        except Exception as e:
            error_panel = Panel(
                Text(f"Error: {str(e)}", style="bold red"),
                title="Error",
                border_style="red",
                expand=False
            )
            console.print(error_panel)

    
    asyncio.run(run_query())

@app.command()
def claude(query:str = typer.Option(..., "-c", "--command", help="Make a request to claude 3 Haiku from duck duck model")) -> None:
    """
    Send a query to Claude 3 Haiku
    """
    model = M.Claude
    async def run_query():
        try: 
            with console.status(f"[bold white] {model.value}[/bold white]", spinner="dots"):
                async with DuckChat(model) as d1:
                    response = await d1.ask_question(query)


                    markdown_content = Markdown(response)
                    panel = Panel(
                        markdown_content,
                        title=f"{model.value}",
                        border_style="red",
                        expand=True
                    )
                    console.print(panel)

        except Exception as e:
            error_panel = Panel(
                Text(f"Error: {str(e)}",style="bold red"),
                title="Error",
                border_style="red",
                expand=False
            )
            
            console.print(error_panel)

    asyncio.run(run_query())


@app.command()
def o3mini(query:str = typer.Option(..., "-c", "--command", help="Make a request to o3 Mini from duck duck model")) -> None:
    """
    Send a query to o3 Mini
    """
    model = M.o3Mini
    async def run_query():
        try: 
            with console.status(f"[bold white] {model.value}[/bold white]", spinner="dots"):
                async with DuckChat(model) as d1:
                    response = await d1.ask_question(query)


                    markdown_content = Markdown(response)
                    panel = Panel(
                        markdown_content,
                        title=f"{model.value}",
                        border_style="red",
                        expand=True
                    )
                    console.print(panel)

        except Exception as e:
            error_panel = Panel(
                Text(f"Error: {str(e)}",style="bold red"),
                title="Error",
                border_style="red",
                expand=False
            )
            
            console.print(error_panel)

    asyncio.run(run_query())

@app.command()
def llama(query: str = typer.Option(..., "-c", "--command",help="The query to send to Llama Light"),
         model: str = typer.Option("8B", "-m", "--model", help="The model to use, e.g., [1B,3B,8B,70B]")
         ) -> None:
    """
    Send a query to Llama with from 1B - 70Bparameters
    """
    lm = Llama_Models

    # Create a mapping of model values to their corresponding Llama_Models attributes
    model_mapping = {
        "1B": lm.Meta_Llama_3_2_1B_Instruct.value,
        "3B": lm.Meta_Llama_3_2_3B_Instruct.value,
        "8B": lm.Meta_Llama_3_2_1_8B_Instruct.value,
        "70B": lm.Meta_Llama_3_2_1_70B_Instruct.value,
        "405B": lm.Meta_Llama_3_2_1_405B_Instruct.value,
        "gpt4":lm.GPT4o.value
    }


    lm = model_mapping.get(model, lm.Meta_Llama_3_2_1_8B_Instruct.value)
    async def run_query():
        try:
            with console.status(f"[bold white] {lm}[/bold white]", spinner="dots"):
                async with ChatLlama(query,lm) as q1:
                    response = await q1.get_response()

                markdown_content = Markdown(response)
                panel = Panel(
                    markdown_content,
                    title=f"{model}",
                    border_style="red",
                    expand=True
                )

                console.print(panel)
        except Exception as e:
            error_panel = Panel(
                Text(f"Error: {str(e)}", style="bold red"),
                title="Error",
                border_style="red",
                expand=False
            )
            console.print(error_panel)

    
    asyncio.run(run_query())


if __name__ == "__main__":
    app()