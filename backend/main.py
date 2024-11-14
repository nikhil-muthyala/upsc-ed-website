# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import faiss
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from data_preprocessing import create_faiss_index

app = FastAPI()

# Load the RAG model and tokenizer
model_name = "sentence-transformers/all-MiniLM-L6-v2"  # Replace with your chosen model if needed
rag_tokenizer = AutoTokenizer.from_pretrained(model_name)
rag_model = AutoModelForCausalLM.from_pretrained(model_name)

# Load the FAISS index
faiss_index, documents = create_faiss_index()

class Query(BaseModel):
    question: str
    response_format: int  # 1 for short, 2 for detailed, 3 for with links

@app.post("/ask")
def ask_question(query: Query):
    """Answer a question using the RAG model."""
    question = query.question
    response_format = query.response_format

    # Embed the question for retrieval
    question_embedding = rag_tokenizer(question, return_tensors="pt")
    with torch.no_grad():
        question_embedding = rag_model(**question_embedding).pooler_output.cpu().numpy()

    # Perform FAISS search to find relevant document
    _, doc_index = faiss_index.search(np.array([question_embedding.squeeze()]), k=1)
    context = documents[doc_index[0][0]]

    # Generate response based on response format
    if response_format == 1:
        answer = f"Short answer: {context[:100]}..."  # Placeholder for short response
    elif response_format == 2:
        answer = f"Intro: {context[:50]}... Body: {context[50:150]}... Conclusion: {context[150:200]}..."
    elif response_format == 3:
        answer = f"{context[:150]}... For more, check sources like [example link](https://example.com)."
    else:
        raise HTTPException(status_code=400, detail="Invalid response format")

    return {"answer": answer}
