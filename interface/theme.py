import customtkinter as ctk


# ======================================================
# AXIOM DESIGN SYSTEM v4
# PREMIUM DARK GLASS INTERFACE
# ======================================================


AXIOM_COLORS = {


    # ===============================
    # BACKGROUNDS
    # ===============================

    "background": "#080A0F",

    "background_alt": "#0D1017",


    "sidebar": "#090B10",


    "panel": "#11151D",

    "panel_light": "#171C26",


    "card": "#151A23",

    "card_hover": "#1D2430",



    # ===============================
    # BORDERS
    # ===============================

    "border": "#242B38",

    "border_light": "#323A49",

    "border_gold": "#D8B15B",




    # ===============================
    # GOLD SYSTEM
    # ===============================

    "gold": "#D8B15B",

    "gold_bright": "#F5CF76",

    "gold_light": "#FFE09A",

    "gold_dark": "#8B6918",

    "gold_hover": "#E8C56A",




    # ===============================
    # TEXT
    # ===============================

    "text": "#F8F8F8",

    "text_secondary": "#9AA1AE",

    "muted": "#697180",




    # ===============================
    # STATUS
    # ===============================

    "success": "#20E889",

    "warning": "#F2C94C",

    "danger": "#FF5555",




    # ===============================
    # BASIC
    # ===============================

    "black": "#000000",

    "white": "#FFFFFF"

}




# ======================================================
# TYPOGRAPHY
# ======================================================


AXIOM_FONT = "Inter"



LARGE_TITLE_FONT = (

    AXIOM_FONT,

    54,

    "bold"

)



TITLE_FONT = (

    AXIOM_FONT,

    36,

    "bold"

)



HEADING_FONT = (

    AXIOM_FONT,

    22,

    "bold"

)



CARD_TITLE_FONT = (

    AXIOM_FONT,

    17,

    "bold"

)



BODY_FONT = (

    AXIOM_FONT,

    15

)



BUTTON_FONT = (

    AXIOM_FONT,

    15,

    "bold"

)



SMALL_FONT = (

    AXIOM_FONT,

    12

)



STATUS_FONT = (

    AXIOM_FONT,

    15,

    "bold"

)



HERO_TITLE = (

    AXIOM_FONT,

    54,
    
    "bold"
)

# Keep compatibility
LARGE_TITLE_FONT = HERO_TITLE




# ======================================================
# WINDOW
# ======================================================


WINDOW_WIDTH = 1450

WINDOW_HEIGHT = 900





# ======================================================
# SIDEBAR
# ======================================================


SIDEBAR_WIDTH = 240

SIDEBAR_COLLAPSED = 78



SIDEBAR_BUTTON_HEIGHT = 58

SIDEBAR_BUTTON_RADIUS = 16





# ======================================================
# BUTTON SYSTEM
# ======================================================


BUTTON_HEIGHT = 54

BUTTON_RADIUS = 15



PRIMARY_BUTTON_HEIGHT = 70

PRIMARY_BUTTON_RADIUS = 18





# ======================================================
# CARDS
# ======================================================


CARD_RADIUS = 22

PANEL_RADIUS = 30



CARD_BORDER_WIDTH = 1



CARD_HEIGHT_SMALL = 120

CARD_HEIGHT = 180

CARD_HEIGHT_LARGE = 260





# ======================================================
# SPACING
# ======================================================


SPACE_XS = 6

SPACE_SMALL = 12

SPACE = 20

SPACE_MEDIUM = 30

SPACE_LARGE = 45

SPACE_XL = 65



PADDING_SMALL = SPACE_SMALL

PADDING = SPACE

PADDING_LARGE = SPACE_LARGE

PADDING_XL = SPACE_XL





# ======================================================
# ICONS
# ======================================================


ICON_SIZE = 22

ICON_SIZE_SMALL = 16

ICON_SIZE_LARGE = 34





# ======================================================
# EFFECTS
# ======================================================


GLOW_RADIUS = 40

GLOW_ALPHA = 70



ANIMATION_SPEED_FAST = 120

ANIMATION_SPEED = 220

ANIMATION_SPEED_SLOW = 400





# ======================================================
# GLOBAL THEME
# ======================================================


def apply_theme():


    ctk.set_appearance_mode(

        "dark"

    )


    ctk.set_default_color_theme(

        "dark-blue"

    )





# ======================================================
# COMPONENT HELPERS
# ======================================================


def create_card(parent):


    return ctk.CTkFrame(

        parent,

        fg_color=AXIOM_COLORS["card"],

        corner_radius=CARD_RADIUS,

        border_width=CARD_BORDER_WIDTH,

        border_color=AXIOM_COLORS["border"]

    )