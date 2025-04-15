from copy import deepcopy
import sys
from random import randint

from utils.read import read_trees
from parametros import DIFICULTIES, DINERO_INICIAL
from clases.arbol import Arbol


def erase_terminal():
    print("\n" * 100)


def print_title(title: str):
    print("-----------------------------")
    print(f"      {title}      ")
    print("-----------------------------")


def print_menu(options: list[str], choose_text: str, min: int, max: int):
    for i, option in enumerate(options):
        print(f"[{i+1}] {option}")
    print()

    while True:
        answer = input(choose_text)

        try:
            number = int(answer)
        except ValueError:
            print("El valor ingresado no es un número.")
            continue

        number = int(answer)

        if number < min or number > max:
            print(f"El número debe estar entre {min} y {max} inclusive.")
            continue

        return number


def get_number_in_range(text: str, min: int, max: int) -> int:
    while True:
        number = input(text)

        try:
            number = int(number)
        except ValueError:
            print("El valor ingresado no es un número.")
            continue

        if number < min or number > max:
            print(f"El número debe estar entre {min} y {max} inclusive.")
            continue

        return number


class Game:
    def __init__(self, player_tree: Arbol, enemy_tree: Arbol):
        self.player_tree = player_tree
        self.enemy_tree = enemy_tree
        self.dinero = DINERO_INICIAL
        self.round = 0

    def pasar_ronda(self):
        self.round += 1
        self.player_tree.pasar_ronda()
        self.enemy_tree.pasar_ronda()

    def loop(self):
        while True:
            erase_terminal()
            print_title("MENU PRINCIPAL")

            print(f"Dinero disponible: ${self.dinero}")
            print(f"Ronda actual: {self.round}")

            options = [
                "Atacar y pasar ronda",
                "Pasar ronda sin atacar",
                "Tienda",
                "Ver información del árbol",
                "Espiar al árbol enemigo",
                "Guardar partida",
                "Salir del juego",
            ]

            answer = print_menu(
                options,
                "Selecciona una opción: ",
                1,
                len(options),
            )

            if answer == 1:
                print(self.player_tree)

                player_choose = get_number_in_range(
                    "¿Con cuál rama quieres atacar? Ingrese el número de la rama: ",
                    1,
                    len(self.player_tree.branches),
                )

                branch = self.player_tree.branches[player_choose - 1]

                player_damage = self.player_tree.atacar(branch)

                print(
                    f"La rama [{self.player_tree.branches.index(branch)+1}] {branch.nombre} ha hecho {player_damage} de daño."
                )

                self.enemy_tree.recibir_dano(player_damage)

                enemy_choose = self.enemy_tree.branches[
                    randint(0, len(self.enemy_tree.branches) - 1)
                ]

                enemy_damage = self.enemy_tree.atacar(enemy_choose)

                print(
                    f"La rama enemiga [{self.enemy_tree.branches.index(enemy_choose)+1}] {enemy_choose.nombre} ha hecho {enemy_damage} de daño."
                )

                self.player_tree.recibir_dano(enemy_damage)

            if answer in (1, 2):
                print("Pasando ronda...")
                self.pasar_ronda()

            if answer == 4:
                print(self.player_tree)

            if answer == 5:
                print(self.enemy_tree.resumir_arbol())

            if answer == 7:
                print("Saliendo del juego, gracias por jugar.")
                return

            input("Presiona ENTER para continuar...")


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

    largest_name_size = max(len(tree.nombre) for tree in trees)

    answer = print_menu(
        [
            f"{tree.nombre} : {' ' * (largest_name_size - len(tree.nombre))} {len(tree.branches)} ramas"
            for tree in trees
        ],
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

    input("Presiona ENTER para continuar...")

    game = Game(player_tree, enemy_tree)

    game.loop()


if __name__ == "__main__":
    main()
