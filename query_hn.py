import sys
from src.hn import get_hn_posts
from sentence_transformers import SentenceTransformer

# Load the model
# model = SentenceTransformer("Linq-AI-Research/Linq-Embed-Mistral")
model = SentenceTransformer("intfloat/e5-small")

print("\n\n\n\n\n\n------------------------------------")
print("scraping posts")

PAGE_COUNT = int(sys.argv[2]) if len(sys.argv) >= 3 else 1
posts = []
for i in range(PAGE_COUNT):
    posts = posts + get_hn_posts(i + 1)

# Generate embeddings
print("creating embeddings")
for post in posts:
    if post.content:
        content_embedding = model.encode(post.content)
        post.embedding = content_embedding

def get_min_similarity_index(results):
    min_similarity = 1
    min_index = -1
    for i in range(len(results)):
        (similarity, _) = results[i]
        if similarity < min_similarity:
            min_index = i
            min_similarity = similarity
    return min_index



while True:
    print("\n\n\n\n\n\n------------------------------------")
    query = input("Query the data:")
    print('Query Processed')
    query_embedding = model.encode(query)

    print("\n\n\n\n\n\n------------------------------------")
    print('Comparing vector values')

    threshold_result_similarity = -1
    closest_post = None
    results_and_similarities = []
    result_count = 10

    for post in posts:
        if post.embedding is not None:
            similarity_tensor = model.similarity(query_embedding, post.embedding)
            similarity = similarity_tensor.item()
            if similarity > threshold_result_similarity:
                if len(results_and_similarities) > result_count:
                    results_and_similarities.pop(get_min_similarity_index(results_and_similarities))
                results_and_similarities.append((similarity, post))
                if len(results_and_similarities) > result_count:
                    threshold_result_similarity = results_and_similarities[get_min_similarity_index(results_and_similarities)][0]
    
    results_and_similarities.sort(key=lambda rs: rs[0], reverse=True)

    print("\n\n\n\n\n\n------------------------------------")
    print("Results:")
    if results_and_similarities:
        for (_, post) in results_and_similarities:
            print(post.title)
            print('\t' + post.href)
