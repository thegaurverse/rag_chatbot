import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.vectorstores.pgvector import PGVector
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import psycopg2
from urllib.parse import urlparse
import time

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

# Initialize database on first run
@st.cache_resource
def initialize_database():
    """Initialize database with vector data if not already done."""
    try:
        # Check if database is already initialized
        connection_string = os.getenv("PGVECTOR_CONNECTION_STRING")
        if not connection_string:
            return False, "PGVECTOR_CONNECTION_STRING not set"
        
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        
        # Check if our collection exists
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'langchain_pg_embedding');")
        table_exists = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        if not table_exists:
            # Run database initialization
            st.info("🔄 Initializing database with health data... This may take a few minutes.")
            exec(open('init_db.py').read())
            return True, "Database initialized successfully"
        else:
            return True, "Database already initialized"
            
    except Exception as e:
        return False, f"Database initialization failed: {str(e)}"

# Load embeddings with progress
@st.cache_resource
def load_embeddings():
    """Load embeddings model with caching."""
    with st.spinner("🧠 Loading embeddings model..."):
        return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

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
    3. Wait for the app to initialize the database automatically
    """)
    st.stop()

# Initialize database if needed
init_status, init_message = initialize_database()
if not init_status:
    st.error(f"🚨 Database Initialization Error: {init_message}")
    st.stop()
else:
    st.success(f"✅ {init_message}")

# Load embeddings
embeddings = load_embeddings()

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

# Load model with better error handling and progress
@st.cache_resource
def load_model():
    """Load language model with progress indication."""
    try:
        with st.spinner("🤖 Loading language model (this may take several minutes on first run)..."):
            model_id = "google/flan-t5-base"
            
            # Add timeout and error handling
            tokenizer = AutoTokenizer.from_pretrained(model_id)
            model = AutoModelForSeq2SeqLM.from_pretrained(
                model_id,
                torch_dtype="auto",
                device_map="auto" if os.getenv("CUDA_VISIBLE_DEVICES") else "cpu"
            )
            
            pipe = pipeline(
                "text2text-generation", 
                model=model, 
                tokenizer=tokenizer, 
                max_length=512,
                do_sample=False,
                temperature=0.1
            )
            
            return HuggingFacePipeline(pipeline=pipe)
    except Exception as e:
        st.error(f"Failed to load model: {str(e)}")
        st.info("The model is large (~1GB) and may take time to download on first deployment.")
        st.stop()

# Check if we should load the model
if 'model_loaded' not in st.session_state:
    llm = load_model()
    st.session_state.model_loaded = True
    st.session_state.llm = llm
else:
    llm = st.session_state.llm

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
        try:
            answer = qa_chain.run(user_query)
            st.markdown("### 📚 Answer")
            st.success(answer)
        except Exception as e:
            st.error(f"Error generating answer: {str(e)}")
            st.info("Please try a different question or wait a moment for the models to fully load.")
