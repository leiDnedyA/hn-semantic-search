from bs4 import BeautifulSoup


def get_body_contents(html):
    soup = BeautifulSoup(html, 'html.parser')
    body_tag = soup.find('body')
    if body_tag:
        return body_tag.get_text()

