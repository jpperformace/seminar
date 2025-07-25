import textwrap

from streamlit_float import float_css_helper


def get_header_css():
    return float_css_helper(
        width="100%",
        top="1cm",
        transition=0,
        margin="0rem",
        additional_css="background-color: white !important; z-index: 1000;"
    )

def get_menu_css():
    return float_css_helper(
        width="38%",
        top="12rem",
        right="2rem",
        transition=0,
        height="25%",
        additional_css="""
            background-color: #f9f9f9;
            border-radius: 0.5rem;
            padding-left: 1rem;
            padding-right: 1rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            z-index: 999;
        """
    )

def get_review_container_css():
    return textwrap.dedent("""
        position: fixed;
        width: 38%;
        top: 53%;
        right: 2rem;
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        z-index: 999;
        height: 40%;
        overflow-y: auto;
    """).replace("\n", " ")