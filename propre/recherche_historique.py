import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder, util
import re
from transformers import AutoTokenizer 
from flask import current_app


from openai import OpenAI
from rechercheFct import search_Rag

embedder = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
cross_encoder = CrossEncoder("cross-encoder/ms-marco-electra-base")


client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)


# Gérer le contexte conversationnel
conversation_history = []  # Stockage de l'historique
history_limit = 6  # Nombre de tours de conversation gardés

def generate_rephrasing(query, contexte_recent):
    """Génère une réponse via Gemma:2b en utilisant un pipeline RAG."""
    
    response = client.chat.completions.create(model="cognitivecomputations/dolphin3.0-r1-mistral-24b:free", messages=[
        {"role": "system", "content": "Étant donné un historique de conversation et la dernière question de l'utilisateur qui pourrait faire référence à un contexte dans l'historique de conversation, formule une question autonome qui peut être comprise sans avoir besoin de l'historique. Ne réponds PAS à la question, reformulez-la simplement si nécessaire, sinon retourne-la telle quelle. Parle en français"},

        {"role": "user", "content": f"Question : {query}\nContexte :\n{contexte_recent}\nRéponse :"}
    ])

    return response.choices[0].message.content



def recuperer_historique_recent(user_query):
    """Ajoute le contexte conversationnel à la requête."""
    context = " ".join(conversation_history[-history_limit:])
    return f"{context} {user_query}" if context else user_query

# Fonction pour interroger le RAG
def ask_rag(user_query):
    """Gère la conversation et interroge le RAG."""
    topk = 10
    # Ajouter la nouvelle question à l'historique
    conversation_history.append(f"[Utilisateur]: {user_query}")
    
    # Limiter la taille de l'historique
    if len(conversation_history) > history_limit:
        conversation_history.pop(0)

    prompt = generate_rephrasing(user_query, conversation_history)
    # Rechercher des résultats pertinents
    results = search_Rag(prompt, embedder, embedder, cross_encoder, cross_encoder, topk, topk)  # Assurez-vous que `search` accepte un prompt formaté
    return results


def generate_answer(query, retrieved_info, contexte_recent):
    """Génère une réponse en utilisant un pipeline RAG."""

    prompt = generate_rephrasing(query, conversation_history)

    
    response = client.chat.completions.create(model="cognitivecomputations/dolphin3.0-r1-mistral-24b:free", messages=[
        {"role": "system", "content": f"""
        Tu es un assistant intelligent. Voici le contexte récent de la conversation : 
        {contexte_recent}

        Voici les documents pertinents sur lesquels tu dois te baser : 
        {retrieved_info}

        L'utilisateur demande : "{prompt}"

        Les instructions sont :
        - Réponds en français.
        - Réponds à la QUESTION en utilisant exclusivement les DOCUMENTS fournis et en tenant compte du CONTEXTE.
        - Ta réponse doit être concise, claire et formulée avec tes propres mots.
        - Donne des exemples concrets si possible.
        - Fournis des explications détaillées si nécessaire.
        - N'hésite pas à donner plusieurs informations.
        - Si la réponse n'est pas contenue dans les documents, réponds simplement que tu n'as pas trouvé d'information sur ce sujet.
        """},
        {"role": "user", "content": f"Question : {prompt}\nInfos trouvées :\n{retrieved_info}\nRéponse :"}
    ]
    )

    return response.choices[0].message.content


# Système RAG : Recherche + Génération
def rag_system(question):
    """Système RAG qui combine recherche web et génération de réponse."""
    
    # Récupérer l'historique récent
    contexte_recent = recuperer_historique_recent(question)
    
    # Recherche Web pour obtenir des informations pertinentes
    # Assurez-vous que la recherche se fait dans le bon contexte Flask
    retrieved_info = ask_rag(question)

    # Génération de la réponse via Gemma:2b
    response = generate_answer(question, retrieved_info, contexte_recent)

    # Mise à jour de l'historique de la conversation
    conversation_history.append(f"[Système]: {response}")

    # Limite de l'historique de la conversation
    if len(conversation_history) > history_limit:
        conversation_history.pop(0)

    return response


