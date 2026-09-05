import customtkinter as ctk

# -------------------------------
# Appearance
# -------------------------------

DEFAULT_APPEARANCE = "Dark"
DEFAULT_COLOR_THEME = "blue"

ctk.set_appearance_mode(DEFAULT_APPEARANCE)
ctk.set_default_color_theme(DEFAULT_COLOR_THEME)

# -------------------------------
# Window
# -------------------------------

APP_TITLE = "VoiceID AI Pro"

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800

SIDEBAR_WIDTH = 220
TOPBAR_HEIGHT = 72

# -------------------------------
# Colors
# -------------------------------

BACKGROUND = "#1E1E1E"
CARD_COLOR = "#2B2B2B"
ACCENT = "#1F6AA5"
TEXT = "#FFFFFF"
MUTED_TEXT = "#A9B1BC"
SURFACE = "#242424"
SURFACE_ALT = "#2E2E2E"
SUCCESS = "#2FA360"
WARNING = "#D9A441"
ERROR = "#D96262"

# -------------------------------
# Fonts
# -------------------------------

TITLE_FONT = ("Segoe UI", 30, "bold")
SUBTITLE_FONT = ("Segoe UI", 20, "bold")
BODY_FONT = ("Segoe UI", 15)
SMALL_FONT = ("Segoe UI", 13)


def apply_theme(appearance=None):

	ctk.set_default_color_theme(DEFAULT_COLOR_THEME)
	ctk.set_appearance_mode(appearance or DEFAULT_APPEARANCE)