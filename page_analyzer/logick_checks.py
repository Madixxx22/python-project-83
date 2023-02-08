import requests


def check_response(url: str):
    info = {}
    try:
        req = requests.get(url)
        info["status_code"] = req.status_code
        info["error"] = False
        return info
    except requests.exceptions.ConnectionError:
        info["error"] = True
        return info
