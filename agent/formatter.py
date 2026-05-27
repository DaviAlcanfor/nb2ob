"""
Handles formatting of raw NotebookLM text into Obsidian markdown notes.
"""

import litellm as lt
lt._turn_on_debug()
# from litellm import completion

from agent.prompt import get_prompt
from config import Config


class Agent:
    def __init__(self, config: Config = None):

        if config is None:
            config = Config()

        self.model = config.agent_model
        self.api_key = config.agent_api_key
        self.prompt = get_prompt()


    def format_note(self, raw_text: str) -> str:

        response = lt.completion(
            model=self.model,
            api_key=self.api_key,
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": raw_text}
            ]
        )

        return response.choices[0].message.content