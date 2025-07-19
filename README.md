# OUSL Credit Calculator Chatbot

A LangChain-powered conversational chatbot with retrieval-augmented generation (RAG), OpenAI integration, memory, and PDF/text document support. This project provides a backend service for answering questions about the BSE degree at OUSL using a combination of LLMs and document retrieval.

## Features

- **Conversational AI**: Uses OpenAI's GPT models for natural language understanding and response.
- **Retrieval-Augmented Generation (RAG)**: Answers are grounded in the content of provided documents (PDF/text).
- **Persistent Vector Store**: Uses ChromaDB to store and retrieve document embeddings.
- **Session Memory**: Maintains chat history per session for context-aware conversations.
- **PDF/Text Support**: Easily extendable to support more documents.

## Requirements

- Python 3.8+
- See `requirements.txt` for Python dependencies:
  - flask
  - langchain
  - langchain-openai
  - langchain-community
  - langchain-core
  - langchain-chroma
  - langchain-text-splitters
  - chromadb
  - tiktoken
  - dotenv
  - pypdf

## Setup

1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables**:
   - Create a `.env` file in the root directory with your OpenAI API key:
     ```env
     OPENAI_API_KEY=your_openai_api_key_here
     ```
4. **Add your documents**:
   - Place your PDF (e.g., `bse-degree-info.pdf`) in the project root, or update the path in `chatbot/config.py`.

## Usage

- **Start the server**:
  ```bash
  python app.py
  ```
- **API Endpoint**:
  - `POST /api/chat`
    - JSON body: `{ "session_id": "<session_id>", "message": "<your question>" }`
    - Returns: `{ "response": "<bot answer>" }`

## Folder Structure

```
ai-service/
├── app.py                # Flask API server
├── bse-degree-info.pdf   # Example PDF for retrieval
├── chatbot/
│   ├── chatbot.py        # Main chatbot logic (RAG, memory, etc.)
│   ├── config.py         # Configuration and environment variables
│   └── memory.py         # Session memory management
├── chroma_db/            # Persistent vector store (auto-generated)
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
```

## Customization

- To use a different document, update `PDF_PATH` in `chatbot/config.py`.
- To add text support, see commented code in `chatbot.py` for `TextLoader`.
