from agent.nodes.formatter import Agent
from api.obsidian import ObsidianAPI
from api.notebooklm import NotebookLMAPI
from interface.App import App

agent = Agent()
obsidian = ObsidianAPI()
notebooklm = NotebookLMAPI()


def on_load() -> list[dict]:
    return notebooklm.list_notebooks()


def on_sync(notebook_ids: list[str]) -> bool:
    contents = notebooklm.sync_notebooks(notebook_ids)

    results = []
    for title, raw_text in contents.items():
        formatted = agent.format_note(raw_text)
        success = obsidian.send_to_obsidian(title, formatted)
        results.append(success)

    return all(results)


if __name__ == "__main__":
    App(on_load=on_load, on_sync=on_sync).run()