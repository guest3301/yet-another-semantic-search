import numpy as np
from fastembed import TextEmbedding
import faiss

import json

with open('to_embed.json', 'r') as r:
    documents = json.loads(r.read())

embedding_model = TextEmbedding()
embeddings_generator = embedding_model.embed(documents)
embeddings_list = list(embeddings_generator)
print(embeddings_list[0], documents[0])

vectors = np.array(embeddings_list)
num_vectors = len(embeddings_list)
dim = len(embeddings_list[0])


faiss_index = faiss.IndexFlatIP(dim)  # Inner product for cosine similarity
# Add vectors to the FAISS index
faiss_index.add(np.array(embeddings_list, dtype=np.float32))
faiss.write_index(faiss_index, "vectors.faiss")

