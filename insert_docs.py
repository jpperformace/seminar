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
import bisect
import asyncio
from typing import List, Dict, Any
from urllib.parse import urlparse, urldefrag
from xml.etree import ElementTree
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, MemoryAdaptiveDispatcher
import requests
from utils import get_chroma_client, get_or_create_collection, add_documents_to_collection
from typing import List, Tuple, Dict

def smart_chunk_markdown(markdown: str, max_len: int = 1000) -> List[Tuple[str, Dict[str, str]]]:
    if markdown == '' or not markdown:
        return []

    """Hierarchisch splitten und Header-Kontext für jeden Chunk zurückgeben."""
    def split_by_header(md, header_pattern, indices_list):
        indices = [m.start() for m in re.finditer(header_pattern, md, re.MULTILINE)]
        if not indices:
            return [md], indices_list
        for idx in indices:
            bisect.insort(indices_list, idx)
        result = [md[indices_list[i]:indices_list[i+1]].strip() for i in range(len(indices_list)-1) if md[indices_list[i]:indices_list[i+1]].strip()]
        return result, indices_list

    """Letztes Satzzeichen finden, um sematisch gut zu splitten."""
    def find_nearest_sentence_end(text: str, max_l: int) -> int:
        sentence_endings = [m.end() for m in re.finditer(r'[.!?](?:\s|$)', text)]
        candidates = [idx for idx in sentence_endings if idx <= max_l]

        if candidates:
            return candidates[-1]
        else:
            return max_l

    chunks_with_meta = []

    h1_chunks, header_indices = split_by_header(markdown, r'^# .+', [len(markdown)])

    for h1_block in h1_chunks:
        lines = h1_block.split('\n')
        h1_headers = [line.strip() for line in lines if re.match(r'^# .+', line)]
        h1_title = h1_headers[0].lstrip("#").strip() if h1_headers else None

        h2_chunks, header_indices = split_by_header(h1_block, r'^## .+', header_indices)
        for h2_block in h2_chunks:
            lines = h2_block.split('\n')
            h2_headers = [line.strip() for line in lines if re.match(r'^## .+', line)]
            h2_title = h2_headers[0].lstrip("##").strip() if h2_headers else None

            h3_chunks, header_indices = split_by_header(h2_block, r'^### .+', header_indices)
            for h3_block in h3_chunks:
                lines = h3_block.split('\n')
                h3_headers = [line.strip() for line in lines if re.match(r'^### .+', line)]
                h3_title = h3_headers[0].lstrip("###").strip() if h3_headers else None

                h4_chunks, header_indices = split_by_header(h3_block, r'^#### .+', header_indices)
                for h4_block in h4_chunks:
                    lines = h4_block.split('\n')
                    h4_headers = [line.strip() for line in lines if re.match(r'^#### .+', line)]
                    h4_title = h4_headers[0].lstrip("####").strip() if h4_headers else None

                    rest_block = h4_block

                    while len(rest_block) > max_len:
                        split_ind = find_nearest_sentence_end(rest_block, max_len)

                        chunks_with_meta.append((
                            rest_block[0:split_ind].strip(),
                            {"h1": h1_title, "h2": h2_title, "h3": h3_title, "h4": h4_title}
                        ))
                        rest_block = rest_block[split_ind:]

                    chunks_with_meta.append((
                        rest_block.strip(),
                        {"h1": h1_title, "h2": h2_title, "h3": h3_title, "h4": h4_title}
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
        chunks = smart_chunk_markdown(md, max_len=args.chunk_size)

        print("Chunks")
        print(chunks)

        for chunk_text, headers in chunks:
            meta = extract_section_info(chunk_text, headers)

            print(chunk_idx)
            print(chunk_text)


            meta["chunk_index"] = chunk_idx
            meta["source"] = doc["filename"]

            ids.append(f"chunk-{chunk_idx}")
            documents.append(chunk_text)
            print(meta)
            print("")
            metadatas.append(meta)
            chunk_idx += 1


    print(f"Inserting {len(documents)} chunks into ChromaDB collection '{args.collection}'...")

    client = get_chroma_client(args.db_dir)
    collection = get_or_create_collection(client, args.collection, embedding_model_name=args.embedding_model)
    add_documents_to_collection(collection, ids, documents, metadatas, batch_size=args.batch_size)

    print(f"Successfully added {len(documents)} chunks to ChromaDB collection '{args.collection}'.")

if __name__ == "__main__":
    main()
