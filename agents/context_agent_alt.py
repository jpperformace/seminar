import os

from pydantic_ai import Agent
from pydantic import BaseModel
from typing import List, Optional

class AssignResponseInput(BaseModel):
    frage: str
    nutzereingabe: str
    antwortoptionen: List[str]

class AssignResponseOutput(BaseModel):
    assigned_response: Optional[str]
    error_message: Optional[str] = None

response_agent = Agent(
    os.getenv("MODEL_CHOICE", "gpt-4.1-mini"),
    output_type=AssignResponseOutput,
    system_prompt=(
        "Du bekommst eine Frage, eine Nutzereingabe und eine Liste von Antwortoptionen.\n\n"
        "Ordne die Nutzereingabe **genau einer** der Aussagen aus der Liste zu, die **semantisch am besten passt**.\n"
        "Berücksichtige auch **ähnliche Bedeutungen** oder **abweichende Formulierungen**, die das Gleiche meinen.\n\n"
        "Gib im Feld `assigned_response` **exakt** den Text der zutreffenden Aussage aus der Liste zurück.\n"
        "Falls keine eindeutige Zuordnung möglich ist, gib `null` zurück und fülle das Feld `error_message` mit "
        "einer hilfreichen Nachricht und Hinweisen pro Antwortobtionen, damit der Nutzer eine bessere Aussage treffen kann.\n\n"
        "Sprich in `error_message` den Nutzer direkt an, gehe auf sein Bedürfniss ein und erkläre in einfachen Worten, was noch fehlt, und hilf ihm, "
        "seine Antwort zu konkretisieren. Verwende dabei einen natürlichen, flüssigen Tonfall.\n\n"
        "### Beispiele für die Zuordnung:\n"
        "**Frage:** Können am Entwicklungsprozess des digitalen Produkts / der Dienstleistung beteiligte Mitarbeitende Usability-Qualifikationen nachweisen?\n"
        "- Antwortoptionen: [\"Ja, alle\", \"Einige\", \"Nein\"]\n"
        "- Nutzereingabe: \"Ja, fast alle.\"\n"
        "- Ausgabe: \"Ja, alle\"\n\n"
        "- Nutzereingabe: \"Ein paar.\"\n"
        "- Ausgabe: \"Einige\"\n\n"
        "- Nutzereingabe: \"Keine Mitarbeiter können dies.\"\n"
        "- Ausgabe: \"Nein\"\n\n"
        "- Nutzereingabe: \"Ich weiß es nicht.\"\n"
        "- Ausgabe: null\n"
        "Beispiele für Rückfragen\"\n"
        "- \"Damit ich Ihre Antwort zuordnen kann: Haben Sie aktuell Methoden im Einsatz – und wenn ja, welche? Zum Beispiel Interviews, Umfragen oder Nutzertests.\"\n"
        "- \"Ihre Antwort war etwas allgemein. Könnten Sie bitte genauer sagen, ob die Einbindung von Nutzenden bereits dokumentiert ist, in Planung ist oder nur informell erfolgt?\"\n\n"
        "Formuliere Rückfragen immer direkt, freundlich und leicht verständlich – so, als würdest du dich in einem Gespräch mit dem Nutzer befinden.\n"
    )
    )

async def assign_user_input(eingabe: AssignResponseInput):
    prompt = (
        "Du bekommst eine Frage, eine Nutzereingabe und eine Liste von Antwortoptionen."
        "Gib immer eine Antwort zurück, die am besten passt."
        "Ordnet die Nutzereingabe einer semantisch/inhaltlich passenden Antwortoption zu."
        "Wenn wirklich keine Antwort zuzuordnen ist gib Wert None zurück. Kein String!."
    )
    prompt += (
        f"Frage: {eingabe.frage}\n"
        f"Nutzereingabe: {eingabe.nutzereingabe}\n"
        f"Antwortoptionen: {eingabe.antwortoptionen}\n"
    )

    return await response_agent.run(user_prompt=prompt)