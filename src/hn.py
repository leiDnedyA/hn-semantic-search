from typing import Any, List, Dict
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests

from src.scrape import get_plaintext_from_url
from .url import is_complete_url, get_full_url
from .cache import load_posts, save_posts

ignore_urls = {'https://github.com/HackerNews/API'}

def post_to_dict(post):
    return {
        'href': post.href,
        'title': post.title,
        'content': post.content
    }

class Post:
    embedding: Any = None
    title: str
    href: str
    content: str | None
    def __str__(self) -> str:
        return f'title: {self.title}\n\n' + f'href: {self.href}\n\n' + f'content: \n\n"""{self.content}"""'
    def __init__(self, title, href, content=None):
        self.title = title
        self.href = href
        self.content = content

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
            posts.append(Post(tag.get_text(), href))
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
    links = list(map(lambda post: Post(post.title, get_full_url(post.href)), links))
    links = list(map(get_hn_post_with_content, links))
    return links

def get_hn_post_with_content(post: Post) -> Post:
    return Post(post.title, post.href, get_plaintext_from_url(post.href))

def get_hn_posts(page=0) -> List[Post]:
    """Scrape Hacker News posts for *page* and cache them.

    1. Previously cached posts are loaded from the JSON cache file.
    2. Newly scraped links that are already cached (based on ``href``) are
       skipped.
    3. The remaining new posts are fetched for their full content.
    4. Both newly scraped posts and existing cached posts are persisted back to
       disk.

    Only **new** posts (i.e. ones not already cached) are returned so that
    downstream code only processes fresh data.
    """

    # Load existing cache data and build a quick-lookup set of hrefs
    cached_posts: List[Dict[str, str]] = load_posts()
    cached_hrefs = {p.get("href") for p in cached_posts}

    # Step 1: scrape links visible on the requested page
    scraped_posts = get_hn_post_urls(page)

    # Step 2: filter out posts we have already cached
    new_posts = [p for p in scraped_posts if p.href not in cached_hrefs]

    # Step 3: fetch content for the new posts only
    new_posts_with_content = list(map(get_hn_post_with_content, new_posts))

    all_posts = []
    seen_hrefs = set()
    for post in new_posts_with_content:
        if post.href not in seen_hrefs:
            all_posts.append(post)
            seen_hrefs.add(post.href)
    for post in cached_posts:
        if post['href'] not in seen_hrefs:
            all_posts.append(Post(post['title'], post['href'], post['content']))
            seen_hrefs.add(post['href'])

    if new_posts_with_content:
        save_posts(list(map(post_to_dict, all_posts)))

    # Return only the newly scraped posts to the caller
    return all_posts
