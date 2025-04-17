from copy import deepcopy
from parametros import DINERO_INICIAL, GANANCIA_POR_RONDA

from clases.arbol import Arbol
from clases.modificador import ModificadorPositivo

from utils.terminal import erase_terminal, print_title, continue_input
from utils.menu import print_menu, get_number_in_set

from utils.save_game import save_game

from random import randint


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

                player_choose = get_number_in_set(
                    "¿Con cuál rama quieres atacar? Ingrese el número de la rama: ",
                    self.player_tree.branches_ids,
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
                continue

            if answer == 4:
                print(self.player_tree)

            if answer == 5:
                print(self.enemy_tree.resumir_arbol())

            if answer == 6:
                print("Guardando partida...")
                save_game(
                    self.dinero,
                    self.round,
                    self.player_tree,
                    self.enemy_tree,
                    "save.txt",
                )
                print("Partida guardada!")

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

            modifier = deepcopy(modifiers[answer - 1])

            if self.dinero >= modifier.precio:
                self.dinero -= modifier.precio

                print(f"Has comprado el modificador {modifier.nombre}.")

                print(self.player_tree)

                branch_choose = get_number_in_set(
                    "Ingrese el número de la rama a la que quieres aplicar el modificador: ",
                    self.player_tree.branches_ids,
                )

                branch = self.player_tree.branches[branch_choose - 1]

                self.player_tree.cargar_modificador(branch, deepcopy(modifier))

            else:
                print("No tienes suficiente dinero para comprar este modificador.")

            continue_input()
