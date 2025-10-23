from typing import Literal

import streamlit as st
import st_yled

import uiconfig
import converters

if not 'theme-primaryColor' in st.session_state:
    st.session_state['theme-primaryColor'] = uiconfig.PRIMARY_COLOR_DEFAULT

# Define session state
if not 'theme-backgroundColor' in st.session_state:
    st.session_state['theme-backgroundColor'] = uiconfig.BACKGROUND_COLOR_DEFAULT

if not 'theme-secondaryBackgroundColor' in st.session_state:
    st.session_state['theme-secondaryBackgroundColor'] = uiconfig.SECONDARY_BACKGROUND_COLOR_DEFAULT

if not 'theme-textColor' in st.session_state:
    st.session_state['theme-textColor'] = uiconfig.TEXT_COLOR_DEFAULT

if not 'theme-linkColor' in st.session_state:
    st.session_state['theme-linkColor'] = uiconfig.LINK_COLOR_DEFAULT

if not 'theme-codeBackgroundColor' in st.session_state:
    st.session_state['theme-codeBackgroundColor'] = uiconfig.CODE_BG_COLOR_DEFAULT

if not 'theme-borderColor' in st.session_state:
    st.session_state['theme-borderColor'] = uiconfig.BORDER_COLOR_DEFAULT

if not 'theme-dataframeBorderColor' in st.session_state:
    st.session_state['theme-dataframeBorderColor'] = uiconfig.DATAFRAME_BORDER_COLOR_DEFAULT

if not 'theme-dataframeHeaderBackgroundColor' in st.session_state:
    st.session_state['theme-dataframeHeaderBackgroundColor'] = uiconfig.DATAFRAME_HEADER_BG_COLOR_DEFAULT

# SIDEBAR session state variables
if not 'theme-sidebar-primaryColor' in st.session_state:
    st.session_state['theme-sidebar-primaryColor'] = uiconfig.SIDEBAR_PRIMARY_COLOR_DEFAULT

if not 'theme-sidebar-backgroundColor' in st.session_state:
    st.session_state['theme-sidebar-backgroundColor'] = uiconfig.SIDEBAR_BACKGROUND_COLOR_DEFAULT

if not 'theme-sidebar-secondaryBackgroundColor' in st.session_state:
    st.session_state['theme-sidebar-secondaryBackgroundColor'] = uiconfig.SIDEBAR_SECONDARY_BACKGROUND_COLOR_DEFAULT

if not 'theme-sidebar-textColor' in st.session_state:
    st.session_state['theme-sidebar-textColor'] = uiconfig.SIDEBAR_TEXT_COLOR_DEFAULT

if not 'theme-sidebar-linkColor' in st.session_state:
    st.session_state['theme-sidebar-linkColor'] = uiconfig.SIDEBAR_LINK_COLOR_DEFAULT

if not 'theme-sidebar-codeBackgroundColor' in st.session_state:
    st.session_state['theme-sidebar-codeBackgroundColor'] = uiconfig.SIDEBAR_CODE_BG_COLOR_DEFAULT

if not 'theme-sidebar-borderColor' in st.session_state:
    st.session_state['theme-sidebar-borderColor'] = uiconfig.SIDEBAR_BORDER_COLOR_DEFAULT

if not 'theme-sidebar-dataframeBorderColor' in st.session_state:
    st.session_state['theme-sidebar-dataframeBorderColor'] = uiconfig.SIDEBAR_DATAFRAME_BORDER_COLOR_DEFAULT

if not 'theme-sidebar-dataframeHeaderBackgroundColor' in st.session_state:
    st.session_state['theme-sidebar-dataframeHeaderBackgroundColor'] = uiconfig.SIDEBAR_DATAFRAME_HEADER_BG_COLOR_DEFAULT


def update_st_from_input(theme_property: str, input_selector_key: str):
    st.session_state[theme_property] = st.session_state[input_selector_key]

def theme_color_picker(theme_property: str,
                        default_hex_value: str,
                        label: str,
                        label_font_size: str = '20px',
                        label_field_width: int = 140,
                        frame_type: Literal["main", "sidebar"] = "main"):

    if frame_type == "sidebar":
        theme_property = "sidebar-" + theme_property
    
    session_state_key = f"theme-{theme_property}"

    color_state_value = st.session_state[session_state_key]

    color_is_default = color_state_value == default_hex_value


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
            key=session_state_key + "-picker",
            label_visibility = "collapsed",
            on_change=update_st_from_input,
            args=(session_state_key, session_state_key + "-picker"),
        )

        st_yled.caption("Select Color", width=100)


st.markdown("**> Theme** Configure global styling of your Streamlit App")


tab_color, tab_font, tab_border, tab_sidebar = st_yled.tabs(
    ["Color", "Font", "Border", "Radius"],
    key = "theme-tabs"
)


with tab_color:

    frame_type = st_yled.radio("Frame Type",
                                options=[":material/width_full: Main", ":material/side_navigation: Sidebar"],
                                key="theme-frame-type",
                                horizontal=True,
                                label_visibility="collapsed",
                                font_size='14px')

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

        theme_color_picker("primaryColor", uiconfig.PRIMARY_COLOR_DEFAULT, "Primary", frame_type=frame_type_select)

        theme_color_picker("backgroundColor", uiconfig.BACKGROUND_COLOR_DEFAULT, "Background", frame_type=frame_type_select)

        theme_color_picker("secondaryBackgroundColor", uiconfig.SECONDARY_BACKGROUND_COLOR_DEFAULT, "Secondary Background", frame_type=frame_type_select)

        theme_color_picker("textColor", uiconfig.TEXT_COLOR_DEFAULT, "Text", frame_type=frame_type_select)

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

            theme_color_picker("linkColor", uiconfig.LINK_COLOR_DEFAULT, "Link", label_font_size='16px', label_field_width=100, frame_type=frame_type_select)

            theme_color_picker("borderColor", uiconfig.BORDER_COLOR_DEFAULT, "Border", label_font_size='16px', label_field_width=100, frame_type=frame_type_select)

            theme_color_picker("dataframeHeaderBackgroundColor", uiconfig.DATAFRAME_HEADER_BG_COLOR_DEFAULT, "DataFrame Header", label_font_size='16px', label_field_width=100, frame_type=frame_type_select)

            theme_color_picker("dataframeBorderColor", uiconfig.DATAFRAME_BORDER_COLOR_DEFAULT, "DataFrame Border", label_font_size='16px', label_field_width=100, frame_type=frame_type_select)

            theme_color_picker("codeBackgroundColor", uiconfig.CODE_BG_COLOR_DEFAULT, "Code Background", label_font_size='16px', label_field_width=100, frame_type=frame_type_select)

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

                with st_yled.container(border_width='3px',
                                        border_style='solid',
                                        border_color=st.session_state[f'{preview_selector_prefix}-borderColor'],
                                        key="bordercolor-preview"):

                    st_yled.markdown("**Border Color**")

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