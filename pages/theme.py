from typing import Literal, Optional

import streamlit as st
import st_yled

import uiconfig
import converters
import utils

import uuid


def init_theme_session_state(key: str, default_value: str):
    """Initialize session state variables for theme settings with default values."""
    
    if key not in st.session_state:
        st.session_state[key] = default_value
        st.session_state[f'{key}-default'] = default_value

def update_st_from_input(theme_property: str, input_selector_key: str):
    st.session_state[theme_property] = st.session_state[input_selector_key]

def reset_defaults(keys: list[str]):

    #print(st.session_state)

    for key in keys:
        default_key = f"{key}-default"
        if default_key in st.session_state:
            st.session_state[key] = st.session_state[default_key]
    
        key_seed = key + '-seed'

        if key_seed in st.session_state:
            del st.session_state[key_seed]

def reset_seed(key: str):
    
    del st.session_state[key]

def frame_select_reset_bar(key: str, reset_keys: list[str]):
    
    with st.container(key=f"{key}-container",
                        horizontal=True,
                        horizontal_alignment="distribute"):

        frame_type = utils.segmented_control_toggle(":material/width_full: Main",
                                                    ":material/side_navigation: Sidebar",
                                                    key=f"{key}-toggle")

        if frame_type == ":material/side_navigation: Sidebar":
            frame_type_select = "sidebar"
            preview_selector_prefix = "theme-sidebar"
        else:
            frame_type_select = "main"
            preview_selector_prefix = "theme"

        # Append whether to reset sidebar or main keys
        reset_keys = [f"{preview_selector_prefix}-{rk}" for rk in reset_keys]

        st_yled.button(
            "Reset",
            icon=":material/settings_backup_restore:",
            on_click=reset_defaults,
            args= (reset_keys,),
            font_size='14px',
            key=f"{key}-reset-button"
        )

        return frame_type_select, preview_selector_prefix


def theme_color_picker(theme_property: str,
                        label: str,
                        label_font_size: str = '20px',
                        label_field_width: int = 140,
                        frame_type: Literal["main", "sidebar"] = "main"):

    if frame_type == "sidebar":
        theme_property = "sidebar-" + theme_property
    
    session_state_key = f"theme-{theme_property}"
    session_state_key_default = f"{session_state_key}-default"

    color_state_value = st.session_state[session_state_key]

    color_is_default = color_state_value == st.session_state[session_state_key_default] 

    code_color = 'grey' if color_is_default else None

    utils.base_color_picker(
        key=theme_property,
        label=label,
        label_font_size=label_font_size,
        label_field_width=label_field_width,
        color_state_value=color_state_value,
        code_color=code_color)


def theme_checkbox(theme_property: str,
                   label: str,
                   label_font_size: str = '20px',
                   label_field_width: int = 140,
                   frame_type: Literal["main", "sidebar"] = "main"):
    
    if frame_type == "sidebar":
        theme_property = "sidebar-" + theme_property
    
    session_state_key = f"theme-{theme_property}"

    # Create a unique seed for component
    input_seed_key = f"theme-{theme_property}-seed"

    if not input_seed_key in st.session_state:
        st.session_state[input_seed_key] = str(uuid.uuid4())

    with st.container(horizontal=True, vertical_alignment="center"):

        st_yled.markdown(label, font_size=label_font_size, width=label_field_width)

        st_yled.checkbox(
            'Enable',
            label_visibility="collapsed",
            value=st.session_state[session_state_key],
            key=theme_property + "-checkbox-" + st.session_state[input_seed_key],
            on_change=update_st_from_input,
            args=(session_state_key, theme_property + "-checkbox-" + st.session_state[input_seed_key])
        )

        st_yled.caption("Enable", width=100)


def theme_size_input(theme_property: str,
                        label: str,
                        label_font_size: str = '20px',
                        label_field_width: int = 140,
                        allowed_units: list[str] = ['px', 'rem'],
                        frame_type: Literal["main", "sidebar"] = "main",
                        return_value_type: Literal["tuple", "int"] = "tuple"):
    
    if frame_type == "sidebar":
        theme_property = "sidebar-" + theme_property
    
    session_state_key = f"theme-{theme_property}"
    
    # Create a unique seed for component
    input_seed_key = f"theme-{theme_property}-seed"

    if not input_seed_key in st.session_state:
        st.session_state[input_seed_key] = str(uuid.uuid4())

    # Get current value tuple or parse from string
    current_value = st.session_state[session_state_key]

    if return_value_type == "tuple":
        current_number, current_unit = current_value
    else:
        current_number = current_value
        current_unit = allowed_units[0]  # Default to first allowed unit

    current_number = float(current_number)

    utils.base_size_input(
        key=session_state_key,
        seed_value=st.session_state[input_seed_key],
        label=label,
        value=current_number,
        step_size=0.1 if current_unit == 'rem' else 1.0,
        unit=current_unit,
        allowed_units=allowed_units,
        label_font_size=label_font_size,
        label_field_width=label_field_width,
        return_value_type=return_value_type
    )


def theme_font_input(theme_property: str,
                        label: str,
                        label_font_size: str = '20px',
                        label_field_width: int = 140,
                        frame_type: Literal["main", "sidebar"] = "main",
                        key: Optional[str] = None):
    
    if frame_type == "sidebar":
        theme_property = "sidebar-" + theme_property
    
    session_state_key = f"theme-{theme_property}"
    
    # Create a unique seed for component
    input_seed_key = f"theme-{theme_property}-seed"

    if not input_seed_key in st.session_state:
        st.session_state[input_seed_key] = str(uuid.uuid4())

    # Get current value tuple or parse from string
    current_value = st.session_state[session_state_key]

    with st.container(horizontal=True, vertical_alignment="center", key=key):

        st_yled.markdown(label, font_size=label_font_size, width=label_field_width)

        options = ['sans-serif', 'serif', 'monospace', 'Google Fonts']
        index_select = options.index(current_value) if current_value in options else 3

        # Number input
        font_value = st.selectbox(
            "Pick font",
            options=options,
            index=index_select,
            width=150,
            key = theme_property + "-font-select-" + st.session_state[input_seed_key]
        )

        if font_value == "Google Fonts":
            
            if current_value not in options:
                current_value = current_value.split(":")
                family_name_value = current_value[0].strip("'")
                font_url_value = ':'.join(current_value[1:])
            else:
                family_name_value, font_url_value = '', ''

            family_name = st.text_input(
                f"Name",
                value=family_name_value,
                key=theme_property + "-font-family",
                width=100,
            )

            font_url = st.text_input(
                "Google Fonts URL",
                value=font_url_value,
                key=theme_property + "-font-url",
                help= "More information on \n[Google Fonts in Streamlit](https://docs.streamlit.io/develop/tutorials/configuration-and-theming/external-fonts)",
                width=240,
            )

            font_value = f"\'{family_name}\':{font_url}"

        # Update session state with tuple value
        st.session_state[session_state_key] = font_value


def theme_weight_input(theme_property: str,
                        label: str,
                        label_font_size: str = '20px',
                        label_field_width: int = 140,
                        frame_type: Literal["main", "sidebar"] = "main"):
    
    if frame_type == "sidebar":
        theme_property = "sidebar-" + theme_property
    
    session_state_key = f"theme-{theme_property}"
    
    # Create a unique seed for component
    input_seed_key = f"theme-{theme_property}-seed"

    if not input_seed_key in st.session_state:
        st.session_state[input_seed_key] = str(uuid.uuid4())

    # Get current value tuple or parse from string
    current_value = st.session_state[session_state_key]

    with st.container(horizontal=True, vertical_alignment="center", width=400):

        st_yled.markdown(label, font_size=label_font_size, width=label_field_width)

        # Number input
        number_value = st.number_input(
            f"Set {label} value",
            value=current_value,
            min_value=100,
            max_value=600,
            step=100,
            key=theme_property + "-number-" + st.session_state[input_seed_key],
            label_visibility="collapsed",
            width=138,
        )

        st.session_state[session_state_key] = number_value



# Initialize main theme session state
init_theme_session_state('theme-primaryColor', uiconfig.PRIMARY_COLOR_DEFAULT)
init_theme_session_state('theme-backgroundColor', uiconfig.BACKGROUND_COLOR_DEFAULT)
init_theme_session_state('theme-secondaryBackgroundColor', uiconfig.SECONDARY_BACKGROUND_COLOR_DEFAULT)
init_theme_session_state('theme-textColor', uiconfig.TEXT_COLOR_DEFAULT)
init_theme_session_state('theme-linkColor', uiconfig.LINK_COLOR_DEFAULT)
init_theme_session_state('theme-codeBackgroundColor', uiconfig.CODE_BG_COLOR_DEFAULT)
init_theme_session_state('theme-dataframeBorderColor', uiconfig.DATAFRAME_BORDER_COLOR_DEFAULT)
init_theme_session_state('theme-dataframeHeaderBackgroundColor', uiconfig.DATAFRAME_HEADER_BG_COLOR_DEFAULT)

# Initialize sidebar theme session state
init_theme_session_state('theme-sidebar-primaryColor', uiconfig.SIDEBAR_PRIMARY_COLOR_DEFAULT)
init_theme_session_state('theme-sidebar-backgroundColor', uiconfig.SIDEBAR_BACKGROUND_COLOR_DEFAULT)
init_theme_session_state('theme-sidebar-secondaryBackgroundColor', uiconfig.SIDEBAR_SECONDARY_BACKGROUND_COLOR_DEFAULT)
init_theme_session_state('theme-sidebar-textColor', uiconfig.SIDEBAR_TEXT_COLOR_DEFAULT)
init_theme_session_state('theme-sidebar-linkColor', uiconfig.SIDEBAR_LINK_COLOR_DEFAULT)
init_theme_session_state('theme-sidebar-codeBackgroundColor', uiconfig.SIDEBAR_CODE_BG_COLOR_DEFAULT)
init_theme_session_state('theme-sidebar-dataframeBorderColor', uiconfig.SIDEBAR_DATAFRAME_BORDER_COLOR_DEFAULT)
init_theme_session_state('theme-sidebar-dataframeHeaderBackgroundColor', uiconfig.SIDEBAR_DATAFRAME_HEADER_BG_COLOR_DEFAULT)

# Initialize border theme session state
init_theme_session_state('theme-borderColor', uiconfig.BORDER_COLOR_DEFAULT)
init_theme_session_state('theme-showWidgetBorder', uiconfig.SHOW_INPUT_WIDGET_BORDER_DEFAULT)
init_theme_session_state('theme-showSidebarBorder', uiconfig.SHOW_SIDEBAR_BORDER_DEFAULT)

# Initialize sidebar border theme session state
init_theme_session_state('theme-sidebar-borderColor', uiconfig.SIDEBAR_BORDER_COLOR_DEFAULT)
init_theme_session_state('theme-sidebar-showWidgetBorder', uiconfig.SIDEBAR_SHOW_INPUT_WIDGET_BORDER_DEFAULT)

# Initialize radius theme session state
init_theme_session_state('theme-baseRadius', uiconfig.BASE_RADIUS_DEFAULT)
init_theme_session_state('theme-buttonRadius', uiconfig.BUTTON_RADIUS_DEFAULT)

# Initialize sidebar radius theme session state
init_theme_session_state('theme-sidebar-baseRadius', uiconfig.SIDEBAR_BASE_RADIUS_DEFAULT)
init_theme_session_state('theme-sidebar-buttonRadius', uiconfig.SIDEBAR_BUTTON_RADIUS_DEFAULT)

# Initialize sidebar font theme session state
init_theme_session_state('theme-font', uiconfig.FONT_DEFAULT)
init_theme_session_state('theme-headingFont', uiconfig.HEADING_FONT_DEFAULT)
init_theme_session_state('theme-baseFontSize', uiconfig.BASE_FONT_SIZE_DEFAULT)
init_theme_session_state('theme-baseFontWeight', uiconfig.BASE_FONT_WEIGHT_DEFAULT)

init_theme_session_state('theme-codeFont', uiconfig.CODE_FONT_DEFAULT)
init_theme_session_state('theme-codeFontSize', uiconfig.CODE_FONT_SIZE_DEFAULT)
init_theme_session_state('theme-codeFontWeight', uiconfig.CODE_FONT_WEIGHT_DEFAULT)

init_theme_session_state('theme-sidebar-font', uiconfig.SIDEBAR_FONT_DEFAULT)
init_theme_session_state('theme-sidebar-headingFont', uiconfig.SIDEBAR_HEADING_FONT_DEFAULT)

init_theme_session_state('theme-sidebar-codeFont', uiconfig.SIDEBAR_CODE_FONT_DEFAULT)
init_theme_session_state('theme-sidebar-codeFontSize', uiconfig.SIDEBAR_CODE_FONT_SIZE_DEFAULT)
init_theme_session_state('theme-sidebar-codeFontWeight', uiconfig.SIDEBAR_CODE_FONT_WEIGHT_DEFAULT)


# region UI

with st.container(key="theme-main-container"):

    st.markdown("**> Theme** Configure global styling of your Streamlit App")

    tab_color, tab_font, tab_border, tab_radius = st_yled.tabs(
        ["Color", "Font", "Border", "Radius"],
        key = "theme-tabs"
    )

    #region Color Tabs
    with tab_color:
        
        frame_type_select, preview_selector_prefix = frame_select_reset_bar(
            key="theme-color-frame-reset-bar",
            reset_keys=[
                "primaryColor",
                "backgroundColor",
                "secondaryBackgroundColor",
                "textColor",
                "linkColor",
                "codeBackgroundColor",
                "dataframeBorderColor",
                "dataframeHeaderBackgroundColor",
            ]
        )

        color_cont = st.container(key="theme-color-container")

        col1, col2 = color_cont.columns([2,1])

        # Define Color Pickers
        with col1.container(key="color-selectors"):

            theme_color_picker("primaryColor", "Primary", frame_type=frame_type_select)

            theme_color_picker("backgroundColor", "Background", frame_type=frame_type_select)

            theme_color_picker("secondaryBackgroundColor", "Secondary Background", frame_type=frame_type_select)

            theme_color_picker("textColor", "Text", frame_type=frame_type_select)

        # Preview Pane
        with col2:

            with st_yled.container(
                key="color-preview",
                background_color=st.session_state[f'{preview_selector_prefix}-backgroundColor'],
                border = False
            ):
                bg_test = st.container(
                    horizontal=True,
                    horizontal_alignment="right",
                )
    
                bg_test.markdown("**Background**", width='content')

                with st_yled.container(
                    key="primary-color-preview",
                    background_color=st.session_state[f'{preview_selector_prefix}-primaryColor'],
                    height=128,
                    width=112
                ):
                    st_yled.markdown("**Primary**", width='content', color='#FFFFFF')

                
                with st.container(horizontal=True, horizontal_alignment="right"):
                    
                    with st_yled.container(
                        key="secondary-color-preview",
                        background_color=st.session_state[f'{preview_selector_prefix}-secondaryBackgroundColor'],
                        height=112,
                        width=112,
                        horizontal=True,
                        horizontal_alignment="right"
                    ):
                        st_yled.markdown("**Secondary Background**", width='content')

                st_yled.markdown("Textcolor",
                                font_size='26px',
                                key="textcolor-preview",
                                color=st.session_state[f'{preview_selector_prefix}-textColor'] )

                st.markdown("")
        
        # TODO: Expander BG Color
        with st_yled.expander("More Color Options",
                            key="theme-color-ext-expander",
                            border_width='0px'):
            
            color_ext_cont = st.container(key="theme-color-ext-container")

            col1, col2 = color_ext_cont.columns([2,1])

            with col1.container(key="color-ext-selectors"):

                theme_color_picker("linkColor", "Link", label_font_size='16px', label_field_width=100, frame_type=frame_type_select)

                theme_color_picker("codeBackgroundColor", "Code Background", label_font_size='16px', label_field_width=100, frame_type=frame_type_select)

                theme_color_picker("dataframeHeaderBackgroundColor", "DataFrame Header", label_font_size='16px', label_field_width=100, frame_type=frame_type_select)

                theme_color_picker("dataframeBorderColor", "DataFrame Border", label_font_size='16px', label_field_width=100, frame_type=frame_type_select)

            with col2:

                with st_yled.container(
                    key="color-ext-preview",
                    background_color=st.session_state[f'{preview_selector_prefix}-backgroundColor'],
                    border = False
                ):

                    st_yled.markdown("[Link Color](https://www.google.com)",
                                    color=st.session_state[f'{preview_selector_prefix}-linkColor'],
                                    key="linkcolor-preview")

                    st_yled.code("# Code Background\nprint(\"Hello\")", background_color=st.session_state[f'{preview_selector_prefix}-codeBackgroundColor'],)


                    with st_yled.container(key="dataframe-border-color-preview",
                                            border_width='3px',
                                            border_style='solid',
                                            border_color=st.session_state[f'{preview_selector_prefix}-dataframeBorderColor'],):

                    
                        with st_yled.container(background_color=st.session_state[f'{preview_selector_prefix}-dataframeHeaderBackgroundColor'],
                                                key="dataframe-header-background-preview"):

                            st_yled.markdown("", width=24)

                    
    #region Font Tabs
    with tab_font:
        
        frame_type_select, preview_selector_prefix = frame_select_reset_bar(
            key="theme-font-frame-reset-bar",
            reset_keys=[
                "font",
                "headingFont",
                "baseFontSize",
                "baseFontWeight",
                "codeFont",
                "codeFontSize",
                "codeFontWeight",
            ])

        font_cont = st.container(key="theme-font-container")

        with font_cont:

            theme_font_input("font", "Base Font", frame_type=frame_type_select, key="theme-base-font-input")

            theme_font_input("headingFont", "Heading Font", frame_type=frame_type_select, key="theme-heading-font-input")

            if frame_type_select == "main":
                
                theme_size_input("baseFontSize", "Base Size", frame_type=frame_type_select, return_value_type="int", allowed_units=['px'])

                theme_weight_input("baseFontWeight", "Base Weight", frame_type=frame_type_select)


        with st_yled.expander("More Font Options",
                            key="theme-font-ext-expander",
                            border_width='0px'):

            font_ext_cont = st.container(key="theme-font-ext-container")
            
            with font_ext_cont:
                
                theme_font_input("codeFont", "Code Font", label_font_size='16px', label_field_width=120, frame_type=frame_type_select)

                theme_size_input("codeFontSize", "Code Size", label_font_size='16px', label_field_width=120, frame_type=frame_type_select, return_value_type="tuple", allowed_units=['px', 'rem'])

                theme_weight_input("codeFontWeight", "Code Weight", label_font_size='16px', label_field_width=120, frame_type=frame_type_select)

    #region Border Tab

    with tab_border:

        frame_type_select, preview_selector_prefix = frame_select_reset_bar(
            key="theme-border-frame-reset-bar",
            reset_keys=[
                "borderColor",
                "showWidgetBorder",
                "showSidebarBorder",
            ]
        )

        border_cont = st.container(key="theme-border-container")

        col1, col2 = border_cont.columns([2,1])

        # Define Color Pickers
        with col1.container(key="border-selectors"):

            theme_color_picker("borderColor", "Border Color", label_font_size='20px', frame_type=frame_type_select)

            theme_checkbox("showWidgetBorder", "Widget Border", label_font_size='20px', frame_type=frame_type_select)

            if frame_type_select == "main":
                theme_checkbox("showSidebarBorder", "Sidebar Border", label_font_size='20px', frame_type=frame_type_select)

        # Preview Pane
        with col2:

            with st_yled.container(
                key="border-preview",
                background_color=st.session_state[f'{preview_selector_prefix}-backgroundColor'],
                border = False
            ):

                # Border Color Preview
                with st_yled.container(border_width='3px',
                                            border_style='solid',
                                            border_color=st.session_state[f'{preview_selector_prefix}-borderColor'],
                                            key="bordercolor-preview"):

                    st_yled.markdown("**Border Color**")

                # Input Widget Border Preview
                if st.session_state[f'{preview_selector_prefix}-showWidgetBorder']:
                    st_yled.text_input("Input Widget Border", border_width='2px', border_style='solid', border_color=st.session_state[f'{preview_selector_prefix}-borderColor'])
                else:
                    st_yled.text_input("Input Widget Border")

                # Sidebar Border Preview
                if frame_type_select == "main":

                    with st_yled.container(
                        key="sidebar-border-preview",
                        width = 120,
                        horizontal=True
                    ):  
                        
                        if st.session_state[f'{preview_selector_prefix}-showSidebarBorder']:
                            css = f"""
                            .st-key-sidebar-border-box-preview {{
                                border-right: 2px solid {st.session_state[f'{preview_selector_prefix}-borderColor']};
                            }}
                            """
                            st.html(f"<style>{css}</style>")                    

                        with st.container(
                            width=40,
                            key="sidebar-border-box-preview"
                        ):
                            st.write(" ")

    #region Radius Tab

    with tab_radius:

        frame_type_select, preview_selector_prefix = frame_select_reset_bar(
            key="theme-radius-frame-reset-bar",
            reset_keys=[
                "baseRadius",
                "buttonRadius",
            ]
        )
        
        radius_cont = st.container(key="theme-radius-container")

        col1, col2 = radius_cont.columns([2,1])

        # Define Radius Selectors
        with col1.container(key="radius-selectors"):

            theme_size_input("baseRadius", "Base Radius", label_font_size='20px', frame_type=frame_type_select)
            theme_size_input("buttonRadius", "Button Radius", label_font_size='20px', frame_type=frame_type_select)

        # Preview Pane
        with col2:

            with st_yled.container(
                key="radius-preview",
            ):

                base_radius_val = st.session_state[f'{preview_selector_prefix}-baseRadius'][0]
                base_radius_unit = st.session_state[f'{preview_selector_prefix}-baseRadius'][1]
                
                css = f"""
                .st-key-radius-preview-base {{
                    border-radius: {base_radius_val}{base_radius_unit};
                    width: calc(100% - 48px);
                }}
                """
                st.html(f"<style>{css}</style>")

                with st_yled.container(
                    key="radius-preview-base",
                    height=68,
                    background_color=st.session_state[f'{preview_selector_prefix}-primaryColor'],
                ):
                    st_yled.markdown("**Base Radius**", color='#FFFFFF', width='content')

                button_radius_val = st.session_state[f'{preview_selector_prefix}-buttonRadius'][0]
                button_radius_unit = st.session_state[f'{preview_selector_prefix}-buttonRadius'][1]

                css = f"""
                .st-key-radius-preview-button button {{
                    border-radius: {button_radius_val}{button_radius_unit};
                }}
                """

                st.html(f"<style>{css}</style>")

                st_yled.button(
                    "Button Radius",
                    key="radius-preview-button",
                    type="primary")