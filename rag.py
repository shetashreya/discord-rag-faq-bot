import os
from langchain_ollama import OllamaEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
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
        # Get embedding for the question
        question_embedding = embeddings.embed_query(question)
        
        # Search in Qdrant using scroll to get all points first
        points, _ = client.scroll(
            collection_name=collection_name,
            limit=100
        )
        
        if not points:
            return "I don't know. This information is not in the provided documents."
        
        # For now, let's just use the first few documents
        # In a production system, you'd implement proper similarity search
        context_parts = []
        for point in points[:3]:  # Take first 3 documents
            if hasattr(point, 'payload') and 'page_content' in point.payload:
                content = point.payload['page_content']
                if question.lower() in content.lower():  # Simple keyword matching
                    context_parts.append(content)
        
        # If no keyword matches, use first few documents
        if not context_parts:
            for point in points[:3]:
                if hasattr(point, 'payload') and 'page_content' in point.payload:
                    context_parts.append(point.payload['page_content'])
        
        context = "\n\n".join(context_parts)
        
        if not context.strip():
            return "I don't know. This information is not in the provided documents."

        prompt = f"""You are an AI assistant for the AI Bootcamp.
Answer ONLY using the context below.
If the answer is not present, say you do not know.

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
        return f"Error: {str(e)}"