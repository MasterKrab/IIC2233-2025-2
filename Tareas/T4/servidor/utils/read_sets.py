from pathlib import Path
from os import listdir
from os.path import isfile
from servidor.parametros import SETS_FOLDER


def read_sets():
    files = listdir(SETS_FOLDER)

    sets = []

    for file_name in files:
        file_path = Path(SETS_FOLDER, file_name)

        if not isfile(file_path) or not file_name.endswith(".txt"):
            continue

        with file_path.open(encoding="utf-8") as file:
            lines = file.readlines()

        name = file_name[:-4]
        description = lines[0].strip()

        words_amount = len(lines) - 1

        sets.append(
            {"name": name, "description": description, "words_amount": words_amount}
        )

    return sets
