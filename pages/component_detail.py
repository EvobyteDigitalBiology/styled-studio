import streamlit as st
import st_yled

import utils
from uidataclasses import StyledComponent

st_yled.init()

qparams = st.query_params
components = utils.load_components()

if not 'show_code_example' in st.session_state:
    st.session_state['show_code_example'] = False

def show_copy_code():
    st.session_state['show_code_example'] = True


def main(slug, select_component: StyledComponent):

    st.markdown("**> Components** " + slug)

    st.space(8)

    st_yled.title(select_component.name, key="component-detail-title", font_size="40px")

    st_yled.markdown(':material/developer_guide: [Docs Link](' + select_component.docs_url + ')',
                     font_size="14px",
                     color="#31333f")

    st.space(8)

    with st_yled.container(
        padding="32px",
        width=360,
        border_color="#F6F6F6",
        border_width="8px",
        border_style="solid",
    ):
        
        st.image(select_component.main_image_url)

    st.space(8)

    with st_yled.container(padding="0px", width=480):

        st_yled.markdown("Description", font_weight="700", key="component-detail-header-description")
        st_yled.markdown(select_component.description)

        st.space(8)

        st_yled.markdown("Usage Pattern", font_weight="700", key="component-detail-header-usage-pattern")
        st_yled.markdown(select_component.usage_pattern)

        st.space(8)

        with st_yled.expander(label="Code Examples", background_color="#F6F6F6", border_width="0px"):

            for code_example in select_component.code_examples:
                st.code(code_example["code"], language="python")
    
    st.space(8)

    with st.container(horizontal=True, vertical_alignment="center"):

        st.button("Copy Code", type="primary", on_click=show_copy_code)
            # python_cmd = select_component.code_copy_template
            # st_yled.code(python_cmd, background_color="#F6F6F6", language="python")

        st.page_link(
            page = 'pages/components.py',
            label = "Back",
            icon = ":material/arrow_back_ios:",
        )

    if st.session_state['show_code_example']:
        st.code(select_component.code_copy_template, language="python") 


# region UI


    #main()


#region DATA

with st.container(key="component-detail-main-container"):

    if "component" in qparams:

        select_slug = qparams["component"]
        if select_slug in components:
            select_component = components[select_slug]
            main(select_slug, select_component)
        else:
            st_yled.warning(f"Component with slug '{select_slug}' not found.")

    else:
        st_yled.warning("No component specified in query parameters.")
