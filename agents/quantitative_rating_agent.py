from enum import Enum

from pydantic import BaseModel
from pydantic_ai.agent import Agent
from typing import Literal, Optional

import os

class Phasen(Enum):
    ORGANIZING = 'Organisieren'
    UNDERSTANDING = 'Verstehen'
    DESIGNING = 'Gestalten'
    EVALUATION = 'Bewerten'

class Antwortoption(BaseModel):
    text: str
    hinweis: Optional[str] = None
    punkte: int
    bewertung: Literal["Ungenügend – nicht zertifizierungsfähig", "Ausreichend – mit Schwächen", "Gut", "Sehr gut"]
    begruendung: str
    verbesserungpotential: str

class BewertungEingabe(BaseModel):
    antwortoptionen: list[Antwortoption]

class BewertungAusgabe(BaseModel):
    gesamtbewertungstext: str
    gesamtbewertung: str
    gesamtbegruendung: str
    gesamtverbesserungspotential: str
    methoden:str
    ki_tools: str

quan_rat_agent = Agent(
    os.getenv("MODEL_CHOICE", "gpt-4.1-mini"),
    output_type=BewertungAusgabe,
    system_prompt=(
        "Du bist ein hilfreicher Assistent zur Reifegradbewertung in Audits zur nutzerzentrierten Entwicklung. "
        "Du soll eine subjektive Einschätzung geben, ob eine Zertifizierung möglich ist."
        "Deine Aufgabe ist es, basierend auf vier Antworten, eine Tendenz für den Reifegrad in der jeweilgen Phase "
        "zu geben. Dafur werden dir bereits Bewertung, Begründung und Verbesserungspotentiale der einzelnen Antworten übergeben."
        "In dem Feld 'gesamtbewertungstext' soll einem kurzen und durch Absätze sturkturierter Text über der Gesamteinschätzung sein."
        "Begründe mit den übergebenen Informationen kausal, damit deutlich wird wie die Gesamtbewertung zurstande kommt."
        "Schreibe die Bewertung kompakt und stelle transparent dar, dass es sich um eine subjektive Einschätzung handelt "
        "basierend auf den Eingabedaten handelt. Stelle den causalen Zusammenhang zwischen Eingabe und Bewertung dar."
        "Mache deutlich, dass eine eindeutige Bewertung durch einen Auditor"
        "getroffen werden kann und man diesen bei Unstimmigkeiten immer zu raten ziehen sollte."
        "Füge ganz am Ende hinzu, dass Rückfragen zur Beurteilung wie auch zu Methoden und KI-Tools der Phase gestellt werden können."
        "Die Felder 'gesamtbewertung', 'gesamtbegruendung' und 'gesamtverbesserungspotential' sollen die einzelnen Punkte verständlich," 
        "aber trotzdem kurz und prägnant zusammenfassen. "
        "Im Feld 'gesamtverbesserungspotential' soll zunächst nur auf Zielebene beschrieben werden, welche allgemeinen Verbesserungsziele verfolgt werden sollten. "
        "Es sollen dort keine konkreten Methoden oder KI-Tools genannt werden."
        "und anschließen in Unterpunkten konkrete Methoden und KI-Tools vorgeschlagen werden."
        "In den Feldern 'Methoden' und 'KI-Tools' soll ergänzend auf Zielebene aufgezeigt werden, welche weiteren Maßnahmen sinnvoll wären."
        "Der Fokus liegt dabei auf konstruktiven, zielgerichteten Vorschlägen. Gib explizit die Namen der empfohlen Methoden und KI-Tools an."
        "Gib nur zusammenhängende Texte keine Aufzählungen innerhalb der Felder zurück."
    )
)

async def evaluate_phase(nutzereingabe:list[str], antworten: BewertungEingabe, phase: str, ux_erfahrung: str, methoden:str, ki_tools:str):
    prompt = (
        f"Bewerte die Phase '{phase}' im Audit zur nutzerzentrierten Entwicklung anhand folgender "
        "vordefinierter Bewertungsschema für die gegebenen Antworten:\n\n"
        f"Je nach UX-Erfahrung des Unternehmens ({ux_erfahrung}) soll der Fokus der Erklärung sowie der Detailgrad der Begründung angepasst werden. Dabei orientiert sich die Gestaltung der Erklärung an den Konzepten von Ye et al.\n\n"
        "- Bei **wenig Erfahrung**:\n"
        "  - **Terminology**: Fachbegriffe (z.B. Methoden) sollen verständlich erklärt werden.\n"
        "  - **Justification**: Die Begründung soll ausführlich darlegen, *warum* eine bestimmte Bewertung vergeben wurde.\n"
        "  - **Traceability** ist in dieser Gruppe weniger vorrangig.\n\n"
        "- Bei **erfahreneren Unternehmen**:\n"
        "  - **Terminology**: Kann reduziert werden – Fachbegriffe müssen nicht mehr ausführlich erläutert werden.\n"
        "  - **Justification**: Die Begründung soll weiterhin klar erkennbar machen, *warum* eine Bewertung erfolgt ist – jedoch kurz, prägnant und fachlich fundiert.\n"
        "  - **Traceability**: Es soll transparent sein, *welche* Kriterien oder Beobachtungen zum Ergebnis geführt haben.\n"
    )
    for i, antwort in enumerate(antworten.antwortoptionen, 0):
        print(nutzereingabe[i])
        prompt += (
            f"Antwort {i}:\n"
            f"Text: {antwort.text}\n"
            f"Eingabe: {nutzereingabe[i]}\n"
            f"Hinweis: {antwort.hinweis}\n"
            f"Methoden: {methoden}\n"
            f"KI-Tools: {ki_tools}\n"
            f"Punkte: {antwort.punkte}\n"
            f"Bewertung: {antwort.bewertung}\n"
            f"Begründung: {antwort.begruendung}\n"
            f"Verbesserungspotential: {antwort.verbesserungpotential}\n\n"
        )
    prompt += (
        f"Gib eine **Gesamtbewertung** der Phase **{phase}** ab, mit einer **kausalen Begründung**, "
        "die kompakt, erklärend und selektiv formuliert ist. Die Bewertung soll auf den Einzelbewertungen beruhen "
        "und klar aufzeigen, an welchen Stellen noch Schwächen bestehen.\n\n"
        "- Berücksichtige die gegebenen Hinweise, sofern vorhanden.\n"
        " -Gib keine weiteren Methoden oder KI-Tools an, außer die im Promt enthaltenen an.\n"
        "- Formatiere die Antwort in **Markdown**.\n"
        "- Fasse alle Informationen in einer zusammenhängenden Einschätzung zusammen, ohne die einzelnen Antworten explizit aufzuführen.\n"
        "- Verwende als Überschrift:\n\n"
        f"#### Vorläufige Bewertung der Phase {phase}\n\n"
        "- Beginne den Text mit: **'Ihr Unternehmen weist insgesamt...**'\n"
    )

    response = await quan_rat_agent.run(user_prompt=prompt)

    return response