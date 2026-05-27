from customtkinter import CTkEntry


from interface.themes import FILE_NAME_INPUT_THEME


class FileNameInput(CTkEntry):
    """
    This is the file name input field for the application. It is styled using the FILE_NAME_INPUT_THEME defined in the themes module
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **{**FILE_NAME_INPUT_THEME, **kwargs})