import textwrap

from ui.css import get_review_container_css

def get_sidebar_html():
    return textwrap.dedent("""
   <style>
   [data-testid="stSidebar"][aria-expanded="true"]{
       min-width: 15%;
       max-width: 15%;
   }
   """)

def get_header_html():
    return textwrap.dedent("""
    <div style="
        position: relative;
        width: 77.5%;
    ">
        <div id="sticky-header" style="
            position: sticky;
            top: 1cm;
            background-color: white;
            padding: 0.1rem;
            margin-bottom: 0.1rem;
            border-bottom: 1px solid #ccc;
            z-index: 1000;
        ">
            <h2 style="margin: 0;">KI-Assistent für Siegel „Nutzerzentriert Entwickelt“</h2>
            <div style="
                margin-top: 0.5rem;
                background-color: #f9f9f9;
                border-left: 6px;
                padding: 0.1rem;
                font-size: 0.95rem;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            ">
                <strong>Hinweis:</strong> Bitte beantworten Sie die Fragen des KI-gestützten Assistenten so ausführlich wie möglich. 
                Sollten Unsicherheiten bestehen, geben Sie diese bitte an – der Assistent kann dadurch gezielter Rückfragen stellen 
                oder weiterführende Informationen bereitstellen.
            </div>
        </div>
    </div>
    """)

def get_padding_html():
    return textwrap.dedent("""
<div style="height: 35px; background-color: white;"></div>
""")

def get_review_heading():
    return """
<div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
<span style="font-size: 1.3rem; position: relative; top: -5px;">💡</span>
<h4 style="margin: 0;">Einschätzung und Potenzialanalyse</h4>
</div>
"""

def get_new_review_text(phase:str, bewertung:str, begruendung:str, verbessung:str, methoden:str, ki_tools:str):
    new_text = f"""
<div style="font-size: 0.85rem;">
    <strong>Phase: {phase}</strong><br>
    <strong>Bewertung:</strong> {bewertung}<br>
    <strong>Begründung:</strong> <br>{begruendung}<br>
    <strong>Verbesserungsvorschlag:</strong> <br>{verbessung}<br>
    <ul style="margin-top: 0.5rem; padding-left: 1.2rem;">
        <li><strong>Methoden:</strong> {methoden}</li>
        <li><strong>KI-Tools:</strong> {ki_tools}</li>
    </ul>
    <hr>
</div>
    """
    return new_text

def get_final_review_html(new_text:str):
    return textwrap.dedent(f"""
    <html>
    <head>
      <style>
        body {{
          font-family: 'Arial', sans-serif;
          font-size: 0.85rem;
          color: #333;
          padding: 2rem;
        }}
      </style>
    </head>
    <body>
      {new_text}
    </body>
    </html>
    """)

def get_default_hint_text():
    return textwrap.dedent("""
    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
    <span style="font-size: 1.3rem; position: relative; top: -5px;">💡</span>
    <h4 style="margin: 0;">Hinweis:</h4>
    </div>
    <p>
    An dieser Stelle wird zukünftig ein zusammenfassendes Dokument zur Einschätzung und Potenzialanalyse für das Siegel <strong>„Nutzerzentriert Entwickelt“</strong> angezeigt.
    Es fasst zentrale Erkenntnisse der Analysephase, die durch die interaktive Konversation mit dem KI-Assistenten gewonnen wurden, zusammen und bietet einen Überblick über empfohlene nächste Schritte im weiteren Entwicklungsprozess.
    </p>
        """)

def get_tertiary_button_html():
    return textwrap.dedent("""
    <style>
    button[kind="tertiary"] {
        height: auto;
        padding-top: 10px !important;
        padding-bottom: 10px !important;
    }
    </style>
    """)

def get_menu_heading_html(phase:str):
    return textwrap.dedent(f"""
                   <div style='font-size: 0.85rem'>
                       <h4 style="margin: 0;">Phase: {phase}</h4>
                   </div>
               """)

def get_review_html(doc_text:str):
    return textwrap.dedent(f"""
<div style="{get_review_container_css()}">
<div style="font-size: 0.85rem; line-height: 1.5; color: #333;">
{doc_text}
</div>
</div>
""")