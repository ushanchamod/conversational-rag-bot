from langchain_community.chat_message_histories import ChatMessageHistory

# Simple in-memory session store
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]
