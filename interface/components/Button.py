from customtkinter import CTkButton

from interface.themes import BUTTON_THEME


class PrimaryButton(CTkButton):
    """
    This is the primary button for the application. It is styled using the BUTTON_THEME defined in the themes module, 
    which ensures a consistent and visually appealing appearance across all instances of the primary button.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **{**BUTTON_THEME, **kwargs})