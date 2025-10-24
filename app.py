import streamlit as st
import st_yled

import uiconfig
import re
from urllib.parse import urlparse


def get_updated_theme_config():
    """Check in session state which theme values were updated compared to default

        dict structure

        {'theme-primaryColor': '#ff0000', ...,
        'theme-sidebar-primaryColor': '#00ff00', ...,
        }

        Returns:
            dict: updated theme config values

    """
    
    updated_config = {}

    for key in st.session_state:
        if key.startswith("theme-") and not key.endswith("-default"):
            default_key = f"{key}-default"
            if st.session_state[key] != st.session_state.get(default_key, None):
                
                # Format correctly for toml
                if isinstance(st.session_state[key], bool):
                    updated_config[key] = "true" if st.session_state[key] else "false"
                elif isinstance(st.session_state[key], tuple):
                    size_value, size_unit = st.session_state[key]
                    updated_config[key] = f'\"{size_value}{size_unit}\"'
                
                elif isinstance(st.session_state[key], int):
                    updated_config[key] = f'{st.session_state[key]}'
                else:
                    updated_config[key] = f'\"{st.session_state[key]}\"'

    return updated_config


def format_theme_toml(theme_txt: str, section_name: str) -> str:
    """Format theme dictionary into toml string for given section

    Returns:
        str: formatted toml string
    """
    toml_line = f"[{section_name}]\n\n"
    toml_line += theme_txt

    return toml_line


def set_config_toml(template_path: str, updated_themes: dict) -> str:

    with open(template_path, "r") as f:
        config_toml = f.readlines()

    form_type = None
    config_lines_update = []

    theme_updates = []
    theme_sidebar_updates = []

    for line in config_toml:
        
        # Remove newlines
        line = line.rstrip('\n')

        if line.startswith("[theme]"):
            form_type = "theme"
        elif line.startswith("[theme.sidebar]"):
            form_type = "theme-sidebar"
        elif line.startswith("["):
            form_type = None
        
        if form_type and re.match(r"^# [a-zA-Z]+ =$", line.strip()):

            config_key = line.strip().replace("# ", "").replace(" =", "")
            config_key_form = f"{form_type}-{config_key}"

            if config_key_form in updated_themes:

                key_line = f"{config_key} = {updated_themes[config_key_form]}"
                config_lines_update.append(key_line)

                if form_type == "theme":
                    theme_updates.append(key_line)
                elif form_type == "theme-sidebar":
                    theme_sidebar_updates.append(key_line)
                else:
                    raise ValueError("Unknown form type")
            else:
                config_lines_update.append(line)
        
        else:
            config_lines_update.append(line)

    return "\n".join(config_lines_update), '\n'.join(theme_updates), '\n'.join(theme_sidebar_updates)


def render_export_theme(config_toml_template_path: str):

    updated_themes = get_updated_theme_config()
    config_toml, theme_updates, theme_sidebar_updates = set_config_toml(config_toml_template_path, updated_themes)

    cont = st.container(key="export-theme-container")
    
    with cont:
        st_yled.markdown("1. Download the `config.toml` file", key="export-theme-step-1-markdown")
        st_yled.markdown("2. Make sure your app has a `.streamlit` directory in the project root", key="export-theme-step-2-markdown")
        st_yled.markdown("3. Place the `config.toml` file inside the `.streamlit` directory", key="export-theme-step-3-markdown")
        st_yled.markdown(
            "More information in the [Streamlit docs](https://docs.streamlit.io/develop/api-reference/configuration/config.toml)",
            font_size="12px",
            key="export-theme-streamlit-docs-link")
        
        st.write("")

        with st.expander("I already have a config.toml file"):
            
            with st.container(key="export-theme-updated-theme-container"):

                if not theme_updates and not theme_sidebar_updates:
                    st.write("")
                    st.markdown("No theme updated found")
                else:
                    st.write("")
                    st.markdown("Copy and add/replace sections in your file")
                    
                    main_theme_code = format_theme_toml(theme_updates, "theme")
                    sidebar_theme_code = format_theme_toml(theme_sidebar_updates, "theme.sidebar")

                    if theme_updates and theme_sidebar_updates:
                        theme_tab, sidebar_tab = st_yled.tabs(["[theme]", "[theme.sidebar]"], key="export-theme-updated-theme-tabs")

                        with theme_tab:
                            st.write("")
                            st.code(main_theme_code)
                        with sidebar_tab:
                            st.write("")
                            st.code(sidebar_theme_code)

                    elif theme_updates:
                        theme_tab = st_yled.tabs(["[theme]"], key="export-theme-updated-theme-tabs")
                        with theme_tab[0]:
                            st.write("")
                            st.code(main_theme_code)

                    else:
                        sidebar_tab = st_yled.tabs(["[theme.sidebar]"], key="export-theme-updated-theme-tabs")
                        with sidebar_tab[0]:
                            st.write("")
                            st.code(sidebar_theme_code)
                    
                    st.write("")

        st.write("")

        bgroup_cont = st.container(key="export-theme-button-group-container", horizontal=True)

        if bgroup_cont.download_button("Download config.toml", data=config_toml, file_name="config.toml", mime="text/plain", type='primary'):
            st.rerun()

        if bgroup_cont.button("Cancel"):
            st.rerun()


@st.dialog(title="Export Theme", width="medium")
def export_config_toml():

    url = st.context.url


    parsed_url = urlparse(str(url))
    if not parsed_url.scheme or not parsed_url.netloc:
        st.error("Invalid URL format")
        raise ValueError("Invalid URL format")

    path_parts = parsed_url.path.strip('/').split('/') if parsed_url.path.strip('/') else []
    url = path_parts

    if len(url) == 1:
        export_page = "theme"
    elif url[1] == "elements":
        export_page = "elements"
    else:
        
        # TODO Fix Here
        st.error("Invalid Export Page Selected")
        raise ValueError("Invalid URL")
    

    if export_page == "theme":
        render_export_theme(uiconfig.CONFIG_TOML_TEMPLATE_PATH)


# region UI

st_yled.init()

theme_page = st.Page("pages/theme.py", title="Theme")
element_page = st.Page("pages/elements.py", title="Elements")
 
pg = st.navigation([theme_page, element_page])

st.set_page_config(page_title="st_yled studio",
                    page_icon="assets/st_yled Logo.png")

st.logo("assets/st_yled Logo.png", size="large")

sticky_header = st_yled.container(
    key="sticky-header",
    horizontal=True,
    vertical_alignment="distribute",
)

with sticky_header:
    
    with st.container(horizontal=True, horizontal_alignment="left"):
        
        #st.image("assets/st_yled Logo.png", width=40)
        st_yled.title("st_yled studio", font_size='32px')

    with st.container(horizontal=True, horizontal_alignment="right"):

        st_yled.button("Export to your App", type='primary', icon=':material/file_export:', on_click=export_config_toml)
        
        # Option for popover export
        # with st_yled.popover("Export Theme", icon=':material/file_export:', background_color=uiconfig.PRIMARY_COLOR_DEFAULT, width=172, color="#ffffff"):
        #     render_export_theme()
        
        st_yled.button("Help", icon=':material/help:')

pg.run()