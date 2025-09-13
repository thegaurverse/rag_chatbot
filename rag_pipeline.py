from langchain_community.vectorstores.pgvector import PGVector
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain import HuggingFacePipeline

from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Set up embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Connect to PGVector
CONNECTION_STRING = os.getenv("PGVECTOR_CONNECTION_STRING")
vectorstore = PGVector(
    collection_name="healthdata",
    connection_string=CONNECTION_STRING,
    embedding_function=embeddings,
)

retriever = vectorstore.as_retriever()

# Load local model
model_id = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

# Create pipeline
pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=512)

# Wrap it for LangChain
llm = HuggingFacePipeline(pipeline=pipe)

# Prompt Template
prompt_template = """
Use the following context to answer the question.

Context: {context}

Question: {question}
"""

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

# Create the RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt},
    return_source_documents=False
)

# Ask a question
query = input("Ask your health-related question: ")
result = qa_chain.run(query)

print(f"\nAnswer : {result}")