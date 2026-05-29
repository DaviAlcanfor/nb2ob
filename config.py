from dataclasses import dataclass, fields
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass
class Config:
    agent_model: str = os.getenv("AGENT_MODEL", "groq/llama-3.3-70b-versatile")
    agent_api_key: str = os.getenv("AGENT_API_KEY")

    obsidian_token: str = os.getenv("OBSIDIAN_TOKEN")
    obsidian_host: str = os.getenv("OBSIDIAN_HOST", "https://127.0.0.1")
    obsidian_port: int = int(os.getenv("OBSIDIAN_PORT", "27124"))


    def __post_init__(self):
        
        missing = [f.name for f in fields(self) 
                   if getattr(self, f.name) is None]
        
        if missing:
            raise EnvironmentError(f"\nMissing .env variables: {', '.join(missing)}")