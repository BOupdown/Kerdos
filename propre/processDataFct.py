import os
import json
import re

MAX_CHUNK_SIZE = 1000 # Taille max d'un chunk avant découpage

def get_document_info(catalogue_path):
    """Récupère le nom du fichier et le codeK depuis catalogue.json"""
    try:
        with open(catalogue_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        title = data.get("languages", {}).get("fr", {}).get("title", "Titre Inconnu")
        codeK = data.get("identifier", "Code Inconnu")
        # Si title est None, on remplace par "Titre Inconnu"
        return title,codeK
    
    except Exception as e:
        print(f"Erreur lors de la lecture de {catalogue_path}: {e}")
        return "Titre Inconnu"

def split_large_chunk(title, content,document,codeK, max_length=1000):
    """Divise un chunk trop long en plusieurs parties si nécessaire"""

    if len(content.strip()) == 0:
        return []
    if len(content) <= max_length:
        return [{"document": document,"codeK" : codeK,"title": title, "content": content.strip()}]
    
    sub_chunks = []
    paragraphs = content.split("\n\n")
    current_text = ""
    
    for para in paragraphs:
        if len(current_text) + len(para) <= max_length:
            current_text += para + "\n\n"
        else:
            if current_text.strip():
                sub_chunks.append({"document": document,"codeK" : codeK,"title": title, "content": current_text.strip()})
            current_text = para + "\n\n"

    if current_text.strip():
        sub_chunks.append({"document": document,"codeK" : codeK,"title": title, "content": current_text.strip()})
    
    return sub_chunks


def chunk_markdown(file_path, catalogue_path):
    """Chunk un fichier Markdown en sections logiques en ignorant certaines balises"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Supprimer les balises COL tout en conservant leur contenu
    content = re.sub(r"===COL===\n(.*?)\n===/COL===", r"\1", content, flags=re.DOTALL)
    
    # Supprimer les marqueurs ---50---
    content = re.sub(r"---50---", "", content)

    # Vérifier si le contenu est vide après nettoyage
    if not content.strip():
        document,codeK = get_document_info(catalogue_path)

        return [{"document": document,"codeK": codeK, "title": "", "content": ""}]

    chunks = []
    document,codeK = get_document_info(catalogue_path)
    current_chunk = {"document": document,"codeK": codeK, "title": None, "content": ""}

    # Séparer les sections basées sur les titres Markdown
    sections = re.split(r"(# .+|## .+)", content)

    skip_section = False

    for section in sections:
        section = section.strip()

        if section.startswith("# "):  
            skip_section = True  # Ignorer les sections de niveau 1
            continue  
        
        if section.startswith("## "):  
            document,codeK = get_document_info(catalogue_path)
            skip_section = False  # Ne pas ignorer les sections de niveau 2 et plus
            if current_chunk["title"] and current_chunk["content"].strip():
                chunks.extend(split_large_chunk(current_chunk["title"], current_chunk["content"],document,codeK, MAX_CHUNK_SIZE))
            current_chunk = {"document": document,"codeK" : codeK,"title": section, "content": ""}
            continue
        
        if not skip_section:
            current_chunk["content"] += section + "\n"

    # Ajouter le dernier chunk s'il est valide
    if current_chunk["title"] and current_chunk["content"].strip():
        document,codeK = get_document_info(catalogue_path)
        chunks.extend(split_large_chunk(current_chunk["title"], current_chunk["content"],document,codeK, MAX_CHUNK_SIZE))
    
    return chunks

def process_folder(base_folder, output_file):
    """Trouve fiche.md dans FRENCH/, récupère le titre et chunk le fichier en regroupant par fichier"""
    catalogue_path = os.path.join(base_folder, "catalogue.json")
    french_md_path = os.path.join(base_folder, "FRENCH", "fiche.md")

    if not os.path.exists(french_md_path):
        print(f"Fichier introuvable : {french_md_path}")
        return []

    chunks = chunk_markdown(french_md_path, catalogue_path)


    return chunks

def process_all_folders(base_folder, output_file):
    """Traite tous les dossiers sous 'base_folder' et fusionne les résultats dans un seul fichier"""
    all_chunks = []
    # Liste tous les dossiers dans "solutions"
    for folder_name in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder_name)
        if os.path.isdir(folder_path):
            print(f"Traitement du dossier : {folder_name}")
            folder_chunks = process_folder(folder_path, output_file)
            all_chunks.extend(folder_chunks)  # Ajoute directement les éléments dans la liste

    # Sauvegarde tout dans le fichier de sortie
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=4, ensure_ascii=False)

    print(f"Traitement terminé ! Tous les résultats sont dans {output_file}")

def processData(data):
    """Fusion de certains chunks du document pour la recherche."""

    documents_dict_content = {}
    documents_dict_codeK = {}
    for section in data:
        if section["document"] :
            doc_title = section["document"].strip()
            
            if doc_title != "Titre inconnu": 
                if doc_title not in documents_dict_content:
                    documents_dict_content[doc_title] = []
                    documents_dict_codeK[doc_title] = section["codeK"].strip()
                section_title = section["title"].strip()
                # Vérifier si le titre fait partie des sections à inclure
                # Cette partie peut être changé pour inclure d'autres sections ou exclure certaines
                if section_title in ["## Définition", "## Application", "## Bilan énergie"]:

                    content = section["content"].strip()
                    # Ajouter le contenu uniquement s'il n'est pas vide ou insignifiant
                    if content and content != "#":
                        documents_dict_content[doc_title].append(content)
    return documents_dict_content,documents_dict_codeK