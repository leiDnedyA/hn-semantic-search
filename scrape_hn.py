import sys
from src.cache import save_embeddings
from src.hn import get_hn_posts
from sentence_transformers import SentenceTransformer

# Load the model
# model = SentenceTransformer("Linq-AI-Research/Linq-Embed-Mistral")
model = SentenceTransformer("intfloat/e5-small")

PAGE_COUNT = int(sys.argv[1]) if len(sys.argv) >= 2 else 1
print("\n\n\n\n\n\n------------------------------------")
print(f"scraping {PAGE_COUNT} pages of posts...")

posts = []
for i in range(PAGE_COUNT):
    posts = posts + get_hn_posts(i + 1)

# Generate embeddings
print("creating embeddings")
embedded_posts = []
for post in posts:
    if post.content:
        content_embedding = model.encode(post.content)
        post.embedding = content_embedding.tolist()
        embedded_posts.append(post)

print(f"Success! Saving {len(embedded_posts)} embeddings to json cache.")
save_embeddings(list({
    "title": post.title,
    "href": post.href,
    "embedding": post.embedding,
    "content": post.content
} for post in embedded_posts))
