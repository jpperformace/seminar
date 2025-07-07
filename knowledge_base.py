import asyncio
import json
import logging
import os
from datetime import datetime, timezone
from logging import INFO

from dotenv import load_dotenv

from insert_docs import load_markdown_files_from_folder, smart_chunk_markdown, extract_section_info, print_chunk_info

load_dotenv()

from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
from graphiti_core.search.search_config_recipes import NODE_HYBRID_SEARCH_RRF

#################################################
# CONFIGURATION
#################################################
# Set up logging and environment variables for
# connecting to Neo4j database
#################################################

# Configure logging
logging.basicConfig(
    level=INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger = logging.getLogger(__name__)

# Neo4j connection parameters
# Make sure Neo4j Desktop is running with a local DBMS started
neo4j_uri = os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
neo4j_user = os.environ.get('NEO4J_USER', 'neo4j')
neo4j_password = os.environ.get('NEO4J_PASSWORD', 'password')

if not neo4j_uri or not neo4j_user or not neo4j_password:
    raise ValueError('NEO4J_URI, NEO4J_USER, and NEO4J_PASSWORD must be set')


async def main():
    #################################################
    # INITIALIZATION
    #################################################
    # Connect to Neo4j and set up Graphiti indices
    # This is required before using other Graphiti
    # functionality
    #################################################

    # Initialize Graphiti with Neo4j connection
    graphiti = Graphiti(neo4j_uri, neo4j_user, neo4j_password)

    try:


        #################################################
        # BASIC SEARCH
        #################################################
        # The simplest way to retrieve relationships (edges)
        # from Graphiti is using the search method, which
        # performs a hybrid search combining semantic
        # similarity and BM25 text retrieval.
        #################################################

        # Perform a hybrid search combining semantic similarity and BM25 retrieval
        print("\nSearching for: 'Welche Methoden brauchen weniger als 30 Minuten?'")
        results = await graphiti.search('Welche Methoden brauchen weniger als 30 Minuten?')

        # Print search results
        print('\nSearch Results:')
        for result in results:
            print(f'UUID: {result.uuid}')
            print(f'Fact: {result.fact}')
            if hasattr(result, 'valid_at') and result.valid_at:
                print(f'Valid from: {result.valid_at}')
            if hasattr(result, 'invalid_at') and result.invalid_at:
                print(f'Valid until: {result.invalid_at}')
            print('---')

    finally:
        #################################################
        # CLEANUP
        #################################################
        # Always close the connection to Neo4j when
        # finished to properly release resources
        #################################################

        # Close the connection
        await graphiti.close()
        print('\nConnection closed')

async def initialize_and_add_episodes(graphiti, folder_path="markdown_files"):
    # Initialize the graph database with graphiti's indices. This only needs to be done once.
    await graphiti.build_indices_and_constraints()

    #################################################
    # ADDING EPISODES
    #################################################
    # Episodes are the primary units of information
    # in Graphiti. They can be text or structured JSON
    # and are automatically processed to extract entities
    # and relationships.
    #################################################

    md_files = load_markdown_files_from_folder("markdown_files")

    if not md_files:
        print("Keine Markdown-Dateien im angegebenen Ordner gefunden.")
    # Chunk and collect metadata
    ids, documents, metadatas = [], [], []
    chunk_idx = 0

    for doc in md_files:
        md = doc["markdown"]
        chunks = smart_chunk_markdown(md, max_len=1000)

        for chunk_text, headers in chunks:
            meta = extract_section_info(chunk_text, headers)

            meta["chunk_index"] = chunk_idx
            meta["source"] = doc["filename"]

            ids.append(f"chunk-{chunk_idx}")
            chunk_idx += 1

            metadata_text = json.dumps(meta, indent=2)
            chunk_with_meta = f"---\n{metadata_text}\n---\n\n{chunk_text}"

            await graphiti.add_episode(
                name= "Chunk:" + str(meta["chunk_index"]) + ' ' + meta["headers"],
                episode_body=chunk_with_meta,
                source_description=meta["headers"],
                reference_time=datetime.now(),
                source=EpisodeType.message,
                group_id='',
            )

if __name__ == '__main__':
    asyncio.run(main())