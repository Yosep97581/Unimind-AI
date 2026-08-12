from src.embeddings import create_embedding

vector = create_embedding("What is machine learning?")

print(len(vector))
print(vector[:10])