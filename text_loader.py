import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import PGVector
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load the PDF
loader = PyPDFLoader("health_data.pdf")
documents = loader.load()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# Create embeddings using Hugging Face (no API key needed)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Store embeddings in PostgreSQL using PGVector
PGVector.from_documents(
    embedding=embeddings,
    documents=texts,
    collection_name="healthdata",
    connection_string=os.getenv("PGVECTOR_CONNECTION_STRING"),
)


