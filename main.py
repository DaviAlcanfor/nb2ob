from typing import TypedDict
import typer
from notebooklm.exceptions import AuthError, NetworkError, RPCTimeoutError

from agent.graph import build_graph
from api import NotebookLMAPI, ObsidianAPI
from infrastructure.display import display_banner

app = typer.Typer(help="nb2ob — sync NotebookLM notebooks to Obsidian")


class SyncReport(TypedDict):
    total_notebooks: int
    notes_failed: int


def _fetch_notebooks(notebooklm_api: NotebookLMAPI, notebook_name: str | None = None) -> list:
    try:
        return notebooklm_api.list_notebook_sources(notebook_name)

    except AuthError:
        typer.echo("NotebookLM session invalid. Run: notebooklm login")
        raise typer.Exit(code=1)

    except (NetworkError, RPCTimeoutError) as e:
        typer.echo(f"Connection error while fetching notebooks: {e}")
        raise typer.Exit(code=1)

    except Exception as e:
        typer.echo(f"Unexpected error: {e}")
        raise typer.Exit(code=1)


@app.command()
def sync(
    notebook: str = typer.Option(None, "--notebook", help="Sync a specific notebook by name"),
):
    """
    Fetches notebooks from NotebookLM, processes them through the agent pipeline,
    and writes the formatted notes to Obsidian.
    """
    display_banner()

    notebooklm_api = NotebookLMAPI()
    obsidian_api   = ObsidianAPI()
    pipeline       = build_graph()

    obsidian_api.check_or_exit()

    typer.echo("Fetching notebooks from NotebookLM...")
    notebooks = _fetch_notebooks(notebooklm_api, notebook)

    report: SyncReport = {
        "total_notebooks": len(notebooks),
        "notes_failed": 0,
    }

    for nb in notebooks:
        result = pipeline.invoke({
            "notebooks":     [nb],
            "called_agents": [],
        })

        for note in result["formatted_notes"]:
            if not obsidian_api.send_to_obsidian(
                notebook_title=note["notebook_title"],
                note_title=note["file_title"],
                note_content=note["content"],
            ):
                report["notes_failed"] += 1

    typer.echo(f"Notebooks processed: {report['total_notebooks']}, Notes failed: {report['notes_failed']}")


if __name__ == "__main__":
    app()