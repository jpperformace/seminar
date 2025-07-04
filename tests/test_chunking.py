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
        "## H2 Title\nMore text",
        "### H3 Title\nEven more",
        "#### H4 Title\nDeep content",
    ]

    expected_titles = [
        {'h1': 'H1 Title', 'h2': None, 'h3': None, 'h4': None},
        {'h1': 'H1 Title', 'h2': 'H2 Title', 'h3': None, 'h4': None},
        {'h1': 'H1 Title', 'h2': 'H2 Title', 'h3': 'H3 Title', 'h4': None},
        {'h1': 'H1 Title', 'h2': 'H2 Title', 'h3': 'H3 Title', 'h4': 'H4 Title'},
    ]

    for i, (chunk_text, chunk_meta) in enumerate(chunks):
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
        "## H2 Title",
        "### H3 Title",
        "#### H4 Title",
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
        expected_length = 500 if i < 2 else 211
        assert len(chunk_text) == expected_length, (
            f"Chunk {i} hat falsche Länge:\nErwartet: {expected_length}, Erhalten: {len(chunk_text)}"
        )

def test_chunking_splits_at_sentence_end():
    md = "# Einleitung\nDies ist der erste Satz. Hier kommt der zweite Satz. Ein dritter Satz ist nun dabei! Und noch ein vierter. Fast Ende? Schließlich ein letzter Satz."

    max_len = 60

    expected_content_1 = "# Einleitung\nDies ist der erste Satz."
    expected_content_2 = "Hier kommt der zweite Satz. Ein dritter Satz ist nun dabei!"
    expected_content_3 = "Und noch ein vierter. Fast Ende?"
    expected_content_4 = "Schließlich ein letzter Satz."

    expected_meta = {'h1': 'Einleitung', 'h2': None, 'h3': None, 'h4': None}

    chunks = smart_chunk_markdown(md, max_len=max_len)

    assert len(chunks) == 4, "Es sollten 4 Chunks entstehen (1200 Zeichen bei max_len=60)"
    assert chunks[0][0] == expected_content_1, f"Inhalt stimmt nicht:\nErwartet:\n{expected_content_1}\nErhalten:\n{chunks[0][0]}"
    assert chunks[1][0] == expected_content_2, f"Inhalt stimmt nicht:\nErwartet:\n{expected_content_2}\nErhalten:\n{chunks[1][0]}"
    assert chunks[2][0] == expected_content_3, f"Inhalt stimmt nicht:\nErwartet:\n{expected_content_3}\nErhalten:\n{chunks[2][0]}"
    assert chunks[3][0] == expected_content_4, f"Inhalt stimmt nicht:\nErwartet:\n{expected_content_4}\nErhalten:\n{chunks[3][0]}"



    for chunk in enumerate(chunks):
        assert chunk[1][1] == expected_meta, (
            f"Metadaten im Chunk {chunk[0]} stimmen nicht:\nErwartet: {expected_meta}\nErhalten: {chunk[1]}"
        )

def test_empty_markdown_returns_empty_list():
    md = ""

    chunks = smart_chunk_markdown(md, max_len=1000)

    assert chunks == [], "Bei leerem Markdown sollte eine leere Liste zurückgegeben werden"

def test_none_input_returns_empty_list():
    md = None

    chunks = smart_chunk_markdown(md, max_len=1000)

    assert chunks == [], "Bei None als Markdown sollte eine leere Liste zurückgegeben werden"