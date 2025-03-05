import sys
import json
from flask import Flask, request, jsonify
from rechercheFct import search_more_relevant_document
from sentence_transformers import SentenceTransformer, CrossEncoder
from flask_cors import CORS

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load models
embedder = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
cross_encoder = CrossEncoder("cross-encoder/ms-marco-electra-base")

def search(query):
    top_k = 10
    documents = search_more_relevant_document(query, embedder, cross_encoder, top_k)
    results = [{"codeK": i + 1, "content": doc} for i, doc in enumerate(documents)]
    return results

@app.route('/search', methods=['POST'])
def handle_search():
    data = request.get_json()
    query = data.get('query', '')

    if query:
        results = search(query)
        return jsonify(results)
    else:
        return jsonify({"error": "Aucune requête fournie"}), 400



if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
