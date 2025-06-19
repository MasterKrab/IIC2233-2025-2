import json
from pathlib import Path


def get_config(folder: str, name: str):
    with Path(folder, name).open(encoding="utf-8") as file:
        data = json.load(file)
        port = int(data["puerto"])
        host = data["host"]

    return port, host
