"""
Here resides the theme configuration for the application. It defines the color scheme and appearance settings for the 
user interface, ensuring a consistent and visually appealing experience across all components of the application. 
The theme settings can be easily modified to allow users to customize the look and feel according to their preferences.
"""


# Reusable colors and styles

PRIMARY = "#7C3AED"
PRIMARY_HOVER = "#6D28D9"
TEXT = "#FFFFFF"
BACKGROUND = "#1E1E1E"

GREEN = "#10B981"
RED = "#EF4444"

FONT_NAME = "Inter"
FONT = (FONT_NAME, 13)
CORNER_RADIUS = 6
BORDER_WIDTH = 2


# Themes

APP_TITLE_THEME = {
    "font": (FONT_NAME, 18, "bold"),
    "text_color": TEXT,
}

TEXT_INPUT_THEME = {
    "fg_color": BACKGROUND,
    "text_color": TEXT,
    "border_color": PRIMARY,
    "border_width": BORDER_WIDTH,
    "corner_radius": CORNER_RADIUS,
    "font": FONT
}

BUTTON_THEME = {
    "fg_color": PRIMARY,
    "hover_color": PRIMARY_HOVER,
    "text_color": TEXT,
    "corner_radius": CORNER_RADIUS,
    "font": FONT
}

FILE_NAME_INPUT_THEME = {
    "fg_color": BACKGROUND,
    "text_color": TEXT,
    "border_color": PRIMARY,
    "border_width": BORDER_WIDTH,
    "corner_radius": CORNER_RADIUS,
    "font": FONT
}

STATUS_MESSAGE_THEME = {
    # The color comes after, dinamically
    "font": (FONT_NAME, 12, "italic")
}