# Démarrer l'application

docker-compose up
python3 lancerApi.py
cd vue-project
npm run dev

# Arrêter les Api

python3 stopApi.py

# Calculs

La partie calculs présente une page divisée en 2.

A gauche, on trouve le form qui permet de creer des variables et de creer de formules à partir de variables existantes.
Le form utile les POST et GET qui se trouvent dans propre/apiCalculs.
Les Get et les Post sont effectués sur la BDD mysql en local.

A droite, on retrouve toutes les formules qui ont été créees.