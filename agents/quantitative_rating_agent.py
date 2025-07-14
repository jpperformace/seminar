from enum import Enum

from pydantic import BaseModel
from pydantic_ai.agent import Agent
from typing import Literal

import os

class Phasen(Enum):
    ORGANIZING = 'Organisieren'
    UNDERSTANDING = 'Verstehen'
    DESIGNING = 'Gestalten'
    EVALUATION = 'Bewerten'

class Antwortoption(BaseModel):
    text: str
    punkte: int
    bewertung: Literal["Ungenügend – nicht zertifizierungsfähig", "Ausreichend – mit Schwächen", "Gut", "Sehr gut"]
    begruendung: str
    verbesserungpotential: str

class BewertungEingabe(BaseModel):
    antwort1: Antwortoption
    antwort2: Antwortoption
    antwort3: Antwortoption
    antwort4: Antwortoption

quan_rat_agent = Agent(
    os.getenv("MODEL_CHOICE", "gpt-4.1-mini"),
    system_prompt=(
        "Du bist ein hilfreicher Assistent zur Reifegradbewertung in Audits zur nutzerzentrierten Entwicklung. "
        "Du soll eine subjektive Einschätzung geben, ob eine Zertifizierung möglich ist."
        "Deine Aufgabe ist es, basierend auf vier Antworten, eine Tendenz für den Reifegrad in der jeweilgen Phase "
        "zu geben. Dafur werden dir bereits Bewertung, Begründung und Verbesserungspotentiale übergeben." 
        "Begründe mit den übergebenen Informationen kausal, damit deutlich wird wie die Gesamtbewertung zurstande kommt."
        "Schreibe die Bewertung kompakt und stelle transparent dar, dass es sich um eine subjektive Einschätzung handelt "
        "basierend auf den Eingabedaten handelt. Mache deutlich, dass eine eindeutige Bewertung durch einen Auditor"
        "getroffen werden kann und man diesen bei Unstimmigkeiten immer zu raten ziehen sollte."
    )
)

async def evaluate_phase(eingabe: BewertungEingabe, phase: str):
    prompt = (
        f"Bewerte die Phase '{phase}' im Audit zur nutzerzentrierten Entwicklung anhand folgender "
        "vordefinierter Bewertungsschema für die gegebenen Antworten:\n\n"
    )
    for i, antwort in enumerate(
        [eingabe.antwort1, eingabe.antwort2, eingabe.antwort3, eingabe.antwort4], 1
    ):
        prompt += (
            f"Antwort {i}:\n"
            f"Text: {antwort.text}\n"
            f"Punkte: {antwort.punkte}\n"
            f"Bewertung: {antwort.bewertung}\n"
            f"Begründung: {antwort.begruendung}\n"
            f"Verbesserungspotential: {antwort.verbesserungpotential}\n\n"
        )
    prompt += (
        f"Gib eine Gesamtbewertung mit kausaler Begründung für die Phase {phase} zurück. Diese soll in kurzer Form erklärend, causal und selektiv sein. "
        f"Die Gesamtbewertung wird auf Grundlage der Einzelbewertungen getroffen. Es soll eindeutig sein, an welchen Stelle noch Schwächen sind."
        "Formatiere die Antwort in Markdown. Fasse diese Informationen bitte kompakt und zusammengefasst zu einer "
        f"vorläufigen Bewertung der Phase {phase} zusammen. Verwende als Überschrift:\n\n"
        f"#### Vorläufige Bewertung der Phase {phase}\n\n" 
        "Beginne mit 'Ihr Unternehmen weißt insgesamt..."
        "Die einzelnen Antworten sollen nicht explizit genannt werden. "
    )

    response = await quan_rat_agent.run(user_prompt=prompt)

    return response