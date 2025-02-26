from weaviate.classes.query import Filter
from bddFct import connect_to_db
from flask import jsonify

def search_more_relevant_document(queryN,embedder,cross_encoder,top_k):
    """Recherche des documents les plus pertinents correspondant à la recherche."""

    client = connect_to_db()
    # Effectuer la recherche
    querryEmbbed = embedder.encode(queryN).tolist()
    collection = client.collections.get("Document")

    # Recherche hybride, combinaison de recherche vectorielle et de recherche par correspondance de texte
    # On limite les résultats à 20
    results = collection.query.hybrid(
        query=queryN,
        vector=querryEmbbed,
        query_properties=["content"],
        alpha=0.45,
        limit=20,
    )

    # La recherche pourrait être seulement vectorielle mais moins précise
    # results = collection.query.near_vector(
    #     near_vector=querryEmbbed, # your query vector goes here
    #     limit=20,
    # )
    
    client.close()
    # Extraire les textes des résultats pour le cross-encoder
    documents = []
    for doc in results.objects:
        properties = doc.properties
        documents.append({
        "content": properties.get('content'),
        "document": properties.get('document'),
        "codeK": properties.get('codeK')
    })


    # # Calcul des scores avec le cross-encoder
    cross_scores = cross_encoder.predict([(queryN, doc["content"]) for doc in documents])

    # Trier les résultats en fonction des scores
    ranked_results = [x for _, x in sorted(zip(cross_scores, documents), key=lambda x: x[0], reverse=True)]
    return ranked_results[:top_k]

def search_more_relevant_chunks_from_document_retrieved(queryN,embedder,documents,cross_encoder,top_k):
    """Recherche des chunks les plus pertinents des documents en paramètre correspondant à la recherche."""

    client = connect_to_db()
    # Effectuer la recherche
    querryEmbbed = embedder.encode(queryN).tolist()
    collection = client.collections.get("Chunk")


    # Recherche vectorielle
    results = collection.query.near_vector(
        near_vector=querryEmbbed, # your query vector goes here
        limit=20,
        filters = Filter.by_property("document").contains_any(documents),
    )

    # Recherche hybride, combinaison de recherche vectorielle et de recherche par correspondance de texte
    # results = collection.query.hybrid(
    #     query=queryN,
    #     vector=querryEmbbed,
    #     query_properties=["content"],
    #     alpha=1,
    #     limit=top_k,
    #     filters = Filter.by_property("content").contains_any(documents)
    # )

    client.close()
    # Extraire les textes des résultats pour le cross-encoder
    documents = []
    for doc in results.objects:
        properties = doc.properties
        documents.append({
        "content": properties.get('content'),
        "document": properties.get('document'),
        "codeK": properties.get('codeK'),
        "title": properties.get('title')
    })

    print(documents)
    # # Calcul des scores avec le cross-encoder
    cross_scores = cross_encoder.predict([(queryN, doc["content"]) for doc in documents])

    # Trier les résultats en fonction des scores
    ranked_results = [x for _, x in sorted(zip(cross_scores, documents), key=lambda x: x[0], reverse=True)]

    return ranked_results[:top_k]

def search_Rag(queryN,embedder_document,embedder_chunk,cross_encoder_document,cross_encoder_chunk,top_k_document,top_k_chunk):
    """Recherche des documents les plus pertinents correspondant à la recherche."""

    # Recherche des documents
    documents = search_more_relevant_document(queryN,embedder_document,cross_encoder_document,top_k_document)

    # Recherche des chunks
    chunks = search_more_relevant_chunks_from_document_retrieved(queryN,embedder_chunk,[doc["document"] for doc in documents],cross_encoder_chunk,top_k_chunk)

    return jsonify(chunks)  # Utilisation de Flask pour renvoyer un JSON valide

