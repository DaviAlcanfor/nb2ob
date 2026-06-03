from enum import StrEnum
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_cerebras import ChatCerebras
from langchain_openai import ChatOpenAI


from config.settings import Config

config = Config()

class Model(StrEnum):
    GEMINI_2_5_FLASH    = "gemini-2.5-flash"
    LLAMA_3_3_VERSATILE = "llama-3.3-70b-versatile"
    QWEN_2_5_PRO        = "qwen-2.5-pro"
    CLAUDE_HAIKU        = "claude-haiku-4-5"
    CLAUDE_SONNET       = "claude-sonnet-4-6"
    LLAMA_3_3_CEREBRAS  = "llama-3.3-70b"         
    DEEPSEEK_V3_FREE    = "deepseek/deepseek-chat-v3-0324:free"  
    


PROVIDER_MAP = {
    Model.GEMINI_2_5_FLASH:    "gemini",
    Model.LLAMA_3_3_VERSATILE: "groq",
    Model.QWEN_2_5_PRO:        "groq",
    Model.CLAUDE_HAIKU:        "claude",
    Model.CLAUDE_SONNET:       "claude",
    Model.LLAMA_3_3_CEREBRAS:  "cerebras",
    Model.DEEPSEEK_V3_FREE:    "openrouter",
}

API_KEYS = {
    "gemini": config.gemini_api_key,
    "groq":   config.groq_api_key,
    "claude": config.anthropic_api_key,
    "cerebras":   config.cerebras_api_key,
    "openrouter": config.openrouter_api_key,
}

BUILDERS = {
    "gemini": ChatGoogleGenerativeAI,
    "groq":   ChatGroq,
    "claude": ChatAnthropic,
    "cerebras":   ChatCerebras,
    "openrouter": ChatOpenAI,  # OpenRouter é compatível com OpenAI
}