import chromadb
from chromadb.utils import embedding_functions
from uuid import uuid4


chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(
name="email_memory",
embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
)


def add_to_memory(email_text):
uid = str(uuid4())
collection.add(documents=[email_text], ids=[uid])
return uid


def check_duplicate(email_text):
results = collection.query(query_texts=[email_text], n_results=1)
if results["documents"] and results["distances"][0][0] < 0.1:
return True # Similar email already exists
return False