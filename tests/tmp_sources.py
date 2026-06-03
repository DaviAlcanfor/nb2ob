import sys
sys.path.insert(0, ".")

from api.notebooklm import NotebookLMAPI

DEVOPS_ID = "0df64d86-f8d9-4beb-8cc8-8a7ff9316341"

api = NotebookLMAPI()
sources = api.list_sources(DEVOPS_ID)

for source in sources:
    print(f"=== {source['title']} ===")
    print(source['content'][:1000])
    print()