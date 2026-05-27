from customtkinter import CTkTextbox

from interface.themes import TEXT_INPUT_THEME

class TextInput(CTkTextbox):
    """
    This is the text input field for the application. It is styled using the TEXT_INPUT_THEME defined in the themes module
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **{**TEXT_INPUT_THEME, **kwargs})


    def get_text(self) -> str:
        """ 
        This method retrieves the text from the text input field and returns it as a string. 
        """
        return self.get("1.0", "end-1c")