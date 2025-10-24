import streamlit as st
import st_yled

def segmented_control_toggle(option1: str, option2: str, key: str, index: int = 0) -> str:

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
    
    seg_control_select = st_yled.radio("Frame Type",
                                options=[option1, option2],
                                key=key,
                                horizontal=True,
                                label_visibility="collapsed",
                                font_size='14px',
                                index = index
                                )
    return seg_control_select
    
    
