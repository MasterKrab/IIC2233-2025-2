from pathlib import Path
from clases.arbol import Arbol
from clases.ramas import (
    Rama,
    Ficus,
    Celery,
    Hyedrid,
    Paalm,
    Alovelis,
    Pine,
    Cactoos,
)

from parametros import DATA_FOLDER, FILES_BY_DIFICULTIES


def create_id_generator():
    id = 0

    def increment_id():
        nonlocal id
        id += 1
        return id

    return increment_id


generate_id = create_id_generator()


def create_branch(name: str) -> Rama:
    for rama in (Ficus, Celery, Hyedrid, Paalm, Alovelis, Pine, Cactoos):
        if rama.nombre.lower() == name.lower():
            return rama(generate_id())


def read_branches(branches_text: str) -> list[Rama]:
    stack = []

    i = 0
    current = ""

    while i < len(branches_text):
        item = branches_text[i]

        if item == "{":
            text = ""

            i += 1

            while branches_text[i] not in "{};":
                text += branches_text[i]
                i += 1

            rama = create_branch(text)

            if stack:
                stack[-1].ramas_hijas.append(rama)

            stack.append(rama)
            current = ""
            continue

        if item not in "{};":
            current += item

        if item in "};":
            if current:
                stack[-1].ramas_hijas.append(create_branch(current))

            current = ""

        if item == "}":
            if len(stack) == 1:
                return stack[0]

            stack.pop(-1)

        i += 1


def read_trees(dificulty: str):
    trees = []

    with Path(DATA_FOLDER, FILES_BY_DIFICULTIES[dificulty]).open() as file:
        for line in file:
            name, branches_text = map(str.strip, line.split(":"))

            main_branch = read_branches(
                branches_text.replace(" ", "").replace("};", "}").replace(";{", "{")
            )

            tree = Arbol(main_branch, name)

            trees.append(tree)

    return trees
