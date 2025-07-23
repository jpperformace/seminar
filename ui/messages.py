import textwrap

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