from typing import Literal

import streamlit as st
import st_yled

import uiconfig
import converters
import utils


def init_theme_session_state(key: str, default_value: str):
    """Initialize session state variables for theme settings with default values."""
    
    if key not in st.session_state:
        st.session_state[key] = default_value
        st.session_state[f'{key}-default'] = default_value

def update_st_from_input(theme_property: str, input_selector_key: str):
    st.session_state[theme_property] = st.session_state[input_selector_key]

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

    with st.container(horizontal=True, vertical_alignment="center"):

        st_yled.markdown(label, font_size=label_font_size, width=label_field_width)

        st_yled.code(
                color_state_value,
                language = None,
                font_size='14px',
                color='grey' if color_is_default else None,
                width=124,
            )

        # If 

        if color_state_value.startswith('#') and len(color_state_value) == 9:
            display_color = converters.hex_with_alpha_to_hex(color_state_value)
        else:
            display_color = color_state_value


        color_picker = st.color_picker(
            f"Pick {label}",
            value=display_color,
            key=theme_property + "-picker",
            label_visibility = "collapsed",
            on_change=update_st_from_input,
            args=(session_state_key, theme_property + "-picker"),
        )

        st_yled.caption("Select Color", width=100)


def theme_checkbox(theme_property: str,
                   label: str,
                   label_font_size: str = '20px',
                   label_field_width: int = 140,
                   frame_type: Literal["main", "sidebar"] = "main"):
    
    if frame_type == "sidebar":
        theme_property = "sidebar-" + theme_property
    
    session_state_key = f"theme-{theme_property}"

    with st.container(horizontal=True, vertical_alignment="center"):

        st_yled.markdown(label, font_size=label_font_size, width=label_field_width)

        st_yled.checkbox(
            'Enable',
            label_visibility="collapsed",
            value=st.session_state[session_state_key],
            key=theme_property + "-checkbox",
            on_change=update_st_from_input,
            args=(session_state_key, theme_property + "-checkbox")
        )

        st_yled.caption("Enable", width=100)


def theme_size_input(theme_property: str,
                        label: str,
                        label_font_size: str = '20px',
                        label_field_width: int = 140,
                        frame_type: Literal["main", "sidebar"] = "main"):
    
    if frame_type == "sidebar":
        theme_property = "sidebar-" + theme_property
    
    session_state_key = f"theme-{theme_property}"
    
    # Get current value tuple or parse from string
    current_value = st.session_state[session_state_key]
    current_number, current_unit = current_value

    with st.container(horizontal=True, vertical_alignment="center", width=400):

        st_yled.markdown(label, font_size=label_font_size, width=label_field_width)

        # Number input
        number_value = st.number_input(
            f"Set {label} value",
            value=current_number,
            min_value=0.0,
            step=0.1 if current_unit == 'rem' else 1.0,
            key=theme_property + "-number",
            label_visibility="collapsed",
        )

        # Unit selectbox
        unit_value = st.selectbox(
            f"Set {label} unit",
            options=['px', 'rem'],
            index=0 if current_unit == 'px' else 1,
            key=theme_property + "-unit",
            label_visibility="collapsed",
            width=90,
        )
        
        number_value = round(number_value,1)

        # Update session state with tuple value
        new_value = (number_value, unit_value)
        st.session_state[session_state_key] = new_value


# Initialize main theme session state
init_theme_session_state('theme-primaryColor', uiconfig.PRIMARY_COLOR_DEFAULT)
init_theme_session_state('theme-backgroundColor', uiconfig.BACKGROUND_COLOR_DEFAULT)
init_theme_session_state('theme-secondaryBackgroundColor', uiconfig.SECONDARY_BACKGROUND_COLOR_DEFAULT)
init_theme_session_state('theme-textColor', uiconfig.TEXT_COLOR_DEFAULT)
init_theme_session_state('theme-linkColor', uiconfig.LINK_COLOR_DEFAULT)
init_theme_session_state('theme-codeBackgroundColor', uiconfig.CODE_BG_COLOR_DEFAULT)
init_theme_session_state('theme-borderColor', uiconfig.BORDER_COLOR_DEFAULT)
init_theme_session_state('theme-dataframeBorderColor', uiconfig.DATAFRAME_BORDER_COLOR_DEFAULT)
init_theme_session_state('theme-dataframeHeaderBackgroundColor', uiconfig.DATAFRAME_HEADER_BG_COLOR_DEFAULT)

# Initialize sidebar theme session state
init_theme_session_state('theme-sidebar-primaryColor', uiconfig.SIDEBAR_PRIMARY_COLOR_DEFAULT)
init_theme_session_state('theme-sidebar-backgroundColor', uiconfig.SIDEBAR_BACKGROUND_COLOR_DEFAULT)
init_theme_session_state('theme-sidebar-secondaryBackgroundColor', uiconfig.SIDEBAR_SECONDARY_BACKGROUND_COLOR_DEFAULT)
init_theme_session_state('theme-sidebar-textColor', uiconfig.SIDEBAR_TEXT_COLOR_DEFAULT)
init_theme_session_state('theme-sidebar-linkColor', uiconfig.SIDEBAR_LINK_COLOR_DEFAULT)
init_theme_session_state('theme-sidebar-codeBackgroundColor', uiconfig.SIDEBAR_CODE_BG_COLOR_DEFAULT)
init_theme_session_state('theme-sidebar-borderColor', uiconfig.SIDEBAR_BORDER_COLOR_DEFAULT)
init_theme_session_state('theme-sidebar-dataframeBorderColor', uiconfig.SIDEBAR_DATAFRAME_BORDER_COLOR_DEFAULT)
init_theme_session_state('theme-sidebar-dataframeHeaderBackgroundColor', uiconfig.SIDEBAR_DATAFRAME_HEADER_BG_COLOR_DEFAULT)

# Initialize border theme session state
init_theme_session_state('theme-showWidgetBorder', uiconfig.SHOW_INPUT_WIDGET_BORDER_DEFAULT)
init_theme_session_state('theme-showSidebarBorder', uiconfig.SHOW_SIDEBAR_BORDER_DEFAULT)

# Initialize sidebar border theme session state
init_theme_session_state('theme-sidebar-showWidgetBorder', uiconfig.SIDEBAR_SHOW_INPUT_WIDGET_BORDER_DEFAULT)

# Initialize radius theme session state
init_theme_session_state('theme-baseRadius', uiconfig.BASE_RADIUS_DEFAULT)
init_theme_session_state('theme-buttonRadius', uiconfig.BUTTON_RADIUS_DEFAULT)

# Initialize sidebar radius theme session state
init_theme_session_state('theme-sidebar-baseRadius', uiconfig.SIDEBAR_BASE_RADIUS_DEFAULT)
init_theme_session_state('theme-sidebar-buttonRadius', uiconfig.SIDEBAR_BUTTON_RADIUS_DEFAULT)



# region UI

st.markdown("**> Theme** Configure global styling of your Streamlit App")

tab_color, tab_font, tab_border, tab_radius = st_yled.tabs(
    ["Color", "Font", "Border", "Radius"],
    key = "theme-tabs"
)

#region Color Tabs
with tab_color:

    frame_type = utils.segmented_control_toggle(":material/width_full: Main", ":material/side_navigation: Sidebar", key="theme-color-frame-type-toggle")

    if frame_type == ":material/side_navigation: Sidebar":
        frame_type_select = "sidebar"
        preview_selector_prefix = "theme-sidebar"
    else:
        frame_type_select = "main"
        preview_selector_prefix = "theme"
    

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
            height=400,
            background_color=st.session_state[f'{preview_selector_prefix}-backgroundColor'],
            border = True
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

    st.write("")
    st.write("")
    
    with st.expander("More Color Options"):
        
        color_ext_cont = st.container(key="theme-color-ext-container")

        col1, col2 = color_ext_cont.columns([2,1])

        with col1.container(key="color-ext-selectors"):

            theme_color_picker("linkColor", "Link", label_font_size='16px', label_field_width=100, frame_type=frame_type_select)

            theme_color_picker("dataframeHeaderBackgroundColor", "DataFrame Header", label_font_size='16px', label_field_width=100, frame_type=frame_type_select)

            theme_color_picker("dataframeBorderColor", "DataFrame Border", label_font_size='16px', label_field_width=100, frame_type=frame_type_select)

            theme_color_picker("codeBackgroundColor", "Code Background", label_font_size='16px', label_field_width=100, frame_type=frame_type_select)

        with col2:

            with st_yled.container(
                key="color-ext-preview",
                background_color=st.session_state[f'{preview_selector_prefix}-backgroundColor'],
                border = False
            ):

                st_yled.markdown("[Link Color](https://www.google.com)",
                                color=st.session_state[f'{preview_selector_prefix}-linkColor'],
                                key="linkcolor-preview")

                st.write("")
                st.write("")

                with st_yled.container(background_color=st.session_state[f'{preview_selector_prefix}-dataframeHeaderBackgroundColor'],
                                        key="dataframe-header-background-preview"):

                    st_yled.markdown("**Dataframe Header**")

                
                with st_yled.container(key="dataframe-border-color-preview",
                                        border_width='3px',
                                        border_style='solid',
                                        border_color=st.session_state[f'{preview_selector_prefix}-dataframeBorderColor'],):

                    st_yled.markdown("**Dataframe Border**", key="dataframe-border-color-preview-text")

                st.write("")

                st_yled.code("# Code Background\nprint(\"Hello\")", background_color=st.session_state[f'{preview_selector_prefix}-codeBackgroundColor'],)


with tab_border:

    frame_type = utils.segmented_control_toggle(":material/width_full: Main", ":material/side_navigation: Sidebar", key="theme-border-frame-type-toggle")

    if frame_type == ":material/side_navigation: Sidebar":
        frame_type_select = "sidebar"
        preview_selector_prefix = "theme-sidebar"
    else:
        frame_type_select = "main"
        preview_selector_prefix = "theme"
    
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
            height=400,
            background_color=st.session_state[f'{preview_selector_prefix}-backgroundColor'],
        ):

            # Border Color Preview
            with st_yled.container(border_width='3px',
                                        border_style='solid',
                                        border_color=st.session_state[f'{preview_selector_prefix}-borderColor'],
                                        key="bordercolor-preview"):

                st_yled.markdown("**Border Color**")

            st.write("")

            # Input Widget Border Preview
            if st.session_state[f'{preview_selector_prefix}-showWidgetBorder']:
                st_yled.text_input("Input Widget Border", border_width='2px', border_style='solid', border_color=st.session_state[f'{preview_selector_prefix}-borderColor'])
            else:
                st_yled.text_input("Input Widget Border")

            st.write("")

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


with tab_radius:

    frame_type = utils.segmented_control_toggle(":material/width_full: Main", ":material/side_navigation: Sidebar", key="theme-radius-frame-type-toggle")

    if frame_type == ":material/side_navigation: Sidebar":
        frame_type_select = "sidebar"
        preview_selector_prefix = "theme-sidebar"
    else:
        frame_type_select = "main"
        preview_selector_prefix = "theme"
    
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
            }}
            """
            st.html(f"<style>{css}</style>")

            with st_yled.container(
                key="radius-preview-base",
                height=60,
                background_color=st.session_state[f'{preview_selector_prefix}-primaryColor'],
            ):
                st_yled.markdown("**Base Radius**", color='#FFFFFF')

            st.write("")

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