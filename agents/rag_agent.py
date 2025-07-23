"""Pydantic AI agent that leverages RAG with a local ChromaDB for Pydantic documentation."""

import os
import sys
import argparse
from dataclasses import dataclass

import asyncio
from typing import Optional

import chromadb

import dotenv
from pydantic_ai import RunContext
from pydantic_ai.agent import Agent


# Load environment variables from .env file
dotenv.load_dotenv()

from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType

from utils import (
    get_chroma_client,
    get_or_create_collection,
    query_collection,
    format_results_as_context
)


print("OpenAI API Key:", os.getenv("OPENAI_API_KEY"))

# Check for OpenAI API key
if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY environment variable not set.")
    print("Please create a .env file with your OpenAI API key or set it in your environment.")
    sys.exit(1)


@dataclass
class RAGDeps:
    """Dependencies for the RAG agent."""
    chroma_client: chromadb.PersistentClient
    collection_name: str
    embedding_model: str
    condition: Optional[str] = None


# Create the RAG agent
chat_agent = Agent(
    os.getenv("MODEL_CHOICE", "gpt-4.1-mini"),
    deps_type=RAGDeps,
    system_prompt="You are a helpful assistant that answers questions based on the provided documentation. "
                  "Use the retrieve tool to get relevant information from the documentation before answering. "
                  "If the documentation doesn't contain the answer, clearly state that the information isn't available "
                  "in the current documentation and provide your best general knowledge response."
                  "In addition, always consider any explicitly provided **post-condition** that may constrain or qualify the answer — "
                  "for example, a required negation or exclusion that is not directly reflected in the retrieved context. "
)

@chat_agent.tool
async def retrieve(context: RunContext[RAGDeps], search_query: str, n_results: int = 10) -> str:
    """Retrieve relevant documents from ChromaDB based on a search query.
    
    Args:
        context: The run context containing dependencies.
        search_query: The search query to find relevant documents.
        n_results: Number of results to return (default: 5).
        
    Returns:
        Formatted context information from the retrieved documents.
    """

    # Get ChromaDB client and collection
    collection = get_or_create_collection(
        context.deps.chroma_client,
        context.deps.collection_name,
        embedding_model_name=context.deps.embedding_model
    )

    print("Retrieving documents...")
    print(n_results)
    print(collection)
    print(search_query)
    print(context.deps.condition)

    # Query the collection
    query_results = query_collection(
        collection,
        search_query,
        n_results=n_results
    )

    formatted_context = format_results_as_context(query_results, context.deps.condition)

    print(f"\n=== Retrieved Context ===\n")
    print(formatted_context)
    print("\n=========================\n")

    return formatted_context




    # Format the results as context
    # return format_results_as_context(query_results)


async def run_rag_agent(
    question: str,
    collection_name: str = "docs",
    db_directory: str = "./chroma_db",
    embedding_model: str = "all-MiniLM-L6-v2",
    n_results: int = 5
) -> str:
    """Run the RAG agent to answer a question about Pydantic AI.
    
    Args:
        question: The question to answer.
        collection_name: Name of the ChromaDB collection to use.
        db_directory: Directory where ChromaDB data is stored.
        embedding_model: Name of the embedding model to use.
        n_results: Number of results to return from the retrieval.
        
    Returns:
        The agent's response.
    """
    # Create dependencies
    deps = RAGDeps(
        chroma_client=get_chroma_client(db_directory),
        collection_name=collection_name,
        embedding_model=embedding_model
    )
    print("Running RAG agent...")
    print(question)
    # Run the agent
    result = await chat_agent.run(question, deps=deps)
    
    return result.data


def main():
    """Main function to parse arguments and run the RAG agent."""
    parser = argparse.ArgumentParser(description="Run a Pydantic AI agent with RAG using ChromaDB")
    parser.add_argument("--question", help="The question to answer about Pydantic AI")
    parser.add_argument("--collection", default="docs", help="Name of the ChromaDB collection")
    parser.add_argument("--db-dir", default="./chroma_db", help="Directory where ChromaDB data is stored")
    parser.add_argument("--embedding-model", default="all-MiniLM-L6-v2", help="Name of the embedding model to use")
    parser.add_argument("--n-results", type=int, default=5, help="Number of results to return from the retrieval")
    
    args = parser.parse_args()
    
    # Run the agent
    response = asyncio.run(run_rag_agent(
        args.question,
        collection_name=args.collection,
        db_directory=args.db_dir,
        embedding_model=args.embedding_model,
        n_results=args.n_results
    ))
    
    print("\nResponse:")
    print(response)


if __name__ == "__main__":
    main()
