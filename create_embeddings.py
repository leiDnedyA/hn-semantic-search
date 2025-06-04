from src.hn import get_hn_posts
from sentence_transformers import SentenceTransformer

# Load the model
# model = SentenceTransformer("Linq-AI-Research/Linq-Embed-Mistral")
model = SentenceTransformer("intfloat/e5-small")

print("\n\n\n\n\n\n------------------------------------")
print("scraping posts")
posts = get_hn_posts()

# Generate embeddings
print("creating embeddings")
for post in posts:
    if post.content:
        content_embedding = model.encode(post.content)
        post.embedding = content_embedding

print("\n\n\n\n\n\n------------------------------------")
query = input("Query the data:")
print('Query Processed')
query_embedding = model.encode(query)

print('Comparing vector values')
similarities = []
for post in posts:
    if post.__getattribute__('embedding') is not None:
        similarities.append(model.similarity(query_embedding, post.embedding))
    else:
        similarities.append(0)


print(similarities)
