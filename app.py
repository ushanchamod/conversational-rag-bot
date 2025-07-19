from flask import Flask, request, jsonify
from chatbot.chatbot import chat_with_bot

app = Flask(__name__)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    session_id = data.get('session_id')
    message = data.get('message')

    if not session_id or not message:
        return jsonify({"error": "Both 'session_id' and 'message' are required."}), 400

    try:
        response = chat_with_bot(session_id, message)
        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
