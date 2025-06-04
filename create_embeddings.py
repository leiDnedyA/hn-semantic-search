from src.hn import get_hn_posts
from sentence_transformers import SentenceTransformer

# Load the model
model = SentenceTransformer("Linq-AI-Research/Linq-Embed-Mistral")

posts = get_hn_posts()

# Generate embeddings
for post in posts:
    if post.content:
        content_embedding = model.encode(post.content)
        post.embedding = content_embedding

query = input("Query the data:")
query_embedding = model.encode(query)

similarities = []
for post in posts:
    if post.embedding:
        similarities.append(model.similarity(query_embedding, post.embedding))
    else:
        similarities.append(0)


print(similarities)
