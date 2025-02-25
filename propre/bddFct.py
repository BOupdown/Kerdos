import json
import weaviate
import uuid
import weaviate.classes.config as wc
import weaviate.classes as wvc
from propre.processDataFct import processData

# A changer pour déploiement sur AWS ou autre
def connect_to_db():
    """Connection à la base de données Weaviate."""
    return weaviate.connect_to_local()

def create_class_Document():
    """Créer la classe Document dans Weaviate."""

    # Connexion à Weaviate
    client = connect_to_db()

    if not client.collections.exists("Document"):
        # Créer la classe Document si elle n'existe pas
        client.collections.create(
            name="Document",
            properties=[
                wc.Property(name="document", data_type=wc.DataType.TEXT),
                wc.Property(name="codeK", data_type=wc.DataType.TEXT),
                wc.Property(name="content", data_type=wc.DataType.TEXT),
            ],
            vectorizer_config=wvc.config.Configure.Vectorizer.none(),

        )
        print("Classe 'Document' créée avec succès")

    client.close()

def create_class_Chunk():
    """Créer la classe Chunk dans Weaviate."""

    # Connexion à Weaviate
    client = connect_to_db()

    if not client.collections.exists("Chunk"):
        # Créer la classe Chunk si elle n'existe pas
        client.collections.create(
            name="Chunk",
            properties=[
                wc.Property(name="document", data_type=wc.DataType.TEXT),
                wc.Property(name="codeK", data_type=wc.DataType.TEXT),
                wc.Property(name="title", data_type=wc.DataType.TEXT),
                wc.Property(name="content", data_type=wc.DataType.TEXT),
            ],
            vectorizer_config=wvc.config.Configure.Vectorizer.none(),

        )
        print("Classe 'Chunk' créée avec succès")

    client.close()

def extract_and_store_documents(json_data, embedder):
    """Extraire les documents depuis un fichier JSON et les stocker dans Weaviate."""

    # Connexion à Weaviate
    client = connect_to_db()

    documents_dict_content, documents_dict_codeK = processData(json_data)


    # Get the collection
    collection = client.collections.get("Document")
    with collection.batch.dynamic() as batch:
        # Ajouter les documents dans Weaviate
        for doc_title, contents in documents_dict_content.items():
            combined_text = f"{doc_title} " + " ".join(contents)

            # Générer un embedding si nécessaire
            embedding = embedder.encode(combined_text).tolist()

            # Créer un ID unique
            doc_id = str(uuid.uuid4())

            # Construire l'objet à envoyer à Weaviate
            document_data = {
                "document": doc_title,
                "codeK": documents_dict_codeK.get(doc_title, ""),
                "content": combined_text
            }

            # Ajouter l'objet au client Weaviate
            batch.add_object(
                properties=document_data,
                uuid=doc_id,
                vector=embedding,
                # references=reference_obj  # You can add references here
            )

            # Check for failed objects
            if len(collection.batch.failed_objects) > 0:
                print(f"Failed to import {len(collection.batch.failed_objects)} objects")
                for failed in collection.batch.failed_objects:
                    print(f"e.g. Failed to import object with error: {failed.message}")

    client.close()        

def process_and_add_document_from_json(file_path,embedder):
    """Ouverture du fichier et ajout des documents à la base de données."""

    #  Ouvrir le fichier JSON
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)  # Charger les données JSON
    except Exception as e:
        print(f" Erreur lors de la lecture du fichier JSON : {e}")
        return
    
    #  Appliquer la fonction d'ajout des chunks à ChromaDB
    extract_and_store_documents(json_data,embedder)

def extract_and_store_chunks(chunks,embedder):
    """Stocker les chunks dans Weaviate."""

    # Connexion à Weaviate
    client = connect_to_db()


    # Get the collection
    collection = client.collections.get("Chunk")
    with collection.batch.dynamic() as batch:
        # Ajouter les documents dans Weaviate
        for chunk in chunks:
            if chunk["document"]:

                document = chunk["document"]
                codeK = chunk["codeK"]
                title = chunk["title"]
                content = chunk["content"]

                embedding = embedder.encode(content).tolist()

                # Créer un ID unique
                doc_id = str(uuid.uuid4())

                # Construire l'objet à envoyer à Weaviate
                document_data = {
                    "document": document,
                    "codeK": codeK,
                    "title": title,
                    "content": content
                }

                # Ajouter l'objet au client Weaviate
                batch.add_object(
                    properties=document_data,
                    uuid=doc_id,
                    vector=embedding,
                )

                # Check for failed objects
                if len(collection.batch.failed_objects) > 0:
                    print(f"Failed to import {len(collection.batch.failed_objects)} objects")
                    for failed in collection.batch.failed_objects:
                        print(f"e.g. Failed to import object with error: {failed.message}")

    client.close()        

def process_and_add_chunks_from_json(file_path,embedder):
    """Ouverture du fichier et ajout des chunkss à la base de données."""

    #  Ouvrir le fichier JSON
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            chunks = json.load(f)  # Charger les données JSON
    except Exception as e:
        print(f" Erreur lors de la lecture du fichier JSON : {e}")
        return
    
    #  Appliquer la fonction d'ajout des chunks à ChromaDB
    extract_and_store_chunks(chunks,embedder)
