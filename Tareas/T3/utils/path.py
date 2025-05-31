from os.path import join
from pathlib import Path

from utils.list import flatten


def normalize_path(path: str) -> Path:
    def normalize(path: str) -> str:
        if "/" in path:
            return [normalize(part) for part in path.split("/")]

        if "\\" in path:
            return [normalize(part) for part in path.split("\\")]

        return [path]

    return join(*flatten(normalize(path.strip().strip("/").strip("\\"))))
