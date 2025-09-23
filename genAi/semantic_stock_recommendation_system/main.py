import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
from pandas._libs.algos import rank_1d

transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

chroma_client = chromadb.PersistentClient(path="./data/vectorstore")
collection = chroma_client.get_or_create_collection(
    name="nse_companies",
    embedding_function=transformer_ef)

stocks_data = pd.read_csv("./data/stocks.csv")
documents, ids, metadatas = [], [], []

for _, row in stocks_data.iterrows():
    doc_text = f"Company: {row['company']}\nBusiness: {row['description']}"
    documents.append(doc_text)
    ids.append(row['symbol'])
    metadatas.append({
        "symbol": row["symbol"],
        "company": row["company"],
        "description": row["description"][:20],  # short snippet
        "sector": row["sector"],
        "market_cap": row["market_cap"]  
    })

collection.upsert(
    ids=ids,
    documents=documents,
    metadatas=metadatas
)

results = collection.query(
    query_texts='Software companies',
    n_results=5
)

for rank, company_id in enumerate(results['ids'][0], start=1):
    print(f"{rank}: {results['metadatas'][0][rank-1]['company']}")
