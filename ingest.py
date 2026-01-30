import os
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import Qdrant
from dotenv import load_dotenv
load_dotenv()

DATA_DIR = "data"

# Qdrant
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

collection_name = os.getenv("QDRANT_COLLECTION")

# Embeddings (local)
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# Delete collection if it exists
try:
    client.delete_collection(collection_name)
    print(f"Deleted existing collection: {collection_name}")
except:
    print(f"Collection {collection_name} doesn't exist, creating new one")

# Create collection
client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
)

documents = []

for file in os.listdir(DATA_DIR):
    if file.endswith(".pdf"):
        loader = PyPDFLoader(os.path.join(DATA_DIR, file))
        docs = loader.load()
        for d in docs:
            d.metadata["source"] = file
        documents.extend(docs)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)

chunks = splitter.split_documents(documents)

# Create vector store
vectorstore = Qdrant(
    client=client,
    collection_name=collection_name,
    embeddings=embeddings
)

# Add documents
vectorstore.add_documents(chunks)

print("✅ Documents ingested into Qdrant")
