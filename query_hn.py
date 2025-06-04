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

print("\n\n\n\n\n\n------------------------------------")
print('Comparing vector values')
max_similarity = -1
closest_post = None
for i in range(len(posts)):
    post = posts[i]
    if post.embedding is not None:
        similarity_tensor = model.similarity(query_embedding, post.embedding)
        similarity = similarity_tensor.item()
        if similarity > max_similarity:
            max_similarity = similarity
            closest_post = post

print("\n\n\n\n\n\n------------------------------------")
print("Result!:")
if closest_post:
    print(closest_post.title, closest_post.href)
