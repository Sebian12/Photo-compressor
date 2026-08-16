import json
import urllib.request
import urllib.error

def get_latest_release():
    url = "https://api.github.com/repos/Sebian12/SnapPress/releases/latest"
    req = urllib.request.Request(url, headers={"User-Agent": "SnapPress-UpdateChecker"})

    try:
        response = urllib.request.urlopen(req, timeout=5)
        data = response.read()
        parsed = json.loads(data)
        return parsed["tag_name"], parsed["html_url"]
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError):
        return None, None