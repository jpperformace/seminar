"""
insert_docs.py
--------------
Command line tool for reading Markdown files from a local directory,
hierarchical chunking of the content (default <1000 characters per chunk), extracting header metadata
and inserting these chunks including metadata into a ChromaDB collection.

Usage:
    python insert_docs.py <markdown_folder> [--collection ...] [--db-dir ...] [--embedding-model ...] [--chunk-size ...]
"""
import argparse
import os
import sys
import re
import bisect
from typing import List, Dict, Any
from utils import get_chroma_client, get_or_create_collection, add_documents_to_collection
from typing import List, Tuple, Dict

def smart_chunk_markdown(markdown: str, max_len: int = 1500) -> List[Tuple[str, Dict[str, str]]]:
    if markdown == '' or not markdown:
        return []

    """Split hierarchically and return header context for each chunk.."""
    def split_by_header(md, header_pattern, indices_list):
        indices = [m.start() for m in re.finditer(header_pattern, md, re.MULTILINE)]

        print("_______________________________")
        print(header_pattern)
        print(indices_list)
        print(indices)
        if not indices:
            return [md], indices_list
        for idx in indices:
            bisect.insort(indices_list, idx)

        print("neue Liste")
        print(indices_list)
        result = [md[indices_list[i]:indices_list[i+1]].strip() for i in range(len(indices_list)-1) if md[indices_list[i]:indices_list[i+1]].strip()]


        return result, indices_list

    """Find last punctuation mark to split sematically well."""
    def find_nearest_sentence_end(text: str, max_l: int) -> int:
        sentence_endings = [m.end() for m in re.finditer(r'[.!?](?:\s|$)', text)]
        candidates = [idx for idx in sentence_endings if idx <= max_l]

        if candidates:
            return candidates[-1]
        else:
            return max_l

    chunks_with_meta = []

    h1_chunks, h1_header_indices = split_by_header(markdown, r'^# .+', [len(markdown)])

    next_h1_block_start = 0
    next_h2_block_start = 0
    next_h3_block_start = 0

    for h1_idx, h1_block in enumerate(h1_chunks):
        lines = h1_block.split('\n')
        h1_headers = [line.strip() for line in lines if re.match(r'^# .+', line)]
        h1_title = h1_headers[0].lstrip("#").strip() if h1_headers else None

        print("H1")
        print(h1_header_indices)

        h2_chunks, h2_header_indices = split_by_header(h1_block, r'^## .+', [0, h1_header_indices[h1_idx + 1] - h1_header_indices[h1_idx]])
        for h2_idx, h2_block in enumerate(h2_chunks):
            lines = h2_block.split('\n')
            h2_headers = [line.strip() for line in lines if re.match(r'^## .+', line)]
            h2_title = h2_headers[0].lstrip("##").strip() if h2_headers else None

            h3_chunks, h3_header_indices = split_by_header(h2_block, r'^### .+', [0, h2_header_indices[h2_idx + 1] - h2_header_indices[h2_idx]])

            for h3_idx, h3_block in enumerate(h3_chunks):
                lines = h3_block.split('\n')
                h3_headers = [line.strip() for line in lines if re.match(r'^### .+', line)]

                h3_title = h3_headers[0].lstrip("###").strip() if h3_headers else None

                h4_chunks, h4_header_indices = split_by_header(h3_block, r'^#### .+', [0, h3_header_indices[h3_idx + 1] - h3_header_indices[h3_idx]])

                for h4_block in h4_chunks:
                    lines = h4_block.split('\n')
                    h4_headers = [line.strip() for line in lines if re.match(r'^#### .+', line)]
                    h4_title = h4_headers[0].lstrip("####").strip() if h4_headers else None

                    rest_block = h4_block

                    print("---------------block start---------------")
                    print(rest_block)
                    print("---------------block end---------------")

                    while len(rest_block) > max_len:
                        split_ind = find_nearest_sentence_end(rest_block, max_len)

                        chunk = rest_block[0:split_ind].strip()

                        chunks_with_meta.append((
                            chunk,
                            {"h1": h1_title, "h2": h2_title, "h3": h3_title, "h4": h4_title}
                        ))
                        rest_block = rest_block[split_ind:]

                    chunk = rest_block.strip()

                    chunks_with_meta.append((
                        chunk,
                        {"h1": h1_title, "h2": h2_title, "h3": h3_title, "h4": h4_title}
                    ))

    return chunks_with_meta

def extract_section_info(chunk: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """Fügt explizite Header-Metadaten und Basisstatistiken hinzu."""
    return {
        "headers": f'#{headers.get("h1")}, ##{headers.get("h2")}, ####{headers.get("h3")}',
        "char_count": len(chunk),
        "word_count": len(chunk.split())
    }

def load_markdown_files_from_folder(folder_path):
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(".md")]
    results = []
    for f in files:
        file_path = os.path.join(folder_path, f)
        with open(file_path, "r", encoding="utf-8") as file:
            markdown = file.read()
            results.append({
                "filename": f,
                "path": file_path,
                "markdown": markdown
            })
    return results

def main():
    parser = argparse.ArgumentParser(description="Insert local Markdown files into ChromaDB")
    parser.add_argument("folder", help="Folder containing Markdown files")
    parser.add_argument("--collection", default="docs", help="ChromaDB collection name")
    parser.add_argument("--db-dir", default="./chroma_db", help="ChromaDB directory")
    parser.add_argument("--embedding-model", default="all-MiniLM-L6-v2", help="Embedding model name")
    parser.add_argument("--chunk-size", type=int, default=1500, help="Max chunk size (chars)")
    parser.add_argument("--batch-size", type=int, default=100, help="ChromaDB insert batch size")
    args = parser.parse_args()

    if not os.path.isdir(args.folder):
        print(f"'{args.folder}' ist kein gültiger Ordner.")
        sys.exit(1)

    md_files = load_markdown_files_from_folder(args.folder)

    if not md_files:
        print("Keine Markdown-Dateien im angegebenen Ordner gefunden.")
        sys.exit(1)
    # Chunk and collect metadata
    ids, documents, metadatas = [], [], []
    chunk_idx = 0

    for doc in md_files:
        md = doc["markdown"]
        chunks = smart_chunk_markdown(md, max_len=args.chunk_size)

        for chunk_text, headers in chunks:
            meta = extract_section_info(chunk_text, headers)

            meta["chunk_index"] = chunk_idx
            meta["source"] = doc["filename"]

            ids.append(f"chunk-{chunk_idx}")
            documents.append(chunk_text)

            metadatas.append(meta)
            chunk_idx += 1

            print(chunk_idx)
            print(chunk_text)
            print(meta)
            print('')


    print(f"Inserting {len(documents)} chunks into ChromaDB collection '{args.collection}'...")

    client = get_chroma_client(args.db_dir)
    collection = get_or_create_collection(client, args.collection, embedding_model_name=args.embedding_model)
    add_documents_to_collection(collection, ids, documents, metadatas, batch_size=args.batch_size)

    print(f"Successfully added {len(documents)} chunks to ChromaDB collection '{args.collection}'.")

if __name__ == "__main__":
    main()
