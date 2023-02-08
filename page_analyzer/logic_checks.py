import requests
from bs4 import BeautifulSoup


def find(find_element: str, soup: BeautifulSoup) -> str:
    if isinstance(find_element, dict):
        find_tag = soup.find(find_element['elem'],
                             attrs={'name': find_element['name']})
        if find_tag is None:
            item = ''
        else:
            item = find_tag['content']
    else:
        item = soup.find(find_element)
        if item is None:
            item = ''
        else:
            item = item.text
    return item


def check_response(url: str) -> dict:
    info = {}
    try:
        req = requests.get(url)
        info["status_code"] = req.status_code
        info["error"] = False
        page = req.text
        soup = BeautifulSoup(page, 'html.parser')
        find_elements = ['h1', 'title',
                         {'elem': 'meta', 'name': 'description'}]
        for i in find_elements:
            if isinstance(i, dict):
                info[i['elem']] = find(i, soup)
            else:
                info[i] = find(i, soup)
        return info
    except requests.exceptions.ConnectionError:
        info["error"] = True
        return info
