from agents.rating_agent import Antwortoption
from audit_process.general import response_options_UX_experience, response_options_expert

organizing_summary = """Die Phase Organisation umfasst alle organisatorischen Elemente, die sicherstellen, 
                      dass die Benutzererfahrung eine hohe Priorität im Unternehmen hat. Dazu gehören die 
                      Verankerung einer nutzerzentrierten Denkweise und das Vorhandensein von UX-Experten."""

organizing_questions = ['Wie würdest du den Reifegrad eurer Organisation im Bereich nutzerzentrierte Entwicklung einschätzen – von Einsteiger bis sehr erfahren?',
             'Wer übernimmt in Ihrem Unternehmen Aufgaben im Bereich Usability und User Experience (UUX)?',
             'Gibt es ein UX-Experten in Ihrem Unternehmen?',
             'Können am Entwickungsprozess des digitalen Produktes / der Dienstleistung beteiligte Mitarbeitende Usability-Qualitfikationen nachweisen?',
             'Wie ist die interne Kommunikation und Zusammenarbeit in Bezug auf "Usability und User Experience" im Entwicklungsprozess strukturiert?']

organizing_response_q1 = [
        Antwortoption(
            text='Es gibt ein ganzes UUX-Team oder eine UUX-Abteilung.',
            punkte=3,
            bewertung="Sehr gut",
            begruendung=(
                "Ein dediziertes \"Usability und User Experience\"-Team zeigt, dass das Unternehmen die Bedeutung nutzerzentrierter Entwicklung "
                "organisatorisch verankert hat. Es ermöglicht Spezialisierung, strukturiertes Vorgehen und nachhaltige "
                "Qualitätssicherung im Bereich Usability & User Experience."
            ),
            verbesserungpotential=(
                "Weiter so – bei der Zertifizierung bestehen hier sehr gute Voraussetzungen. Wichtig ist, dass das Team "
                "in Entwicklungszyklen frühzeitig eingebunden ist und mit anderen Fachbereichen koordiniert arbeitet."
            )
        ),
        Antwortoption(
                text='Es gibt einen UUX-Experten.',
                punkte=2,
                bewertung="Gut",
                begruendung=(
                        "Die Benennung eines Experten zeigt, dass das Thema erkannt wurde und zumindest eine zentrale fachliche "
                        "Verantwortung existiert. Die Person kann Methoden und Werkzeuge nutzerzentrierter Entwicklung anwenden."
                ),
                verbesserungpotential=(
                        "Ausbau in Richtung eines Teams oder Einbindung zusätzlicher Rollen zur Entlastung. "
                        "Schaffung klarer Prozesse zur Integration von UUX in alle Projektphasen. "
                        "Sicherstellung, dass die Expertise des Einzelnen auch tatsächlich wirksam in Entscheidungen einfließt."
                )
        ),
        Antwortoption(
            text='Andere Mitarbeitende (z.B. Software-Developer, Projektleitung, Produktmanagement).',
            punkte=1,
            bewertung="Ausreichend – mit Schwächen",
            begruendung=(
                "Die Verantwortung für UUX ist unklar verteilt. Zwar kann bei motivierten Teams auch ohne dedizierte Rolle "
                "Nutzerzentrierung entstehen, doch fehlt es oft an methodischer Tiefe, systematischem Vorgehen und konsequenter Umsetzung."
            ),
            verbesserungpotential=(
                "Einführung einer klaren Rolle oder Zuständigkeit für UUX. "
                "Schulung vorhandener Mitarbeitender in UX-Methoden. "
                "Etablierung von UX-Aktivitäten als festen Bestandteil des Entwicklungsprozesses."
            )
        ),
        Antwortoption(
            text='Bisher gibt es hierfür niemand Dezidiertes.',
            punkte=0,
            bewertung="Ungenügend – nicht zertifizierungsfähig",
            begruendung=(
                "Es bestehen keine klaren Zuständigkeiten für UUX. Damit ist eine systematische nutzerzentrierte Entwicklung "
                "nicht möglich. Dies widerspricht zentralen Anforderungen von UUX-Normen und Zertifizierungen."
            ),
            verbesserungpotential=(
                "Kurzfristig: Benennung einer verantwortlichen Person für Usability & UX. "
                "Mittelfristig: Aufbau eines Kompetenzteams oder Integration der Rolle in bestehende Projektstrukturen. "
                "Langfristig: Verankerung von UUX als Bestandteil der Unternehmensstrategie und des Qualitätsmanagements."
            )
        )
]

organizing_response_q2 = [
        Antwortoption(
            text='Ja, alle',
            punkte=2,
            bewertung="Sehr gut",
            begruendung=(
                "Die flächendeckende Qualifikation aller Mitarbeitenden im Bereich Usability und UX zeigt ein hohes "
                "Engagement des Unternehmens für nutzerzentrierte Entwicklung und sichert die Qualität über alle "
                "Entwicklungsphasen hinweg."
            ),
            verbesserungpotential=(
                "Weiter so – wichtig ist, diese Qualifikationen aktuell zu halten und praxisorientierte Weiterbildung sicherzustellen."
            )
        ),
        Antwortoption(
            text='Einige',
            punkte=1,
            bewertung="Ausreichend – mit Schwächen",
            begruendung=(
                "Teilweise Qualifikationen zeigen, dass das Unternehmen das Thema Usability erkannt hat, "
                "aber noch nicht alle relevanten Mitarbeitenden entsprechend geschult sind."
            ),
            verbesserungpotential=(
                "Ausbau der Qualifizierungsmaßnahmen, um mehr Mitarbeitende zu befähigen und ein einheitliches Qualitätsniveau "
                "im Team sicherzustellen."
            )
        ), Antwortoption(
            text='Nein',
            punkte=0,
            bewertung="Ungenügend – nicht zertifizierungsfähig",
            begruendung=(
                "Es fehlt an formalen Usability- und UX-Kompetenzen im Team, was die erfolgreiche Umsetzung nutzerzentrierter "
                "Entwicklung deutlich erschwert und Risiken für die Produktqualität birgt."
            ),
            verbesserungpotential=(
                "Sofortige Einführung von Schulungen und Weiterbildungen im Bereich Usability & UX. "
                "Langfristig Aufbau von Kompetenzträgern zur Sicherstellung der Nutzerorientierung."
            )
        )
]

organizing_response_q3 = [
        Antwortoption(
            text='Es gibt regelmäßige Meetings ausschließlich zu UUX-Themen mit allen Beteiligten.',
            punkte=3,
            bewertung="Sehr gut",
            begruendung=(
                "Regelmäßige, dedizierte Meetings zeigen ein hohes Maß an organisatorischer Verankerung von UUX "
                "und fördern den kontinuierlichen Austausch sowie die frühzeitige Integration von Nutzerfeedback."
            ),
            verbesserungpotential=(
                "Diese Praxis ist vorbildlich. Wichtig ist, die Meetings effizient zu gestalten und Ergebnisse systematisch "
                "in den Entwicklungsprozess zu integrieren."
            )
        ),
        Antwortoption(
            text='UUX ist ein fester Tagesordnungspunkt in regulären Projektmeetings.',
            punkte=2,
            bewertung="Gut",
            begruendung=(
                "Die regelmäßige Einbindung von UUX-Themen in Projektmeetings stellt sicher, dass das Thema präsent bleibt "
                "und berücksichtigt wird."
            ),
            verbesserungpotential=(
                "Eine mögliche Verbesserung wäre die Einrichtung separater UUX-Meetings zur vertieften Bearbeitung spezifischer Themen."
            )
        ),
        Antwortoption(
            text='Die Kommunikation zu UUX findet unregelmäßig und ad hoc statt.',
            punkte=1,
            bewertung="Ausreichend – mit Schwächen",
            begruendung=(
                "Ad-hoc-Kommunikation führt zu inkonsistenter Berücksichtigung von UUX-Aspekten und erschwert eine "
                "kontinuierliche Nutzerzentrierung."
            ),
            verbesserungpotential=(
                "Etablierung regelmäßiger Austauschformate und klarer Kommunikationsstrukturen zur Förderung der Zusammenarbeit."
            )
        ),
        Antwortoption(
            text='Es gibt keine spezifische Kommunikation zu UUX.',
            punkte=0,
            bewertung="Ungenügend – nicht zertifizierungsfähig",
            begruendung=(
                "Ohne spezifische Kommunikation zu UUX fehlen wichtige Voraussetzungen für eine erfolgreiche nutzerzentrierte "
                "Entwicklung."
            ),
            verbesserungpotential=(
                "Sofortige Einführung von Kommunikationskanälen und Meetings zu UUX-Themen sowie Sensibilisierung aller "
                "Beteiligten."
            )
        )
]


all_response_lists = [
    organizing_response_q1,
    organizing_response_q2,
    organizing_response_q3
]

organzing_rating_metrik = alternative_bewertung_organizing = [
    {"bewertung": option.bewertung, "inhalt": option.text}
    for antwortliste in all_response_lists
    for option in antwortliste
]

organzing_response_text_options = [
    response_options_UX_experience,
    [option.text for option in organizing_response_q1],
    response_options_expert,
    [option.text for option in organizing_response_q2],
    [option.text for option in organizing_response_q3]
]