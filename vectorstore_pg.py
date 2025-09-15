from langchain.vectorstores.pgvector import PGVector
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ Load env variables
CONNECTION_STRING = os.getenv("PGVECTOR_CONNECTION_STRING")  # .env se le raha
COLLECTION_NAME = "healthdata"

# ✅ Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# ✅ Setup PGVector
vectorstore = PGVector(
    connection_string=CONNECTION_STRING,
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings
)

# ✅ Function to add texts (chunks) to DB
def add_chunks_to_pg(chunks):
    vectorstore.add_texts(texts=chunks)

# ✅ Function to search similar docs from PG
def get_relevant_chunks(query, k=3):
    return vectorstore.similarity_search(query, k=k)

