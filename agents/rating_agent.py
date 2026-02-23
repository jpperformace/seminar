from enum import Enum

from pydantic import BaseModel
from pydantic_ai.agent import Agent
from typing import Literal, Optional

import os

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

class ResponseTextOutput(BaseModel):
    antworttext: str

rating_agent = Agent(
    os.getenv("MODEL_CHOICE", "gpt-4.1-mini"),
    output_type=ResponseTextOutput,
    system_prompt=(
        "Du bist ein hilfreicher Assistent zur Reifegradbewertung in Audits zur nutzerzentrierten Entwicklung. "
        "Inhalt:"
        "Du gibst auf Basis der übergebenen Antworten einen einzigen zusammenhängenden Gesamtbewertungstext zurück, "
        "der alle relevanten Inhalte vereint. Der Text soll in folgende Abschnitte unterteilt sein,"
        "wobei zwischen den Abschnitten zur besseren Lesbarkeit Zeilenumbrüche sind"

        "1.  eine Gesamteinschätzung, die aus einer einsatz langen Bewertung der Phase und einer drei bis vier Sätzen langen Begründung besteht, "
        "   die transparent und kausal erklärt warum die Beurteilung zustande kommt"
        "   Du nennst keine Scores, sondern argumentierst qualitativ anhand der Bewertungsmetrik."
        "   Die kausale Begründung erklärt nachvollziehbar, wie die Einschätzung aus den übergebenen Informationen "
        "   abgeleitet wurde und endet mit einem einzelnen kontrafaktischen Satz, der beschreibt, was sich inhaltlich hätte "
        "   ändern müssen, damit die Bewertung besser ausgefallen wäre (ohne Zahlen oder konkrete Punktwerte). "
        
        "2.  gib allgemein Verbesserungspotenziale und anschließend Empfehlungen zu Methoden (die nicht explizit verwendet werden) "
        "   und KI-Tools inklusive kurzer Erläuterung für die Vorschlägen, mit der jeweils geeignetsten Option und kontrastiver Begründung für weniger passende Alternativen. "
        "   Die Verbesserungspotenziale werden auf Zielebene formuliert, ohne konkrete Maßnahmen zu beschreiben; "
        "   konkrete Empfehlungen erscheinen ausschließlich in kurzen Erläuterungen in den Abschnitten zu Methoden und KI-Tools. " 
        
        "3.  Die subjektive Natur deiner Einschätzung muss klar benannt werden, ebenso der Hinweis, dass eine verbindliche "
        "   Bewertung immer durch einen Auditor erfolgt und dieser bei Unstimmigkeiten hinzugezogen werden sollte."
        "   Schließe den Gesamtbewertungstext immer mit dem Hinweis, dass Rückfragen zur Bewertung oder zu Methoden "
        "   und KI-Tools der Phase gestellt werden können."

        ""
        "Struktur"
        "Die Darstellung erfolgt als kompakter Text ohne Aufzählungen. "
        "Füge eine Überschrift hinzu. Stukturiere den Text mit Zeilenumbrüchen übersichtlich. "
        "Versuche alle Teile im Bewertungstext kurz und verständlich zu benennen"
        "Der Text soll nicht länger als 10 Sätze sein"
        "Markiere alle Kernwörter wie die genaue Bewertung, einzelne Kirterienen, Verbesserungsvorschläge und konkrete Methoden udn KI-Tools Fett"
    )
)

final_rating_agent = Agent(
    os.getenv("MODEL_CHOICE", "gpt-4.1-mini"),
    output_type=ResponseTextOutput,
    system_prompt=(
        "Du bist ein hilfreicher Assistent zur Reifegradbewertung in Audits zur nutzerzentrierten Entwicklung. "
        "Erstelle einen finalen Reprot in HTML-Code der folgendes enthält: eine subjektive Gesamteinschätzung, eine transparente kausale Begründung, "
        "übergeordnete Verbesserungspotenziale sowie Empfehlungen zu Methoden und KI-Tools inklusive kurzer Erläuterung "
        "der jeweils geeignetsten Option und kontrastiver Begründung für weniger passende Alternativen. "
        "Du nennst keine Scores, sondern argumentierst qualitativ anhand der Bewertungsmetrik."
        "Strukturiere klar mit Zeilenumbrüchen."

    )
)


def evaluate_phase_and_get_response(nutzereingabe:list[str], antworten: BewertungEingabe, groesse:str, phase: str, ux_erfahrung: str, methoden:str, ki_tools:str, evaluation_metrik:str):
    prompt = (
        f"Bewerte die Phase '{phase}' im Audit zur nutzerzentrierten Entwicklung anhand folgender "
        "vordefinierter Bewertungsschema für die gegebenen Antworten:\n\n"
        f"Methoden: {methoden}\n"
        f"KI-Tools: {ki_tools}\n"
        f"Bewertungsmetrik: {evaluation_metrik}\n\n"
    )
    for i, antwort in enumerate(antworten.antwortoptionen, 0):
        print(nutzereingabe[i])
        prompt += (
            f"Antwort {i}:\n"
            f"Text: {antwort.text}\n"
            f"Eingabe: {nutzereingabe[i]}\n"
            f"Hinweis: {antwort.hinweis}\n"
            f"Punkte: {antwort.punkte}\n"
            f"Bewertung: {antwort.bewertung}\n"
            f"Begründung: {antwort.begruendung}\n"
            f"Verbesserungspotential: {antwort.verbesserungpotential}"
        )

    prompt += (
        f"Starte mit der Überschrift: ### Vorläufige Bewertung der Phase {phase}"
        f"Gib eine **Gesamtbewertungtext** der Phase **{phase}** ab, mit einer **kausalen Begründung**, "
        "die kompakt, erklärend und selektiv formuliert ist. Die Bewertung soll auf den Einzelbewertungen beruhen "
        "und klar aufzeigen, an welchen Stellen noch Schwächen bestehen. "
        "Fasse alle Informationen in einer zusammenhängenden Einschätzung zusammen, ohne die einzelnen Antworten explizit aufzuführen.\n"
        f"Berücksichtige die Unternehmensgröße **{groesse}** ausdrücklich: "
        "Kleinere Unternehmen sind grundsätzlich weicher zu bewerten, da nicht alle Maßnahmen, Rollen oder formalen Prozesse realistisch umsetzbar sind. "
        "Bewerte daher vor allem, ob nutzerzentrierte Prinzipien unter den gegebenen Ressourcen praktikabel angewendet werden und vermeide idealtypische Maßstäbe."
    )

    prompt += (
        f"Je nach UX-Erfahrung des Unternehmens ({ux_erfahrung}) soll der Fokus der Erklärung sowie der Detailgrad der Begründung angepasst werden. "
        "Dabei orientiert sich die Gestaltung der Erklärung an den Konzepten von Ye et al.\n\n"
        "- Bei **wenig Erfahrung**:\n"
        "  - **Terminology**: Fachbegriffe (z.B. Methoden) sollen verständlich erklärt werden.\n"
        "  - **Justification**: Die Begründung soll ausführlich darlegen, *warum* eine bestimmte Bewertung vergeben wurde.\n"
        "  - **Traceability** ist in dieser Gruppe weniger vorrangig.\n\n"
        "- Bei **erfahreneren Unternehmen**:\n"
        "  - **Terminology**: Kann reduziert werden – Fachbegriffe müssen nicht mehr ausführlich erläutert werden.\n"
        "  - **Justification**: Die Begründung soll weiterhin klar erkennbar machen, *warum* eine Bewertung erfolgt ist – jedoch kurz, prägnant und fachlich fundiert.\n"
        "  - **Traceability**: Es soll transparent sein, *welche* Kriterien oder Beobachtungen zum Ergebnis geführt haben.\n")

    return rating_agent.run_stream(user_prompt=prompt)

def get_final_report(phase:str, groesse:str, ux_erfahrung:str, pre_evaluation:str, message_history):
    prompt = (
        f"Erstelle eine finale Auditbewertung für die Phase {phase}. "
        "Übernimm die Inhalte der vorläufigen Bewertung und überarbeite sie auf Basis der message_history. "
        "Berücksichtige dabei alle Rückmeldungen des Nutzers zur vorläufigen Bewertung: "
        "Korrigiere Fehlinterpretationen, integriere Verbesserungshinweise und vertiefe Inhalte, "
        "die der Nutzer explizit nachgefragt hat (z. B. konkrete Methoden oder KI-Tools). "
        "Füge auf keinen Fall Informationen des letzen Abschnittes aus der vorläufigen Bewertung ein."
        f"Die vorläufige Bewertung lautet: {pre_evaluation}"
    )


    prompt += (
        f"Berücksichtige die Unternehmensgröße ({groesse}): "
        "Kleinere Unternehmen sind grundsätzlich differenziert und pragmatisch zu bewerten, "
        "da nicht alle Maßnahmen, Rollen oder formalen Prozesse realistisch umsetzbar sind. "
        "Bewerte daher primär, ob nutzerzentrierte Prinzipien unter den gegebenen Ressourcen praktikabel angewendet werden, "
        "und vermeide idealtypische Maßstäbe.\n\n"
        f"Passe zudem den Detailgrad und die fachliche Tiefe an die UX-Erfahrung des Unternehmens ({ux_erfahrung}) an: "
        "Für unerfahrene Unternehmen formuliere verständlicher und erklärender. "
        "Für erfahrene Unternehmen ergänze vertiefende und strategische Hinweise."
    )

    prompt += (
        f"""
                Verwende exakt folgende Überschiften. Füge keine weitere Überschift hinzu. Strukturiere die Bewertung wie folgt:

                ### Bewertung:
                Gib eine kurze, prägnante Gesamtbeurteilung.

                ### Begründung:
                Formuliere eine ausführliche, kausale Begründung unter Bezug auf die Kriterien und die Antworten des Nutzers.

                ### Verbesserungspotential:
                Gib konkrete Vorschläge zur Weiterentwicklung, um eine bessere Bewertung zu erreichen.

                #### UX-Methoden:
                Fließtext mit vorgeschlagenen Methoden. Erläutere geeignete vorgeschlagene Methoden genauer und begründe, welche im Kontext am besten passen.

                #### KI-Tools:
                Fließtext mit vorgeschlagenen KI-Tools. Erläutere geeignete vorgeschlagene KI-Tools genauer und begründe, welche im Kontext am sinnvollsten sind.
            """
    )


    return final_rating_agent.run_stream(user_prompt=prompt, message_history=message_history)
