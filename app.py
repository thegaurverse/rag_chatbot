import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.vectorstores.pgvector import PGVector
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.llms import OpenAI
import psycopg2
from urllib.parse import urlparse
import time
import openai

# Load environment variables
load_dotenv()

# Main header with better styling
st.markdown("# 🩺 RAG Health Q&A Chatbot")
st.markdown("## Intelligent Health Information System powered by WHO Data")
st.markdown("---")



# Sidebar info
with st.sidebar:
    st.markdown("### ℹ About")
    st.markdown("""
    **Type:** Retrieval-Augmented Generation (RAG)
    
    **Model:** OpenRouter API (GPT-3.5-turbo default)
    
    **Embeddings:** HuggingFace MiniLM (Local)
    
    **Vector Store:** PostgreSQL (PGVector)
    
    **Data Source:** WHO Health Statistics 2025
    """)
    
    st.markdown("---")
    st.markdown("### 🎯 About This Project")
    st.markdown("""
    This is an advanced **Retrieval-Augmented Generation (RAG)** system that provides accurate, 
    evidence-based answers to health-related questions using official WHO health data.
    
    **Perfect For:**
    - 📚 Students studying public health
    - 🔬 Researchers looking for WHO data insights
    - 📊 Health professionals seeking quick references
    - 🌍 Anyone interested in global health statistics
    """)
    
    st.markdown("---")
    st.markdown("### 🔧 Model Selection")
    # Model selection will be added by the load_model function
    
    st.markdown("---")
    st.markdown("### 💡 Sample Questions")
    st.markdown("""
    Try asking:
    - What is HALE?
    - What are the main health indicators?
    - How is life expectancy calculated?
    - What factors affect health outcomes?
    - Tell me about global health trends
    """)
    
    st.markdown("---")
    st.markdown("### ℹ️ Important Note")
    st.warning("⚠️ This chatbot is for educational purposes only and should not replace professional medical advice.")

# Check API keys
def check_api_keys():
    """Check if required API keys are set."""
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_key:
        st.error("🚨 OpenRouter API Key Required")
        st.info("Please add your OpenRouter API key as an environment variable:")
        st.code("OPENROUTER_API_KEY=your_openrouter_api_key_here")
        st.markdown("Get your API key from: https://openrouter.ai/keys")
        return False
    return True

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

# Load embeddings with local model
@st.cache_resource
def load_embeddings():
    """Load local HuggingFace embeddings."""
    with st.spinner("🧠 Loading local embeddings model..."):
        return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Database connection check
def check_database_connection():
    """Check if database is accessible and has the required data."""
    try:
        connection_string = os.getenv("PGVECTOR_CONNECTION_STRING")
        if not connection_string:
            return False, "PGVECTOR_CONNECTION_STRING environment variable not set"
        
        # Test basic connection
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        
        # Check if vector extension exists
        cursor.execute("SELECT * FROM pg_extension WHERE extname = 'vector';")
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return False, "PGVector extension not installed"
        
        cursor.close()
        conn.close()
        return True, "Database connection successful"
        
    except Exception as e:
        return False, f"Database connection failed: {str(e)}"

# Check API keys first
if not check_api_keys():
    st.stop()

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
    # Show system status in a nice way
    st.success("✅ System Ready - Database Connected, AI Models Loaded")
    st.markdown("---")

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

# Custom OpenRouter LLM class
class OpenRouterLLM:
    def __init__(self, model_name="openai/gpt-3.5-turbo", temperature=0.1, max_tokens=500):
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY")
        )
    
    def __call__(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

# Load OpenRouter model
@st.cache_resource
def load_model():
    """Load OpenRouter model."""
    model_choice = st.sidebar.selectbox(
        "Choose Model:",
        [
            "openai/gpt-3.5-turbo",
            "anthropic/claude-3-haiku",
            "microsoft/wizardlm-2-8x22b",
            "google/gemma-2-9b-it:free",
            "meta-llama/llama-3.1-8b-instruct:free"
        ]
    )
    return OpenRouterLLM(model_name=model_choice)

llm = load_model()

# Prompt template
prompt = PromptTemplate(
    template="""
Use the following context to answer the question about health topics.

Context: {context}

Question: {question}

Please provide a clear, accurate answer based on the provided context. If the context doesn't contain enough information to answer the question, say so.
""",
    input_variables=["context", "question"]
)

# Custom QA Chain for OpenRouter
def run_qa_chain(query):
    """Run the QA chain with OpenRouter LLM."""
    # Get relevant documents
    docs = retriever.get_relevant_documents(query)
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # Format prompt
    formatted_prompt = prompt.format(context=context, question=query)
    
    # Get response from OpenRouter
    response = llm(formatted_prompt)
    return response

# Main content area - Chatbot Interface
st.markdown("### 💬 Ask Your Health Question")
st.markdown("Enter any health-related question below. The AI will search through WHO health data to provide you with accurate, evidence-based answers.")

# Input box
user_query = st.text_input(
    "Your Question:",
    placeholder="e.g., What is HALE and how is it measured?",
    help="Ask any question related to health statistics, indicators, or global health trends"
)

# Quick demo section
if not user_query:
    st.markdown("### 🚀 Quick Demo - Try These Questions:")
    demo_col1, demo_col2, demo_col3 = st.columns(3)
    
    with demo_col1:
        if st.button("🔍 What is HALE?", use_container_width=True, type="secondary"):
            user_query = "What is HALE?"
    
    with demo_col2:
        if st.button("📊 Health Indicators", use_container_width=True, type="secondary"):
            user_query = "What are the main health indicators?"
    
    with demo_col3:
        if st.button("🌍 Global Health Trends", use_container_width=True, type="secondary"):
            user_query = "Tell me about global health trends"

if user_query:
    with st.spinner("🔍 Searching WHO health data and generating response..."):
        try:
            answer = run_qa_chain(user_query)
            
            # Display answer with better formatting
            st.markdown("### 📚 Answer")
            st.success(answer)
            
            # Add some helpful information
            st.info("💡 This answer is based on WHO health data and statistics. For personalized medical advice, please consult with healthcare professionals.")
            
        except Exception as e:
            st.error(f"❌ Error generating answer: {str(e)}")
            st.info("Please check your OpenRouter API key and try again, or try rephrasing your question.")

# Footer section
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("#### 🌍 Global Health Intelligence")
    st.markdown("**Powered by WHO Data • Built with Streamlit • Enhanced with AI**")
    st.caption("Educational Purpose Only • Not a Substitute for Medical Advice")
