from copy import deepcopy
import sys
from random import randint

from utils.read import read_trees
from parametros import DIFICULTIES, DINERO_INICIAL, GANANCIA_POR_RONDA
from clases.arbol import Arbol
from clases.modificador import ModificadorPositivo


def erase_terminal():
    print("\n" * 100)


def print_title(title: str, lateral_space: int = 10):

    bar = "-" * (len(title) + 2 * lateral_space)

    lateral_space_text = " " * lateral_space

    print(bar)
    print(f"{lateral_space_text}{title}{lateral_space_text}")
    print(bar)


def create_table(
    table: list[str, str],
):
    largest_size = max(len(row[0]) for row in table) + len(str(len(table)))

    rows = []

    for i in range(len(table)):
        separation = " " * (largest_size - len(table[i][0]) - len(str(i + 1)))

        rows.append(f"[{i+1}] {table[i][0]} {separation}: {table[i][1]}")

    return "\n".join(rows)


def continue_input():
    input("Presiona ENTER para continuar...")


def print_menu(
    table: list[str, str] | list[str],
    choose_text: str,
    min: int,
    max: int,
    exit_text: str = None,
):

    if isinstance(table[0], str):
        for i in range(len(table)):
            print(f"[{i+1}] {table[i]}")
    else:
        print(create_table(table))

    if exit_text:
        print(f"[{len(table) + 1}] {exit_text}")

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
                    f"La rama [{branch.id}] {branch.nombre} ha hecho {player_damage} de daño."
                )

                self.enemy_tree.recibir_dano(player_damage)

                enemy_choose = self.enemy_tree.branches[
                    randint(0, len(self.enemy_tree.branches) - 1)
                ]

                enemy_damage = self.enemy_tree.atacar(enemy_choose)

                print(
                    f"La rama [{enemy_choose.id}] {enemy_choose.nombre} ha hecho {enemy_damage} de daño."
                )

                self.player_tree.recibir_dano(enemy_damage)

            if answer in (1, 2):
                print("Pasando ronda...")
                self.pasar_ronda()
                self.dinero += GANANCIA_POR_RONDA
                print(f"Ganancia por ronda: ${GANANCIA_POR_RONDA}")

            if answer == 3:
                self.store()

            if answer == 4:
                print(self.player_tree)

            if answer == 5:
                print(self.enemy_tree.resumir_arbol())

            if answer == 7:
                print("Saliendo del juego, gracias por jugar.")
                return

            continue_input()

    def store(self):
        modifiers = [
            ModificadorPositivo(name) for name in ModificadorPositivo.get_modifiers()
        ]

        options = [(modifier.nombre, f"${modifier.precio}") for modifier in modifiers]

        while True:
            erase_terminal()
            print_title("TIENDA")

            print(f"Dinero disponible: ${self.dinero}")

            answer = print_menu(
                options,
                "Selecciona una opción: ",
                1,
                len(options) + 1,
                "Volver al menú principal",
            )

            if answer == len(options) + 1:
                break

            modifier = modifiers[answer - 1]

            if self.dinero >= modifier.precio:
                self.dinero -= modifier.precio

                print(f"Has comprado el modificador {modifier.nombre}.")

                print(self.player_tree)

                branch_choose = get_number_in_range(
                    "Ingrese el número de la rama a la que quieres aplicar el modificador: ",
                    1,
                    len(self.player_tree.branches),
                )

                branch = self.player_tree.branches[branch_choose - 1]

                self.player_tree.cargar_modificador(branch, modifier)

            else:
                print("No tienes suficiente dinero para comprar este modificador.")

            continue_input()


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
