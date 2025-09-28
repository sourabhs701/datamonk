import pandas as pd
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import LlamaCpp
from langchain_community.vectorstores import Chroma

model_path = "/Users/srb/Downloads/gemma-3-1b-it-IQ4_NL.gguf"

# Load the LLM
llm = LlamaCpp(
    model_path=model_path,
    n_ctx=32768,         # Context window size
    max_tokens=500,      # Max tokens to generate
    seed=42,             # For reproducible results, means ask one question 10 time answer will be somewhat similar.
    verbose=False        # Set to True to see model details
)

print("Gemma model loaded successfully!")


def ingest_stocks_csv_to_text(csv_path="stocks.csv"):
    stock_data = pd.read_csv(csv_path)
    texts = []
    for _, row in stock_data.iterrows():
        # Combine company and business info into one string using available columns
        doc_text = f"Symbol: {row['symbol']}\nCompany: {row['company']}\nSector: {row['sector']}\nRevenue: {row['revenue']}\nNet Profit: {row['net_profit']}\nEPS: {row['eps']}\nPE Ratio: {row['pe']}\nMarket Cap: {row['market_cap']}\nDebt to Equity: {row['debt_to_equity']}"
        texts.append(doc_text)
    print(f"Loaded {len(texts)} company descriptions.")
    return texts


# Load the model that will create our embeddings
embedding_model = HuggingFaceEmbeddings(
    model_name='thenlper/gte-small'
)

print("Embedding model loaded successfully!")

# Create the vector database from our text documents
db = Chroma.from_texts(
    texts=ingest_stocks_csv_to_text(),  # here will come the stock text that you had stored in a variable.
    embedding=embedding_model  # here will come the model which will do the embedding.
)

print("Vector database created and data stored successfully!")

# This template guides the LLM on how to answer
template = """
Use the following company information to answer the user's question.
If you don't know the answer, just say that you don't know.

Context: {context}

Question: {question}

Answer:
"""

prompt = PromptTemplate.from_template(template)

# Create the final RAG chain
rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=db.as_retriever(),  # Use our ChromaDB as the retriever
    chain_type_kwargs={"prompt": prompt}
)

print("RAG chain created and ready to answer questions!")

while True:
    question = input("\nAsk a question about a company's business:\n> ")
    if question.lower() == 'exit':
        break

    # Get the answer from our RAG chain
    result = rag_chain.invoke({"query": question})

    print("\nAnswer:")
    print(result["result"])
