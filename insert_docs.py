"""
insert_docs.py
--------------
Command-line utility to crawl any URL using Crawl4AI, detect content type (sitemap, .txt, or regular page),
use the appropriate crawl method, chunk the resulting Markdown into <1000 character blocks by header hierarchy,
and insert all chunks into ChromaDB with metadata.

Usage:
    python insert_docs.py <URL> [--collection ...] [--db-dir ...] [--embedding-model ...]
"""
import argparse
import os
import sys
import re
import asyncio
from typing import List, Dict, Any
from urllib.parse import urlparse, urldefrag
from xml.etree import ElementTree
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, MemoryAdaptiveDispatcher
import requests
from utils import get_chroma_client, get_or_create_collection, add_documents_to_collection
from typing import List, Tuple, Dict

def smart_chunk_markdown(markdown: str, max_len: int = 1000) -> List[Tuple[str, Dict[str, str]]]:
    """Hierarchisch splitten und Header-Kontext für jeden Chunk zurückgeben."""

    def split_by_header(md: str, pattern: str):
        sections = re.split(f'({pattern})', md, flags=re.MULTILINE)
        grouped = []
        for i in range(1, len(sections), 2):
            header = sections[i].strip()
            body = sections[i+1].strip() if i+1 < len(sections) else ""
            full = f"{header}\n{body}".strip()
            grouped.append((header, full))
        return grouped

    chunks_with_meta = []


    for h1_header, h1_block in split_by_header(markdown, r'^# .+'):
        h1_title = h1_header.lstrip("#").strip()
        for h2_header, h2_block in split_by_header(h1_block, r'^## .+'):
            h2_title = h2_header.lstrip("#").strip()
            for h3_header, h3_block in split_by_header(h2_block, r'^#### .+'):
                h3_title = h3_header.lstrip("#").strip()
                # Split if too long
                if len(h3_block) > max_len:
                    for i in range(0, len(h3_block), max_len):
                        chunks_with_meta.append((
                            h3_block[i:i+max_len].strip(),
                            {"h1": h1_title, "h2": h2_title, "h3": h3_title}
                        ))
                else:
                    chunks_with_meta.append((
                        h3_block.strip(),
                        {"h1": h1_title, "h2": h2_title, "h3": h3_title}
                    ))

    return chunks_with_meta

def is_sitemap(url: str) -> bool:
    return url.endswith('sitemap.xml') or 'sitemap' in urlparse(url).path

def is_txt(url: str) -> bool:
    return url.endswith('.txt')

async def crawl_recursive_internal_links(start_urls, max_depth=3, max_concurrent=10) -> List[Dict[str,Any]]:
    """Recursive crawl using logic from 5-crawl_recursive_internal_links.py. Returns list of dicts with url and markdown."""
    browser_config = BrowserConfig(headless=True, verbose=False)
    run_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, stream=False)
    dispatcher = MemoryAdaptiveDispatcher(
        memory_threshold_percent=70.0,
        check_interval=1.0,
        max_session_permit=max_concurrent
    )

    visited = set()

    def normalize_url(url):
        return urldefrag(url)[0]

    current_urls = set([normalize_url(u) for u in start_urls])
    results_all = []

    async with AsyncWebCrawler(config=browser_config) as crawler:
        for depth in range(max_depth):
            urls_to_crawl = [normalize_url(url) for url in current_urls if normalize_url(url) not in visited]
            if not urls_to_crawl:
                break

            results = await crawler.arun_many(urls=urls_to_crawl, config=run_config, dispatcher=dispatcher)
            next_level_urls = set()

            for result in results:
                norm_url = normalize_url(result.url)
                visited.add(norm_url)

                if result.success and result.markdown:
                    results_all.append({'url': result.url, 'markdown': result.markdown})
                    for link in result.links.get("internal", []):
                        next_url = normalize_url(link["href"])
                        if next_url not in visited:
                            next_level_urls.add(next_url)

            current_urls = next_level_urls

    return results_all

async def crawl_markdown_file(url: str) -> List[Dict[str,Any]]:
    """Crawl a .txt or markdown file using logic from 4-crawl_and_chunk_markdown.py."""
    browser_config = BrowserConfig(headless=True)
    crawl_config = CrawlerRunConfig()

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=url, config=crawl_config)
        if result.success and result.markdown:
            return [{'url': url, 'markdown': result.markdown}]
        else:
            print(f"Failed to crawl {url}: {result.error_message}")
            return []

def parse_sitemap(sitemap_url: str) -> List[str]:
    resp = requests.get(sitemap_url)
    urls = []

    if resp.status_code == 200:
        try:
            tree = ElementTree.fromstring(resp.content)
            urls = [loc.text for loc in tree.findall('.//{*}loc')]
        except Exception as e:
            print(f"Error parsing sitemap XML: {e}")

    return urls

async def crawl_batch(urls: List[str], max_concurrent: int = 10) -> List[Dict[str,Any]]:
    """Batch crawl using logic from 3-crawl_sitemap_in_parallel.py."""
    browser_config = BrowserConfig(headless=True, verbose=False)
    crawl_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, stream=False)
    dispatcher = MemoryAdaptiveDispatcher(
        memory_threshold_percent=70.0,
        check_interval=1.0,
        max_session_permit=max_concurrent
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        results = await crawler.arun_many(urls=urls, config=crawl_config, dispatcher=dispatcher)
        return [{'url': r.url, 'markdown': r.markdown} for r in results if r.success and r.markdown]


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
    parser.add_argument("--chunk-size", type=int, default=1000, help="Max chunk size (chars)")
    parser.add_argument("--max-depth", type=int, default=3, help="Recursion depth for regular URLs")
    parser.add_argument("--max-concurrent", type=int, default=10, help="Max parallel browser sessions")
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
        print(md)
        chunks = smart_chunk_markdown(md, max_len=args.chunk_size)

        for chunk_text, headers in chunks:
            meta = extract_section_info(chunk_text, headers)

            print(chunk_idx)

            print(chunk_text)
            print("")

            meta["chunk_index"] = chunk_idx
            meta["source"] = doc["filename"]

            ids.append(f"chunk-{chunk_idx}")
            documents.append(chunk_text)
            print(meta)
            metadatas.append(meta)
            chunk_idx += 1

    print(metadatas)
    print(f"Inserting {len(documents)} chunks into ChromaDB collection '{args.collection}'...")

    client = get_chroma_client(args.db_dir)
    collection = get_or_create_collection(client, args.collection, embedding_model_name=args.embedding_model)
    add_documents_to_collection(collection, ids, documents, metadatas, batch_size=args.batch_size)

    print(f"Successfully added {len(documents)} chunks to ChromaDB collection '{args.collection}'.")

if __name__ == "__main__":
    main()
