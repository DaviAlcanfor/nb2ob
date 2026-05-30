from enum import StrEnum
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from config.settings import Config

config = Config()

class Model(StrEnum):
    GEMINI_2_5_FLASH    = "gemini-2.5-flash"
    LLAMA_3_3_VERSATILE = "llama-3.3-70b-versatile"
    QWEN_2_5_PRO        = "qwen-2.5-pro"
    CLAUDE_HAIKU        = "claude-haiku-4-5"
    CLAUDE_SONNET       = "claude-sonnet-4-6"
    EMBEDDING_MODEL     = "gemini-embeddings-2-preview"
    


PROVIDER_MAP = {
    Model.GEMINI_2_5_FLASH:    "gemini",
    Model.LLAMA_3_3_VERSATILE: "groq",
    Model.QWEN_2_5_PRO:        "groq",
    Model.CLAUDE_HAIKU:        "claude",
    Model.CLAUDE_SONNET:       "claude",
}

API_KEYS = {
    "gemini": config.gemini_api_key,
    "groq":   config.groq_api_key,
    "claude": config.anthropic_api_key,
}

BUILDERS = {
    "gemini": ChatGoogleGenerativeAI,
    "groq":   ChatGroq,
    "claude": ChatAnthropic,
}