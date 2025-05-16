import subprocess
import signal
import sys

# 1. Liste des commandes à lancer
commands = [
    "python3 apiCalculs.py",
    "python3 apiChatBot.py",
    "python3 apiRecherche.py",
]

processes = []

def lancer_api(cmd):
    """Démarre un sous-processus et l’ajoute à la liste."""
    p = subprocess.Popen(cmd, shell=True)
    print(f"API lancée avec la commande : {cmd}")
    processes.append(p)

# 2. Handler pour arrêter proprement tous les enfants
def handle_sigterm(signum, frame):
    print("SIGTERM reçu, on arrête tout…")
    for p in processes:
        p.terminate()
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)

# 3. Lancer toutes les API
for c in commands:
    lancer_api(c)

# 4. Bloquer jusqu’à la fin de chaque process
for p in processes:
    p.wait()
