from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()


_AGENT_MODEL = os.getenv("AGENT_MODEL", "gemini-2.0-pro")
_AGENT_API_KEY = os.getenv("AGENT_API_KEY")

_OBSIDIAN_TOKEN = os.getenv("OBSIDIAN_TOKEN")
_OBSIDIAN_PORT = int(os.getenv("OBSIDIAN_PORT", "27123"))
_OBSIDIAN_HOST = os.getenv("OBSIDIAN_HOST", "https://127.0.0.1")
_OBSIDIAN_PORT = int(os.getenv("OBSIDIAN_PORT", "27124"))


@dataclass
class Config:
    agent_model: str = _AGENT_MODEL
    agent_api_key: str = _AGENT_API_KEY 

    obsidian_token: str = _OBSIDIAN_TOKEN
    obsidian_host: str = _OBSIDIAN_HOST
    obsidian_port: int = _OBSIDIAN_PORT