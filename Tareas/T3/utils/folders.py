from os.path import join, isdir
from os import listdir, getcwd


def search_folders(path: str) -> list[str]:
    base = join(getcwd(), path)

    def search(path: str) -> list[str]:
        if not isdir(path):
            return []

        folders = [path[len(base) + 1 :]] if path != base else []

        for item in listdir(path):
            folders = [*folders, *search(join(path, item))]

        return folders

    folders = search(base)

    return folders
