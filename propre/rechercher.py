import sys
import json
from rechercheFct import search_more_relevant_document
from sentence_transformers import SentenceTransformer, CrossEncoder
import os

# Charger les modèles


EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
CROSS_ENCODING_MODEL = os.getenv("CROSS_ENCODER_MODEL")


embedder = SentenceTransformer(EMBEDDING_MODEL)
cross_encoder = CrossEncoder(CROSS_ENCODING_MODEL)

def main(query):
    # Paramètres de recherche
    top_k = 10

    # Effectuer la recherche RAG
    documents = search_more_relevant_document(query,embedder,cross_encoder,top_k)

    # Formater les résultats pour l'envoi au frontend
    results = [{"codeK": i + 1, "content": doc} for i, doc in enumerate(documents)]
    return results

if __name__ == "__main__":
    # Récupérer la requête depuis les arguments de la ligne de commande
    query = sys.argv[1]

    # Exécuter la recherche
    results = main(query)

    # Envoyer les résultats au format JSON
    print(json.dumps(results))