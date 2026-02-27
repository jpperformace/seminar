#!/bin/sh
set -e

echo "🔄 Konvertiere Word-Dateien zu Markdown..."
python convert_folder.py word_documents

echo "📦 Erstelle Chunks / aktualisiere ChromaDB..."
python insert_docs.py markdown_files

echo "🚀 Starte Streamlit..."
exec streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0