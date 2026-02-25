from agents.rating_agent import Antwortoption

evaluation_summary = """Die Phase Bewerten beschreibt die systematische Überprüfung von 
                        Konzepten, Prototypen oder bestehenden Anwendungen hinsichtlich 
                        ihrer Usability und Funktionalität. Ziel ist es sicherzustellen, 
                        dass die entwickelte Lösung den Bedürfnissen und Erwartungen 
                        der Nutzenden entspricht. Auf Basis der Evaluation wird entschieden, 
                        ob Anpassungen erforderlich sind oder vorherige Phasen erneut 
                        durchlaufen werden müssen."""

evaluation_questions = [
    'Wie werden Nutzer:innen in den Entwicklungsprozess eingebunden, um erste Entwürfe der Benutzerschnittstelle zu bewerten?',
    'Nach welchen Kriterien erfolgt die Auswahl und Vorselektion der Testteilnehmenden für Evaluationsmaßnahmen?',
    'Welche Methoden setzen Sie insgesamt zur Bewertung der Usability und User Experience (UUX) ein?'
]

evaluation_examples = [
    'Anwendende sollten strukturiert und wiederholt in die Bewertung erster UI-Entwürfe eingebunden werden, um die Erfüllung der Anforderungen und die Nutzererfahrung frühzeitig zu überprüfen. Ein hoher Reifegrad zeigt sich daran, dass Evaluationen geplant stattfinden, '
    'Ergebnisse dokumentiert werden und konkrete Verbesserungen daraus abgeleitet werden. Geringe Reife liegt vor, wenn Feedback nur gelegentlich oder informell eingeholt wird und keine nachvollziehbaren Konsequenzen für die Weiterentwicklung hat. Entscheidend ist, '
    'dass Erkenntnisse systematisch in den Entwicklungsprozess zurückfließen.',
    
    'Die Rekrutierung der Teilnehmenden basiert auf den definierten Zielgruppen sowie den zu beantwortenden Fragestellungen; sie erfolgt anhand relevanter Quoten, wobei Rand-, Special-Interest- sowie Menschen mit Beeinträchtigungen systematisch berücksichtigt werden.',

    'Beispiele für Methoden zur Bewertung von Usability und User Experience (UUX) sind unter anderem Thinking Aloud, halbstrukturierte Interviews, '
    'use-case basiertes Vorgehen, Verhaltensbeobachtungen, Selbsteinschätzungen, objektive Ratings wie Task Success, Nutzerbefragungen, Chatbot-Analysen, Kundenworkshops, '
    'asynchrone oder moderierte UX-Tests. Ergänzend können Benchmarking, expertenbasierte oder heuristische Evaluationen nach ISO 9241 eingesetzt werden, '
    'um die Qualität der Nutzererfahrung systematisch zu beurteile.'
]

evaluation_response_q1 = [
    Antwortoption(
        text='Durch kontinuierliche Zusammenarbeit während des gesamten Prozesses.',
        punkte=3,
        bewertung="Sehr gut",
        begruendung=(
            "Anwendende sind durchgängig in den Entwicklungsprozess eingebunden. "
            "Entwürfe werden frühzeitig und wiederholt bewertet, und Rückmeldungen "
            "fließen systematisch in die Weiterentwicklung ein."
        ),
        verbesserungpotential=(
            "Sichern Sie die kontinuierliche Einbindung verbindlich ab "
            "und stellen Sie sicher, dass Erkenntnisse konsequent "
            "dokumentiert und umgesetzt werden."
        )
    ),
    Antwortoption(
        text='Durch regelmäßige Tests und Iterationen.',
        punkte=2,
        bewertung="Gut",
        begruendung=(
            "Anwendende werden regelmäßig einbezogen und Entwürfe "
            "iterativ überprüft. Rückmeldungen fließen grundsätzlich "
            "in die Weiterentwicklung ein."
        ),
        verbesserungpotential=(
            "Binden Sie Anwendende noch früher und kontinuierlicher "
            "in den gesamten Entwicklungsprozess ein."
        )
    ),
    Antwortoption(
        text='Durch gelegentliche Treffen und Fragebögen.',
        punkte=1,
        bewertung="Ausreichend – mit Schwächen",
        begruendung=(
            "Die Einbindung erfolgt unregelmäßig und wenig strukturiert. "
            "Entwürfe werden nur punktuell bewertet, wodurch "
            "Optimierungspotenziale möglicherweise unentdeckt bleiben."
        ),
        verbesserungpotential=(
            "Etablieren Sie eine regelmäßige und systematische "
            "Einbindung von Anwendenden zur Bewertung erster Entwürfe."
        )
    ),
    Antwortoption(
        text='Sie werden nicht einbezogen.',
        punkte=0,
        bewertung="Ungenügend – nicht zertifizierungsfähig",
        begruendung=(
            "Ohne Einbindung von Anwendenden werden Entwürfe nicht validiert. "
            "Dies erhöht das Risiko von Fehlentwicklungen und geringer Akzeptanz."
        ),
        verbesserungpotential=(
            "Integrieren Sie die Einbindung von Anwendenden als festen "
            "Bestandteil Ihres Entwicklungsprozesses."
        )
    )
]


evaluation_response_q2 = [
    Antwortoption(
        text='Die Auswahl erfolgt systematisch auf Basis definierter Zielgruppen, klarer Fragestellungen und relevanter Quoten. Diversität wird strukturiert berücksichtigt.',
        punkte=2,
        bewertung="Sehr gut",
        begruendung=(
            "Die Rekrutierung der Testteilnehmenden basiert nachvollziehbar auf "
            "definierten Zielgruppen und konkreten Evaluationsfragestellungen. "
            "Relevante Quoten werden angewendet und auch Rand- sowie spezielle "
            "Zielgruppen werden gezielt einbezogen. Diversitätsaspekte sind "
            "grundsätzlich berücksichtigt."
        ),
        verbesserungpotential=(
            "Verankern Sie die Berücksichtigung von Menschen mit Beeinträchtigungen "
            "verbindlich und durchgängig in Ihrer Rekrutierungsstrategie, "
            "um Inklusion systematisch sicherzustellen."
        )
    ),
    Antwortoption(
        text='Die Auswahl orientiert sich an Zielgruppen und Fragestellungen, erfolgt jedoch nicht durchgängig strukturiert oder diversitätsorientiert.',
        punkte=1,
        bewertung="Ausreichend – mit Schwächen",
        begruendung=(
            "Die Rekrutierung basiert grundsätzlich auf definierten Zielgruppen, "
            "jedoch werden Quoten, Randgruppen oder Diversitätsaspekte nicht "
            "konsequent und systematisch berücksichtigt. Dadurch kann die "
            "Repräsentativität der Evaluation eingeschränkt sein."
        ),
        verbesserungpotential=(
            "Definieren Sie verbindliche Auswahlkriterien einschließlich klarer "
            "Quoten und Diversitätsmerkmale. Stellen Sie sicher, dass auch "
            "Menschen mit Beeinträchtigungen regelmäßig einbezogen werden."
        )
    ),
    Antwortoption(
        text='Die Auswahl der Testteilnehmenden erfolgt ohne klar definierte Kriterien oder strukturierte Vorselektion.',
        punkte=0,
        bewertung="Ungenügend – nicht zertifizierungsfähig",
        begruendung=(
            "Ohne klar definierte Zielgruppen, Fragestellungen und Auswahlkriterien "
            "besteht ein hohes Risiko, dass die Testteilnehmenden nicht die "
            "relevante Nutzendengruppe repräsentieren. Evaluationsergebnisse "
            "sind dadurch nur eingeschränkt belastbar."
        ),
        verbesserungpotential=(
            "Etablieren Sie eine strukturierte und dokumentierte Rekrutierungsstrategie "
            "auf Basis definierter Zielgruppen, klarer Fragestellungen und "
            "relevanter Diversitätskriterien."
        )
    )
]

evaluation_response_q3 = [
    Antwortoption(
        text='Eine Vielzahl an Methoden (z.B. A/B-Tests, Eye-Tracking, Usability-Tests, Valenzmethode)',
        punkte=4,
        bewertung="Sehr gut",
        begruendung=(
            "Der Einsatz vieler Methoden zeigt ein hohes methodisches Niveau. "
            "Verschiedene Perspektiven auf das Nutzererlebnis ermöglichen fundierte Entscheidungen."
        ),
        verbesserungpotential=(
            "Sorgen Sie dafür, dass die Ergebnisse systematisch ausgewertet und projektgerecht kombiniert werden."
        )
    ),
    Antwortoption(
        text='Einige wenige Standardmethoden (z.B. Usability-Tests, Fragebögen)',
        punkte=3,
        bewertung="Gut",
        begruendung=(
            "Mehrere etablierte Methoden werden genutzt, was auf ein solides Vorgehen hinweist. "
            "Weitere Methoden könnten die Ergebnisse ergänzen."
        ),
        verbesserungpotential=(
            "Ergänzen Sie bei Bedarf zusätzliche Methoden wie Eye-Tracking oder A/B-Tests, um differenziertere Erkenntnisse zu gewinnen."
        )
    ),
    Antwortoption(
        text='Gelegentliche Nutzerbefragungen',
        punkte=2,
        bewertung="Ausreichend – mit Schwächen",
        begruendung=(
            "Die UUX-Bewertung ist nur rudimentär vorhanden und kann einseitige Ergebnisse liefern. "
            "Wichtige Aspekte des Nutzererlebnisses könnten übersehen werden."
        ),
        verbesserungpotential=(
            "Führen Sie regelmäßig standardisierte Methoden durch, um konsistente und umfassendere Erkenntnisse zu erhalten."
        )
    ),
    Antwortoption(
        text='Keine spezifischen Methoden',
        punkte=0,
        bewertung="Ungenügend – nicht zertifizierungsfähig",
        begruendung=(
            "Es werden keine systematischen Verfahren eingesetzt, um die User Experience zu beurteilen. "
            "Das Risiko, wichtige Usability-Probleme zu übersehen, ist hoch."
        ),
        verbesserungpotential=(
            "Ohne Methoden fehlen Grundlagen für eine fundierte UUX-Bewertung. Starten Sie mit einfachen Methoden wie Usability-Tests oder Nutzerbefragungen, um erste Erkenntnisse zu gewinnen."
        )
    )
]


all_evaluation_response_lists = [
    evaluation_response_q1,
    evaluation_response_q2,
    evaluation_response_q3
]

evaluation_rating_metrik = [
    {"bewertung": option.bewertung, "inhalt": option.text}
    for antwortliste in all_evaluation_response_lists
    for option in antwortliste
]

evaluation_rating_metrik_with_help = [
    {
        "bewertung": option.bewertung,
        "inhalt": option.text,
        "begruendung": option.begruendung,
        "verbesserungpotential": option.verbesserungpotential
    }
    for antwortliste in all_evaluation_response_lists
    for option in antwortliste
]

evaluation_response_text_options = [
    [option.text for option in evaluation_response_q1],
    [option.text for option in evaluation_response_q2],
    [option.text for option in evaluation_response_q3]
]
