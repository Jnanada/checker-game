from typing import Tuple

from streamlit.delta_generator import DeltaGenerator
import streamlit as st
from constants import SQUARE_STYLE, ColorEnum


def squares(parent_container: DeltaGenerator):
    st_square_box = parent_container.container(height=50, border=True)
    st_square_box.markdown(SQUARE_STYLE, unsafe_allow_html=True)
    return st_square_box


def circle(container: DeltaGenerator, color: ColorEnum):
    style = (
        "<style>.circle-"
        f"{color.name.lower()}"
        "{margin:-20px auto;border-radius:50%;width:32px;height:32px;border:1px solid "
        f"rgb{color.value};background-color:rgb{color.value};"
        "}</style>"
    )
    div = f"<div class='circle-{color.name.lower()}'></div>"
    with container:
        st.markdown(div + style, unsafe_allow_html=True)
