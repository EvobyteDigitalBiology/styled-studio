import logging
import os
import re
from urllib.parse import urlparse
import streamlit as st
import boto3
import st_yled
import dotenv

import uiconfig

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

dotenv.load_dotenv()

try:
    ses_client = boto3.client('ses', region_name=os.getenv("AWS_REGION"), 
                              aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                              aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))

    feedback_email = os.getenv("FEEDBACK_MAIL")
    if not feedback_email:
        raise ValueError("FEEDBACK_MAIL not set in environment variables")

except Exception as e:
    logger.error(f"Failed to create SES client: {e}")
    ses_client = None


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

                    # Round float values to 2 decimal places
                    if isinstance(size_value, float):
                        size_value = round(size_value, 2)

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


def format_css_from_dict(css_dict: dict) -> str:

    css_lines = []

    for selector in css_dict:
        css_lines.append(f"{selector} {{")
        for prop in css_dict[selector]:
            value = css_dict[selector][prop]
            css_lines.append(f"  {prop}: {value};")
        css_lines.append("}\n")

    return "\n".join(css_lines)



def render_export_theme(config_toml_template_path: str):

    st_yled.init()

    updated_themes = get_updated_theme_config()
    config_toml, theme_updates, theme_sidebar_updates = set_config_toml(config_toml_template_path, updated_themes)

    st.write("")

    cont = st_yled.container(key="export-theme-container")
    
    with cont:
        
        with st_yled.container(key="export-theme-info-box", background_color='#F6F6F6', padding="16px"):

            st_yled.markdown("1. Make sure your project has a `.streamlit` directory", key="export-theme-step-1-markdown")
            st_yled.markdown("2. Download and place the `config.toml` file inside the `.streamlit` directory", key="export-theme-step-2-markdown")
            # st_yled.markdown("3. Place the `config.toml` file inside the `.streamlit` directory", key="export-theme-step-3-markdown")

            st_yled.markdown(
                "More information in the [Streamlit docs](https://docs.streamlit.io/develop/api-reference/configuration/config.toml)",
                font_size="12px",
                key="export-theme-streamlit-docs-link")

        if not theme_updates and not theme_sidebar_updates:
            st_yled.info("**:material/notifications: No theme updates found - yet**\n\nUse the theme editor to make your first changes")
        
        else:
            with st_yled.expander("I already have a config.toml file",
                                    background_color=uiconfig.SECONDARY_BACKGROUND_COLOR_DEFAULT,
                                    key="export-theme-existing-config-expander",
                                    border_style="none"):
            
                st.write("")
                st.markdown("Copy and add/replace sections in your `config.toml` file")
                
                main_theme_code = format_theme_toml(theme_updates, "theme")
                sidebar_theme_code = format_theme_toml(theme_sidebar_updates, "theme.sidebar")

                if theme_updates and theme_sidebar_updates:
                    theme_tab, sidebar_tab = st_yled.tabs(["[theme]", "[theme.sidebar]"], key="export-theme-updated-theme-tabs")

                    with theme_tab:
                        st.code(main_theme_code)
                    with sidebar_tab:
                        st.code(sidebar_theme_code)

                elif theme_updates:
                    theme_tab = st_yled.tabs(["[theme]"], key="export-theme-updated-theme-tabs")
                    with theme_tab[0]:
                        st.code(main_theme_code)

                else:
                    sidebar_tab = st_yled.tabs(["[theme.sidebar]"], key="export-theme-updated-theme-tabs")
                    with sidebar_tab[0]:
                        st.code(sidebar_theme_code)
                
                st.write("")

        bgroup_cont = st.container(key="export-theme-button-group-container", horizontal=True)

        if bgroup_cont.download_button("Download config.toml", data=config_toml, file_name="config.toml", mime="text/plain", type='primary'):
            st.rerun()

        if bgroup_cont.button("Cancel"):
            st.rerun()



def render_export_elements():

    st_yled.init()

    # Extract all values related to elements from session state
    # Get for those elements the values and related css properties
    # Write properties into css format
    # Provide option to download css file OR copy code

    export_elements = {}
    excluded_elements_message = ""

    for key in st.session_state:

        if key.startswith("element-") and key.endswith("-value"):            
            
            css_prop_format = key.split("-")[-2]
            element_name = key.split("-")[1]

            if element_name not in uiconfig.ELEMENTS_EXCLUDED_FROM_CSS:
                if element_name not in export_elements:
                    export_elements[element_name] = {}
                export_elements[element_name][css_prop_format] = st.session_state[key]
            else:
                excluded_elements_message = f"Some elements are excluded from CSS export, e.g., {element_name}. Use \"Copy Python\" in the element editor instead."



    # Get CSS for element
    export_css = {}

    for element_name in export_elements.keys():

        element_config = st_yled.styler.get_element_style(element_name)
        element_config_css = element_config['css']

        for css_prop_format in export_elements[element_name]:
            
            # Example css_format
            # 
            # ".stButton:has(button[kind="secondary"]) > button":{
            #   "background-color":NULL
            # }
            
            css_format = element_config_css[css_prop_format]

            # css_selector example: .stButton:has(button[kind="secondary"]) > button

            for css_selector in css_format.keys():
                
                # css_prop example: background-color
                css_prop = list(css_format[css_selector].keys())[0]

                if css_selector not in export_css:
                    export_css[css_selector] = {}
                
                export_css[css_selector][css_prop] = export_elements[element_name][css_prop_format]
    
    # Convert export dict into css
    export_css_format = format_css_from_dict(export_css)

    cont = st.container(key="export-elements-container")
    
    with cont:

        with st_yled.container(key="export-elements-info-box", background_color='#F6F6F6', padding="16px"):

            st_yled.markdown("1. Make sure your project has a `.streamlit` directory", key="export-elements-step-1-markdown")
            
            st_yled.markdown("2. Download and place the `st-styled.css` file inside the `.streamlit` directory", key="export-elements-step-2-markdown")

            st_yled.markdown(":material/notification_important: Make sure to run `st_yled.init()` on each app page", key="export-elements-note")

            st_yled.markdown(
                "More information in the [st_yled docs](https://st-styled.evo-byte.com/)",
                font_size="12px",
                key="export-elements-docs-link")
                    
        if not export_css_format:

            st_yled.info("**:material/notifications: No element updates found - yet**\n\nUse the element editor to create first styling", key="export-elements-no-updates-info")

        else:

            with st_yled.expander("I already have a st-styled.css file",
                                    border_style='none',
                                    background_color=uiconfig.SECONDARY_BACKGROUND_COLOR_DEFAULT,
                                    key="export-elements-existing-css-expander"):

                st.write("")
                st.markdown("Copy and add/replace sections in your `st-styled.css` file")
                    
                st.code(export_css_format)

        if excluded_elements_message != "":
            st_yled.markdown(f":material/notification_important: {excluded_elements_message}",
                             key="export-elements-excluded-elements-note",
                             font_size="14px",
                             color="#31333F99")  

        bgroup_cont = st.container(key="export-elements-button-group-container", horizontal=True)

        if bgroup_cont.download_button("Download st-styled.css", data=export_css_format, file_name="st-styled.css", mime="text/plain", type='primary'):
            st.rerun()

        if bgroup_cont.button("Cancel"):
            st.rerun()

    # Required format
    # element name -> css property -> value



def render_export_components():

    st_yled.init()

    st.markdown("""
    Using new components in your app is super easy! Every component described here is available from the [st_yled Python package](https://st-styled.evo-byte.com/).
    Here are a few examples how to use them in your Streamlit app.
    """)

    st.write("")
    st.markdown("**Example: Card Component**")

    st_yled.code("""
st_yled.badge_card_one(
    badge_text="New",
    badge_icon=":material/star:",
    title="Badge Card",
    text="A card with a badge")
""")

    st.write("")
    st.markdown("**Example: Perform a page redirect**")
    
    st_yled.code("""
if st_yled.button("Go to Streamlit website"):
    st_yled.redirect("https://streamlit.io")""")

    if st.button("Close", type='secondary', width=90):
        st.rerun()


# region Dialogs

@st.dialog(title="Export to your app", width="medium")
def export_config_toml():

    url = st.context.url

    parsed_url = urlparse(str(url))
    if not parsed_url.scheme or not parsed_url.netloc:
        st.error("Invalid URL format")
        raise ValueError("Invalid URL format")

    path_parts = parsed_url.path.strip('/').split('/')
    url = path_parts

    if url[0] == "":
        export_page = "theme"
    elif url[0] == "elements":
        export_page = "elements"
    elif url[0] == "components" or url[0].startswith("component-detail"):
        export_page = "components"
    else:
        # TODO Fix Here
        st.error("Invalid Export Page Selected")
        raise ValueError("Invalid URL")
    

    if export_page == "theme":
        render_export_theme(uiconfig.CONFIG_TOML_TEMPLATE_PATH)
    elif export_page == "elements":
        render_export_elements()
    elif export_page == "components":
        render_export_components()
    else:
        st.error("Invalid Export Page Selected")
        raise ValueError("Invalid Export Page")


@st.dialog("Getting help", width="medium")
def render_help_dialog():
    
    st_yled.init()

    help_cont = st.container(key="help-dialog-container")

    with st_yled.container(key="help-dialog-intro-container",
                            horizontal=True,
                            vertical_alignment="center",
                            background_color="#F6F6F6",
                            padding='16px'):

        st.image("assets/logo_small.svg", width=40)

        st_yled.markdown("Welcome to st_yled studio - your place for beautiful Streamlit apps", key="help-dialog-welcome-markdown")

    st.markdown("""
    With st_yled studio you can easily configure the layout and adapt UI elements of your Streamlit app.
    Use st_yled studio together with the [st_yled Python package](https://st-styled.evo-byte.com/) to apply custom UI styling in your own apps.
    """)

    st.write("")
    st.write("")

    st.markdown("""
    On the Theme page you can test and configure your global theme, including primary color and font.
    """)

    with st_yled.expander("More on **Theme**",
                            border_width=0,
                            background_color=uiconfig.SECONDARY_BACKGROUND_COLOR_DEFAULT,
                            key="help-dialog-theme-expander",
                            padding="0px"):

        with st_yled.container(key="help-dialog-theme-expander-content",
                               background_color="#f7f8fa",
                               padding="16px"):

            st_yled.markdown("""
            Streamlit comes with built-in configuration options for different aspects of its layout. 
            This includes primary and secondary colors, background or font settings.
            
            Use the Theme editor to try out different configurations for your app. The preview pages will help you guide your optimal layout.
            
            Those settings are configured in your app with a `config.toml` file. This file is placed inside the `.streamlit` folder at your project root directory.
            
            Your can create and download the `config.toml` by clicking the *Export to your app* button.
            The `config.toml` file contains `[theme]` and `[theme.sidebar]` section where global theme settings can be configured.
            """, 
            key="help-dialog-more-on-theme-markdown")

            st_yled.markdown(
                "More information in the [Streamlit docs](https://docs.streamlit.io/develop/api-reference/configuration/config.toml)",
                font_size="12px",
                key="help-theme-streamlit-docs-link")

    st.markdown("""
    On the Elements page you can customize many Streamlit components and widgets with your own unique colors, sizes and backgrounds.
    This gives your apps a distinct appeal and alignment with your brand.
    """)

    with st_yled.expander("More on **Elements**",
                            border_width=0,
                            background_color=uiconfig.SECONDARY_BACKGROUND_COLOR_DEFAULT,
                            key="help-dialog-elements-expander",
                            padding="0px"):

        with st_yled.container(key="help-dialog-elements-expander-content",
                               background_color="#f7f8fa",
                               padding="16px"):

            st_yled.markdown("""
            Customizing Streamlit elements is super easy. Just add an element to the editor pane and configure properties like color, text or border. 
            The interactive preview shows the effect of those changes. 
            
            Once you are happy, click *Export to your app*. From here you can download the `st-styled.css` file and place in the `.streamlit` folder of your app,
            or directly copy the css code.
            
            You can also copy Python code directly from the editor cards of each element.

            :material/notifications: Styling individual elements requires the `st-styled` package available in your Streamlit project.
            On each of your app pages run `st_yled.init()` to load the configurations from the `st-styled.css`.
            """,
            key="help-dialog-more-on-elements-markdown")

            st_yled.markdown(
                "More information in the [st-styled Python package](https://st-styled.evo-byte.com/)",
                font_size="12px",
                key="help-elements-styled-docs-link")


    st.markdown("""
    On the New Components page you can find new Streamlit components available from the st_yled package.
    """)

    with st_yled.expander("More on **New Components**",
                            border_width=0,
                            background_color=uiconfig.SECONDARY_BACKGROUND_COLOR_DEFAULT,
                            key="help-dialog-new-components-expander",
                            padding="0px"):

        with st_yled.container(key="help-dialog-new-components-expander-content",
                               background_color="#f7f8fa",
                               padding="16px"):

            st_yled.markdown("""
            The st_yled package comes with new components that extend the default Streamlit functionality.
            Those components are designed to help you build even more engaging and interactive apps, faster and easier.
            Each component comes with documentation, usage patterns and code examples to get you started quickly.
                             
            Explore the available components and integrate them into your apps to enhance user experience.
            Send us a message if you have ideas for new components you would like to see!
            """,
            key="help-dialog-more-on-new-components-markdown")

    st.write("")

    st.markdown("""
    Click *Export to your app* when you are happy with your styling. 
    From here you can download or copy the theme or element styling to your Streamlit project.
    """)

    st.write("")

    if st.button("Close", type='secondary', width=90):
        st.rerun()
    
    st_yled.markdown("""
    Do you have questions, ideas or suggestions?
    """,
    key="help-dialog-contact-markdown")

    st_yled.markdown("""
    Join the [Github discussion](https://github.com/EvobyteDigitalBiology/st-styled/discussions) or email info@evo-byte.com
    """,
    font_size="12px",
    key="help-dialog-contact-link-markdown")



@st.dialog("Send your feedback", width="medium")
def render_feedback_dialog():

    st_yled.init()

    # Which features, functions or components are missing? 
    feedback_cont = st.container(key="feedback-dialog-container")

    with st_yled.container(key="feedback-dialog-intro-container",
                            horizontal=True,
                            vertical_alignment="center",
                            background_color="#F6F6F6",
                            padding='16px'):

        st.image("assets/logo_small.svg", width=40)

        st_yled.markdown("""
Which **features**, **styles** or **components** are missing?

Send us your **feedback** and **ideas**!
""",
key="feedback-dialog-intro-markdown")
    
    st.write("")

    with st_yled.container(key="feedback-dialog-form-container"):

        email = st_yled.text_input("Your email (optional)", width=512, key="feedback-email-input")

        feedback = st_yled.text_area("Your feedback, ideas or suggestions", width=512, key="feedback-text-area")

        st.write("")

        bgroup_cont = st_yled.container(key="send-feedback-button-group-container", horizontal=True)

        if bgroup_cont.button("Send", icon=':material/send:', type='primary', key="send-feedback-button"):
            
            if feedback.strip() == "":
                st_yled.warning("Please provide feedback before sending", width=512, key="feedback-empty-warning")
            else:

                st.session_state["feedback-submitted"] = True
                if email.strip() != "":
                    logger.info("Feedback received from %s", email)
                    print(f"Feedback received from {email}")

                if ses_client:

                    email_message = f"Feedback:\n{feedback}\n\n"
                    if email.strip() != "":
                        email_message += f"From: {email}\n"

                    ses_client.send_email(
                        **{
                            "Source": feedback_email,
                            "Destination": {'ToAddresses': [feedback_email]},
                            "Message": {
                                "Subject": {"Data": "st_yled studio Feedback"},
                                "Body": {"Text": {"Data": email_message}},
                            },
                        }
                    )
                
                logger.info("Feedback received: %s", feedback)
                print(f"Feedback received: {feedback}")
            
                st_yled.rerun()

        if bgroup_cont.button("Cancel"):
            st_yled.rerun()

    st.write("")
    st.write("")


# region UI

st_yled.init()

theme_page = st.Page("pages/theme.py", title="Theme")
element_page = st.Page("pages/elements.py", title="Elements")
components_page = st.Page("pages/components.py", title="New Components")
components_detail = st.Page("pages/component_detail.py", title="Component Detail", url_path="component-detail")

 
pg = st.navigation([theme_page, element_page, components_page, components_detail])

st.set_page_config(page_title="st_yled studio",
                    page_icon="assets/st_yled Logo.png")

st.logo("assets/st_yled_logo_corer.svg", size="large")

if "feedback-submitted" in st.session_state:
    if st.session_state["feedback-submitted"]:
        st.toast("Thank you for your feedback!", icon=":material/check_circle:", duration="long")
        del st.session_state["feedback-submitted"]

# region SIDEBAR FOOTER

with st.sidebar.container(key="sidebar-footer-container"):
    
    st_yled.markdown("Getting started with your app", font_size="12px", color='#31333F99', key="sidebar-footer-getting-started-markdown")

    st_yled.markdown("[st_yled Python Package](https://st-styled.evo-byte.com/)", font_size="14px", key="sidebar-footer-styled-pkg-link-markdown")
    
    st_yled.markdown("For help and support", font_size="12px", color='#31333F99', key="sidebar-footer-help-markdown")

    st_yled.markdown("[st_yled Community](https://github.com/EvobyteDigitalBiology/st-styled/discussions)", font_size="14px", key="sidebar-footer-community-link-markdown")
    st.write("")

    with st.container(key="sidebar-footer-letter-container", horizontal=True, vertical_alignment="center",
                    gap = "medium"):

        st.image("assets/logo_small.svg", width=80)

        st_yled.markdown("""**styled studio**\n\nwith :heart: from [EVOBYTE](https://evo-byte.com)\n(c)2025-2026""",
                        font_size="14px",
                        color='#31333F99',
                        key="sidebar-footer-logo-side",
                        width=80)


# region HEADER

sticky_header_bg = st_yled.container(
    key="sticky-header-bg",
    background_color=uiconfig.SECONDARY_BACKGROUND_COLOR_DEFAULT,
)

with sticky_header_bg:
    st.write("")

sticky_header = st_yled.container(
    key="sticky-header",
    horizontal=True,
    vertical_alignment="center",
)

with sticky_header:
    
    with st.container(horizontal=True, horizontal_alignment="left", key="header-left-container", vertical_alignment="center", width=250):
        
        #st.image("assets/st_yled Logo.png", width=40)
        st_yled.title("st_yled studio", font_size='26px', key="header-title", color="#97A6C3")

    with st.container(horizontal=True, horizontal_alignment="right", vertical_alignment="center"):

        st_yled.button("Export to your app", type='primary', icon=':material/file_export:', on_click=export_config_toml, key="export-button")
        
        # Option for popover export
        # with st_yled.popover("Export Theme", icon=':material/file_export:', background_color=uiconfig.PRIMARY_COLOR_DEFAULT, width=172, color="#ffffff"):
        #     render_export_theme()

        st_yled.button("Help", icon=':material/help:', key="help-button", type='secondary', on_click=render_help_dialog, border_style="none", background_color="#97a6c326")

        st_yled.button("Feedback", icon=':material/comment:', key="feedback-button", type='secondary', on_click=render_feedback_dialog, border_style="none", background_color="#97a6c326")


pg.run()
