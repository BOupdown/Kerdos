import subprocess

def lancer_api(commande):
    """Lance une API en utilisant une commande shell."""
    try:
        subprocess.Popen(commande, shell=True)
        print(f"API lancée avec la commande : {commande}")
    except Exception as e:
        print(f"Erreur lors du lancement de l'API : {e}")

# Commandes pour lancer les API
commande_api_calculs = "python3 propre/apiCalculs.py"
commande_api_chatbot = "python3 propre/apiChatBot.py"
commande_api_recherche = "python3 propre/apiRecherche.py"

# Lancer les API
lancer_api(commande_api_calculs)
lancer_api(commande_api_chatbot)
lancer_api(commande_api_recherche)
