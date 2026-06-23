"""
NotebookLM API wrapper for listing notebooks and extracting content.
"""

import asyncio
from notebooklm import NotebookLMClient
from typing import List

import typer

from api._types import Notebook, Sources, SummarizedSource
from api._cleaning import _clean_content
from api._summarizer import _build_summary_prompt, _parse_summaries
from infrastructure.decorators import get_logger, log_call

logger = get_logger(__name__)

DELAY_BETWEEN_SOURCES = 2
DELAY_BETWEEN_NOTEBOOKS = 4


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
                logger.info(f"Fetching source: {sr.title}")
                
                fulltext = await client.sources.get_fulltext(notebook_id, sr.id)
                await asyncio.sleep(DELAY_BETWEEN_SOURCES)
                
                SourcesList.append({
                    "id": sr.id,
                    "title": sr.title,
                    "content": _clean_content(fulltext.content)
                })
        
        return SourcesList
    
    @log_call
    async def _fetch_all(self, notebook_name: str | None = None) -> List[Notebook]:
        notebooks = await self._fetch_notebooks()

        if notebook_name:
            notebooks = [nb for nb in notebooks if nb["title"] == notebook_name]

            if not notebooks:
                typer.echo(f"Notebook '{notebook_name}' not found.")
                raise typer.Exit(code=1)

        for nb in notebooks:
            sources = await self._fetch_sources(nb["id"])
            nb["sources"] = sources
            nb["summaries"] = await self._summarize_sources(nb["id"], sources)
            await asyncio.sleep(DELAY_BETWEEN_NOTEBOOKS)

        return notebooks
            

    async def _ask_notebook(self, notebook_id: str, prompt: str) -> str:
        async with NotebookLMClient.from_storage() as client:
            result = await client.chat.ask(notebook_id, prompt)
        return result.answer

    @log_call
    async def _summarize_sources(self, notebook_id: str, sources: List[Sources]) -> List[SummarizedSource]:
        """
        Summarizes all sources in a single chat.ask call per notebook.

        Args:
            notebook_id: str
            sources: List[Sources]

        Returns:
            List[SummarizedSource]
        """
        title_to_id, prompt = _build_summary_prompt(sources)
        answer = await self._ask_notebook(notebook_id, prompt)
        
        return _parse_summaries(answer, title_to_id)
        

    def list_notebooks(self) -> list[dict]:
        return asyncio.run(self._fetch_notebooks())
    
    def list_sources(self, notebook_id) -> list[dict]:
        return asyncio.run(self._fetch_sources(notebook_id))

    def list_notebook_sources(self, notebook_name: str | None = None) -> list[dict]:
        return asyncio.run(self._fetch_all(notebook_name))