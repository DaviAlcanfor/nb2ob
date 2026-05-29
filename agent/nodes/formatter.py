"""
Handles formatting of raw NotebookLM text into Obsidian markdown notes.
"""

import litellm as lt

lt.set_verbose = False
lt.suppress_debug_info = True

from agent.prompts.formatter import get_prompt
from config.settings import Config
from infrastructure.decorators import get_logger, log_call

logger = get_logger(__name__)


class Agent:
    def __init__(self, config: Config = None):

        if config is None:
            config = Config()

        self.model = config.agent_model
        self.api_key = config.agent_api_key
        self.prompt = get_prompt()


    @log_call
    def format_note(self, raw_text: str) -> str:

        response = lt.completion(
            model=self.model,
            api_key=self.api_key,
            max_tokens=8192,
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": raw_text}
            ]
        )

        return response.choices[0].message.content