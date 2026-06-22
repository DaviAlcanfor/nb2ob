import sys
sys.path.insert(0, ".")

from api.notebooklm import NotebookLMAPI

api = NotebookLMAPI()
notebooks = api.list_notebooks()
for nb in notebooks:
    print(nb['id'], nb['title'])