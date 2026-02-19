from agents.rating_agent import Antwortoption

understanding_summary = """Die Phase Verstehen beinhaltet die systematische Untersuchung von Nutzungskontext, Nutzerverhalten 
                      und Zielen. Ziel ist es, fundierte Erkenntnisse über die Bedürfnisse der Nutzer zu gewinnen, um daraus 
                      Anforderungen und Gestaltungsansätze abzuleiten."""

understanding_questions = [  'Wie führen Sie Nutzerforschung entlang des Produktentwicklungsprozess durch, um Ihre Zielgruppe und deren Bedürfnisse zu verstehen?',
                             'Wie definieren und dokumentieren Sie Ihre Nutzergruppen?',
                             'Welche Methoden werden insgesamt zur Analyse der Nutzenden angewendet?',
                             'Wie werden die Ergebnisse in den Produktentwicklungsprozess integriert?']

understanding_examples = [
    'User Research wird systematisch und regelmäßig durchgeführt, mit relevanten Zielgruppen, Nutzungskontextanalyse zu Beginn, Usability-Tests im Projektverlauf und expliziter Berücksichtigung von Menschen mit Beeinträchtigungen.',
    'Die Nutzergruppen werden aus der grundsätzlichen Zielgruppe abgeleitet und anhand mehrerer relevanter Variablen differenziert, z. B. Bedürfnisse, Vorerfahrungen oder Barrierefreiheit. Auch spezielle Zielgruppen („special interests“) und deren Bedürfnisse werden berücksichtigt. Für spezifische Anwendungsfälle oder Zielgruppen werden gezielt Personas erstellt.',
    'Nutzerinterviews, User Journeys, Personas, Generierung von Szenarien, Nutzungskontextanalyse, Fokusgruppen, Rollenkonzepte, Nutzerbefragung',
    'Die Ergebnisse werden systematisch in den Produktentwicklungsprozess integriert, wobei Empfehlungen für UX und Produktumfang abgeleitet werden. Relevante Rahmenbedingungen fließen in die Priorisierung ein, und für jeden Feedbackkanal existiert ein standardisierter Prozess zur Integration des Feedbacks.'
]

understanding_response_q1 = [
    Antwortoption(
        text='Nutzergruppen klar definiert, dokumentiert und differenziert nach relevanten Variablen; spezielle Personas für besondere Zielgruppen erstellt',
        punkte=2,
        bewertung="Sehr gut",
        begruendung=(
            "Die Nutzergruppen sind umfassend definiert und dokumentiert, einschließlich relevanter Variablen wie "
            "Bedürfnisse, Vorerfahrungen, Einschränkungen (Barrierefreiheit) und special interests. "
            "Spezifische Personas für besondere Zielgruppen gewährleisten zielgerichtete Umsetzung in Design und Entwicklung."
        ),
        verbesserungpotential=(
            "Überprüfen Sie regelmäßig, ob die Definitionen aktuell sind, insbesondere bei neuen Zielgruppen oder geänderten Anforderungen."
        )
    ),
    Antwortoption(
        text='Nutzergruppen definiert, aber nur teilweise dokumentiert oder differenziert; wenige spezifische Personas vorhanden',
        punkte=1,
        bewertung="Ausreichend – mit Schwächen",
        begruendung=(
            "Es liegt eine Grunddefinition der Nutzergruppen vor, jedoch fehlt eine systematische Differenzierung "
            "nach relevanten Variablen oder spezifische Personas werden nur eingeschränkt verwendet."
        ),
        verbesserungpotential=(
            "Ergänzen Sie die Dokumentation und Differenzierung der Nutzergruppen und erstellen Sie gezielt Personas für besondere Zielgruppen."
        )
    ),
    Antwortoption(
        text='Nutzergruppen nicht klar definiert oder dokumentiert; keine Differenzierung oder Personas',
        punkte=0,
        bewertung="Ungenügend – nicht zertifizierungsfähig",
        begruendung=(
            "Fehlende Definition und Dokumentation der Nutzergruppen bedeutet, dass Entscheidungen im Produktdesign "
            "nicht ausreichend nutzerzentriert getroffen werden können."
        ),
        verbesserungpotential=(
            "Definieren und dokumentieren Sie alle relevanten Nutzergruppen anhand klarer Variablen und entwickeln Sie Personas, "
            "um Design und Entwicklung zielgerichtet zu unterstützen."
        )
    )
]

understanding_response_q2 = [
    Antwortoption(
        text='Systematisch und umfassend',
        punkte=4,
        bewertung="Sehr gut",
        begruendung=(
            "Die Nutzerforschung wird konsequent entlang des gesamten Produktentwicklungsprozesses durchgeführt. "
            "Zielgruppen, Nutzungskontexte und Barrierefreiheit werden klar definiert und kontinuierlich überprüft. "
            "Ergebnisse fließen aktiv in die Produktgestaltung ein."
        ),
        verbesserungpotential=(
            "Überprüfen Sie regelmäßig, ob neue Zielgruppen oder Nutzungsszenarien berücksichtigt werden und dokumentieren Sie die Auswirkungen auf Entscheidungen."
        )
    ),
    Antwortoption(
        text='Strukturiert, aber teilweise lückenhaft',
        punkte=3,
        bewertung="Gut",
        begruendung=(
            "Nutzerforschung erfolgt methodisch, jedoch nicht in allen Phasen oder für alle relevanten Zielgruppen. "
            "Einige Aspekte, wie Barrierefreiheit oder Nutzungskontexte, werden nur teilweise berücksichtigt."
        ),
        verbesserungpotential=(
            "Erweitern Sie die Nutzerforschung auf alle Projektphasen und stellen Sie sicher, dass sämtliche Zielgruppen systematisch einbezogen werden."
        )
    ),
    Antwortoption(
        text='Gelegentlich und unsystematisch',
        punkte=2,
        bewertung="Ausreichend – mit Schwächen",
        begruendung=(
            "Nutzerforschung findet sporadisch statt, oft reaktiv oder nur bei offensichtlichen Problemen. "
            "Methoden wie Usability-Tests werden nicht konsequent durchgeführt, und Barrierefreiheit bleibt meist unberücksichtigt."
        ),
        verbesserungpotential=(
            "Integrieren Sie standardisierte Methoden (Interviews, Beobachtungen, Usability-Tests) systematisch in den Entwicklungsprozess."
        )
    ),
    Antwortoption(
        text='Selten und unstrukturiert',
        punkte=1,
        bewertung="Ungenügend – nicht zertifizierungsfähig",
        begruendung=(
            "Nutzerforschung findet nur punktuell statt und ist nicht in den Prozess eingebettet. "
            "Wichtige Erkenntnisse über Zielgruppen, Nutzungskontexte oder Barrierefreiheit fehlen."
        ),
        verbesserungpotential=(
            "Etablieren Sie ein regelmäßiges, methodisches Vorgehen mit klar definierten Zielgruppen, Nutzungsszenarien und Tests."
        )
    ),
    Antwortoption(
        text='Keine Nutzerforschung',
        punkte=0,
        bewertung="Ungenügend – nicht zertifizierungsfähig",
        begruendung=(
            "Es wird keine Nutzerforschung durchgeführt, wodurch keine validen Erkenntnisse über Zielgruppen oder Nutzungskontexte vorliegen. "
            "Barrierefreiheit und Usability werden nicht berücksichtigt."
        ),
        verbesserungpotential=(
            "Starten Sie mit grundlegenden Methoden wie Nutzerinterviews oder Beobachtungen und bauen Sie diese Schritt für Schritt systematisch aus."
        )
    )
]

understanding_response_q3 = [
    Antwortoption(
        text='5–6 Methoden aus den Methoden Nutzerinterviews, User Journeys, Personas, Generierung von Szenarien, Nutzungskontextanalyse, Fokusgruppen oder weitere Methoden wurden genannt.',
        hinweis='Die Methoden Nutzerinterviews, User Journeys, Personas, Generierung von Szenarien, Nutzungskontextanalyse, Fokusgruppen sind von besonderer Bedeutung.',
        punkte=4,
        bewertung="Sehr gut",
        begruendung=(
            "Die Nutzung vielfältiger Methoden zur Nutzeranalyse zeigt ein hohes methodisches Reifegradniveau. "
            "Unterschiedliche Perspektiven auf die Nutzenden ermöglichen fundierte Entscheidungen in der Produktentwicklung."
        ),
        verbesserungpotential=(
            "Achten Sie darauf, die Methoden situations- und projektgerecht auszuwählen und die Ergebnisse systematisch weiterzuverarbeiten."
        )
    ),
    Antwortoption(
        text='3–4 Methoden aus den Methoden Nutzerinterviews, User Journeys, Personas, Generierung von Szenarien, Nutzungskontextanalyse, Fokusgruppen oder weitere Methoden wurden genannt.',
        hinweis='Die Methoden Nutzerinterviews, User Journeys, Personas, Generierung von Szenarien, Nutzungskontextanalyse, Fokusgruppen sind für die Phase Verstehen von besonderer Bedeutung.',
        punkte=3,
        bewertung="Gut",
        begruendung=(
            "Es werden mehrere etablierte Methoden eingesetzt, was auf ein gutes Verständnis der Nutzeranalyse hinweist. "
            "Potenzial besteht in der Ausweitung auf weitere Perspektiven oder Anwendungsbereiche."
        ),
        verbesserungpotential=(
            "Ergänzen Sie die vorhandenen Methoden bei Bedarf um zusätzliche qualitative oder kontextbezogene Ansätze."
        )
    ),
    Antwortoption(
        text='2 Methoden aus den Methoden Nutzerinterviews, User Journeys, Personas, Generierung von Szenarien, Nutzungskontextanalyse, Fokusgruppen oder weitere Methoden wurden genannt.',
        hinweis='Die Methoden Nutzerinterviews, User Journeys, Personas, Generierung von Szenarien, Nutzungskontextanalyse, Fokusgruppen sind für die Phase Verstehen von besonderer Bedeutung.',
        punkte=2,
        bewertung="Ausreichend – mit Schwächen",
        begruendung=(
            "Die Nutzeranalyse ist vorhanden, aber in ihrer Vielfalt begrenzt. "
            "Dies kann zu einseitigen Ergebnissen führen, die nicht alle Nutzungsszenarien abdecken."
        ),
        verbesserungpotential=(
            "Prüfen Sie, ob weitere Methoden sinnvoll ergänzt werden können, um ein umfassenderes Bild der Nutzerbedürfnisse zu erhalten."
        )
    ),
    Antwortoption(
        text='1 Methode aus den Methoden Nutzerinterviews, User Journeys, Personas, Generierung von Szenarien, Nutzungskontextanalyse, Fokusgruppen oder weitere Methoden wurden genannt.',
        hinweis='Die Methoden Nutzerinterviews, User Journeys, Personas, Generierung von Szenarien, Nutzungskontextanalyse, Fokusgruppen sind für die Phase Verstehen von besonderer Bedeutung.',
        punkte=1,
        bewertung="Ungenügend – nicht zertifizierungsfähig",
        begruendung=(
            "Der Einsatz nur einer Methode ist unzureichend, um komplexe Nutzerbedürfnisse zu erfassen. "
            "Es besteht das Risiko, wichtige Erkenntnisse zu übersehen."
        ),
        verbesserungpotential=(
            "Nutzen Sie ergänzende Methoden wie Interviews, Szenarien oder Fokusgruppen, um verschiedene Perspektiven einzubeziehen."
        )
    ),
    Antwortoption(
        text='Keine Methode aus den Methoden Nutzerinterviews, User Journeys, Personas, Generierung von Szenarien, Nutzungskontextanalyse, Fokusgruppen',
        hinweis='Die Methoden Nutzerinterviews, User Journeys, Personas, Generierung von Szenarien, Nutzungskontextanalyse, Fokusgruppen sind für die Phase Verstehen von besonderer Bedeutung.',
        punkte=0,
        bewertung="Ungenügend – nicht zertifizierungsfähig",
        begruendung=(
            "Ohne systematische Analyse der Nutzenden fehlt die Grundlage für nutzerzentrierte Entwicklung. "
            "Das stellt ein erhebliches Risiko für die Produktqualität dar."
        ),
        verbesserungpotential=(
            "Beginnen Sie mit einfachen, leicht umsetzbaren Methoden wie Nutzerinterviews oder Personas, "
            "um ein erstes Bild der Zielgruppe zu gewinnen."
        )
    )
]


understanding_response_q4 = [
    Antwortoption(
        text='Zur direkten Beeinflussung von Design und Entwicklung',
        punkte=2,
        bewertung="Sehr gut",
        begruendung=(
            "Die systematische Nutzung von Ergebnissen aus der Anwenderanalyse zur Steuerung von Design und Entwicklung "
            "zeigt eine hohe Reife im Umgang mit Nutzerfeedback."
        ),
        verbesserungpotential=(
            "Sichern Sie ab, dass diese Praxis über alle Projekte hinweg konsequent angewendet wird."
        )
    ),
    Antwortoption(
        text='Als allgemeine Orientierung',
        punkte=1,
        bewertung="Ausreichend – mit Schwächen",
        begruendung=(
            "Die Nutzung der Ergebnisse ist vorhanden, aber nicht zielgerichtet genug, um konkrete Auswirkungen "
            "auf Designentscheidungen sicherzustellen."
        ),
        verbesserungpotential=(
            "Fördern Sie die konkrete Umsetzung von Erkenntnissen in Gestaltungsentscheidungen und Entwicklungsprozesse."
        )
    ),
    Antwortoption(
        text='Werden nicht systematisch verwendet',
        punkte=0,
        bewertung="Ungenügend – nicht zertifizierungsfähig",
        begruendung=(
            "Fehlende systematische Nutzung von Anwenderanalysen bedeutet, dass wertvolle Erkenntnisse ungenutzt bleiben "
            "und Entscheidungen nicht ausreichend nutzerbasiert getroffen werden."
        ),
        verbesserungpotential=(
            "Entwickeln Sie Prozesse, um Nutzeranalysen auszuwerten und deren Ergebnisse gezielt in Design und Entwicklung zu integrieren."
        )
    )
]


all_response_list = [
    understanding_response_q1,
    understanding_response_q2,
    understanding_response_q3,
    understanding_response_q4
]

understanding_rating_metrik = [
    {"bewertung": option.bewertung, "inhalt": option.text}
    for response in all_response_list
    for option in response
]

organzing_rating_metrik_with_help = [
    {"bewertung": option.bewertung, "inhalt": option.text, "begrundung": option.begruendung, "verbesserungspotential": option.verbesserungpotential}
    for antwortliste in all_response_list
    for option in antwortliste
]


understanding_response_text_options = [
    [option.text for option in response] for response in all_response_list
]