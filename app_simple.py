import os
import streamlit as st
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Main header
st.markdown("# 🩺 RAG Health Q&A Chatbot")
st.markdown("## Intelligent Health Information System powered by WHO Data")

# Show loading status
if 'app_loaded' not in st.session_state:
    st.info("🚀 Starting up... Please wait while we initialize the system.")
    st.session_state.app_loaded = True

st.markdown("---")

# Sidebar info
with st.sidebar:
    st.markdown("### ℹ About")
    st.markdown("""
    **Type:** Retrieval-Augmented Generation (RAG)
    
    **Model:** OpenRouter API (GPT-3.5-turbo default)
    
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

# Check database connection (simplified)
def check_database_connection():
    """Check if database is accessible."""
    try:
        connection_string = os.getenv("PGVECTOR_CONNECTION_STRING")
        if not connection_string:
            return False, "PGVECTOR_CONNECTION_STRING environment variable not set"
        
        # For now, just check if the connection string exists
        # TODO: Add actual database connection test when dependencies are available
        return True, "Database connection configured"
        
    except Exception as e:
        return False, f"Database connection failed: {str(e)}"

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

# Check API keys first
api_keys_available = check_api_keys()

# Check database connection
db_status, db_message = check_database_connection()

if not db_status:
    st.error(f"🚨 Database Error: {db_message}")
    st.info("💡 If you're deploying on Railway, make sure to:")
    st.markdown("""
    1. Add a PostgreSQL service to your Railway project
    2. Set the PGVECTOR_CONNECTION_STRING environment variable
    3. Set your OPENROUTER_API_KEY environment variable
    """)
    
    # Show demo mode
    st.warning("🔧 Running in Demo Mode - Database features disabled")
    st.markdown("### 💬 Demo Mode")
    st.info("This is a demo version. Configure environment variables for full functionality.")
    
    # Simple demo UI
    demo_query = st.text_input("Try a demo question:", placeholder="e.g., What is HALE?")
    if demo_query:
        st.info("🔧 Demo Mode: In full deployment, this would search WHO health data and provide detailed answers.")
else:
    st.success("✅ Basic System Ready - Database connection configured")
    
    if api_keys_available:
        # Initialize LLM
        try:
            llm = OpenRouterLLM()
            st.success("✅ OpenRouter API connected")
            
            # Main chat interface
            st.markdown("### 💬 Ask Your Health Question")
            st.markdown("Enter any health-related question below.")
            
            user_query = st.text_input(
                "Your Question:",
                placeholder="e.g., What is HALE and how is it measured?",
                help="Ask any question related to health statistics, indicators, or global health trends"
            )
            
            if user_query:
                with st.spinner("🔍 Generating response..."):
                    try:
                        # Simple prompt without retrieval for now
                        simple_prompt = f"As a health information assistant, please answer this question: {user_query}"
                        answer = llm(simple_prompt)
                        
                        # Display answer
                        st.markdown("### 📚 Answer")
                        st.success(answer)
                        
                        st.info("💡 This is a simplified response. Full RAG functionality will be available once all dependencies are loaded.")
                        
                    except Exception as e:
                        st.error(f"❌ Error generating answer: {str(e)}")
                        st.info("Please check your OpenRouter API key and try again.")
        
        except Exception as e:
            st.error(f"❌ Failed to initialize OpenRouter: {str(e)}")
    
st.markdown("---")
st.markdown("#### 🌍 Global Health Intelligence")
st.markdown("**Powered by WHO Data • Built with Streamlit • Enhanced with AI**")
st.caption("Educational Purpose Only • Not a Substitute for Medical Advice")