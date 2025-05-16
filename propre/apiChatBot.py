import sys
import json
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from recherche_historique import rag_system  # Importer la fonction rag_system du fichier python.py
from recherche import rag_system_websearch
from flask_cors import cross_origin

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app, resources={r"/chatbot/*": {"origins": "*"}})
chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route("/ask", methods=["POST", "OPTIONS"])
@cross_origin(origins="*")
def ask():
    data = request.get_json()
    user_query = data.get('question', '')
    
    if not user_query:
        return jsonify({'error': 'No question provided'}), 400
    
    response, sources = rag_system(user_query)
    
    return jsonify({'answer': response, 'sources': sources})


@chatbot_bp.route("/ask2", methods=["POST", "OPTIONS"])
@cross_origin(origins="*")
def ask2():
    data = request.get_json()
    user_query = data.get('question', '')
    
    if not user_query:
        return jsonify({'error': 'No question provided'}), 400
    
    response = rag_system_websearch(user_query)
    
    return jsonify({'answer': response})

app.register_blueprint(chatbot_bp, url_prefix="/chatbot")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

