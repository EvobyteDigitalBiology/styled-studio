import streamlit as st
import st_yled

import utils

st_yled.init()


components = utils.load_components()

# region UI

with st.container(key="components-main-container"):
    st.markdown("**> Components** More components and functions for your apps")

    st.space(8)

    ix = 0
    component_cols = st.columns([1, 1, 1], gap="medium")

    for component_slug, component in components.items():
        col_ix = ix % 3

        with component_cols[col_ix]:
            with st_yled.container(
                background_color="#F6F6F6",
                padding="16px",
                key=f"component-card-{component_slug}",
            ):
                with st_yled.container(
                    height=120,
                    horizontal=True,
                    background_color="#FFFFFF",
                    border_width="1px",
                    horizontal_alignment="center",
                    vertical_alignment="center",
                ):
                    st.image(component.preview_image_url, width=140)

                with st_yled.container(
                    height=110, padding="0px", padding_left="8px", border_width="0px"
                ):
                    st_yled.subheader(component.name, font_size="20px")
                    st_yled.markdown(
                        component.preview_description,
                        font_size="12px",
                        font_weight="500",
                    )

                st_yled.page_link(
                    page="pages/component_detail.py",
                    label="More",
                    icon=":material/arrow_forward_ios:",
                    query_params={"component": component_slug},
                )

            st.space(40)

        ix += 1
