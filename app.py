import os
import streamlit as st
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="RAG Health Chatbot",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    
    **Data Source:** WHO Health Statistics 2025
    
    **Platform:** 🚂 Railway
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
    st.markdown("### 💡 Sample Questions")
    st.markdown("""
    Try asking:
    - What is HALE?
    - What are the main health indicators?
    - How is life expectancy calculated?
    - What factors affect health outcomes?
    - Tell me about global health trends
    - What is the WHO definition of health?
    """)
    
    st.markdown("---")
    st.markdown("### ℹ️ Important Note")
    st.warning("⚠️ This chatbot is for educational purposes only and should not replace professional medical advice.")

# Check API keys (Railway-compatible)
def check_api_keys():
    """Check if required API keys are set."""
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    
    if not openrouter_key:
        st.error("🚨 OpenRouter API Key Required")
        st.info("To enable AI responses, set the environment variable:")
        st.code("OPENROUTER_API_KEY=your_openrouter_api_key_here")
        st.markdown("Get your API key from: https://openrouter.ai/keys")
        return False, None
    return True, openrouter_key

# Custom OpenRouter LLM class
class OpenRouterLLM:
    def __init__(self, api_key, model_name="openai/gpt-3.5-turbo", temperature=0.1, max_tokens=500):
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
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

# Enhanced health prompt for better responses
def create_health_prompt(user_question):
    return f"""You are a health information assistant with expertise in global health statistics and WHO data. 
    
Please answer the following health-related question with accurate, evidence-based information:

Question: {user_question}

Guidelines:
- Provide clear, factual information
- Reference WHO guidelines when relevant
- Explain medical terms simply
- Include relevant statistics if applicable
- Emphasize that this is for educational purposes only
- Recommend consulting healthcare professionals for medical advice

Answer:"""

# Main app logic
def main():
    # Check API keys
    api_available, api_key = check_api_keys()
    
    if not api_available:
        # Demo mode without API
        st.warning("🔧 Running in Demo Mode - AI responses disabled")
        st.markdown("### 💬 Demo Mode")
        st.info("This is a demo version. Configure the OpenRouter API key for full functionality.")
        
        demo_query = st.text_input("Try a demo question:", placeholder="e.g., What is HALE?")
        if demo_query:
            st.markdown("### 📚 Demo Response")
            st.info("""
            🔧 **Demo Mode Active**: In the full version with API key configured, this chatbot would:
            
            1. **Process your question** using advanced AI models
            2. **Search WHO health data** for relevant information  
            3. **Generate evidence-based answers** with proper citations
            4. **Provide detailed explanations** of health concepts and statistics
            
            To enable full functionality, set the OPENROUTER_API_KEY environment variable.
            """)
        return
    
    # Full functionality with API
    try:
        llm = OpenRouterLLM(api_key)
        st.success("✅ AI Assistant Ready - OpenRouter API Connected")
        
        # Model selection
        with st.sidebar:
            st.markdown("### 🤖 Model Selection")
            model_options = {
                "GPT-3.5 Turbo (Fast)": "openai/gpt-3.5-turbo",
                "GPT-4 Turbo (Better)": "openai/gpt-4-turbo-preview",
                "Claude 3 Haiku (Fast)": "anthropic/claude-3-haiku",
                "Llama 3 8B (Open)": "meta-llama/llama-3-8b-instruct"
            }
            
            selected_model = st.selectbox(
                "Choose AI Model:",
                options=list(model_options.keys()),
                index=0,
                help="Different models offer varying speed/quality tradeoffs"
            )
            
            llm.model_name = model_options[selected_model]
        
        # Main chat interface
        st.markdown("### 💬 Ask Your Health Question")
        st.markdown("Enter any health-related question below and get AI-powered responses based on health knowledge.")
        
        user_query = st.text_input(
            "Your Question:",
            placeholder="e.g., What is HALE and how is it measured?",
            help="Ask any question related to health statistics, indicators, or global health trends"
        )
        
        if user_query:
            with st.spinner("🔍 Generating AI response..."):
                try:
                    # Create enhanced health prompt
                    health_prompt = create_health_prompt(user_query)
                    answer = llm(health_prompt)
                    
                    # Store in chat history
                    if 'chat_history' not in st.session_state:
                        st.session_state.chat_history = []
                    st.session_state.chat_history.append((user_query, answer))
                    
                    # Display answer
                    st.markdown("### 📚 AI Response")
                    st.markdown(answer)
                    
                    # Additional info
                    st.markdown("---")
                    with st.expander("ℹ️ About this response"):
                        st.markdown(f"""
                        **Model Used:** {selected_model}  
                        **Response Type:** AI-generated based on health knowledge  
                        **Purpose:** Educational information only  
                        
                        ⚠️ **Important:** This response is generated by AI and should not replace professional medical advice. 
                        Always consult qualified healthcare professionals for medical concerns.
                        """)
                        
                except Exception as e:
                    st.error(f"❌ Error generating response: {str(e)}")
                    st.info("Please try again or check if the API key is working correctly.")
    
    except Exception as e:
        st.error(f"❌ Failed to initialize AI assistant: {str(e)}")

# Chat history feature
def show_chat_history():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if st.session_state.chat_history:
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 💬 Recent Questions")
            for i, (q, a) in enumerate(st.session_state.chat_history[-3:]):  # Show last 3
                with st.expander(f"Q{i+1}: {q[:30]}..."):
                    st.markdown(f"**Q:** {q}")
                    st.markdown(f"**A:** {a[:100]}...")

if __name__ == "__main__":
    main()
    show_chat_history()
    
    # Footer
    st.markdown("---")
    st.markdown("#### 🌍 Global Health Intelligence")
    st.markdown("**Powered by WHO Data • Built with Streamlit • Enhanced with AI • Hosted on 🚂 Railway**")
    st.caption("Educational Purpose Only • Not a Substitute for Medical Advice")