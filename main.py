from src.hn import get_hn_post_urls

for link in get_hn_post_urls(3):
    print(link)
