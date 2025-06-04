import numpy as np
from src.cache import load_embeddings, load_posts
from src.hn import Post, get_hn_posts
from sentence_transformers import SentenceTransformer

# Load the model
# model = SentenceTransformer("Linq-AI-Research/Linq-Embed-Mistral")
model = SentenceTransformer("intfloat/e5-small")

def get_min_similarity_index(results):
    min_similarity = 1
    min_index = -1
    for i in range(len(results)):
        (similarity, _) = results[i]
        if similarity < min_similarity:
            min_index = i
            min_similarity = similarity
    return min_index

raw_posts = load_embeddings()
posts = []
for raw_post in raw_posts:
    post = Post(raw_post["title"], raw_post["href"])
    post.content = raw_post["content"]
    post.embedding = np.array(raw_post["embedding"], dtype=np.float32)
    posts.append(post)

def query_hn(query):
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
    results = [result[1] for result in results_and_similarities]
    return results


while True:
    print("\n\n\n\n\n\n------------------------------------")
    query = input("Query the data:")
    results = query_hn(query)

    print('Query Processed')

    print("\n\n\n\n\n\n------------------------------------")
    print("Results:")
    if results:
        for post in results:
            print(post.title)
            print('\t' + post.href)
