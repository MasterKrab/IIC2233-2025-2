from clases.arbol import Arbol
from clases.ramas import Rama, get_branch_class

from utils.input import read_input

from parametros import DATA_FOLDER, FILES_BY_DIFICULTIES

from pathlib import Path


def create_branch(name: str, id: int) -> Rama:
    branch = get_branch_class(name)

    return branch(id)


def read_branches(branches_text: str, id_start: int) -> Rama:
    stack = []

    id = id_start

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

            rama = create_branch(text, id)
            id += 1

            if stack:
                stack[-1].ramas_hijas.append(rama)

            stack.append(rama)
            current = ""
            continue

        if item not in "{};":
            current += item

        if item in "};":
            if current:
                stack[-1].ramas_hijas.append(create_branch(current, id))
                id += 1

            current = ""

        if item == "}":
            if len(stack) == 1:
                return stack[0]

            stack.pop(-1)

        i += 1


def read_trees(dificulty: str) -> list[Arbol]:
    trees = []

    id = 1

    with Path(DATA_FOLDER, FILES_BY_DIFICULTIES[dificulty]).open() as file:
        for line in file:
            name, branches_text = read_input([str, str], ":", line)

            main_branch = read_branches(
                branches_text.replace(" ", "").replace("};", "}").replace(";{", "{"),
                id,
            )

            tree = Arbol(main_branch, name)

            id = max(tree.branches_ids) + 1
            trees.append(tree)

    return trees
