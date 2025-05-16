import sys
import json
from flask import Flask, request, jsonify, Blueprint
from rechercheFct import search_more_relevant_document
from sentence_transformers import SentenceTransformer, CrossEncoder
from flask_cors import CORS
from flask_cors import cross_origin
import os


# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app, resources={r"/recherche/*": {"origins": "*"}})
recherche_bp = Blueprint("recherche", __name__)

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
CROSS_ENCODING_MODEL = os.getenv("CROSS_ENCODER_MODEL")


# Load models
embedder = SentenceTransformer(EMBEDDING_MODEL)
cross_encoder = CrossEncoder(CROSS_ENCODING_MODEL)

def search(query):
    top_k = 10
    documents = search_more_relevant_document(query, embedder, cross_encoder, top_k)
    results = [{"codeK": i + 1, "content": doc} for i, doc in enumerate(documents)]
    return results

@recherche_bp.route('/search', methods=['POST', 'OPTIONS'])
@cross_origin(origins="*")  # autorise toutes origines sur ce endpoint
def handle_search():
    data = request.get_json()
    query = data.get('query', '')

    if query:
        results = search(query)
        return jsonify(results)
    else:
        return jsonify({"error": "Aucune requête fournie"}), 400


app.register_blueprint(recherche_bp, url_prefix="/recherche")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
