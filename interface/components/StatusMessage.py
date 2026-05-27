from customtkinter import CTkLabel

from interface.themes import (
    STATUS_MESSAGE_THEME,
    GREEN, 
    RED
)

class StatusMessage(CTkLabel):
    """
    This is the status message label for the application. It is styled using the STATUS_MESSAGE_THEME defined in the themes module, 
    which ensures a consistent and visually appealing appearance across all instances of the status message label.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **{**STATUS_MESSAGE_THEME, **kwargs})

    def set_status(
        self, 
        message: str, 
        success: bool = True
    ):
        """
        This method sets the status message and changes the text color based on the status type (info, success, error).

        Args:
            message (str): The status message to display.
            success (bool): A boolean value indicating the status. True for success, False for error.
        """

        self.configure(text_color=GREEN if success else RED)
        self.configure(text=message)