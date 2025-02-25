from enum import Enum


class DuckModelType(Enum):
    GPT4o_Mini = "gpt-4o-mini"
    Claude = "claude-3-haiku-20240307"
    Llama3o1 = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
    Mixtral = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    o3Mini = "o3-mini"

class DefaultModels(Enum):
    GPT4o_Full = "gpt-4o",
    GPT35o_Turbo = "gpt3.5-turbo"

class LlamaModels(Enum):
    Meta_Llama_3_2_1B_Instruct = "Meta-Llama-3.2-1B-Instruct"
    Meta_Llama_3_2_3B_Instruct = "Meta-Llama-3.2-3B-Instruct"
    Meta_Llama_3_2_1_8B_Instruct = "Meta-Llama-3.1-8B-Instruct"
    Meta_Llama_3_2_1_70B_Instruct = "Meta-Llama-3.1-70B-Instruct"


class DeepSeek(Enum):
    Deep_Seek_R1 = "deepseek-ai/DeepSeek-R1"
    Deep_Seek_v3 = "deepseek-ai/DeepSeek-v3"
    Deep_Seek_Distill_Llama_70B = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B"




    