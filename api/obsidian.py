"""
Obsidian API wrapper for sending notes.

This module defines the `ObsidianAPI` class, which provides a method to send formatted markdown notes to an Obsidian
vault using the Obsidian API. The class handles authentication and constructs the appropriate HTTP requests to create 
or update notes in the vault.
"""

import requests
import typer
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from config.settings import Config
from infrastructure.decorators import log_call
from infrastructure.config import get_logger


log = get_logger(__name__)

class ObsidianAPI:
    _STATUS_SUCCESS = 204

    def __init__(self, config: Config = None):
    
        if config is None:
            config = Config()

        self.token = config.obsidian_token
        self.folder = config.obsidian_folder
        
        self.base_url = f"{config.obsidian_host}:{config.obsidian_port}"
        self.api_url  = f"{self.base_url}/vault/"
        
    
    def is_running(self) -> bool:
        """
        Checks if Obsidian is open and the Local REST API plugin is active.

        Returns:
            bool: True if reachable, False otherwise
        """
        try:
            response = requests.get(
                self.base_url,
                headers={"Authorization": f"Bearer {self.token}"},
                verify=False,
                timeout=3,
            )
            return response.status_code == 200
        
        except requests.ConnectionError:
            return False    
        

    @log_call
    def send_to_obsidian(
            self,
            notebook_title: str,
            note_title: str, 
            note_content: str
        ) -> bool:
        
        log.info(f"Sending {notebook_title} to obsidian")
        
        URL = f"{self.api_url}{self.folder}/{notebook_title}/{note_title}.md"

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
        

    def check_or_exit(self) -> None:
        """
        Checks if Obsidian is running. Exits the CLI if not.
        """
        if not self.is_running():
            typer.echo("Obsidian is not running. Open Obsidian and enable the Local REST API plugin.")
            raise typer.Exit(code=1)