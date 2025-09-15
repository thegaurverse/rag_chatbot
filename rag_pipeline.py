from langchain_community.vectorstores.pgvector import PGVector
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import openai

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

# Initialize OpenRouter LLM
llm = OpenRouterLLM()

# Prompt Template
prompt_template = """
Use the following context to answer the question about health topics.

Context: {context}

Question: {question}

Please provide a clear, accurate answer based on the provided context. If the context doesn't contain enough information to answer the question, say so.
"""

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

# Custom QA function for OpenRouter
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

# Example usage
if __name__ == "__main__":
    # Ask a question
    query = input("Ask your health-related question: ")
    result = run_qa_chain(query)
    print(f"\nAnswer: {result}")