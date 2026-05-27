import customtkinter as ctk

from interface.theme import BUTTON_THEME


class PrimaryButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, **{**BUTTON_THEME, **kwargs})