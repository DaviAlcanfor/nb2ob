from agent.formatter import Agent
from api.obsidian import ObsidianAPI
from interface.App import App

agent = Agent()
obsidian = ObsidianAPI()


def on_send(raw_text: str, file_name: str) -> bool:
    """
    Sends a formatted note to Obsidian. 
    This is the function that gets called when the user clicks the "Send to Obsidian"

    Args:
        raw_text (str): The raw text input from the user.
        file_name (str): The name of the file to be created in Obsidian.

    Returns:
        bool: True if the note was successfully sent to Obsidian, False otherwise.
    """

    formatted = agent.format_note(raw_text)

    return obsidian.send_to_obsidian(file_name, formatted)


if __name__ == "__main__":
    App(on_send=on_send).run()