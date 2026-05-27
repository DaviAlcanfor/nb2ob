import customtkinter as ctk
from typing import Callable
from PIL import Image, ImageTk 
from pathlib import Path

from interface.components import (
    AppTitle,
    TextInput,
    FileNameInput,
    PrimaryButton,
    StatusMessage
)
from interface.themes import BACKGROUND


img = Image.open("icon/icon.png").convert("RGBA")
img.save("icon/icon.ico", format="ICO", sizes=[(256, 256)])

ICON_PATH = Path(__file__).parent.parent / "icon" / "icon.ico"

_WIDTH = 760
_HEIGHT = 400
_GEOMETRY = f"{_WIDTH}x{_HEIGHT}"

_PADX = 20
_PADY = 5

_PROJECT_NAME = "nb2ob"



class App(ctk.CTk):
    def __init__(self, on_send: Callable = None):

        super().__init__()

        self._on_send = on_send

        self.title(_PROJECT_NAME)
        self.resizable(False, False)
        
        self.iconbitmap(str(ICON_PATH))

        self.geometry(_GEOMETRY)
        self.configure(fg_color=BACKGROUND)
        self._setup_widgets()
        self._setup_layout()


    def _setup_widgets(self):

        # TITLE 
        self.app_title = AppTitle(self, text=_PROJECT_NAME)

        # FILE NAME INPUT
        self.file_name_input = FileNameInput(self, placeholder_text="Note name...")

        # SEND BUTTON
        self.send_button = PrimaryButton(self, 
                                         text="Send", 
                                         command=self.on_send
                                         )
        
        # TEXT INPUT
        self.text_input = TextInput(self, 
                                    width=_WIDTH, 
                                    height=_HEIGHT
                                    )
        
        # STATUS MESSAGE
        self.status = StatusMessage(self, text="")


    def _setup_layout(self):
        self.grid_columnconfigure(0, weight=1)

        # TITLE
        self.app_title.grid(row=0, column=0, padx=_PADX, pady=_PADY, sticky="w")

        # FILE NAME INPUT
        self.file_name_input.grid(row=1, column=0, padx=_PADX, pady=_PADY, sticky="ew")
        self.send_button.grid(row=1, column=1, padx=(0, _PADX), pady=_PADY)

        # TEXT INPUT
        self.text_input.grid(row=2, column=0, columnspan=2, padx=_PADX, pady=_PADY)

        # STATUS MESSAGE
        self.status.grid(row=3, column=0, columnspan=2, padx=_PADX, pady=_PADY)


    def _is_valid(
        self, 
        raw_text: str, 
        file_name: str
    ) -> bool:
        """
        This method checks if the raw text and file name inputs are valid (not empty or just whitespace). 

        Args:
            raw_text (str): The raw text input from the user.
            file_name (str): The file name input from the user.

        Returns:
            bool: True if both inputs are valid, False otherwise.
        """
        return bool(raw_text.strip() and file_name.strip())
    

    def on_send(self):
        raw_text = self.text_input.get_text()
        file_name = self.file_name_input.get()

        if not self._is_valid(raw_text, file_name):
            self.status.set_status(
                "Please fill in all fields.", 
                success=False
            )
            return

        if self._on_send:
            try:
                success = self._on_send(raw_text, 
                                        file_name)
                
                self.status.set_status(
                    "Note created successfully!" if success 
                    else "Failed to send to Obsidian.",
                    success=success
                )

            except Exception as e:
                self.status.set_status(f"Error: {str(e)}", 
                                       success=False)

    def run(self):
        self.mainloop()