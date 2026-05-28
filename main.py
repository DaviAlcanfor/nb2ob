from agent.formatter import Agent
from api.obsidian import ObsidianAPI
from interface.App import App

agent = Agent()
obsidian = ObsidianAPI()


def on_send(raw_text: str, file_name: str) -> bool:
    formatted = agent.format_note(raw_text)
    
    return obsidian.send_to_obsidian(file_name, formatted)


if __name__ == "__main__":
    App(on_send=on_send).run()
