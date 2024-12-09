from enum import Enum


class ModelType(Enum):
    GPT4o_Mini = "gpt-4o-mini"
    GPT4o_Full = "gpt-4o",
    GPT35o_Turbo = "gpt3.5-turbo"
    Claude = "claude-3-haiku-20240307"
    Llama3o1 = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
    Mixtral = "mistralai/Mixtral-8x7B-Instruct-v0.1"


    