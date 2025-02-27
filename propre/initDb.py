from sentence_transformers import SentenceTransformer

from bddFct import create_class_Document, create_class_Chunk, process_and_add_document_from_json,process_and_add_chunks_from_json

create_class_Document()
create_class_Chunk()

file_path = "propre/chunks_total.json"

embedder = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")

process_and_add_document_from_json(file_path,embedder)

process_and_add_chunks_from_json(file_path,embedder)
