# 🩺 RAG Health Chatbot

A Retrieval-Augmented Generation (RAG) health chatbot that answers questions based on WHO health data using advanced NLP techniques.

## ✨ Features

- **Intelligent Q&A**: Ask health-related questions and get accurate answers
- **RAG Architecture**: Combines retrieval and generation for better responses
- **Vector Search**: Uses PGVector for efficient similarity search
- **Local Models**: Runs entirely with HuggingFace models (no API keys needed)
- **Streamlit UI**: Clean and intuitive web interface

## 🏗️ Architecture

```
📁 Project Structure
├── app.py                 # Main Streamlit application
├── rag_pipeline.py        # RAG pipeline implementation
├── text_loader.py         # PDF processing and vector storage
├── vectorstore_pg.py      # PostgreSQL vector store utilities
├── health_data.pdf        # WHO health data source
├── requirements.txt       # Python dependencies
└── Procfile              # Railway deployment configuration
```

## 🚀 Tech Stack

- **Framework**: Streamlit
- **Language Model**: Google Flan-T5-Base
- **Embeddings**: HuggingFace MiniLM (sentence-transformers/all-MiniLM-L6-v2)
- **Vector Database**: PostgreSQL with PGVector extension
- **Text Processing**: LangChain
- **PDF Processing**: PyPDF

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL with PGVector extension
- Git

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd rag-health-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   PGVECTOR_CONNECTION_STRING=your_postgresql_connection_string
   ```

4. **Initialize the database**
   ```bash
   python text_loader.py
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 💡 Usage

1. Open your browser and go to `http://localhost:8501`
2. Type your health-related question in the input box
3. Get instant, accurate answers based on the WHO health data

### Example Questions:
- "What is HALE?"
- "What are the main health indicators?"
- "How is life expectancy calculated?"
- "What factors affect health outcomes?"

## 🔧 Configuration

### Environment Variables
- `PGVECTOR_CONNECTION_STRING`: PostgreSQL connection string with PGVector support

### Model Configuration
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Language Model**: `google/flan-t5-base`
- **Chunk Size**: 500 characters
- **Chunk Overlap**: 50 characters

## 📊 How It Works

1. **Document Processing**: PDF is loaded and split into chunks
2. **Embedding Generation**: Text chunks are converted to vectors using HuggingFace embeddings
3. **Vector Storage**: Embeddings are stored in PostgreSQL with PGVector
4. **Query Processing**: User questions are converted to vectors
5. **Similarity Search**: Most relevant chunks are retrieved from the database
6. **Answer Generation**: Language model generates answers based on retrieved context

## 🎯 Key Components

### `app.py`
Main Streamlit application with user interface and RAG pipeline integration.

### `rag_pipeline.py`
Core RAG implementation with retrieval and generation components.

### `text_loader.py`
Handles PDF processing, text chunking, and vector database initialization.

### `vectorstore_pg.py`
PostgreSQL vector store utilities for storing and retrieving embeddings.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [WHO](https://www.who.int/) for providing health data
- [HuggingFace](https://huggingface.co/) for pre-trained models
- [LangChain](https://langchain.com/) for RAG framework
- [Streamlit](https://streamlit.io/) for the web interface

---

**Note**: This chatbot is for educational purposes and should not replace professional medical advice.
