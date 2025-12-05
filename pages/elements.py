
import uuid
import re

import streamlit as st
from streamlit_split_button import split_button

import st_yled

import uiconfig
import utils

st_yled.init()

def add_element_to_selection(element_name: str):
    
    if element_name in st.session_state['element-select-names']:
        return

    if 'element-select' not in st.session_state:
        st.session_state['element-select'] = dict()

    element_hash = str(uuid.uuid4())

    # Get styling options for this element
    variants = st_yled.styler.get_element_variants(element_name)
    
    element_entry = {
        'name': element_name,
        'types': dict()
    }

    if len(variants) == 0:
        variants = ['default']
    
    # Combine variants into the element entry
    for variant in variants:
        
        if variant == 'default':
            element_config = st_yled.styler.get_element_style(element_name)
        else:
            element_config = st_yled.styler.get_element_style(element_name + '_' + variant)

        element_config = element_config.copy()
        # Strip element config to css[element]
        element_css = dict()
        for css_prop in list(element_config['css'].keys()):
            element_css[css_prop] = None
        element_config['css'] = element_css

        element_entry['types'][variant] = element_config
    
    st.session_state['element-select'][element_hash] = element_entry
    st.session_state['element-select-names'].append(element_name)


def remove_element_from_selection(element_hash: str,
                                element_key_base: str,
                                element_name: str):

    element_name_prefix = 'element-' + element_name

    # Remove from selection and available elements for selection
    del st.session_state['element-select'][element_hash]
    st.session_state['element-select-names'].remove(element_name)

    # Remove all associated session state keys
    keys_to_remove = [key for key in st.session_state.keys() if key.startswith(element_name_prefix) and key.endswith("-value")]
    input_seed_keys_to_remove = [key for key in st.session_state.keys() if key.startswith(element_name_prefix) and key.endswith("-value-seed")]

    for key in keys_to_remove:
        del st.session_state[key]

    for key in input_seed_keys_to_remove:
        del st.session_state[key]


def reset_element_styles(element_key_base: str):

    # Remove all associated session state keys
    value_keys_to_remove = [key for key in st.session_state.keys() if key.startswith(element_key_base) and key.endswith("-value")]
    input_seed_keys_to_remove = [key for key in st.session_state.keys() if key.startswith(element_key_base) and key.endswith("-value-seed")]

    for key in value_keys_to_remove:
        del st.session_state[key]
    
    for key in input_seed_keys_to_remove:
        del st.session_state[key]


# def copy_element_styles_to_clipboard(element_name: str, element_key_base: str):
    
#     # Get values for all associated session state keys
#     keys_to_copy = [key for key in st.session_state.keys() if key.startswith(element_key_base) and key.endswith("-value")]

#     # Extract properrties from keys
#     all_args = []
#     for key in keys_to_copy:
#         key_parse = key.replace("-value", "").replace("element-", "")
#         css_prop_format = key_parse.split("-")[-1]
#         value = st.session_state[key]
#         arg_str = f"{css_prop_format}=\"{value}\""
#         all_args.append(arg_str)
#     all_args_str = ", ".join(all_args)

#     if all_args_str:
#         python_cmd = f"st_yled.{element_name}(*, {all_args_str})"
#     else:
#         python_cmd = f"st_yled.{element_name}(*)"

#     pyperclip.copy(python_cmd)
#     st.toast("Element Python copied to clipboard", icon=":material/content_copy:")


def get_element_styles_to_python(element_name: str, element_key_base: str, type_select: str = None) -> str:
    
    # Get values for all associated session state keys
    keys_to_copy = [key for key in st.session_state.keys() if key.startswith(element_key_base) and key.endswith("-value")]

    # Extract properties from keys
    all_args = []
    for key in keys_to_copy:
        key_parse = key.replace("-value", "").replace("element-", "")
        css_prop_format = key_parse.split("-")[-1]
        value = st.session_state[key]
        arg_str = f"{css_prop_format}=\"{value}\""
        all_args.append(arg_str)
    all_args_str = ", ".join(all_args)

    if type_select:
        type_args_str = f", type=\"{type_select}\""
    else:
        type_args_str = ""

    if all_args_str:
        python_cmd = f"st_yled.{element_name}(*{type_args_str}, {all_args_str})"
    else:
        python_cmd = f"st_yled.{element_name}(*{type_args_str})"

    return python_cmd



def elements_color_picker(elements_key: str,
                        label: str,
                        label_font_size: str = '20px',
                        label_field_width: int = 130):

    if elements_key in st.session_state:
        color_state_value = st.session_state[elements_key]
        code_color = None
    else:
        color_state_value = "default"
        code_color = "grey"

    input_seed_key = key + "-seed"

    if not input_seed_key in st.session_state:
        st.session_state[input_seed_key] = str(uuid.uuid4())

    utils.base_color_picker(
        key=elements_key,
        seed_value=st.session_state[input_seed_key],
        label=label,
        label_font_size=label_font_size,
        label_field_width=label_field_width,
        color_state_value=color_state_value,
        code_color=code_color,
        caption_width=80
    )

def elements_selectbox(key: str,
                        label: str,
                        options: list[str],
                        label_font_size: str = '16px',
                        label_field_width: int = 130,
                        format_func = lambda x: x):

    input_seed_key = key + "-seed"

    if not input_seed_key in st.session_state:
        st.session_state[input_seed_key] = str(uuid.uuid4())

    seed_value = st.session_state[input_seed_key]

    with st.container(horizontal=True, vertical_alignment="center"):

        st_yled.markdown(label, font_size=label_font_size, width=label_field_width)

        selected_option = st_yled.selectbox(
            "Select an option",
            options=options,
            format_func=format_func,
            index=None,
            key=key + "-selectbox-" + seed_value,
            label_visibility="collapsed",
            on_change=utils.update_st_from_input,
            placeholder = "default",
            args=(key, key + "-selectbox-" + seed_value),
            width = 160
        )

        st_yled.caption("Select Option", width=80)


def elements_size_input(key,
                        label: str,
                        allowed_units: list[str],
                        unit_step_sizes: list[float],
                        label_font_size: str = '16px',
                        label_field_width: int = 130):

    if key in st.session_state:
        size_state_value = st.session_state[key]

        if size_state_value.startswith("None"):
            size_state_value = size_state_value.replace("None", "")
        
        # None found
        current_number = re.findall(r'\d+\.?\d*', size_state_value)
        if current_number:
            current_number = float(current_number[0])
        else:
            current_number = None
        
        # Filter out potentila None values
        current_unit = re.findall(r'[a-zA-Z]+', size_state_value)[0]
    else:
        current_number = None
        current_unit = allowed_units[0]

    input_seed_key = key + "-seed"

    if not input_seed_key in st.session_state:
        st.session_state[input_seed_key] = str(uuid.uuid4())

    step_size = unit_step_sizes[allowed_units.index(current_unit)]

    # TODO Fix None
    utils.base_size_input(
        key=key,
        seed_value=st.session_state[input_seed_key],
        label=label,
        value=current_number,
        step_size=step_size,
        unit=current_unit,
        allowed_units=allowed_units,
        label_font_size=label_font_size,
        label_field_width=label_field_width,
        return_value_type='str'
    )


def weight_display_func(option):

    options = ["100", "200", "300", "400", "500", "600", "700", "800", "900"]
    display_options = ["thin", "extra-light", "light", "normal", "medium", "semi-bold", "bold", "extra-bold", "black"]

    if option is None:
        return None
    else:
        return display_options[options.index(option)]


def get_input_widget_for_property(prop: str, key: str, display_name: str):

    widget_type = uiconfig.css_properties_input_widget[prop]
    
    if widget_type == 'color_picker':
        elements_color_picker(key, display_name, label_font_size='16px')
    
    elif widget_type == 'size_input':
        allowed_units = ['px', 'em', 'rem']
        unit_step_sizes = [1.0, 0.1, 0.1]
        elements_size_input(
            key,
            display_name,
            allowed_units,
            unit_step_sizes,
            label_font_size='16px'
        )
    
    elif widget_type == 'selectbox':
        if prop == 'border_style':
            options = ['none', 'solid', 'dashed', 'dotted', 'double', 'groove', 'ridge', 'inset', 'outset', 'hidden']
            elements_selectbox(key, display_name, options, label_font_size='16px')
        elif prop == 'font_weight':
            options = ["100", "200", "300", "400", "500", "600", "700", "800", "900"]

            elements_selectbox(key, display_name, options, format_func=lambda x: weight_display_func(x), label_font_size='16px')
    else:
        pass


# region data

if 'element-select' not in st.session_state:
    st.session_state['element-select'] = dict()
if 'element-select-names' not in st.session_state:
    st.session_state['element-select-names'] = list()
if 'element-first-open' not in st.session_state:
    st.session_state['element-first-open'] = True

# TODO Add default

# Load all components
# Load categories and related components

element_categories = st_yled.styler.get_stylable_elements_by_category()
category_options = list(element_categories.keys())

category_display_slug_map = utils.CATEGORY_SLUGS
category_slug_display_map = utils.revert_category_slugs()

# Get all display names for categories
category_display_options = [category_slug_display_map[cat] for cat in category_options]

# Add button as a default example for styling

if st.session_state['element-first-open']:
    add_element_to_selection("button")
    st.session_state['element-first-open'] = False

# region UI

with st.container(key="elements-main-container"):

    st.markdown("**> Elements** Style and customize individual Streamlit UI elements")

    with st_yled.popover('Style element',
                        icon=":material/style:",
                        background_color="#ff4b4b",
                        color="#ffffff",
                        key="elements-add-element-popover"):

        cont = st.container(width=600)

        col1, col2 = cont.columns([4,3])

        with col1:

            col1_cat, col2_cat = col1.columns([1,2])

            with col1_cat:
                # Returns display names for categories
                category_select_display = st_yled.radio(
                    "Category",
                    options=category_display_options,
                    key="elements-category-select",
                )

            category_select = category_display_slug_map[category_select_display]
            cat_elements = element_categories[category_select]

            # Remove cat_elements already in selection
            selected_elements = st.session_state['element-select-names']
            cat_elements = [el for el in cat_elements if el not in selected_elements]

            with col2_cat:
                element_select = st_yled.radio(
                    "Element",
                    options=cat_elements,
                    index=0,
                    key="elements-state-select",
                )

        with col2:

            if element_select:

                # Top Button Controls for Adding Element Styles
                with st.container(key = "elements-add-element-selection-container"):

                    st_yled.button(
                        "Add to editor pane",
                        key="elements-add-element-selection",
                        icon=":material/add_box:",
                        type="primary",
                        on_click=add_element_to_selection,
                        args=(element_select,)
                    )

                    with st_yled.container(key = "elements-add-element-preview-container", background_color="#F6F6F6"):

                        st_yled.subheader(element_select, font_size=24)

                        element_config = st_yled.styler.get_element_style(element_select)

                        if 'example' in element_config:
                            kwargs = {'key': f'preview-example-{element_select}'}
                            eval(element_config['example'])
                        else:
                            st_yled.info("No preview available", icon=":material/info:")


    elements_display = st.session_state['element-select']
    display_keys = list(elements_display.keys())[::-1]  # Reverse order for display


# region Render Cards

    for ix, element_hash in enumerate(display_keys):

        element_card_props = elements_display[element_hash]
        element_types = list(element_card_props['types'].keys())
        element_name = element_card_props['name']

        # Define a random key for the element card split button
        if 'element-card-split-' + element_hash not in st.session_state:
            st.session_state['element-card-split-' + element_hash] = str(uuid.uuid4())
        
        # Check if multiple types
        if len(element_types) == 1:
            type_selector = False
            type_select = element_types[0]
        else:
            type_selector = True
            if 'secondary' in element_types:
                type_select = 'secondary'
            else:
                type_select = element_types[0]

        # Get available css properties for this element type
        css_props = list(element_card_props['types'][type_select]['css'].keys())
        css_tabs = {uiconfig.css_properties_tabs[prop] for prop in css_props}

        tabs_render = []
        if 'Color' in css_tabs:
            tabs_render.append('Color')
        if 'Font' in css_tabs:
            tabs_render.append('Font')
        if 'Border' in css_tabs:
            tabs_render.append('Border')

        with st_yled.container(background_color='#F6F6F6',
                                key=f"element-card-container-{element_hash}"):
            
            # Apply card css
            css = f"""
                .st-key-element-card-container-{element_hash} {{
                    padding: 16px 16px;
                }}

                .st-key-element-{element_hash}-type-select .stSelectbox div {{
                    height: 32px;
                    line-height: 32px;
                    display: flex;
                    align-items: center;
                }}

                .st-key-element-card-container-{element_hash} .stTabs {{
                    margin-top: 12px;
                }}

                .st-key-element-card-container-{element_hash} .stTabs div[data-baseweb="tab-panel"]{{
                    margin-top: 12px;
                }}

                .st-key-element-card-container-{element_hash} .stTabs p {{
                    font-weight: 500;
                }}

                .st-key-element-card-container-{element_hash} .stTabs .stVerticalBlock {{
                    gap: 32px;
                }}

                .st-key-element-{element_hash}-example-container {{
                    padding: 32px 16px;
                    margin-top: 24px;
                    margin-bottom: 24px;
                }}
                """
            st.html(f"<style>{css}</style>")

            col1, col2 = st.columns([1,2], gap="medium")

            with col1:
                
                st_yled.subheader(element_name, font_size=24)

                # Check if multiple types
                if type_selector:
                    type_select = st_yled.selectbox(
                        "Select Type",
                        options=element_types,
                        index=element_types.index(type_select),
                        key=f"element-{element_hash}-type-select",
                        format_func=lambda x: uiconfig.element_type_format.get(x),
                        label_visibility="collapsed",
                        font_size='14px',
                        width=180
                    )
                else:
                    st.write("")

                element_key_base = 'element-' + element_name
                if type_selector:
                    element_key_base = element_key_base + "-" + type_select
                
                # Create example container
                with st_yled.container(horizontal_alignment="center",
                                        key=f"element-{element_hash}-example-container",
                                        background_color="#FFFFFF"):
                    
                    kwargs = {}
                    # Extract all css properties for this element type
                    for key in st.session_state.keys():
                        if key.startswith(element_key_base) and key.endswith("-value"):
                            css_prop = key.replace(element_key_base + '-', "").replace('-value', "")
                            css_value = st.session_state[key]
                            kwargs[css_prop] = css_value
                    
                    # Create example to displa changes
                    if 'example' in element_card_props['types'][type_select]:
                        eval(element_card_props['types'][type_select]['example'])

                res = split_button(
                    label = "Copy Python",
                    key=st.session_state['element-card-split-' + element_hash],
                    options=["Remove", "Reset"]
                )
            
                if res == "Remove":

                    # Make sure to delete variants if any
                    remove_element_from_selection(element_hash,element_key_base,element_name)
                    
                    # Required to render new key for split button on action and reset state
                    st.session_state['element-card-split-' + element_hash] = str(uuid.uuid4())
                    st.rerun()
                
                elif res == "Reset":
                    reset_element_styles(element_key_base)
                    # Required to render new key for split button on action and reset state
                    st.session_state['element-card-split-' + element_hash] = str(uuid.uuid4())

                    # Delete all input seed keys associated with this element
                    #input_seed_keys_to_remove = [key for key in st.session_state.keys() if key

                    st.rerun()

            with col2:

                tabs = st.tabs(tabs_render)
                
                for ix, tab in enumerate(tabs):

                    with tab:

                        for prop in css_props:
                            if uiconfig.css_properties_tabs[prop] == tabs_render[ix]:
                                display_name = uiconfig.css_properties_display_name.get(prop, prop)

                                element_key = element_key_base + f"-{prop}-value"
                                get_input_widget_for_property(prop, element_key, display_name)

                                # Get the right display function and def


            # Final bottom
            if res == "Copy Python":
                
                if type_selector:
                    type_select_arg = type_select
                else:
                    type_select_arg = None

                python_cmd = get_element_styles_to_python(element_name, element_key_base, type_select_arg)

                st_yled.code(python_cmd, background_color="#FFFFFF", language="python")

                # Required to render new key for split button on action and reset state
                st.session_state['element-card-split-' + element_hash] = str(uuid.uuid4())