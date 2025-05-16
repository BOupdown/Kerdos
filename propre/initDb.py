import os

from sentence_transformers import SentenceTransformer
from bddFct import create_class_Document, create_class_Chunk, process_and_add_document_from_json,process_and_add_chunks_from_json

create_class_Document()
create_class_Chunk()

file_path = "chunks_total.json"

embedding_model = os.getenv("EMBEDDING_MODEL")

embedder = SentenceTransformer(embedding_model)

process_and_add_document_from_json(file_path,embedder)

process_and_add_chunks_from_json(file_path,embedder)
