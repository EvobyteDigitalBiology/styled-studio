from typing import Dict, Literal

import streamlit as st
import st_yled

import converters
from uidataclasses import StyledComponent


CATEGORY_SLUGS = {
    "Write": "write",
    "Text": "text",
    "Data": "data",
    "Chart": "chart",
    "Input": "input",
    "Media": "media",
    "Layout": "layout",
    "Chat": "chat",
    "Status": "status",
    "Execution": "execution",
    "Navigation": "navigation",
    "Configuration": "configuration",
    "Button": "button",
}


def revert_category_slugs():
    """Return a dictionary that maps slugs back to category names"""
    return {slug: category for category, slug in CATEGORY_SLUGS.items()}

def segmented_control_toggle(
    option1: str, option2: str, key: str, index: int = 0
) -> str:
    css = f"""
    .st-key-{key} label[data-baseweb="radio"]:has(input) {{
    border-radius: 4px;
    background-color: #b9b9b933;
    border-width: 1px;
    border-color: #31333f80;
    border-style: none;
    padding: 8px 16px;
    margin: 0px;
    }}

    .st-key-{key} label[data-baseweb="radio"]:has(input) p {{
        color: #31333f80;
    }}

    .st-key-{key} label[data-baseweb="radio"]:has(input[tabindex="0"]) {{
        background-color: #ff4b4b33;
        border: 1px none #ff4b4b;
        margin: 0px;
    }}

    .st-key-{key} label[data-baseweb="radio"]:has(input[tabindex="0"]) p {{
        color: #ff4b4b;
    }}

    .st-key-{key} label[data-baseweb="radio"] > div:first-child {{
        display: none;
    }}

    .st-key-{key} label[data-baseweb="radio"] > div {{
        padding: 0px;
    }}
    """

    st.html(f"<style>{css}</style>")

    return st_yled.radio(
        "Frame Type",
        options=[option1, option2],
        key=key,
        horizontal=True,
        label_visibility="collapsed",
        font_size="14px",
        index=index,
    )

def update_st_from_input(theme_property: str, input_selector_key: str):
    # Reset if input selector is none
    if st.session_state[input_selector_key] is None:
        del st.session_state[theme_property]
    else:
        st.session_state[theme_property] = st.session_state[input_selector_key]


def update_st_size_value_from_input(
    theme_property: str,
    input_selector_key: str,
    current_unit: str,
    return_value_type: str,
):
    # Reset if input selector is none
    if st.session_state[input_selector_key] is None:
        del st.session_state[theme_property]
    else:
        new_value = st.session_state[input_selector_key]

        if return_value_type == "str":
            st.session_state[theme_property] = f"{new_value}{current_unit}"
        elif return_value_type == "tuple":
            st.session_state[theme_property] = (new_value, current_unit)
        else:  # int
            st.session_state[theme_property] = int(new_value)


def update_st_size_unit_from_input(
    theme_property: str,
    input_selector_key: str,
    current_number: float,
    return_value_type: str,
):
    # Reset if input selector is none
    if st.session_state[input_selector_key] is None:
        del st.session_state[theme_property]
    else:
        new_value = st.session_state[input_selector_key]

        if return_value_type == "str":
            st.session_state[theme_property] = f"{current_number}{new_value}"
        elif return_value_type == "tuple":
            st.session_state[theme_property] = (current_number, new_value)
        else:  # int
            st.session_state[theme_property] = int(current_number)


def base_color_picker(
    key: str,
    seed_value: str,
    label: str,
    label_font_size: str,
    label_field_width: int,
    color_state_value: str,
    code_color: str,
    caption_width: int,
):
    with st.container(horizontal=True, vertical_alignment="center"):
        st_yled.markdown(
            label,
            font_size=label_font_size,
            width=label_field_width,
            key=key + "-label",
        )

        st_yled.code(
            color_state_value,
            language=None,
            font_size="14px",
            color=code_color,
            width=124,
            key=key + "-code-" + seed_value,
        )

        if color_state_value.startswith("#") and len(color_state_value) == 9:
            display_color = converters.hex_with_alpha_to_hex(color_state_value)
        elif color_state_value.startswith("#"):
            display_color = color_state_value
        else:
            display_color = None

        st.color_picker(
            f"Pick {label}",
            value=display_color,
            key=key + "-picker-" + seed_value,
            label_visibility="collapsed",
            on_change=update_st_from_input,
            args=(key, key + "-picker-" + seed_value),
        )

        st.caption("Select Color", width=caption_width)


def base_size_input(
    key,
    seed_value: str,
    label,
    value: float,
    step_size: float,
    unit: str,
    allowed_units: list[str],
    label_font_size: str = "16px",
    label_field_width: int = 140,
    return_value_type: Literal["int", "tuple", "str"] = "str",
):
    with st.container(horizontal=True, vertical_alignment="center", width=400):
        st_yled.markdown(
            label,
            font_size=label_font_size,
            width=label_field_width,
            key=key + "-label",
        )

        # Number input // Operate on float
        number_value = st.number_input(
            f"Set {label} value",
            value=value,
            min_value=0.0,
            step=step_size,
            key=key + "-number-" + seed_value,
            label_visibility="collapsed",
            on_change=update_st_size_value_from_input,
            placeholder="default",
            args=(key, key + "-number-" + seed_value, unit, return_value_type),
        )

        index_select = allowed_units.index(unit)
        unit_disabled = len(allowed_units) == 1

        # Unit selectbox
        st.selectbox(
            f"Set {label} unit",
            options=allowed_units,
            index=index_select,
            key=key + "-unit-" + seed_value,
            label_visibility="collapsed",
            width=90,
            disabled=unit_disabled,
            on_change=update_st_size_unit_from_input,
            args=(key, key + "-unit-" + seed_value, number_value, return_value_type),
        )


def load_components() -> Dict[str, StyledComponent]:
    components = st_yled.constants.COMPONENTS
    return {
        slug: StyledComponent(**component) for slug, component in components.items()
    }
