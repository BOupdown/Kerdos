import requests
from transformers import AutoTokenizer
from recherche_historique import generate_answer
import nltk
from nltk.corpus import stopwords
from recherche_historique import recuperer_historique_recent


# Clé API et ID moteur de recherche pour Google Custom Search
API_KEY = 'AIzaSyBdaQew_B0cvIp1iLxsUPCtG8xtzgluZDM'
SEARCH_ENGINE_ID = '14514bd4afbb647a0'
modele = "cognitivecomputations/dolphin3.0-r1-mistral-24b:free"
num_results=5

# Fonction de Recherche Web avec Google Custom Search
def web_search(query, num_results):
    """Effectue une recherche sur Internet et retourne les résultats depuis des sites spécifiques."""

    # Filtrer les mots inutiles dans la question
    filtered_query = filter_stop_words(query)
    
    # Construire l'URL de l'API Google Custom Search
    url = f"https://www.googleapis.com/customsearch/v1?q={filtered_query}&cx={SEARCH_ENGINE_ID}&key={API_KEY}"
    
    response = requests.get(url)
    data = response.json()

    results = []
    if 'items' in data:
        for item in data['items'][:num_results]:
            results.append(item['snippet'])  # Extraire les extraits des résultats
    return "\n".join(results)

# Fonction pour enlever les mots inutiles (stopwords)
def filter_stop_words(text):
    """Enlève les mots inutiles de la question."""
    # Télécharger les stopwords si ce n'est pas déjà fait
    nltk.download('stopwords')
    stop_words = set(stopwords.words('french'))

    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return " ".join(filtered_words)

# Système RAG : Recherche + Génération
def rag_system_websearch(question):
    """Système RAG qui combine recherche web et génération de réponse."""

    contexte_recent = recuperer_historique_recent(question)

    # Recherche Web pour obtenir des informations pertinentes
    retrieved_info = web_search(question, num_results)  
    
    # Génération de la réponse
    response,source = generate_answer(question, retrieved_info,modele, contexte_recent)
    
    return response
