"""
Obsidian API wrapper for sending notes.

This module defines the `ObsidianAPI` class, which provides a method to send formatted markdown notes to an Obsidian
vault using the Obsidian API. The class handles authentication and constructs the appropriate HTTP requests to create 
or update notes in the vault.
"""

import requests
from config import Config

CONFIG = Config()


_OBSIDIAN_HOST = CONFIG.obsidian_host
_OBSIDIAN_PORT = CONFIG.obsidian_port
_OBSIDIAN_TOKEN = CONFIG.obsidian_token

_API_URL = f"{_OBSIDIAN_HOST}:{_OBSIDIAN_PORT}/vault/"


class ObsidianAPI:
    _STATUS_SUCCESS = 200

    def __init__(self):
        self.token = _OBSIDIAN_TOKEN
        self.api_url = _API_URL


    def send_to_obsidian(
            self,
            note_title: str, 
            note_content: str
        ) -> bool:

        URL = f"{self.api_url}{note_title}.md"

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
        
