import requests
import itertools
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def get_full_url(url):
    if is_complete_url(url):
        return url
    return 'https://news.ycombinator.com/' + url

def is_complete_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def is_hn_site_link(link):
    url_data = urlparse(link)
    # Exception: links to a thread (e.g Show HN, Ask HN)
    if url_data.path and url_data.path.startswith('item'):
        return False
    if not is_complete_url(link):
        return True
    if url_data.hostname and "ycombinator.com" in url_data.hostname:
        return True
    return False
    
def get_links(html):
    links = []
    soup = BeautifulSoup(html, 'html.parser')
    a_tags = soup.find_all('a')
    for tag in a_tags:
        href = tag['href']
        if href and not is_hn_site_link(href):
            links.append(href)
    return links

def get_body_contents(html):
    soup = BeautifulSoup(html, 'html.parser')
    body_tag = soup.find('body')
    if body_tag:
        return body_tag.get_text()

def get_hn_posts(page=0):
    r = None
    if page:
        r = requests.get(f"https://news.ycombinator.com/?p={page}")
    else:
        r = requests.get("https://news.ycombinator.com/")

    links = get_links(r.text)
    links = list(map(get_full_url, links))
    return links

for link in get_hn_posts():
    print(link)

