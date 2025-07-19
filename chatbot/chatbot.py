from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from .memory import get_session_history
from . import config
import os

# Initialize LLM and Embeddings
llm = ChatOpenAI(model=config.CHAT_MODEL, temperature=0.0)
embedding_model = OpenAIEmbeddings(model=config.EMBEDDING_MODEL)



if os.path.exists(config.CHROMA_PERSIST_DIR):
    vector_store = Chroma(persist_directory=config.CHROMA_PERSIST_DIR, embedding_function=embedding_model)
else:
    print("Vector store not found, creating new one")
    # Load and split documents
    loader = PyPDFLoader(config.PDF_PATH)
    # loader = TextLoader(config.TEXT_PATH)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
    splits = splitter.split_documents(docs)

    vector_store = Chroma.from_documents(
        documents=splits,
        embedding=embedding_model,
        persist_directory=config.CHROMA_PERSIST_DIR
    )


retriever = vector_store.as_retriever()


contextualize_system_prompt = (
    "Given the chat history and the latest user question, reformulate the question to be self-contained. "
    "If it's already clear, return it unchanged."
)


contextualize_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])


history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_prompt
)

system_prompt = (
    "You are a helpful and knowledgeable assistant. "
    "Use the provided context to answer the user's question accurately and clearly. "
    "If the answer is not in the context, say you don't know. "
    "Be concise and informative.\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])

qa_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)


# Conversational Chain with Memory
conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)

def chat_with_bot(session_id: str, message: str) -> str:
    try:
        print(f"Session ID: {session_id}")
        print(f"Message: {message}")
        response = conversational_rag_chain.invoke(
            {"input": message},
            config={"configurable": {"session_id": session_id}}
        )
        return response["answer"]
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, something went wrong while processing your request."
