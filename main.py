from typing import TypedDict

import typer

from agent.graph import build_graph
from api import NotebookLMAPI, ObsidianAPI

app = typer.Typer(help="nb2ob — sync NotebookLM notebooks to Obsidian")


class ResponseType(TypedDict):
    total_notebooks: int
    notes_failed: int   


@app.command()
def sync():
    
    notebooklm_api = NotebookLMAPI()
    obsidian_api = ObsidianAPI()
    pipeline = build_graph()

    typer.echo("Fetching notebooks from NotebookLM...")
    notebooks = notebooklm_api.list_notebooks_sources()
    
    response: ResponseType = { 
        "total_notebooks": len(notebooks),
        "notes_failed": 0    
    }
    
    for nb in notebooks:
        result = pipeline.invoke({
            "notebooks": [nb], 
            "called_agents": [] 
        })
        
        for note in result["formatted_notes"]:
            
            if not obsidian_api.send_to_obsidian(
                    notebook_title=note["notebook_title"],
                    note_title=note["file_title"],
                    note_content=note["content"],
                ):
                
                response["notes_failed"] += 1
    
    typer.echo(f"Notebooks processed: {response['total_notebooks']}, Notes failed: {response['notes_failed']}")

if __name__ == "__main__":
    app()