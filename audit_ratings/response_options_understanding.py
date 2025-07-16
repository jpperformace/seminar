from agents.quantitative_rating_agent import Antwortoption

understanding_question_1 = [
    Antwortoption(
        text='Immer',
        punkte=4,
        bewertung="Sehr gut",
        begruendung=(
            "Regelmäßige und kontinuierliche Nutzerforschung zeigt ein tiefes Verständnis für die Zielgruppe "
            "und ermöglicht eine konsistente Ausrichtung der Entwicklung an den tatsächlichen Bedürfnissen der Nutzer."
        ),
        verbesserungpotential=(
            "Stellen Sie sicher, dass die gewonnenen Erkenntnisse in allen Entwicklungsphasen systematisch berücksichtigt werden."
        )
    ),
    Antwortoption(
        text='Oft',
        punkte=3,
        bewertung="Gut",
        begruendung=(
            "Häufige Nutzerforschung ist ein gutes Zeichen für gelebte Nutzerzentrierung, könnte aber noch systematischer "
            "oder umfassender erfolgen."
        ),
        verbesserungpotential=(
            "Prüfen Sie, ob alle relevanten Nutzungskontexte und Zielgruppen regelmäßig einbezogen werden."
        )
    ),
    Antwortoption(
        text='Gelegentlich',
        punkte=2,
        bewertung="Ausreichend – mit Schwächen",
        begruendung=(
            "Gelegentliche Nutzerforschung zeigt, dass das Thema bekannt ist, aber noch nicht systematisch verankert wurde."
        ),
        verbesserungpotential=(
            "Integrieren Sie Nutzerforschung als festen Bestandteil im Entwicklungsprozess – idealerweise zu mehreren Zeitpunkten."
        )
    ),
    Antwortoption(
        text='Selten',
        punkte=1,
        bewertung="Ungenügend – nicht zertifizierungsfähig",
        begruendung=(
            "Seltene Nutzerforschung deutet darauf hin, dass Nutzerbedürfnisse nur am Rande berücksichtigt werden."
        ),
        verbesserungpotential=(
            "Etablieren Sie feste Prozesse für Nutzerforschung, um fundierte Entscheidungen treffen zu können."
        )
    ),
    Antwortoption(
        text='Nie',
        punkte=0,
        bewertung="Ungenügend – nicht zertifizierungsfähig",
        begruendung=(
            "Ohne Nutzerforschung fehlt die Grundlage, um nutzerzentrierte Produkte zu entwickeln. Dies stellt ein erhebliches Risiko dar."
        ),
        verbesserungpotential=(
            "Starten Sie mit ersten, einfachen Methoden der Nutzerforschung (z. B. Interviews, Beobachtungen), um ein Grundverständnis zu entwickeln."
        )
    )
]


understanding_question_2 = [
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

understanding_methods_analysis_question = [
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