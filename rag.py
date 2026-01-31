import os
from langchain_ollama import OllamaEmbeddings
from qdrant_client import QdrantClient
import ollama
from dotenv import load_dotenv

load_dotenv()

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)
collection_name = os.getenv("QDRANT_COLLECTION")

embeddings = OllamaEmbeddings(model="mxbai-embed-large")

def answer_question(question: str) -> str:
    try:
       
        question_vector = embeddings.embed_query(question)
        
        
        search_results = client.query_points(
            collection_name=collection_name,
            query=question_vector,
            limit=3,
            with_payload=True
        )
        
       
        if not search_results or not search_results.points:
            return "I don't know."
        
       
        context_chunks = []
        for point in search_results.points:
            if point.payload and "page_content" in point.payload:
                context_chunks.append(point.payload["page_content"])
        
        
        if not context_chunks:
            return "I don't know."
        
        
        context = "\n\n".join(context_chunks)
        
        
        prompt = f"""Based on the provided context, answer the question directly. If you can reasonably infer the answer from the context, provide it. Only respond with "I don't know" if the context contains no relevant information.

Context:
{context}

Question: {question}

Answer:"""

        response = ollama.chat(
            model="llama3.2:1b",
            messages=[{"role": "user", "content": prompt}]
        )

        return response["message"]["content"]
        
    except Exception as e:
        print(f"Error in answer_question: {e}")
        return "I don't know."