from insert_docs import smart_chunk_markdown

def test_single_h1_chunk():
    md = "# Header 1\nThis is some content under H1."
    chunks = smart_chunk_markdown(md, max_len=1000)
    assert len(chunks) == 1
    assert chunks[0][1] == {'h1': 'Header 1', 'h2': None, 'h3': None, 'h4': None}

def test_hierarchical_splitting_creates_all_chunks():
    md = "# H1 Title\nIntro text\n\n## H2 Title\nMore text\n\n### H3 Title\nEven more\n\n#### H4 Title\nDeep content"

    chunks = smart_chunk_markdown(md, max_len=1000)

    assert len(chunks) == 4, "Es sollten 4 Chunks entstehen – jeweils pro Header"

    expected_contents = [
        "# H1 Title\nIntro text",
        "# H1 Title\n## H2 Title\nMore text",
        "# H1 Title\n## H2 Title\n### H3 Title\nEven more",
        "# H1 Title\n## H2 Title\n### H3 Title\n#### H4 Title\nDeep content",
    ]

    expected_titles = [
        {'h1': 'H1 Title', 'h2': None, 'h3': None, 'h4': None},
        {'h1': 'H1 Title', 'h2': 'H2 Title', 'h3': None, 'h4': None},
        {'h1': 'H1 Title', 'h2': 'H2 Title', 'h3': 'H3 Title', 'h4': None},
        {'h1': 'H1 Title', 'h2': 'H2 Title', 'h3': 'H3 Title', 'h4': 'H4 Title'},
    ]

    for i, (chunk_text, chunk_meta) in enumerate(chunks):
        print(chunk_text)
        assert chunk_text == expected_contents[i], (
            f"Inhalt des Chunks {i} stimmt nicht:\n"
            f"Erwartet:\n{expected_contents[i]}\n\nErhalten:\n{chunk_text}"
        )
        assert chunk_meta == expected_titles[i], (
            f"Metadaten des Chunks {i} stimmen nicht:\n"
            f"Erwartet: {expected_titles[i]}\nErhalten: {chunk_meta}"
        )

def test_no_header():
    md = "Just some content without any markdown header."

    chunks = smart_chunk_markdown(md, max_len=1000)

    assert len(chunks) == 1, "Es sollte 1 Chunk entstehen, auch ohne Header"

    expected_content = "Just some content without any markdown header."
    expected_meta = {'h1': None, 'h2': None, 'h3': None, 'h4': None}

    chunk_text, chunk_meta = chunks[0]
    assert chunk_text == expected_content, f"Inhalt stimmt nicht:\nErwartet:\n{expected_content}\nErhalten:\n{chunk_text}"
    assert chunk_meta == expected_meta, f"Metadaten stimmen nicht:\nErwartet: {expected_meta}\nErhalten: {chunk_meta}"


def test_headers_only():
    md = "# H1 Title\n\n## H2 Title\n\n### H3 Title\n\n#### H4 Title"

    chunks = smart_chunk_markdown(md, max_len=1000)

    assert len(chunks) == 4, "Es sollten 4 Chunks entstehen, auch wenn kein Text vorhanden ist"

    expected_contents = [
        "# H1 Title",
        "# H1 Title\n## H2 Title",
        "# H1 Title\n## H2 Title\n### H3 Title",
        "# H1 Title\n## H2 Title\n### H3 Title\n#### H4 Title",
    ]

    expected_titles = [
        {'h1': 'H1 Title', 'h2': None, 'h3': None, 'h4': None},
        {'h1': 'H1 Title', 'h2': 'H2 Title', 'h3': None, 'h4': None},
        {'h1': 'H1 Title', 'h2': 'H2 Title', 'h3': 'H3 Title', 'h4': None},
        {'h1': 'H1 Title', 'h2': 'H2 Title', 'h3': 'H3 Title', 'h4': 'H4 Title'},
    ]

    for i, (chunk_text, chunk_meta) in enumerate(chunks):
        assert chunk_text == expected_contents[i], (
            f"Inhalt des Chunks {i} stimmt nicht:\nErwartet:\n{expected_contents[i]}\nErhalten:\n{chunk_text}"
        )
        assert chunk_meta == expected_titles[i], (
            f"Metadaten des Chunks {i} stimmen nicht:\nErwartet: {expected_titles[i]}\nErhalten: {chunk_meta}"
        )

def test_chunk_split_by_max_length():
    long_text = "A" * 1200
    md = "# H1 Title\n" + long_text

    chunks = smart_chunk_markdown(md, max_len=500)

    assert len(chunks) == 3, "Es sollten 3 Chunks entstehen (1200 Zeichen bei max_len=500)"

    expected_meta = {'h1': 'H1 Title', 'h2': None, 'h3': None, 'h4': None}

    for i, (chunk_text, chunk_meta) in enumerate(chunks):
        assert chunk_meta == expected_meta, (
            f"Metadaten im Chunk {i} stimmen nicht:\nErwartet: {expected_meta}\nErhalten: {chunk_meta}"
        )
        expected_length = 500 if i < 2 else 233
        assert len(chunk_text) == expected_length, (
            f"Chunk {i} hat falsche Länge:\nErwartet: {expected_length}, Erhalten: {len(chunk_text)}"
        )

def test_chunking_splits_at_sentence_end():
    md = "# Einleitung\nDies ist der erste Satz. Hier kommt der zweite Satz. Ein dritter Satz! Und noch ein vierter. Fast Ende? Schließlich ein letzter Satz."

    max_len = 60

    expected_content_1 = "# Einleitung\nDies ist der erste Satz."
    expected_content_2 = "# Einleitung\nHier kommt der zweite Satz. Ein dritter Satz!"
    expected_content_3 = "# Einleitung\nUnd noch ein vierter. Fast Ende?"
    expected_content_4 = "# Einleitung\nSchließlich ein letzter Satz."

    expected_meta = {'h1': 'Einleitung', 'h2': None, 'h3': None, 'h4': None}

    chunks = smart_chunk_markdown(md, max_len=max_len)

    assert len(chunks) == 4, "Es sollten 4 Chunks entstehen (bei max_len=60)"
    assert chunks[0][0] == expected_content_1, f"Inhalt stimmt nicht:\nErwartet:\n{expected_content_1}\nErhalten:\n{chunks[0][0]}"
    assert chunks[1][0] == expected_content_2, f"Inhalt stimmt nicht:\nErwartet:\n{expected_content_2}\nErhalten:\n{chunks[1][0]}"
    assert chunks[2][0] == expected_content_3, f"Inhalt stimmt nicht:\nErwartet:\n{expected_content_3}\nErhalten:\n{chunks[2][0]}"
    assert chunks[3][0] == expected_content_4, f"Inhalt stimmt nicht:\nErwartet:\n{expected_content_4}\nErhalten:\n{chunks[3][0]}"



    for chunk in enumerate(chunks):
        assert chunk[1][1] == expected_meta, (
            f"Metadaten im Chunk {chunk[0]} stimmen nicht:\nErwartet: {expected_meta}\nErhalten: {chunk[1]}"
        )

def test_chunking_with_nested_headers():
    markdown = (
        "# KI\n"
        "Einführung in die Künstliche Intelligenz.\n\n"
        "## Geschichte\n"
        "Die Geschichte der KI begann in den 1950ern mit den ersten Theorien über maschinelles Denken.\n\n"
        "### Turing-Test\n"
        "Ein Konzept von Alan Turing zur Bewertung von Maschinenintelligenz, das bis heute diskutiert wird.\n\n"
        "#### Definition\n"
        "Der Turing-Test prüft, ob eine Maschine menschlich wirkt, indem sie einen Menschen im Gespräch täuscht.\n\n"
        "#### Kritik\n"
        "Der Test misst nur Verhalten, nicht echtes Verstehen oder Bewusstsein der Maschine.\n\n"
        "### Symbolische KI\n"
        "Eine der ersten KI-Methoden, bei der Wissen in logischen Regeln modelliert wird.\n\n"
        "#### Expertensysteme\n"
        "Programme wie MYCIN nutzten Regeln zur medizinischen Diagnose und waren in den 1980ern weit verbreitet.\n\n"
        "## Anwendungen\n"
        "Moderne KI findet Anwendung in vielen Bereichen wie Medizin, Finanzen und Bildung.\n\n"
        "### NLP\n"
        "Verarbeitung natürlicher Sprache durch Maschinen ermöglicht neue Kommunikationsformen.\n\n"
        "#### Chatbots\n"
        "Systeme wie ChatGPT verstehen und erzeugen Sprache, um mit Menschen auf natürliche Weise zu interagieren.\n"
    )

    expected_chunks_with_metadata = [
        ("# KI\nEinführung in die Künstliche Intelligenz.",
         {"h1": "KI", "h2": None, "h3": None, "h4": None}),

        ("# KI\n## Geschichte\nDie Geschichte der KI begann in den 1950ern mit den ersten Theorien über maschinelles Denken.",
         {"h1": "KI", "h2": "Geschichte", "h3": None, "h4": None}),

        ("# KI\n## Geschichte\n### Turing-Test\nEin Konzept von Alan Turing zur Bewertung von Maschinenintelligenz, das bis heute diskutiert wird.",
         {"h1": "KI", "h2": "Geschichte", "h3": "Turing-Test", "h4": None}),

        ("# KI\n## Geschichte\n### Turing-Test\n#### Definition\nDer Turing-Test prüft, ob eine Maschine menschlich wirkt, indem sie einen Menschen im Gespräch täuscht.",
         {"h1": "KI", "h2": "Geschichte", "h3": "Turing-Test", "h4": "Definition"}),

        ("# KI\n## Geschichte\n### Turing-Test\n#### Kritik\nDer Test misst nur Verhalten, nicht echtes Verstehen oder Bewusstsein der Maschine.",
         {"h1": "KI", "h2": "Geschichte", "h3": "Turing-Test", "h4": "Kritik"}),

        ("# KI\n## Geschichte\n### Symbolische KI\nEine der ersten KI-Methoden, bei der Wissen in logischen Regeln modelliert wird.",
         {"h1": "KI", "h2": "Geschichte", "h3": "Symbolische KI", "h4": None}),

        ("# KI\n## Geschichte\n### Symbolische KI\n#### Expertensysteme\nProgramme wie MYCIN nutzten Regeln zur medizinischen Diagnose und waren in den 1980ern weit verbreitet.",
         {"h1": "KI", "h2": "Geschichte", "h3": "Symbolische KI", "h4": "Expertensysteme"}),

        ("# KI\n## Anwendungen\nModerne KI findet Anwendung in vielen Bereichen wie Medizin, Finanzen und Bildung.",
         {"h1": "KI", "h2": "Anwendungen", "h3": None, "h4": None}),

        ("# KI\n## Anwendungen\n### NLP\nVerarbeitung natürlicher Sprache durch Maschinen ermöglicht neue Kommunikationsformen.",
         {"h1": "KI", "h2": "Anwendungen", "h3": "NLP", "h4": None}),

        ("# KI\n## Anwendungen\n### NLP\n#### Chatbots\nSysteme wie ChatGPT verstehen und erzeugen Sprache, um mit Menschen auf natürliche Weise zu interagieren.",
         {"h1": "KI", "h2": "Anwendungen", "h3": "NLP", "h4": "Chatbots"}),
    ]

    chunks_with_metadata = smart_chunk_markdown(markdown, max_len=500)

    assert len(chunks_with_metadata) == 10, "Es sollten insgesamt 10 Chunks entstehen, jeweils pro Überschrift (bei max_len=500)"

    for i, (chunk, meta) in enumerate(chunks_with_metadata):
        expected_chunk, expected_meta = expected_chunks_with_metadata[i]
        assert chunk.strip() == expected_chunk.strip(), f"Chunk {i} stimmt nicht: \n{chunk} \n≠\n {expected_chunk}"
        assert meta == expected_meta, f"Metadaten {i} stimmen nicht: \n{meta} \n≠\n {expected_meta}"


def test_chunking_with_nested_headers_easy():
    markdown = (
        "# H1.1\n"
        "Das ist ein Satz für H1.1.\n\n"
        "## H2.1\n"
        "Das ist ein Satz für H2.1.\n\n"
        "# H1.2\n"
        "Das ist ein Satz für H1.2.\n\n"
        "### H3.2\n"
        "Das ist ein Satz für H3.2.\n\n"
    )

    chunks = smart_chunk_markdown(markdown, max_len=500)

    expected = [
        (
            "# H1.1\nDas ist ein Satz für H1.1.",
            {"h1": "H1.1", "h2": None, "h3": None, "h4": None}
        ),
        (
            "# H1.1\n## H2.1\nDas ist ein Satz für H2.1.",
            {"h1": "H1.1", "h2": "H2.1", "h3": None, "h4": None}
        ),
        (
            "# H1.2\nDas ist ein Satz für H1.2.",
            {"h1": "H1.2", "h2": None, "h3": None, "h4": None}
        ),
        (
            "# H1.2\n### H3.2\nDas ist ein Satz für H3.2.",
            {"h1": "H1.2", "h2": None, "h3": "H3.2", "h4": None}
        ),
    ]

    assert len(chunks) == len(
        expected), f"Es sollten {len(expected)} Chunks entstehen, aber es wurden {len(chunks)} erzeugt."

    for i, ((chunk_text, meta), (expected_text, expected_meta)) in enumerate(zip(chunks, expected)):
        assert chunk_text.strip() == expected_text.strip(), f"Chunk {i} Text stimmt nicht:\n{chunk_text}\n\nErwartet:\n{expected_text}"
        assert meta == expected_meta, f"Chunk {i} Metadaten stimmen nicht:\n{meta}\n\nErwartet:\n{expected_meta}"

def test_empty_markdown_returns_empty_list():
    md = ""

    chunks = smart_chunk_markdown(md, max_len=1000)

    assert chunks == [], "Bei leerem Markdown sollte eine leere Liste zurückgegeben werden"

def test_none_input_returns_empty_list():
    md = None

    chunks = smart_chunk_markdown(md, max_len=1000)

    assert chunks == [], "Bei None als Markdown sollte eine leere Liste zurückgegeben werden"