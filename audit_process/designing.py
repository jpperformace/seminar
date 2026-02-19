from agents.rating_agent import Antwortoption

designing_summary = """Die Phase Gestalten beschreibt die kreative und iterative Entwicklung von 
                      Lösungsansätzen. Ziel ist es, Ideen in testbare, interaktive Prototypen 
                      zu überführen. Der Fokus liegt dabei auf den Bedürfnissen der Nutzenden 
                      sowie auf einer intuitiven Gestaltung der Benutzeroberfläche."""

designing_questions = [
    'In welchem Umfang nutzen Sie Prototyping im Designprozess?',
    'Wie erfolgt die Einbindung von Designstandards und -richtlinien in ihre Produktentwicklung?',
    'Wie wird die Konsistenz des Designs über verschiedene Produkte bzw. Features hinweg gewährleistet?'
]

designing_examples = [
    'Low- und High-Fidelity-Prototypen (Scribbles, Wireframes, interaktive Figma-Prototypen) werden systematisch eingesetzt, um Konzepte früh zu prüfen, Usability-Tests durchzuführen, die Marktfähigkeit zu bewerten und die Entwicklung vorzubereiten; kontinuierliche Weiterentwicklung auf Basis von Nutzerfeedback.',

    'Ein zentrales Design System mit definierten Komponenten und UX-Writing-Richtlinien sorgt für klare Standards; Bei der Umsetzung von Konzeptideen können Designer auf umfangreiche Design Libraries und Tokens zurückgreifen; Accessibility wird berücksichtigt; Design-Team übernimmt die Qualitätssicherung (Governance ) des Design-Systems; verbindliche Nutzung in Figma sowie Dokumentation und Verlinkung in Confluence und JIRA.',

    'Konsistenz über Produkte und Features hinweg wird durch ein übergreifendes Design System sichergestellt; Figma dient als zentrale Referenz („Single Source of Truth“); strukturierte Abstimmung zwischen Design, Nutzeranforderungen und Entwicklung.'
]

designing_response_q1 = [
    Antwortoption(
        text='Wir erstellen Prototypen für alle neuen Features und Designs.',
        punkte=3,
        bewertung="Sehr gut",
        begruendung=(
            "Prototyping ist vollständig in Ihrem Designprozess verankert. "
            "Durch die konsequente Erstellung von Prototypen werden Ideen frühzeitig visualisiert, "
            "Annahmen überprüft und Risiken reduziert. Dies ermöglicht iteratives Arbeiten und "
            "eine systematische Ausrichtung an den Bedürfnissen der Nutzenden."
        ),
        verbesserungpotential=(
            "Sehr gute Grundlage für eine Zertifizierung. "
            "Achten Sie darauf, Prototypen regelmäßig mit realen Nutzenden zu evaluieren "
            "und Erkenntnisse strukturiert in den Entwicklungsprozess zurückzuführen."
        )
    ),
    Antwortoption(
        text='Prototypen werden für die meisten, aber nicht alle Designs erstellt.',
        punkte=2,
        bewertung="Gut",
        begruendung=(
            "Prototyping ist weitgehend etabliert, wird jedoch nicht durchgängig angewendet. "
            "Dadurch können bei einzelnen Features oder Designentscheidungen "
            "wichtige Validierungsschritte fehlen."
        ),
        verbesserungpotential=(
            "Definieren Sie klare Kriterien, wann Prototyping verpflichtend ist. "
            "Idealerweise wird es als Standardbestandteil jedes Designprozesses "
            "verankert – unabhängig von Komplexität oder Projektgröße."
        )
    ),
    Antwortoption(
        text='Wir erstellen selten Prototypen, meist nur für komplexe Features.',
        punkte=1,
        bewertung="Ausreichend – mit Schwächen",
        begruendung=(
            "Prototyping wird nur selektiv eingesetzt. Dadurch werden viele "
            "Designentscheidungen nicht systematisch überprüft, was das Risiko "
            "für Usability-Probleme im späteren Entwicklungsverlauf erhöht."
        ),
        verbesserungpotential=(
            "Etablieren Sie Prototyping als regelmäßige Praxis im Designprozess – "
            "auch für kleinere oder inkrementelle Änderungen. "
            "Bereits einfache Low-Fidelity-Prototypen können wertvolle Erkenntnisse liefern."
        )
    ),
    Antwortoption(
        text='Wir nutzen kein Prototyping im Designprozess.',
        punkte=0,
        bewertung="Ungenügend – nicht zertifizierungsfähig",
        begruendung=(
            "Ohne Prototyping fehlt ein zentraler Bestandteil nutzerzentrierter "
            "Gestaltung. Designentscheidungen werden nicht iterativ überprüft, "
            "wodurch Fehlentwicklungen häufig erst spät erkannt werden."
        ),
        verbesserungpotential=(
            "Führen Sie schrittweise Prototyping in Ihren Entwicklungsprozess ein. "
            "Beginnen Sie mit einfachen Wireframes oder klickbaren Mockups. "
            "Langfristig sollte Prototyping als verbindlicher Bestandteil "
            "Ihrer Design- und Qualitätsstrategie etabliert werden."
        )
    )
]

designing_response_q2 = [
    Antwortoption(
        text='Wir haben detaillierte Designstandards und -richtlinien, die konsequent in jedem Projekt angewendet werden.',
        punkte=2,
        bewertung="Sehr gut",
        begruendung=(
            "Verbindliche und konsequent angewendete Designstandards gewährleisten "
            "Konsistenz, Wiedererkennbarkeit und eine hohe Usability-Qualität. "
            "Sie reduzieren Interpretationsspielräume, beschleunigen Entwicklungsprozesse "
            "und fördern eine einheitliche User Experience über alle Produkte hinweg."
        ),
        verbesserungpotential=(
            "Sehr gute Grundlage für nachhaltige Qualität. "
            "Stellen Sie sicher, dass die Standards regelmäßig überprüft, "
            "weiterentwickelt und an neue technologische sowie normative Anforderungen "
            "(z. B. Accessibility) angepasst werden."
        )
    ),
    Antwortoption(
        text='Es gibt allgemeine Richtlinien, deren Anwendung variiert oder nicht immer überprüft wird.',
        punkte=1,
        bewertung="Ausreichend – mit Schwächen",
        begruendung=(
            "Grundlegende Richtlinien sind vorhanden, jedoch fehlt eine konsequente "
            "Verbindlichkeit oder Qualitätssicherung. Dadurch kann es zu "
            "Inkonsistenzen im Design und zu Uneinheitlichkeit in der Nutzererfahrung kommen."
        ),
        verbesserungpotential=(
            "Präzisieren Sie bestehende Richtlinien und definieren Sie klare "
            "Verantwortlichkeiten für deren Einhaltung. "
            "Etablieren Sie Review-Prozesse oder Design-Governance-Strukturen, "
            "um eine konsistente Anwendung sicherzustellen."
        )
    ),
    Antwortoption(
        text='Wir haben keine festgelegten Designstandards oder -richtlinien.',
        punkte=0,
        bewertung="Ungenügend – nicht zertifizierungsfähig",
        begruendung=(
            "Ohne definierte Designstandards fehlt eine zentrale Grundlage "
            "für konsistente und qualitativ hochwertige Benutzeroberflächen. "
            "Dies erhöht das Risiko von Inkonsistenzen, Bedienproblemen "
            "und erhöhtem Entwicklungsaufwand."
        ),
        verbesserungpotential=(
            "Entwickeln Sie ein verbindliches Set an Designstandards oder "
            "ein Designsystem, das Komponenten, Interaktionsmuster und "
            "Accessibility-Anforderungen definiert. "
            "Diese Standards sollten dokumentiert, zugänglich und verpflichtend "
            "in allen Projekten angewendet werden."
        )
    )
]

designing_response_q3 = [
    Antwortoption(
        text='Wir nutzen ein zentrales Design-System, das über alle Produkte und Features hinweg angewendet wird, um Konsistenz zu gewährleisten.',
        punkte=2,
        bewertung="Sehr gut",
        begruendung=(
            "Ein zentrales Design-System stellt sicher, dass Komponenten, "
            "Interaktionsmuster und visuelle Elemente einheitlich verwendet werden. "
            "Dies fördert Wiedererkennbarkeit, reduziert Entwicklungsaufwand "
            "und unterstützt eine konsistente User Experience über alle Produkte hinweg."
        ),
        verbesserungpotential=(
            "Sehr gute Grundlage für nachhaltige Designqualität. "
            "Achten Sie darauf, das Design-System regelmäßig zu pflegen, "
            "weiterzuentwickeln und durch Governance-Prozesse sowie "
            "klare Verantwortlichkeiten abzusichern."
        )
    ),
    Antwortoption(
        text='Konsistenz wird fallweise betrachtet, ohne systematischen Ansatz.',
        punkte=1,
        bewertung="Ausreichend – mit Schwächen",
        begruendung=(
            "Designkonsistenz wird berücksichtigt, jedoch fehlt eine "
            "strukturierte und verbindliche Grundlage. Dadurch können "
            "Inkonsistenzen entstehen, die die Usability und das Markenerlebnis beeinträchtigen."
        ),
        verbesserungpotential=(
            "Entwickeln Sie ein verbindliches Design-System oder definieren Sie "
            "klare UI-Guidelines. Ergänzend sollten Review-Prozesse etabliert werden, "
            "um die konsistente Anwendung in allen Projekten sicherzustellen."
        )
    ),
    Antwortoption(
        text='Designkonsistenz ist kein expliziter Fokus in unserer Entwicklung.',
        punkte=0,
        bewertung="Ungenügend – nicht zertifizierungsfähig",
        begruendung=(
            "Ohne expliziten Fokus auf Konsistenz entstehen häufig unterschiedliche "
            "Bedienmuster, visuelle Inkonsistenzen und eine fragmentierte User Experience. "
            "Dies erhöht die kognitive Belastung der Nutzenden und den Wartungsaufwand."
        ),
        verbesserungpotential=(
            "Verankern Sie Designkonsistenz als strategisches Qualitätsziel. "
            "Starten Sie mit der Definition zentraler UI-Standards oder dem Aufbau "
            "eines Design-Systems, das verbindlich in allen Produkten angewendet wird."
        )
    )
]

all_designing_response_lists = [
    designing_response_q1,
    designing_response_q2,
    designing_response_q3
]

designing_rating_metrik = [
    {"bewertung": option.bewertung, "inhalt": option.text}
    for antwortliste in all_designing_response_lists
    for option in antwortliste
]

designing_rating_metrik_with_help = [
    {
        "bewertung": option.bewertung,
        "inhalt": option.text,
        "begruendung": option.begruendung,
        "verbesserungspotential": option.verbesserungspotential
    }
    for antwortliste in all_designing_response_lists
    for option in antwortliste
]

designing_response_text_options = [
    [option.text for option in designing_response_q1],
    [option.text for option in designing_response_q2],
    [option.text for option in designing_response_q3]
]