#!/bin/bash

VENV_DIR="venv"

echo "🔹 Création de l'environnement virtuel..."
python3 -m venv $VENV_DIR

echo "🔹 Activation de l'environnement..."
source $VENV_DIR/bin/activate

echo "🔹 Mise à jour de pip et installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Installation terminée. Utilise 'source venv/bin/activate' pour activer l'environnement."
