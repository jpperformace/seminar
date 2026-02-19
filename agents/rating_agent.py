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

quan_rat_agent = Agent(
    os.getenv("MODEL_CHOICE", "gpt-4.1-mini"),
    output_type=BewertungAusgabe,
    system_prompt=(
        "Du bist ein hilfreicher Assistent zur Reifegradbewertung in Audits zur nutzerzentrierten Entwicklung. "
        "Du soll eine subjektive Einschätzung geben, ob eine Zertifizierung möglich ist."
        "Deine Aufgabe ist es, basierend auf vier Antworten, eine Tendenz für den Reifegrad in der jeweilgen Phase "
        "zu geben. Dafur werden dir bereits Bewertung, Begründung und Verbesserungspotentiale der einzelnen Antworten übergeben."
        "In dem Feld 'gesamtbewertungstext' soll einem kurzen und durch Absätze sturkturierter Text über der Gesamteinschätzung sein."
        "Schreibe die Bewertung kompakt und stelle transparent dar, dass es sich um eine subjektive Einschätzung handelt "
        "basierend auf den Eingabedaten handelt. Stelle den causalen Zusammenhang zwischen Eingabe und Bewertung dar."
        "Mache deutlich, dass eine eindeutige Bewertung durch einen Auditor getroffen werden kann und man diesen bei Unstimmigkeiten immer zu raten ziehen sollte."
        "Füge ganz am Ende hinzu, dass Rückfragen zur Beurteilung wie auch zu Methoden und KI-Tools der Phase gestellt werden können."
        "Die Felder 'gesamtbewertung', 'gesamtbegruendung' und 'gesamtverbesserungspotential' sollen die einzelnen Punkte verständlich," 
        "aber trotzdem kurz und prägnant zusammenfassen. "
        "In das Feld 'gesamtbegruendung' soll mit den übergebenen Informationen kausal begründet werden, damit deutlich wird wie die Gesamtbewertung zurstande kommt."
        "In das Feld 'gesamtbegruendung' soll am Ende ein einzelner kontrafaktischer Satz eingebaut werden, der hypothetisch beschreibt, "
        "was inhaltlich anders hätte sein müssen, damit eine bessere Bewertung erzielt worden wäre." 
        "Dieser Satz muss ohne konkrete Punktzahl oder Score formuliert sein und soll auf der übergeben Bewertungsmetrik basieren."
        "Er ist integraler Bestandteil der Gesamtbegründung und darf nicht ausgelassen werden."
        "Es soll in der gesamtbegruendung keine Score genannt werden sondern qualitativ begründet werden."
        "Im Feld 'Gesamtverbesserungspotenzial' soll zunächst ausschließlich auf Zielebene beschrieben werden, "
        "welche übergeordneten Verbesserungsziele verfolgt werden sollten. Konkrete Methoden oder KI-Tools dürfen hier nicht genannt werden. "
        "In den Feldern 'Methoden' und 'KI-Tools' soll ebenfalls auf Zielebene argumentiert werden, jedoch mit dem Ziel, geeignete Maßnahmen zu identifizieren. "
        "Dabei sind explizit die Namen der empfohlenen Methoden bzw. KI-Tools anzugeben. "
        "Die jeweils am besten passende Methode bzw. das geeignetste KI-Tool soll etwas ausführlicher erläutert werden. "
        "Zusätzlich sind alternative Vorschläge zu nennen und kontrastiv (contrastive) zu erklären, weshalb diese im Vergleich weniger geeignet erscheinen. "
        "Der Detaillierungsgrad der Ausführungen soll sich an der Bewertung orientieren: Je schlechter die Bewertung, desto ausführlicher die Beschreibung; "
        "bei guter Bewertung genügen knappe Hinweise. "
        "Der Fokus liegt insgesamt auf konstruktiven, zielgerichteten Vorschlägen. "
        "Gib die Inhalte als durchgehenden Fließtext ohne Aufzählungen aus."
    )
)

rating_agent = Agent(
    os.getenv("MODEL_CHOICE", "gpt-4.1-mini"),
    output_type=ResponseTextOutput,
    system_prompt=(
        "Du bist ein hilfreicher Assistent zur Reifegradbewertung in Audits zur nutzerzentrierten Entwicklung. "
        "Du gibst auf Basis der vier übergebenen Antworten einen einzigen zusammenhängenden Gesamtbewertungstext zurück, "
        "der alle relevanten Inhalte vereint: eine subjektive Gesamteinschätzung, eine transparente kausale Begründung, "
        "übergeordnete Verbesserungspotenziale sowie Empfehlungen zu Methoden und KI-Tools inklusive kurzer Erläuterung "
        "der jeweils geeignetsten Option und kontrastiver Begründung für weniger passende Alternativen. "
        "Die Darstellung erfolgt als kompakter Text ohne Aufzählungen. Füge eine Überschrift hinzu. Stukturier den Text mi Zeilenumbrüchen übersichtlich. "
        "Du nennst keine Scores, sondern argumentierst qualitativ anhand der Bewertungsmetrik. "
        "Die subjektive Natur deiner Einschätzung muss klar benannt werden, ebenso der Hinweis, dass eine verbindliche "
        "Bewertung immer durch einen Auditor erfolgt und dieser bei Unstimmigkeiten hinzugezogen werden sollte. "
        "Die kausale Begründung erklärt nachvollziehbar, wie die Einschätzung aus den übergebenen Informationen "
        "abgeleitet wurde und endet mit einem einzelnen kontrafaktischen Satz, der beschreibt, was sich inhaltlich hätte "
        "ändern müssen, damit die Bewertung besser ausgefallen wäre (ohne Zahlen oder konkrete Punktwerte). "
        "Die Verbesserungspotenziale werden auf Zielebene formuliert, ohne konkrete Maßnahmen zu beschreiben; "
        "konkrete Empfehlungen erscheinen ausschließlich in kurzen Erläuterungen in den Abschnitten zu Methoden und KI-Tools. "
        "Die Ausführlichkeit der Empfehlungen richtet sich nach der Bewertung: "
        "Je schwächer die Gesamteinschätzung, desto detaillierter die Beschreibung. "
        "Schließe den Gesamtbewertungstext immer mit dem Hinweis, dass Rückfragen zur Bewertung oder zu Methoden "
        "und KI-Tools der Phase gestellt werden können."
        "Versuche alle Teile im Bewertungstext kurz und verständlich zu benennen"
    )
)

async def evaluate_phase(nutzereingabe:list[str], antworten: BewertungEingabe, phase: str, ux_erfahrung: str, methoden:str, ki_tools:str, evaluation_metrik:str):
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

    response = await quan_rat_agent.run(user_prompt=prompt)

    return response


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

def final_report(phase:str, groesse:str, ux_erfahrung:str, pre_evaluation:str, message_history):
    prompt = (
        f"Erstelle eine finale Auditberwertung für die Phase {phase}. "
        f"Du sollst die Inhalte der vorläufigen Bewertung übernehmen und die finalen Bericht entsprechend der message_histroy so überarbeiten, "
        f"dass du Verbesserung / Fehlinterpretatetionen die der Nutzer dir als Rückmeldungen auf die Bewertung gegeben hat, in den finalen Report einfließen lässt. "
        f"dass du Informationen die der Nutzer explizit angefragt hat im Report vertiefst. (zum Beispiel über vorgebene Methoden oder KI-Tools). "
        f"Die Vorläufige Bewertung lautet: {pre_evaluation}"
    )


    prompt += (
        f"Starte mit der Überschrift: ### Bewertung der Phase {phase}"
        f"Strukturiere die Bewertung wie folgt: "
        f"Bewertung: (hier kurz und knapp)"
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

    return rating_agent.run_stream(user_prompt=prompt, message_history=message_history)
