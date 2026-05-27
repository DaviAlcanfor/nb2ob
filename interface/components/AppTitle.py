from customtkinter import CTkLabel

from interface.themes import APP_TITLE_THEME

class AppTitle(CTkLabel):
    """
    This is the title label for the application. It is styled using the APP_TITLE_THEME defined in the themes module, 
    which ensures a consistent and visually appealing appearance across all instances of the title label.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **{**APP_TITLE_THEME, **kwargs})