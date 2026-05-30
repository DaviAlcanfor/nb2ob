from dataclasses import dataclass, fields
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass
class Config:
    # Obsidian
    obsidian_token: str = os.getenv("OBSIDIAN_TOKEN")
    obsidian_host: str = os.getenv("OBSIDIAN_HOST", "https://127.0.0.1")
    obsidian_port: int = int(os.getenv("OBSIDIAN_PORT", "27124"))
    obsidian_folder: str = os.getenv("OBSIDIAN_FOLDER", "NotebookLM")
    
    # LLM Providers
    gemini_api_key: str = os.getenv("GEMINI_API_KEY")
    groq_api_key: str = os.getenv("GROQ_API_KEY")
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY")


    def __post_init__(self):

        obsidian_missing = [f.name for f in fields(self)
                            if getattr(self, f.name) is None
                            and f.name.startswith("obsidian")]
        
        no_agent_key = not any(
            getattr(self, f.name) is not None
            for f in fields(self)
            if f.name.endswith("api_key")
        )
        
        errors = []
        
        if obsidian_missing:
            errors.append(f"Missing Obsidian vars: {', '.join(obsidian_missing)}")
        
        if no_agent_key:
            errors.append("At least one API key is required (gemini_api_key, groq_api_key, anthropic_api_key)")
        
        if errors:
            raise EnvironmentError("\n" + "\n".join(errors))