from copy import deepcopy
import sys
from random import randint

from clases.game import Game
from utils.read import read_trees
from utils.terminal import print_title, continue_input
from utils.menu import print_menu
from parametros import DIFICULTIES


def main():
    dificulties_text = ", ".join(DIFICULTIES)

    if len(sys.argv) <= 1:
        print(f"Se debe específicar la dificultad ({dificulties_text}).")
        print("Formato: python main.py [dificultad]")
        return

    dificulty = sys.argv[1].lower()

    if dificulty not in DIFICULTIES:
        print(f"La dificultad no existe, las disponibles son {dificulties_text}.")
        return

    trees = read_trees(dificulty)

    print_title("SELECCIÓN INICIAL")

    answer = print_menu(
        [(tree.nombre, f"{len(tree.branches)} ramas") for tree in trees],
        "Selecciona el árbol guerrero: ",
        1,
        len(trees),
    )

    player_tree = deepcopy(trees[answer - 1])

    print(
        f"Has seleccionado el árbol guerrero {player_tree.nombre} con {len(player_tree.branches)} ramas."
    )

    enemy_tree = deepcopy(trees[randint(0, len(trees) - 1)])

    print(
        f"El árbol enemigo es {enemy_tree.nombre} con {len(enemy_tree.branches)} ramas."
    )

    continue_input()

    game = Game(player_tree, enemy_tree)

    game.loop()


if __name__ == "__main__":
    main()
