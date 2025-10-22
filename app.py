import streamlit as st
import st_yled


@st.dialog(title="Export Configuration")
def export_config_toml():

    url = st.context.url
    url = url.replace('http://', '').split('/')

    if len(url) == 1:
        export_page = "theme"
    elif url[1] == "elements":
        export_page = "elements"
    else:
        st.error("Invalid Export Page Selected")

    # TODO: Design Export Function

    
    

st_yled.init()

theme_page = st.Page("pages/theme.py", title="Theme")
element_page = st.Page("pages/elements.py", title="Element Styling")
 
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
        st_yled.title("st_yled Studio", font_size='32px')

    
    with st.container(horizontal=True, horizontal_alignment="right"):

        st_yled.button("Export to your App", type='primary', icon=':material/file_export:', on_click=export_config_toml)
        st_yled.button("Help", icon=':material/help:')


pg.run()