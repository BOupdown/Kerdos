from sentence_transformers import SentenceTransformer
<<<<<<< HEAD
from propre.bddFct import create_class_Document, create_class_Chunk, process_and_add_document_from_json,process_and_add_chunks_from_json
=======
from bddFct import create_class_Document, create_class_Chunk, process_and_add_document_from_json,process_and_add_chunks_from_json
>>>>>>> 6d53c07147104bf23848275f46896e305f75fab1

create_class_Document()
create_class_Chunk()

file_path = "propre/chunks_total.json"

embedder = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")

process_and_add_document_from_json(file_path,embedder)

process_and_add_chunks_from_json(file_path,embedder)
