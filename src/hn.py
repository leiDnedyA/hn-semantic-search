from urllib.parse import urlparse

from bs4 import BeautifulSoup
from .url import is_complete_url, get_full_url
import requests

ignore_urls = {'https://github.com/HackerNews/API'}

def _get_hn_post_links(html):
    posts = []
    soup = BeautifulSoup(html, 'html.parser')
    a_tags = soup.find_all('a')
    for tag in a_tags:
        href = tag['href']
        parent_class = tag.parent.get('class') 
        if parent_class and ('age' in parent_class or 'subline' in parent_class):
            continue
        if href and href in ignore_urls:
            continue
        if href and not _is_hn_site_link(href):
            posts.append((tag.get_text(), href))
    return posts

def _is_hn_site_link(link):
    url_data = urlparse(link)
    # Exception: links to a thread (e.g Show HN, Ask HN)
    if url_data.path and url_data.path.startswith('item'):
        return False
    if not is_complete_url(link):
        return True
    if url_data.hostname and "ycombinator.com" in url_data.hostname:
        return True
    return False


def get_hn_post_urls(page=0):
    r = None
    if page:
        r = requests.get(f"https://news.ycombinator.com/?p={page}")
    else:
        r = requests.get("https://news.ycombinator.com/")

    links = _get_hn_post_links(r.text)
    links = list(map(lambda post: (post[0], get_full_url(post[1])), links))
    return links
