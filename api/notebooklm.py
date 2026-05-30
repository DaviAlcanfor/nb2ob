"""
NotebookLM API wrapper for listing notebooks and extracting content.
"""

import asyncio
from notebooklm import NotebookLMClient
from typing import List, TypedDict

from infrastructure.decorators import get_logger, log_call

logger = get_logger(__name__)

class Sources(TypedDict):
    id: str
    title: str
    content: str

class Notebook(TypedDict):
    id: str
    title: str
    sources_count: int
    sources: List[Sources]


# Possible to replace the 
# `async with NotebookLMClient.from_storage() as client:` 
# repetition with a function or dependency injection at the class
class NotebookLMAPI:

    @log_call
    async def _fetch_notebooks(self) -> List[Notebook]:
        """
        Fetch all notebooks from the user 
        
        Returns:
            NotebookList: list[Notebook] - list with all the notebooks
        """
        
        async with NotebookLMClient.from_storage() as client:
            NotebookList: list[Notebook] = []
            notebooks = await client.notebooks.list()
        
            for nb in notebooks:
                logger.info(f"Extracting: {nb.title}")
                
                NotebookList.append({
                    "id": nb.id,
                    "title": nb.title,
                    "sources_count": nb.sources_count
                })

        return NotebookList
        
    
    @log_call
    async def _fetch_sources(self, notebook_id: str) -> List[Sources]:
        """
        Fetch the sources from the user
        
        Args: 
            notebook_id: str
            
        Returns:
            SourcesList: List[Sources] - list of all sources object
        """
        
        async with NotebookLMClient.from_storage() as client:
            sources = await client.sources.list(notebook_id)
            
            SourcesList: list[Sources] = []
            for sr in sources:
                fulltext = await client.sources.get_fulltext(notebook_id, sr.id)
                
                SourcesList.append({
                    "id": sr.id,
                    "title": sr.title,
                    "content": fulltext.content
                })
        
        return SourcesList
    
    @log_call
    async def _fetch_all(self) -> List[Notebook]:
        """
        Fetchs both the notebook with the sources inputed
        
        Returns:
            NotebookList: List[Notebook] - list of notebook with sources inputed
        """
        
        notebooks = await self._fetch_notebooks()
        
        for nb in notebooks:
            sources = await self._fetch_sources(nb["id"])
            nb["sources"] = sources
        
        return notebooks
        
        

    def list_notebooks(self) -> list[dict]:
        return asyncio.run(self._fetch_notebooks())
    
    def list_sources(self, notebook_id) -> list[dict]:
        return asyncio.run(self._fetch_sources(notebook_id))

    def list_notebook_sources(self) -> list[dict]:
        return asyncio.run(self._fetch_all())