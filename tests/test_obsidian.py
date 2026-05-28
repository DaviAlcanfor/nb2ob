# teste_obsidian.py
from api.obsidian import ObsidianAPI
import requests
import os
from dotenv import load_dotenv

load_dotenv()

print(repr(os.getenv("OBSIDIAN_TOKEN")))

api = ObsidianAPI()

conteudo = """---
date: 2026-05-27
tags: []
source: NotebookLM
---

## Resumo
Teste direto na API do Obsidian.
"""

URL = f"{api.api_url}teste-debug.md"

response = requests.put(
    URL,
    headers={
        "Authorization": f"Bearer {api.token}",
        "Content-Type": "text/markdown",
    },
    data=conteudo.encode("utf-8"),
    verify=False
)

print(f"Status code: {response.status_code}")
print(f"Resposta: {response.text}")


