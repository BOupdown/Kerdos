# Avant le lancement

Il faut se rendre dans le .env et remplir les variables manquantes.

API_KEY_OPEN_ROUTER : Créer un compte sur https://openrouter.ai/ puis aller dans votre profil puis keys puis create API Key et copié collé la key.

API_KEY_WEB_SEARCH & SEARCH_ENGINE_ID : Suivre la procédure décrite dans la partie [Generation avec web search](#generation-avec-web-search)



# Démarrer l'application

Pour le premier lancement (il faut attendre environ 15 min): 

docker compose up --build

Pour les prochains lancements une fois que le buld est fait : 

docker compose up 


# Changements de modèles

Dans l'objectif de changer les modèles utilisés pour optimiser les résultats, il faut changer les modèles dans le .env.

Modèle d'embeddings, actuellement : paraphrase-multilingual-mpnet-base-v2 : 

app.py, initDb, rechercheHistorique, rechercher

Modèle de reranking (CrossEncoder) actuellement : cross-encoder/ms-marco-electra-base : 

app.py, rechercher_historique,rechercher*

Ces modèles fonctionnent avec la librairies d'HuggingFace sentence_Transformers. 
Modèle de langage, actuellement : cognitivecomputations/dolphin3.0-r1-mistral-24b:free :

recherche_historique.py.
Ce modèle fonctionne avec l'API de Open Router.

# Base de données
La base de données vectorielle est weaviate, elle contient deux collections : Document et Chunk.
La collection Document est utilisé pour la recherche des documents.
Elle contient le titre du document, le codeK du document ainsi qu'un content qui est une assemblage du titre, et des parties #Application #Definition et #Synthèse économique si elles existent. C'est ce content qui est vectorisé.
La collection Chunk est utilisé pour la recherche des chunks importants. 
Elle contient le titre du document, le codeK du document, le titre de la section ainsi que le contenu de la section. C'est le contenu qui est vectorisé.
Pour initialiser cette base de données, il faut utiliser le script initDb qui permet de créer les collections et le contenu. La vectorisation des données prend du temps, il faut environ 15 minutes pour l'execution totale.
La création des données se fait via un fichier chunks_total.json qui contient tous les chunks.

Pour générer ce fichier, il faut utiliser la fonction process_all_folders du fichier processDataFct. 

Dans l'objectif d'une implémentation à la base de données contenant les fiches, il faudrait créer la pipeline de connexion a la bdd et adapter les fonction permettant de transformer les données.

L'intérêt de l'utilisation de Weaviate est son implémentation dans AWS et ses nombreuses fonctions.
Dans l'idée d'une implémentation avec AWS, il suffirait de changer la fonction connect_to_db présente dans le fichier bddFct.

# Barre de recherche :
## Retrieval : 
La barre de recherche permet de chercher les fiches via leurs nom ou via une requête en langage naturel.
Pour cela, il faut se rendre dans l'onglet recherche et taper sa requête.
La recherche retourne les 10 résultats les plus pertinents.
La recherche fonctionne en deux parties.
Une première partie qui recherche les documents les plus proche dans la base de donnée Weaviate.
Cette recherche est hybride, c'est à dire qu'elle est à la fois vectorielle et à la fois par fréquence de mots.
La deuxième partie permet de reclasser ces résultats pour obtenir les plus pertinents en premier.

Cette fonction se trouve dans le fichier rechercheFct sous le nom de search_more_relevant_document.
Elle prend en paramètre :
query : une requête en langage naturel.
embedder : un modèle de vectorisation ici paraphrase-multilingual-mpnet-base-v2
cross_encoder : un modèle de reranking ici cross-encoder/ms-marco-electra-base
top_k : le nombre de document à retourné après le rerank actuellement 10
Il est possible de modifier le nombre d'élément à rerank dans la fonction actuellement 20.
Cette fonction repose sur la fonction de weaviate de recherche hybride qui contient de nombreux paramètres pouvant plus ou moins amélioré les résultats. Elle cherche dans la collection Document.

Elle obtient un score de 60% de réussite sur des requêtes provenant du fichier gain_CO2.xlsx.
Ce pourcentage peut être amélioré en finetunant le reranker sur les données pour le top 20 sans reranker on obtient un score de 86%.

# Chatbot :
## Retrieval :

La partie recherche de documents pertinents du chatBot Rag se base sur deux recherches.
Une recherche de docoument permtinent présenté au-dessus.
Une recherche de chunks pertinent parmi les documents retrouvés précédement.
Cette double recherche permet d'éviter de retrouver des chunks similaire d'autres document qui n'aurait pas de sens dans le contexte.

Cette recherche se base sur la fonction search rag du fichier rechercheFct et retourne une liste de document avec le titre du doucment, le titre de la section, le codeK du document et le contenu de la section.

Elle est composée de la fonction search_more_relevant_document et de la fonction search_more_relevant_chunks_from_document_retrieved qui a comme paramètre : 

query : une requête en langage naturel.

embedder : un modèle de vectorisation ici paraphrase-multilingual-mpnet-base-v2

cross_encoder : un modèle de reranking ici cross-encoder/ms-marco-electra-base

documents : le titre des documents dans lesquels on veut chercher les chunks les plus pertinents

top_k : le nombre de document à retourné après le rerank actuellement 10.

Cette fonction est basée sur une recherche purement vectorielle qui se fait via une fonction de weaviate filtrer sur les documents recupérés en paramètres. Elle cherche dans la collection Chunk. Il est possible de changer le nombre d'élément à rerank actuellement 20.

## Génération de texte :
Une fois que les documents les plus pertinents en réponse à la requête de l'utilisateur ont été identifiés par le système de retrieval, nous allons générer du texte à partir de ces documents.

### Génération sans web search :
La génération de texte sans recherche internet fonctionne en plusieurs étapes :

1. Récupérer l'historique de la conversation

2. Réinterpréter la question de l'utilisateur avec l'historique pour formuler une question autonome qui peut être comprise sans avoir besoin de l'historique

Pour cela on utilise le modèle Dolphin3.0 R1 Mistral 24B avec l'API de OpenRouter.

Pourquoi utiliser OpenRouter

Nous avons décidé de prendre ce modèle pour ces raisons : 
- Modèle puissant avec une meilleure compréhension du français que d'autres modèles
- Modèle de 24 milliards de paramètres donc très précis


### Generation avec web search
La génération de texte avec la recherhe internet fonctionne avec un moteur de recherche personnalisé.

Pour ce moteur de recherche nous avons choisi Google Programmable Search Engine pour les raisons suivantes :
1. Accès aux résultats de Google
2. Personnalisation avancée (restreindre la recherche à un ensemble précis de sites web)
3. Facilité d'intégration
4. Google CSE est gratuit pour un usage basique

Les contraintes sont : 
1. Publicité Google parfois affichée dans les résultats gratuits
2. Moins de contrôle sur l'indexation des données

Des alternatives à Google Programmable Search Engine peuvent être :
- SerpAPI
- Algolia
- MeiliSearch
- Bing Custom Search
- Whoogle

Pour ce créer un moteur de recherche Programmable Search Engine :
1. S'inscrire sur Programmable Search Engine
2. Créer un moteur de recherche personnalisé
3. Choisir des sites ou pages spécifiques sur lesquels les recherches seront basées ou choisir l'ensemble du Web.
4. Choisir des sites ou pages spécifiques à éviter (facultatif)

Un identifiant du moteur de recherche personnalisé sera généré.

Pour générer la clé API, il faut :
1. S'inscrire sur Google Cloud Platform
2. Créer ou sélectionner un projet où la clé API sera créée
3. Cliquer sur les 3 barres du menu navigation en haut à gauche > APIs & Services > Identifiants
4. En haut, cliquer sur créer des identifiants > clé API

Une clé API sera générée. Gardez la clé quelque part en sécurité.

Ensuite, dans le fichier .env changer les variables :
API_KEY = 'votre_clé_API'
SEARCH_ENGINE_ID = 'votre_identifiant_moteur_de_recherche'

Pour la fonction recherche web, notre chatbot va se baser sur un certain nombre de résultats par le moteur de recherche que l'on déterminera nous même.
num_results est le nombre de résultats internet sur lesquels la chatbot va se baser pour la génération d'une réponse.

Le modèle de génération de texte choisi est le même que pour la recherche sans internet pour les mêmes raisons.

La génération de texte avec recherche internet prend aussi en compte l'historique de la conversation de la même manière que la recherche sans internet.

# Calculs

La partie Calculs présente une interface utilisateur intuitive, divisée en deux sections principales pour une expérience utilisateur optimale. 

## Section gauche : Création de variables et formules
À gauche, un formulaire interactif permet aux utilisateurs de créer des variables et de générer des formules en utilisant les variables existantes. Ce formulaire repose sur des requêtes HTTP de type POST et GET, gérées par l'API propre/apiCalculs. Ces requêtes interagissent directement avec une base de données MySQL locale, stockant les variables et les formules dans les tables respectives `variables` et `formules`. Par exemple, lorsqu'un utilisateur crée une nouvelle variable, celle-ci est immédiatement enregistrée dans la table `variables`, et peut ensuite être référencée dans une formule via son `id` ou son `name`. De même, les formules créées sont stockées dans la table `formules`, avec une structure claire et organisée.

## Section droite : Affichage des formules 
À droite, l'interface affiche toutes les formules qui ont été créées et enregistrées dans la base de données. Cette section est dynamique et se met à jour en temps réel dès qu'une nouvelle formule est ajoutée ou modifiée. Les utilisateurs peuvent ainsi visualiser l'ensemble des calculs disponibles, ce qui facilite la gestion et l'utilisation des formules existantes.

## Interaction fluide entre les sections
L'interface est conçue pour offrir une interaction fluide entre les deux sections. Par exemple, lorsqu'une variable est créée dans la section gauche, elle devient immédiatement disponible pour être utilisée dans une nouvelle formule. Les résultats des calculs sont mis à jour en temps réel, offrant une expérience réactive et intuitive. Cette synergie entre les sections permet aux utilisateurs de travailler de manière efficace, sans avoir à recharger la page ou à effectuer des actions supplémentaires.

En résumé, cette interface combine une gestion robuste des données via une base de données MySQL locale avec une expérience utilisateur réactive et intuitive, facilitant la création et l'utilisation de variables et de formules.
