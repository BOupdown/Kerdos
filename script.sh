#!/bin/bash

# Lancer Docker Compose
echo "Lancement de Docker Compose..."
docker-compose up -d

# Lancer le serveur Node.js
echo "Lancement de Node.js server.js..."
node server.js &

# Lancer le premier script Python
echo "Lancement de python3 propre/app.py..."
python3 propre/app.py &

# Lancer le deuxième script Python
echo "Lancement de python3 propre/app2.py..."
python3 propre/app2.py &

# Lancer le projet Vue.js
echo "Lancement de npm run dev dans vue-project..."
cd vue-project
npm run dev
