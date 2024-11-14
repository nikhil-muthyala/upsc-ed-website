# data_preprocessing.py
import os
import fitz  # PyMuPDF for PDF processing
import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch

# Load tokenizer and model for embeddings
model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def embed_text(text):
    """Embed text using a transformer model."""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=512)
    with torch.no_grad():
        embeddings = model(**inputs).pooler_output
    return embeddings.squeeze().cpu().numpy()

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file using PyMuPDF."""
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            text += page.get_text("text")
    return text

def create_faiss_index(documents_path="documents/"):
    """Process documents and create FAISS index."""
    documents = []
    embeddings = []

    for file_name in os.listdir(documents_path):
        file_path = os.path.join(documents_path, file_name)
        
        if file_name.endswith(".pdf"):
            # Extract text from PDF files
            content = extract_text_from_pdf(file_path)
        elif file_name.endswith(".txt"):
            # Read text from text files
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            continue  # Skip non-supported files

        documents.append(content)
        embeddings.append(embed_text(content))

    # Convert embeddings to a numpy array for FAISS
    dimension = embeddings[0].shape[0]
    faiss_index = faiss.IndexFlatL2(dimension)
    faiss_index.add(np.array(embeddings))
    
    return faiss_index, documents

# Run only if this is the main module
if __name__ == "__main__":
    faiss_index, documents = create_faiss_index()
    print("FAISS index created with", len(documents), "documents.")
