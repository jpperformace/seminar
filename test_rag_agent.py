import asyncio

from agents.rag_agent import run_rag_agent

# ← Importiere aus deinem bestehenden Modul

# === Testkonfiguration ===
QUESTION = "Welche Methoden gibt es in der Phase Organisieren?"
COLLECTION_NAME = "docs"
DB_DIRECTORY = "./chroma_db"  # Passe an, wenn deine DB woanders liegt
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # oder dein eingesetztes Modell
N_RESULTS = 5


async def test_query():
    print(f"\n🔍 Testfrage: {QUESTION}\n")
    result = await run_rag_agent(
        question=QUESTION,
        collection_name=COLLECTION_NAME,
        db_directory=DB_DIRECTORY,
        embedding_model=EMBEDDING_MODEL,
        n_results=N_RESULTS
    )

    print("\n📨 Antwort vom Agent:")
    print(result)


if __name__ == "__main__":
    asyncio.run(test_query())