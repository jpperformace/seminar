from graphiti_core.nodes import EpisodeType

episodes = [
            {
                'content':  'Frage: Wer übernimmt in Ihrem Unternehmen Aufgaben im Bereich Usability und User Experience?'
                            'Antwort 1: Es gibt ein ganzes "Usability und User Experience"-Team oder eine "Usability und User Experience"-Abteilung. Punkte: 3'
                            'Antwort 2: Es gibt einen "Usability und User Experience"-Experten. Punkte: 2'
                            'Antwort 3: Andere Mitarbeitende (z.B. Software-Developer, Projekteitung, Produktmanagement). Punkte: 1'
                            'Antwort 4: Bisher gibt es hierfür niemand Dezidiertes. Punkte: 0',
                'type': EpisodeType.text,
                'description': 'UX-Zuständigkeit',
            },
            {
                'content': 'Frage: Können am Entwickungsprozess des digitalen Produtkes / der Dienstleistung beteiligte Mitarbeitende Usability-Qualitfikationen nachweisen?'
                           'Antwort 1: Alle Mitarbeiter können "Usability und User Experience"-Qualitfikationen nachweisen. Punkte: 2'
                           'Antwort 2: Einige Mitarbeiter können "Usability und User Experience"-Qualitfikationen nachweisen. Punkte: 1'
                           'Antwort 3: Keine Mitarbeiter können "Usability und User Experience"-Qualitfikationen nachweisen. Punkte: 0',
                'type': EpisodeType.text,
                'description': 'Usability-Qualifikationen der Mitarbeiter',
            },
            {
                'content': 'Frage: Wie ist die interne Kommunikation und Zusammenarbeit in Bezug auf "Usability und User Experience" im Entwicklungsprozess strukturiert?'
                           'Antwort 1: Es gibt regelmäßige Meetings ausschließlich zu "Usability und User Experience"-Themen mit allen Beteiligten. Punkte: 3'
                           'Antwort 2: "Usability und User Experience" ist ein fester Tagesordnungspunkt in regulären Projektmeetings. Punkte: 2'
                           'Antwort 3: Die Kommunikation zu "Usability und User Experience" findet unregelmäßig und ad hoc statt. Punkte: 1'
                           'Antwort 4: Es gibt keine spezifische Kommunikation zu "Usability und User Experience". Punkte: 0',
                'type': EpisodeType.text,
                'description': 'Kommunikation zu "Usability und User Experience"',
            },
            {
                'content': 'Frage: In welchem Umfang ist die Einbindung von Nutzer im Entwicklungsprozess geplant?'
                           'Antwort 1: Es gibt eine verbindliche und dokumentierte Planung, wie und wann Nutzer systematisch in mehreren Projektphasen einbezogen werden (z.B. Anforderungsanalyse, Tests, Evaluation).. Punkte: 3'
                           'Antwort 2: Es ist eine Einbindung vorgesehen (z.B. Tests oder Interviews), aber nicht verbindlich dokumentiert oder nicht für alle Phasen geplant. Punkte: 2'
                           'Antwort 3: Eine gelegentliche Einbindung ist angedacht oder erfolgt erfahrungsgemäß, aber ohne klare Planung. Punkte: 1'
                           'Antwort 4: Es gibt keine vorgesehene Planung zur Einbindung von Nutzer. Punkte: 0',
                'type': EpisodeType.text,
                'description': 'Planung über Einbindung der Nutzer',
            },
        ]