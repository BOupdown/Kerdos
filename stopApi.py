import os
import signal
import psutil

def arreter_api(nom_script):
    """Arrête une API en utilisant le nom du script."""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and isinstance(cmdline, list) and nom_script in " ".join(cmdline):
                pid = proc.info['pid']
                print(f"Arrêt du processus {pid} ({nom_script})")
                os.kill(pid, signal.SIGTERM)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

# Noms des scripts à arrêter
noms_scripts = ["propre/apiCalculs.py", "propre/apiChatBot.py", "propre/apiRecherche.py"]

# Arrêter les API
for nom in noms_scripts:
    arreter_api(nom)
