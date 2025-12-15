import os

from pydantic_ai import Agent
from pydantic import BaseModel
from typing import List, Optional

class AssignResponseInput(BaseModel):
    frage: str
    nutzereingabe: str
    antwortoptionen: List[str]
    naechste_frage: str

class AssignUserResponseInput(BaseModel):
    frage: str
    nutzereingabe: str
    antwortoptionen: List[str]

class NextResponseInput(BaseModel):
    frage: str
    nutzereingabe: str
    naechste_frage: Optional[str] = None

class AssignUserResponseOutput(BaseModel):
    zugeordnete_antwort: Optional[str]

class ResponseTextOutput(BaseModel):
    antworttext: str

class AssignResponseOutput(BaseModel):
    zugeordnete_antwort: Optional[str]
    antworttext: str

response_agent = Agent(
    os.getenv("MODEL_CHOICE", "gpt-4.1-mini"),
    output_type=AssignResponseOutput,
    system_prompt=(
        "Du bekommst eine Frage, eine Nutzereingabe und eine Liste von Antwortoptionen.\n\n"
        "Ordne die Nutzereingabe **genau einer** der Aussagen aus der Liste zu, die **semantisch am besten passt**.\n"
        "Berücksichtige auch **ähnliche Bedeutungen** oder **abweichende Formulierungen**, die das Gleiche meinen. Aber ordne nicht zu wenn der Nutzer unsicher ist. \n\n"
        "Gib im Feld `zugeordnete_antwort` **exakt** den Text der zutreffenden Aussage aus der Liste zurück.\n"
        "Falls eine eindeutige Zuordnung möglich ist, versuche natürlich auf die nächste Frage überzuleiten und frage die Frage, "
        "Falls keine eindeutige Zuordnung möglich ist, gib None zurück. Kein String!!!"
        "Falls du None zurück gibst, gehe das Feld `antworttext` mit einer hilfreichen Nachricht und Hinweisen pro Antwortoptionen, damit der Nutzer eine bessere Aussage treffen kann."
        "Falls du None zurück gibst, leite auf keinen Fall / niemals auf die nächste Frage über sondern versuche bei Unsicherheiten mehr Informationen über die Antwortoptionen zu geben, um die zuordnung zu erleichtern. \n\n"
        "Sprich in `antworttext` den Nutzer direkt an, gehe auf sein Bedürfniss ein und erkläre in einfachen Worten, was noch fehlt, und hilf ihm, "
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

check_response_agent = Agent(
    os.getenv("MODEL_CHOICE", "gpt-4.1-mini"),
    output_type=AssignUserResponseOutput,
    system_prompt=(
        "Du bekommst eine Frage, eine Nutzereingabe und eine Liste von Antwortoptionen.\n\n"
        "Ordne die Nutzereingabe **genau einer** der Aussagen aus der Liste zu, die **semantisch am besten passt**.\n"
        "Berücksichtige auch **ähnliche Bedeutungen** oder **abweichende Formulierungen**, die das Gleiche meinen. "
        "Ordne nicht eine Antwort nicht zu wenn der Nutzer unsicher ist. \n\n"
        "Gib im Feld `zugeordnete_antwort` **exakt** den Text der zutreffenden Aussage aus der Liste zurück.\n"
        "Falls keine eindeutige Zuordnung möglich ist, gib None zurück. Kein String!!! \n"
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
        "- Ausgabe: None\n"
    )
    )

help_response_agent = Agent(
    os.getenv("MODEL_CHOICE", "gpt-4.1-mini"),
    output_type=ResponseTextOutput,
    system_prompt=(
        "Du bekommst eine Frage, eine Nutzereingabe und eine Liste von Antwortoptionen.\n\n"
        "Die Antwort des Nutzers konnte keiner Antwortoption zugeordnet werden. "
        "Gehe auf die Antwort des Nutzers ein. "
        "Versuche zusätzlich ihm mehr Details über die Zuordnung von Antworten zu geben,"
        "um dem Nutzer die Beantwortung der Frage zu erleichtern."
        "Versuche sinnvoll und verständlich den Nutzer zur erneuten Beantwortung der Frage zu bitten."
    )
    )

response_text_agent = Agent(
    os.getenv("MODEL_CHOICE", "gpt-4.1-mini"),
    output_type=ResponseTextOutput,
    system_prompt=(
        "Versuche natürlich und verständlich zu antworten. Gehe immer auf die Fragen den Nutzeres ein. "
        "Gib die Antwort in antworttext zurück"
    )
    )

def assign_user_input(eingabe: AssignResponseInput, nachrichtenverlauf):
    prompt = (
        "Du bekommst eine Frage, eine Nutzereingabe und eine Liste von Antwortoptionen."
        "Gib immer genau eine Antwort zurück, die am besten passt."
        "Ordnet die Nutzereingabe einer semantisch/inhaltlich passenden Antwortoption zu."
        "Wenn wirklich keine Antwort zuzuordnen ist gib Wert None zurück. Kein String!."
    )
    prompt += (
        f"Frage: {eingabe.frage}\n"
        f"Nutzereingabe: {eingabe.nutzereingabe}\n"
        f"Antwortoptionen: {eingabe.antwortoptionen}\n"
    )

    return response_agent.run_stream(user_prompt=prompt, message_history=nachrichtenverlauf)

async def assign_user_input_to_response_option(eingabe: AssignUserResponseInput):
    prompt = (
        "Du bekommst eine Frage, eine Nutzereingabe und eine Liste von Antwortoptionen."
        "Gib immer genau eine Antwort zurück, die am besten passt."
        "Ordnet die Nutzereingabe einer semantisch/inhaltlich passenden Antwortoption zu."
        "Wenn wirklich keine Antwort zuzuordnen ist gib Wert None zurück. Kein String!."
    )
    prompt += (
        f"Frage: {eingabe.frage}\n"
        f"Nutzereingabe: {eingabe.nutzereingabe}\n"
        f"Antwortoptionen: {eingabe.antwortoptionen}\n"
    )

    response = await check_response_agent.run(user_prompt=prompt)
    return response

def help_user_to_response(eingabe: AssignUserResponseInput, nachrichtenverlauf):
    prompt = (
        "Du bekommst eine Frage, eine Nutzereingabe und eine Liste von Antwortoptionen."
        "Gib eine Nachricht zurück die auf die Nutzereingabe eingeht. "
        "Versuche weitere Details zu geben, die dem Nutzer bei der Beantwortung helfen könnten."
    )
    prompt += (
        f"Frage: {eingabe.frage}\n"
        f"Nutzereingabe: {eingabe.nutzereingabe}\n"
        f"Antwortoptionen: {eingabe.antwortoptionen}\n"
    )

    return response_text_agent.run_stream(user_prompt=prompt, message_history=nachrichtenverlauf)


def ask_next_question(eingabe: NextResponseInput, nachrichtenverlauf):
    prompt = (
        "Du bekommst eine Frage, eine Nutzereingabe und eine Frage, die du als nächstes stellen sollst."
        "Gib eine Nachricht zurück die auf die Nutzereingabe eingeht. "
        "Versuche flüssig und natürlich auf die nachste Frage überzuleiten und stelle die nächste Frage. "
        "Formuliere die Frage inhaltlich nicht um."
    )
    prompt += (
        f"Frage: {eingabe.frage}\n"
        f"Nutzereingabe: {eingabe.nutzereingabe}\n"
        f"Nächste Frage lautet: {eingabe.naechste_frage}\n"
    )

    return response_text_agent.run_stream(user_prompt=prompt, message_history=nachrichtenverlauf)