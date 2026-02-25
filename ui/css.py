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

def get_download_button_css():
    return float_css_helper(
        width="38%",
        top="90%",
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

def get_title_css():
    return """
<style>
.report-container {
    font-family: 'Arial', sans-serif;
    font-size: 0.85rem;
    color: #333;
}

.report-container h1 {
    font-size: 2.2rem;
    font-weight: 700;
    line-height: 1.2;
    color: #111;
}

.highlight-marker {
    position: relative;
    display: inline-block;
    z-index: 0;
}

.highlight-marker::after {
    content: "";
    position: absolute;
    left: -6px;
    right: -6px;
    bottom: 6px;
    height: 16px;
    background: linear-gradient(100deg, rgba(244,197,66,0.9) 0%, rgba(255,221,87,0.85) 100%);
    z-index: -1;
    transform: rotate(-1.2deg);
    border-radius: 6px;
}
</style>
"""