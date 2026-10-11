import numpy as np
from fastembed import TextEmbedding
import faiss
import json

documents = json.loads(open('to_embed.json', 'r').read())
index_data = json.loads(open("index.json", "r").read())

embedding_model = TextEmbedding()
faiss_index = faiss.read_index("vectors.faiss")

def search(query):
    # da search begins
    query_vector = embedding_model.embed([query])
    k = 3  # Number of nearest neighbors to retrieve
    distances, indices = faiss_index.search(np.array(list(query_vector), dtype=np.float32), k)
    # Print the most similar documents
    for i, index in enumerate(indices[0]):
        distance = distances[0][i]
        print(f"Nearest neighbor {i+1}: {index_data[index]["url"]}, Distance {distance}")

while True:
    q = input("Search (q to exit): ")
    if q == "q":
        break
    search(q)