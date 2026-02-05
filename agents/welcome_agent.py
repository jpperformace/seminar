# Einfacher API-basierter Willkommens-Agent
from typing import Sequence

from pydantic import BaseModel
from pydantic_ai import Agent
import os

from audit_process.organizing import organizing_summary
from audit_process.understanding import understanding_summary

class WelcomeOutput(BaseModel):
    simulation_gestartet: bool
    antworttext: str

# Agent, der die Willkommensnachricht **über das Modell** generiert
welcome_agent = Agent(
    os.getenv("MODEL_CHOICE", "gpt-4.1-mini"),
    output_type=WelcomeOutput,
    system_prompt=(
        f"Du bist ein KI-Assistent, der Nutzer in ein Audit zur nutzerzentrierten Entwicklung einführt. "
        f"Erzeuge eine freundliche, klare und einladende Willkommensnachricht, die erklärt: \n"
        f"- dass der Assistent dabei helfen soll sich auf Audits zur nutzerzentrierten Entwicklung vorzubereiten.\n"
        f"- dass der Assistent entlang vier Phasen leitet: Organisieren, Verstehen, Gestalten und Bewerten. \n"
        f"- dass er grundlegend zwei Feature hat: "
        f"   1. Vereinfachte Simulation des Auditsprozess: Was sind grundlegende Aspekte/Anfornderungen? Die Simulation dauert ungefähr 30 Minuten. \n"
        f"   2. Informationsvermittlung von UX-Praktiken: Welche UX-Methoden kann ich in der Phase anwenden? Was für KI-Tools würden mich dabei unterstützen? \n"
        f"Der KI-Assistent beginnt in der ersten Phase und leitet dann Schritt für Schritt durch die Phasen und deren Anforderungen. \n"
        f"Versuche einen natürlichen Dialog zu erzeugen. Erkläre verständlich. \n\n"
        f"Folgende Informationen sind über die Phasen gegeben: "
        f"- Organisieren: {organizing_summary} \n"
        f"- Verstehen: {understanding_summary}"
    )
)


# Funktion zum Abrufen der Begrüßung
def get_welcome_message(phase:str, frage:str):
    prompt = (f"Erzeuge ein kurze Willkommensnachricht für die jeweilige Phase."
              f"Aktuell befindest sich die Simulation in der Phase {phase}. \n"
              f"- Wenn die Simulation in der ersten Phase Organisieren ist, dann beginne zuerst mit einer Einleitung, die erklärt wofür der KI-Assisstent da ist und was er bietet."
              f"Füge anschließen eine allgemeine Erklärung der aktuellen Phase hinzu. Gehe nicht auf einzelne Kriterien ein. \n"
              f"- Wenn der KI-Assitent sich in einer fortgeschrittenen Phase befindet, dann versuche eine Überleitung zu der Phase zu geben und erkläre was die Kernaspekte der Phase ist. \n"
              f"Weise anschließend drauf hin, dass man bei Unsicherheiten zu einzelnen Fragen/Kriterien immer Rückfragen stellen kann und nach der Auditbeurteilung,"
              f"man die möglichkeit hat Fragen zu stellen oder Informationen zu vorgeschlagenen Verbesserungen wie möglich Methoden und KI-Tools erhalten kann. "
              f"Beginne am Ende die Simulation, indem du ganz am Ende der Einleitung flüssig die erste Frage stellt: {frage}")

    return welcome_agent.run_stream(user_prompt=prompt)

def start_simulation(nutzereingabe:str, frage:str, nachrichtenverlauf):

    prompt = (
        f"Der Nutzer schrieb: '{nutzereingabe}'.\n"
        f"Falls dies ein Startsignal für die Simulation ist, antworte mit der ersten Frage {frage}. Antworte hierbei flüssig "
        f"und mit kurzem Übergang. Gib deine Nachricht in 'antworttext' zurück und setzte 'simulation_gestartet' True. \n"
        f"Falls nicht, sage nur, dass die Simulation noch nicht gestartet wurde und frage nochmal ob sie gestartet werden soll. "
        f"Gib deine Nachricht in 'antworttext' zurück und setzte 'simulation_gestartet' False. ")

    return welcome_agent.run_stream(user_prompt=prompt, message_history=nachrichtenverlauf)