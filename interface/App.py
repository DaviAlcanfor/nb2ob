import threading
import customtkinter as ctk
from pathlib import Path
from PIL import Image
from typing import Callable

from interface.components import AppTitle, PrimaryButton, StatusMessage
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
    def __init__(self, on_load: Callable, on_sync: Callable):
        super().__init__()

        self._on_load = on_load
        self._on_sync = on_sync
        self._checkboxes = {}

        self.title(_PROJECT_NAME)
        self.resizable(False, False)
        self.iconbitmap(str(ICON_PATH))
        self.geometry(_GEOMETRY)
        self.configure(fg_color=BACKGROUND)

        self._setup_widgets()
        self._setup_layout()
        self._load_notebooks()

    def _setup_widgets(self):
        self.app_title = AppTitle(self, text=_PROJECT_NAME)

        self.notebook_frame = ctk.CTkScrollableFrame(self, width=700, height=280)

        self.sync_button = PrimaryButton(self, text="Sync", command=self._on_sync_click)
        self.status = StatusMessage(self, text="")

    def _setup_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.app_title.grid(row=0, column=0, padx=_PADX, pady=_PADY, sticky="w")
        self.notebook_frame.grid(row=1, column=0, padx=_PADX, pady=_PADY, sticky="ew")
        self.sync_button.grid(row=2, column=0, padx=_PADX, pady=_PADY)
        self.status.grid(row=3, column=0, padx=_PADX, pady=_PADY)

    def _load_notebooks(self):
        self.status.set_status("Loading notebooks...", success=True)

        def load():
            notebooks = self._on_load()
            self.after(0, lambda: self._populate_notebooks(notebooks))

        threading.Thread(target=load, daemon=True).start()

    def _populate_notebooks(self, notebooks: list[dict]):
        for nb in notebooks:
            var = ctk.BooleanVar(value=False)
            cb = ctk.CTkCheckBox(self.notebook_frame, text=nb["title"], variable=var)
            cb.pack(anchor="w", pady=2)
            self._checkboxes[nb["id"]] = var

        self.status.set_status("", success=True)

    def _on_sync_click(self):
        selected = [nb_id for nb_id, var in self._checkboxes.items() if var.get()]

        if not selected:
            self.status.set_status("Select at least one notebook.", success=False)
            return

        self.sync_button.configure(state="disabled")
        self.status.set_status("Syncing...", success=True)

        def sync():
            success = self._on_sync(selected)
            self.after(0, lambda: self._on_sync_done(success))

        threading.Thread(target=sync, daemon=True).start()

    def _on_sync_done(self, success: bool):
        self.sync_button.configure(state="normal")
        self.status.set_status(
            "Sync complete!" if success else "Sync failed.",
            success=success
        )

    def run(self):
        self.mainloop()