# KI-Assistent zur Auditsimulation für Siegel "Nutzerzentritert Entwickelt"

Ein intelligenter Retrieval-Augmented-Generation-(RAG)-Agent zur semantischen Durchsuchung von Word-basierten Dokumentationen.  
Das System basiert auf **Pydantic AI** und nutzt eine Kombination aus Word-zu-Markdown-Konvertierung, hierarchischem Chunking und semantischer Vektorsuche mit **ChromaDB**.  
Die Interaktion mit dem System erfolgt über ein benutzerfreundliches **Streamlit-Interface**.

---

## Hintergrund

Ursprünglich wurde das Projekt aus dem Repository [ottomator-agents](https://github.com/coleam00/ottomator-agents/tree/main/crawl4AI-agent-v2) geklont und sollte Webdokumentationen automatisiert crawlen und verarbeiten.  
Aufgrund von Einschränkungen bei der Verarbeitung von WordPress-Websites (z. B. Inhalte hinter Popups oder dynamisch geladene Elemente) wurde der Web-Crawling-Ansatz verworfen.  

Stattdessen basiert das System nun vollständig auf **lokal gespeicherten Word-Dokumenten**.

---

## Voraussetzungen

- Python 3.11+
- OpenAI API key
- Abhängigkeiten von der `requirements.txt` installieren

---

## Installation

1. **Klone das Repository:**
   ```bash
   git clone https://gitlab.kit.edu/kit/win/h-lab/students/thesis/1745_pade_jule.git
   cd 1745_pade_jule/implementation/ai_assistent_seal
   ```

2. **Installiere Abhängigkeiten:**

    Mit venv:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

    Mit Conda:
   ```bash
    conda create -n seal-env python=3.11 -y
    conda activate seal-env
    pip install -r requirements.txt
   ```

3. **Füge die notwenigen Umgebungsvariablen ein:**
   - Kopiere `.env.example` zu `.env`
   - Füge in `.env` deinen API-Key ein und dein präferiertes Modell:
     ```env
     OPENAI_API_KEY=your_openai_api_key
     MODEL_CHOICE=gpt-4.1-mini  # or your preferred OpenAI model
     ```

---

## Funktionsweise

### 1. Word zu Markdown Konvertierung

Die `.docx`-Dateien werden mit dem Skript `convert_docx.py` in semantisch sinnvolles Markdown überführt.

Dabei wird:

- **Mammoth** zur Extraktion von HTML aus Word verwendet,
- der HTML-Inhalt mit **markdownify** in Markdown konvertiert,
- die Ausgaben im Ordner `markdown_files/` gespeichert.

> #### ⚠️ Hinweis vor der Konvertierung in Markdown  
> Beim Konvertieren werden nur `.md`-Dateien **überschrieben**, deren Namen exakt mit einer aktuellen `.docx`-Datei übereinstimmen.  
> Veraltete Markdown-Dateien, für die keine passende `.docx`-Quelle mehr existiert, bleiben im Ordner `markdown_files/` bestehen und müssen **manuell gelöscht** werden.

#### Nutzung:

```bash
python convert_folder.py <input_folder> [-v]
```

#### Beispiel:

```bash
python convert_folder.py word_documents
```

### 2. Chunking und Vektor-Datenbank

Die erzeugten Markdown-Dateien werden mit dem Tool `insert_docs.py`:

- hierarchisch nach Überschriftenebenen (H1–H4) in sinnvolle semantische Chunks zerlegt
  - Teilt den Inhalt zuerst nach #, dann nach ## und schließlich nach ### und #### Überschriften. 
  - Wenn ein Abschnitt immer noch zu groß ist, wird er nach Zeichenanzahl geteilt.
- mit Metadaten versehen (z.B. Dokumentname, Pfad, Heading-Struktur),  
- in eine **ChromaDB**-Vektor-Datenbank eingefügt.

> #### ⚠️ Hinweis vor dem Einfügen in die Vektor-Datenbank
> Bevor neue Daten in die ChromaDB eingefügt werden, sollte die bestehende Datenbank **vollständig gelöscht** werden. So wird sichergestellt, dass keine veralteten oder inkonsistenten Chunks in der Datenbasis verbleiben.
> 
> Die aktuellste Version der Inhalte sollte immer im Ordner `markdown_files/` enthalten sein.  
> Nur diese Version wird zur Erstellung der ChromaDB verwendet.


#### Nutzung:

```bash
python insert_docs.py <markdown_folder> \
    [--collection <collection_name>] \
    [--db-dir <path_to_db>] \
    [--embedding-model <model>] \
    [--chunk-size <int>]
```  

#### Beispiel:

```bash
python insert_docs.py markdown_files
```

### 3. Verwendung des Streamlit-RAG-Interface

Nach der Konvertierung in Markdown und dem Einfügen von Dokumenten starten Sie die Streamlit-App für die Auditsimulation und die Beantwortung von Fragen:
```bash
streamlit run streamlit_app.py
```

- Das Interface wird verfügbar sein unter [http://localhost:8501](http://localhost:8501)
- Fragen Sie Informationen zu Audits zur benutzerorientierten Entwicklung in natürlicher Sprache ab und erhalten Sie kontextreiche Antworten.
