import json
import urllib.request
import urllib.error
from collections import namedtuple

UpdateCheckResult = namedtuple("UpdateCheckResult", ["status", "url"])

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

def is_newer(remote, local):
    remote = remote.lstrip("v").split("-")[0]
    local = local.lstrip("v").split("-")[0]

    remote_parts = remote.split(".")
    local_parts = local.split(".")

    max_len = max(len(remote_parts), len(local_parts))
    remote_parts += ["0"] * (max_len - len(remote_parts))
    local_parts += ["0"] * (max_len - len(local_parts))

    try:
        remote_nums = [int(x) for x in remote_parts]
        local_nums = [int(x) for x in local_parts]
    except ValueError:
        return False

    return remote_nums > local_nums

def check_for_updates(current_version):
    latest_version, release_url = get_latest_release()
    if latest_version is None:
        return UpdateCheckResult("error", None)

    if is_newer(latest_version, current_version):
        return UpdateCheckResult("update_available", release_url)
    else:
        return UpdateCheckResult("up_to_date", None)