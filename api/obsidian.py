"""
Obsidian API wrapper for sending notes.

This module defines the `ObsidianAPI` class, which provides a method to send formatted markdown notes to an Obsidian
vault using the Obsidian API. The class handles authentication and constructs the appropriate HTTP requests to create 
or update notes in the vault.
"""

import requests

from config.settings import Config
from infrastructure.decorators import log_call

class ObsidianAPI:
    _STATUS_SUCCESS = 204

    def __init__(self, config: Config = None):
    
        if config is None:
            config = Config()

        self.token = config.obsidian_token
        self.folder = config.obsidian_folder
        
        self.api_url = f"{config.obsidian_host}:{config.obsidian_port}/vault/"

    @log_call
    def send_to_obsidian(
            self,
            note_title: str, 
            note_content: str
        ) -> bool:

        URL = f"{self.api_url}{self.folder}/{note_title}.md"

        response = requests.put(
            URL, 
            headers= {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "text/markdown",
            }, 
            data=note_content.encode("utf-8"), 
            verify=False
        )
        
        return response.status_code == self._STATUS_SUCCESS
        
