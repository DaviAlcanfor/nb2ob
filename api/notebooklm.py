"""
NotebookLM API wrapper for listing notebooks and extracting content.
"""

import asyncio
from notebooklm import NotebookLMClient

from infrastructure.decorators import get_logger

logger = get_logger(__name__)


_EXTRACTION_PROMPT = (
    "Liste todo o conteúdo deste notebook de forma detalhada, organizado por seção ou arquivo de origem. "
    "Para cada seção, explique todos os conceitos, preserve comandos e termos técnicos exatos, "
    "e inclua todos os exemplos de código. Não resuma. O objetivo é extrair o máximo de informação possível."
)


class NotebookLMAPI:

    async def _fetch_all(self, notebook_ids: list[str]) -> dict[str, str]:

        client = await NotebookLMClient.from_storage()

        async with client:
            notebooks = await client.notebooks.list()
            
            results = {}
            for nb in notebooks:
                if nb.id in notebook_ids:

                    logger.info(f"Extracting: {nb.title}")

                    result = await client.chat.ask(nb.id, _EXTRACTION_PROMPT)
                    results[nb.title] = result.answer

            return results
        

    async def _fetch_notebooks(self) -> list[dict]:

        async with await NotebookLMClient.from_storage() as client:
            
            notebooks = await client.notebooks.list()

            return [{"id": nb.id, "title": nb.title} for nb in notebooks]

    def list_notebooks(self) -> list[dict]:
        return asyncio.run(self._fetch_notebooks())

    def sync_notebooks(self, notebook_ids: list[str]) -> dict[str, str]:
        return asyncio.run(self._fetch_all(notebook_ids))