import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder, util
import re
from transformers import AutoTokenizer 
from flask import current_app


from openai import OpenAI
from rechercheFct import search_Rag

embedder = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
cross_encoder = CrossEncoder("cross-encoder/ms-marco-electra-base")
modele = "cognitivecomputations/dolphin3.0-r1-mistral-24b:free"

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)


# Gérer le contexte conversationnel
conversation_history = []  # Stockage de l'historique
history_limit = 6  # Nombre de tours de conversation gardés

def generate_rephrasing(query, contexte_recent,modele):
    """Reformule la question et le contexte pour un meilleur retrieval."""
    
    response = client.chat.completions.create(model=modele, messages=[
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

    prompt = generate_rephrasing(user_query, conversation_history, modele)
    print("PPPPPPPPPPPPPPPPPPPPPPPPPPPROMPT")
    print(prompt)
    print("PPPPPPPPPPPPPPPPPPPPPPPPPPPROMPT")

    # Rechercher des résultats pertinents
    results = search_Rag(prompt, embedder, embedder, cross_encoder, cross_encoder, topk, topk)  # Assurez-vous que `search` accepte un prompt formaté
    return results

def extract_documents(text, retrieved_info):
    """Extraire la section "Extrait" pour récupérer les sources de la réponses."""

    match = re.search(r'Extrait\s*[:\-]\s*(.*)', text, re.IGNORECASE | re.DOTALL)
    if not match:
        return []
    
    extrait_section = match.group(1)
    extrait_titles = [title.strip() for title in extrait_section.split(',')]
    matching_docs = []
    
    for doc in retrieved_info:  
        doc_name = doc.get("document", "").lower()
        codeK = doc.get("codeK", "")
        
        if any(extrait_title.lower() in doc_name for extrait_title in extrait_titles):
            matching_docs.append({'document': doc_name, 'codeK': codeK})
    
    return matching_docs


# Système RAG : Recherche + Génération
def generate_answer(query, retrieved_info, modele, contexte_recent):
    """Génère une réponse en utilisant les documents et le contexte."""
    queryRephrase = generate_rephrasing(query, conversation_history, modele)

    # chunks = [f"{i+1}: {doc['content']}" for i, doc in enumerate(retrieved_info)]
    chunks = [f"Titre : {doc['document']}: {doc['content']}" for i, doc in enumerate(retrieved_info)]
    chunks = "\n".join(chunks)
    message=[
        {"role": "system", "content": f"""
        Tu es un assistant intelligent. Voici le contexte récent de la conversation : 
        {contexte_recent}

        Voici les documents pertinents sur lesquels tu dois te baser : 
        {chunks}

        L'utilisateur demande : "{queryRephrase}"

        Les instructions sont :
        - Réponds en français.
        - Réponds à la QUESTION en utilisant exclusivement les DOCUMENTS fournis et en tenant compte du CONTEXTE.
        - Ta réponse doit être concise, claire et formulée avec tes propres mots.
        - Ta réponse doit sembler naturelle et humaine et venir de toi.
        - Donne des exemples concrets si possible.
        - Fournis des explications détaillées si nécessaire.
        - N'hésite pas à donner plusieurs informations.
        - Donne le titre de tous les documents que tu as utilisé UNIQUEMENT en fin de réponse sous la forme Extrait : [Titre1,Titre2].
        - Si la réponse n'est pas contenue dans les documents, réponds simplement que tu n'as pas trouvé d'information sur ce sujet.
        """},
        {"role": "user", "content": f"Question : {queryRephrase}\nInfos trouvées :\n{chunks}\nRéponse :"}
    ]
    response = client.chat.completions.create(model=modele, messages=message
    )
    sources = extract_documents(response.choices[0].message.content, retrieved_info)
    return response.choices[0].message.content,sources


# Système RAG : Recherche + Génération
def rag_system(question):
    """Système RAG qui combine recherche et génération de réponse."""
    contexte_recent = recuperer_historique_recent(question)
    
    # Recherche Web pour obtenir des informations pertinentes
    retrieved_info = ask_rag(question)

    # Génération de la réponse via Gemma:2b
    response,sources = generate_answer(question, retrieved_info, modele, contexte_recent)

    conversation_history.append(f"[Système]: {response}")

    if len(conversation_history) > history_limit:
        conversation_history.pop(0)

    return response,sources
