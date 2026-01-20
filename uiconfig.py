CONFIG_TOML_TEMPLATE_PATH = "assets/template_config.toml"

css_properties_display_name = {
    "background_color": "Background Color",
    "color": "Text Color",
    "font_size": "Font Size",
    "font_weight": "Font Weight",
    "border_style": "Border Style",
    "border_color": "Border Color",
    "border_width": "Border Width",
    "padding": "All-sides",
    "padding_top": "Top",
    "padding_right": "Right",
    "padding_bottom": "Bottom",
    "padding_left": "Left",
    "label_color": "Label Color",
    "label_font_size": "Label Font Size",
    "label_font_weight": "Label Font Weight",
    "value_color": "Value Color",
    "value_font_size": "Value Font Size",
    "value_font_weight": "Value Font Weight",
}

css_properties_tabs = {
    "background_color": "Color",
    "color": "Color",
    "font_size": "Font",
    "font_weight": "Font",
    "border_style": "Border",
    "border_color": "Border",
    "border_width": "Border",
    "padding": "Padding",
    "padding_top": "Padding",
    "padding_right": "Padding",
    "padding_bottom": "Padding",
    "padding_left": "Padding",
    "label_color": "Label",
    "label_font_size": "Label",
    "label_font_weight": "Label",
    "value_color": "Value",
    "value_font_size": "Value",
    "value_font_weight": "Value",
}

element_type_format = {
    "primary": "Primary",
    "secondary": "Secondary (Default)",
    "tertiary": "Tertiary",
}

css_properties_input_widget = {
    "background_color": "color_picker",
    "color": "color_picker",
    "font_size": "size_input",
    "font_weight": "selectbox",
    "border_style": "selectbox",
    "border_color": "color_picker",
    "border_width": "size_input",
    "padding": "size_input",
    "padding_top": "size_input",
    "padding_right": "size_input",
    "padding_bottom": "size_input",
    "padding_left": "size_input",
    "label_color": "color_picker",
    "label_font_size": "size_input",
    "label_font_weight": "selectbox",
    "value_color": "color_picker",
    "value_font_size": "size_input",
    "value_font_weight": "selectbox",
}


# Elements not exported to CSS
ELEMENTS_EXCLUDED_FROM_CSS = ["container"]


# theme default values - COLOR
PRIMARY_COLOR_DEFAULT = "#ff4b4b"
BACKGROUND_COLOR_DEFAULT = "#ffffff"
SECONDARY_BACKGROUND_COLOR_DEFAULT = "#f0f2f6"
TEXT_COLOR_DEFAULT = "#31333f"

LINK_COLOR_DEFAULT = "#0054a3"
CODE_BG_COLOR_DEFAULT = "#f0f2f6"
BORDER_COLOR_DEFAULT = "#31333f20"
DATAFRAME_BORDER_COLOR_DEFAULT = "#31333f10"
DATAFRAME_HEADER_BG_COLOR_DEFAULT = "#f8f9fb"

SIDEBAR_PRIMARY_COLOR_DEFAULT = "#ff4b4b"
SIDEBAR_BACKGROUND_COLOR_DEFAULT = "#f0f2f6"
SIDEBAR_SECONDARY_BACKGROUND_COLOR_DEFAULT = "#ffffff"
SIDEBAR_TEXT_COLOR_DEFAULT = "#31333f"

SIDEBAR_LINK_COLOR_DEFAULT = "#0054a3"
SIDEBAR_CODE_BG_COLOR_DEFAULT = "#f0f2f6"
SIDEBAR_BORDER_COLOR_DEFAULT = "#31333f20"
SIDEBAR_DATAFRAME_BORDER_COLOR_DEFAULT = "#31333f10"
SIDEBAR_DATAFRAME_HEADER_BG_COLOR_DEFAULT = "#f8f9fb"

# theme default values - BORDER
SHOW_INPUT_WIDGET_BORDER_DEFAULT = False
SHOW_SIDEBAR_BORDER_DEFAULT = False

SIDEBAR_SHOW_INPUT_WIDGET_BORDER_DEFAULT = False

# theme default values - RADIUS
BASE_RADIUS_DEFAULT = (0.5, "rem")
BUTTON_RADIUS_DEFAULT = (0.5, "rem")

SIDEBAR_BASE_RADIUS_DEFAULT = (0.5, "rem")
SIDEBAR_BUTTON_RADIUS_DEFAULT = (0.5, "rem")

# theme values font

FONT_DEFAULT = "sans-serif"  # font
BASE_FONT_SIZE_DEFAULT = 16  # baseFontSize
BASE_FONT_WEIGHT_DEFAULT = 400  # baseFontWeight
HEADING_FONT_DEFAULT = "sans-serif"  # headingFont

CODE_FONT_DEFAULT = "monospace"  # codeFont
CODE_FONT_SIZE_DEFAULT = (14, "px")  # codeFontSize # Must be PX or REM
CODE_FONT_WEIGHT_DEFAULT = 400  # codeFontWeight

SIDEBAR_FONT_DEFAULT = "sans-serif"  # font
SIDEBAR_HEADING_FONT_DEFAULT = "sans-serif"  # headingFont

SIDEBAR_CODE_FONT_DEFAULT = "monospace"  # codeFont
SIDEBAR_CODE_FONT_SIZE_DEFAULT = (14, "px")  # codeFontSize # Must be PX or REM
SIDEBAR_CODE_FONT_WEIGHT_DEFAULT = 400  # codeFontWeight
