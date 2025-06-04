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
