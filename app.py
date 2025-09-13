import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.vectorstores.pgvector import PGVector
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

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

# Connect to PGVector
vectorstore = PGVector(
    connection_string=os.getenv("PGVECTOR_CONNECTION_STRING"),
    collection_name="healthdata",
    embedding_function=embeddings,
)

retriever = vectorstore.as_retriever()

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