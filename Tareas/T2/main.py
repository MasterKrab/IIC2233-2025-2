from clases.game import Game

from utils.read import read_trees
from utils.terminal import print_title, continue_input
from utils.menu import print_menu
from utils.read_save import read_save

from parametros import DIFICULTIES, SAVES_FOLDER

from random import choice
from pathlib import Path
import sys


def main():
    dificulties_text = ", ".join(DIFICULTIES)

    if len(sys.argv) <= 1:
        print(
            f"Se debe específicar la dificultad ({dificulties_text}) o el nombre de un archivo de guardado."
        )
        print("Formato: python main.py [dificultad, archivo de guardado]")

        return

    dificulty_or_save_file = sys.argv[1].lower()

    is_save_file = Path(SAVES_FOLDER, dificulty_or_save_file).exists()

    if is_save_file:
        print("Leyendo partida guardada...")
        game = read_save(dificulty_or_save_file)
        print("¡Partida leída existosamente!")
        game.loop()
        return

    if dificulty_or_save_file not in DIFICULTIES and not is_save_file:
        print(
            f"El valor entregado no es una dificultad válida ni archivo de guardado "
            f"existente, las dificutades disponibles son {dificulties_text}."
        )
        return

    trees = read_trees(dificulty_or_save_file)

    print_title("SELECCIÓN INICIAL")

    answer = print_menu(
        [(tree.nombre, f"{len(tree.branches)} ramas") for tree in trees],
        "Selecciona el árbol guerrero: ",
        1,
        len(trees),
    )

    player_tree = trees[answer - 1].copy(1)

    print(
        f"Has seleccionado el árbol guerrero {player_tree.nombre} con "
        f"{len(player_tree.branches)} ramas."
    )

    print(player_tree.resumir_arbol())

    enemy_tree = choice(trees).copy(max(player_tree.branches_ids) + 1)

    print(
        f"El árbol enemigo es {enemy_tree.nombre} con {len(enemy_tree.branches)} ramas."
    )

    print(enemy_tree.resumir_arbol())

    print("¡Bienvenido a DCConquista de Yggdrasil!")

    continue_input()

    game = Game(player_tree, enemy_tree)

    game.loop()


if __name__ == "__main__":
    main()
