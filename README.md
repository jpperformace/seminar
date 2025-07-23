# KI-Assistent für Siegel "Nutzerzentritert Entwickelt"

Ein intelligenter Retrieval-Augmented-Generation-(RAG)-Agent zur semantischen Durchsuchung von Word-basierten Dokumentationen.  
Das System basiert auf **Pydantic AI** und nutzt eine Kombination aus Word-zu-Markdown-Konvertierung, hierarchischem Chunking und semantischer Vektorsuche mit **ChromaDB**.  
Die Interaktion mit dem System erfolgt über ein benutzerfreundliches **Streamlit-Interface**.

---

## Hintergrund

Ursprünglich wurde das Projekt aus dem Repository [ottomator-agents](https://github.com/coleam00/ottomator-agents/tree/main/crawl4AI-agent-v2) geklont und sollte Webdokumentationen automatisiert crawlen und verarbeiten.  
Aufgrund von Einschränkungen bei der Verarbeitung von WordPress-Websites (z. B. Inhalte hinter Popups oder dynamisch geladene Elemente) wurde der Web-Crawling-Ansatz verworfen.  

Stattdessen basiert das System nun vollständig auf **lokal gespeicherten Word-Dokumenten**.

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
python convert_docx.py <input_folder> [-v]
```

#### Beispiel:

```bash
python convert_docx.py word_documents
```

### 2. Chunking und Vektor-Datenbank

Die erzeugten Markdown-Dateien werden mit dem Tool `insert_docs.py`:

- hierarchisch nach Überschriftenebenen (H1–H4) in sinnvolle semantische Chunks zerlegt,  
- mit Metadaten versehen (z. B. Dokumentname, Pfad, Heading-Struktur),  
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


## Prerequisites

- Python 3.11+
- OpenAI API key (for embeddings and LLM-powered search)
- Crawl4AI/Playwright and other dependencies in `requirements.txt`
- (Optional) Streamlit for the web interface

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/coleam00/ottomator-agents.git
   cd ottomator-agents/crawl4AI-agent-v2
   ```

2. **Install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   playwright install
   ```

3. **Set up environment variables:**
   - Copy `.env.example` to `.env`
   - Edit `.env` with your API keys and preferences:
     ```env
     OPENAI_API_KEY=your_openai_api_key
     MODEL_CHOICE=gpt-4.1-mini  # or your preferred OpenAI model
     ```

---

## Usage

### 1. Crawling and Inserting Documentation

The main entry point for crawling and vectorizing documentation is [`insert_docs.py`](insert_docs.py):

#### Supported URL Types

- **Regular documentation sites:** Recursively crawls all internal links, deduplicates by URL (ignoring fragments).
- **Markdown or .txt pages (such as llms.txt):** Fetches and chunks Markdown content.
- **Sitemaps (`sitemap.xml`):** Batch-crawls all URLs listed in the sitemap.

#### Example Usage

```bash
python insert_docs.py <URL> [--collection mydocs] [--db-dir ./chroma_db] [--embedding-model all-MiniLM-L6-v2] [--chunk-size 1000] [--max-depth 3] [--max-concurrent 10] [--batch-size 100]
```

**Arguments:**
- `URL`: The root URL, .txt file, or sitemap to crawl.
- `--collection`: ChromaDB collection name (default: `docs`)
- `--db-dir`: Directory for ChromaDB data (default: `./chroma_db`)
- `--embedding-model`: Embedding model for vector storage (default: `all-MiniLM-L6-v2`)
- `--chunk-size`: Maximum characters per chunk (default: `1000`)
- `--max-depth`: Recursion depth for regular URLs (default: `3`)
- `--max-concurrent`: Max parallel browser sessions (default: `10`)
- `--batch-size`: Batch size for ChromaDB insertion (default: `100`)

**Examples for each type (regular URL, .txt, sitemap):**
```bash
python insert_docs.py https://ai.pydantic.dev/
python insert_docs.py https://ai.pydantic.dev/llms-full.txt
python insert_docs.py https://ai.pydantic.dev/sitemap.xml
```

#### Chunking Strategy

- Splits content first by `#`, then by `##`, then by `###` headers.
- If a chunk is still too large, splits by character count.
- All chunks are less than the specified `--chunk-size` (default: 1000 characters).

#### Metadata

Each chunk is stored with:
- Source URL
- Chunk index
- Extracted headers
- Character and word counts

---

### 2. Example Scripts

The `crawl4AI-examples/` folder contains modular scripts illustrating different crawling and chunking strategies:

- **`3-crawl_sitemap_in_parallel.py`:** Batch-crawls a list of URLs from a sitemap in parallel with memory tracking.
- **`4-crawl_llms_txt.py`:** Crawls a Markdown or `.txt` file, splits by headers, and prints chunks.
- **`5-crawl_site_recursively.py`:** Recursively crawls all internal links from a root URL, deduplicating by URL (ignoring fragments).

You can use these scripts directly for experimentation or as templates for custom crawlers.

---

### 3. Running the Streamlit RAG Interface

After crawling and inserting docs, launch the Streamlit app for semantic search and question answering:

```bash
streamlit run streamlit_app.py
```

- The interface will be available at [http://localhost:8501](http://localhost:8501)
- Query your documentation using natural language and get context-rich answers.

---

## Project Structure

```
crawl4AI-agent-v2/
├── crawl4AI-examples/
│   ├── 3-crawl_docs_FAST.py
│   ├── 4-crawl_and_chunk_markdown.py
│   └── 5-crawl_recursive_internal_links.py
├── insert_docs.py
├── rag_agent.py
├── streamlit_app.py
├── utils.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## Advanced Usage & Customization

- **Chunking:** Tune `--chunk-size` for your retrieval use case.
- **Embeddings:** Swap out the embedding model with `--embedding-model`.
- **Crawling:** Adjust `--max-depth` and `--max-concurrent` for large sites.
- **Vector DB:** Use your own ChromaDB directory or collection for multiple projects.

---

## Troubleshooting

- Ensure all dependencies are installed and environment variables are set.
- For large sites, increase memory or decrease `--max-concurrent`.
- If you encounter crawling issues, try running the example scripts for isolated debugging.