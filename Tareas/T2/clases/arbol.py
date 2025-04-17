from clases.ramas import Rama
from clases.modificador import Modificador

from utils.id import create_id_generator

from copy import deepcopy
from random import choice
from typing import Self


class Arbol:

    def __init__(self, rama_principal: Rama, nombre: str):
        self.rama_principal = rama_principal
        self.nombre = nombre

    def cargar_modificador(self, rama: Rama, modificador: Modificador):
        rama.cargar_modificador(modificador)

    def atacar(self, rama: Rama):
        return rama.atacar()

    def pasar_ronda(self):
        for rama in self.branches:
            rama.pasar_ronda()

    def presentarse(self):
        text = ""

        text += "------------------------------\n"
        text += f"{self.nombre}\n"
        text += "------------------------------\n"

        def mostrar_rama(rama: Rama, level: int = 0) -> str:
            text = "  " * level + f"[{rama.id}] {rama}\n"

            if not rama.ramas_hijas:
                return text

            text += "  " * (level + 1) + "\--subramas-\n"

            for rama_hija in rama.ramas_hijas:
                text += mostrar_rama(rama_hija, level + 1)

            return text

        return text + mostrar_rama(self.rama_principal)

    def __str__(self):
        return self.presentarse()

    def __repr__(self):
        return self.presentarse()

    @property
    def branches(self) -> list[Rama]:
        def get_branches(rama: Rama):
            branches = [rama]

            for rama_hija in rama.ramas_hijas:
                branches = [*branches, *get_branches(rama_hija)]

            return branches

        return get_branches(self.rama_principal)

    @property
    def branches_by_level(self) -> list[tuple[int, Rama]]:
        def get_branches(rama: Rama, level: int = 1):
            branches = [(level, rama)]

            for rama_hija in rama.ramas_hijas:
                branches = [*branches, *get_branches(rama_hija, level + 1)]

            return branches

        return get_branches(self.rama_principal)

    @property
    def max_deep(self) -> int:
        return max([branch[0] for branch in self.branches_by_level])

    @property
    def branches_ids(self) -> set[int]:
        ids = set()

        for branch in self.branches:
            ids.add(branch.id)

        return ids

    def get_random_deeper_branch(self) -> Rama:
        deeper_branches = []

        for branch in self.branches_by_level:
            if branch[0] == self.max_deep:
                deeper_branches.append(branch[1])

        return choice(deeper_branches)

    def find_parent(self, target_branch: Rama) -> Rama | None:
        def find_parent(rama: Rama):
            if rama == target_branch:
                return None

            if target_branch in rama.ramas_hijas:
                return rama

            for rama_hija in rama.ramas_hijas:
                parent = find_parent(rama_hija)

                if parent is not None:
                    return parent

            return None

        return find_parent(self.rama_principal)

    def find_by_id(self, id: int) -> Rama | None:
        for branch in self.branches:
            if branch.id == id:
                return branch

        return None

    def remove_branch(self, target_branch: Rama):
        if target_branch == self.rama_principal:
            self.rama_principal = None
            return

        parent = self.find_parent(target_branch)

        if parent is None:
            raise ValueError("La rama no está en el árbol.")

        parent.ramas_hijas.remove(target_branch)

    def recibir_dano(self, dano: int):
        branch = self.get_random_deeper_branch()

        print(f"La rama [{branch.id}] {branch.nombre} ha sido atacada.")

        while branch and dano > 0:
            dano = branch.recibir_dano(dano)
            branch = self.find_parent(branch)

        for branch in self.branches:
            if branch.salud == 0:
                print(f"La rama [{branch.id}] {branch.nombre} ha muerto.")
                self.remove_branch(branch)

    def resumir_arbol(self) -> str:
        total_health = 0
        total_damage = 0

        for branch in self.branches:
            total_health += branch.salud
            total_damage += branch.atacar()

        average_damage = total_damage / len(self.branches)

        return f"{self.nombre}, {len(self.branches)} ramas, {total_health} salud, {average_damage} daño promedio, {self.max_deep} profundida máxima."

    def copy(self, id_start) -> Self:
        generate_id = create_id_generator(id_start)

        tree_copy = deepcopy(self)

        for branch in tree_copy.branches:
            branch.id = generate_id()

        return tree_copy
