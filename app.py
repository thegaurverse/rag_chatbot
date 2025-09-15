import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.vectorstores.pgvector import PGVector
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import psycopg2
from urllib.parse import urlparse

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(page_title="Health Chatbot", page_icon="💬", layout="centered")

# Title
st.title("🩺 Health Q&A Chatbot")
st.markdown("Ask health-related questions based on the uploaded WHO report (health_data.pdf).")

# Sidebar info
with st.sidebar:
    st.header("ℹ About")
    st.markdown("""
    - *Type*: Retrieval-Augmented Generation (RAG)
    - *Model*: google/flan-t5-base
    - *Embeddings*: HuggingFace MiniLM
    - *Vector Store*: PostgreSQL (PGVector)
    """)

# Load embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Database connection check
def check_database_connection():
    """Check if database is accessible and has the required data."""
    try:
        connection_string = os.getenv("PGVECTOR_CONNECTION_STRING")
        if not connection_string:
            return False, "PGVECTOR_CONNECTION_STRING environment variable not set"
        
        # Test basic connection
        parsed = urlparse(connection_string)
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        
        # Check if vector extension exists
        cursor.execute("SELECT * FROM pg_extension WHERE extname = 'vector';")
        if not cursor.fetchone():
            return False, "PGVector extension not installed"
        
        # Check if our collection exists
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'langchain_pg_embedding');")
        if not cursor.fetchone()[0]:
            return False, "Vector database not initialized. Please run init_db.py first"
        
        cursor.close()
        conn.close()
        return True, "Database connection successful"
        
    except Exception as e:
        return False, f"Database connection failed: {str(e)}"

# Check database connection
db_status, db_message = check_database_connection()

if not db_status:
    st.error(f"🚨 Database Error: {db_message}")
    st.info("💡 If you're deploying on Railway, make sure to:")
    st.markdown("""
    1. Add a PostgreSQL service to your Railway project
    2. Set the PGVECTOR_CONNECTION_STRING environment variable
    3. Run the database initialization script
    """)
    st.stop()

# Connect to PGVector
try:
    vectorstore = PGVector(
        connection_string=os.getenv("PGVECTOR_CONNECTION_STRING"),
        collection_name="healthdata",
        embedding_function=embeddings,
    )
    retriever = vectorstore.as_retriever()
except Exception as e:
    st.error(f"🚨 Failed to connect to vector database: {str(e)}")
    st.stop()

# Load model
@st.cache_resource
def load_model():
    model_id = "google/flan-t5-base"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
    pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=512)
    return HuggingFacePipeline(pipeline=pipe)

llm = load_model()

# Prompt template
prompt = PromptTemplate(
    template="""
Use the following context to answer the question.

Context: {context}

Question: {question}
""",
    input_variables=["context", "question"]
)

# QA Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt},
    return_source_documents=False
)

# Input box
user_query = st.text_input("💬 Ask a health-related question:", placeholder="e.g., What is HALE?")

if user_query:
    with st.spinner("Thinking..."):
        answer = qa_chain.run(user_query)
    st.markdown("### 📘 Answer")
    st.success(answer)