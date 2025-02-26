import sys
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from recherche_historique import rag_system  # Importer la fonction rag_system du fichier python.py

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_query = data.get('question', '')
    
    if not user_query:
        return jsonify({'error': 'No question provided'}), 400
    
    response = rag_system(user_query)
    
    return jsonify({'answer': response})




if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=7000)
