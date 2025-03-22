import utilidades
from pathlib import Path
from collections import deque


# Files constants
READ_FOLDER = "data"
WRITE_FOLDER = "visualizaciones"

# Messages
NOT_ALLOWED = "No permitido"
DONE = "Realizado"
NOT_FOUND = "No encontrado"

# Actions
MODIFY_FLOWER = "Modificar Flor"
REMOVE_NODE = "Quitar Nodo"


class Bonsai:
    def __init__(
        self, identificador: str, costo_corte: int, costo_flor: int, estructura: list
    ) -> None:
        self.identificador = identificador
        self.costo_corte = costo_corte
        self.costo_flor = costo_flor
        self.estructura = estructura

    def cargar_bonsai_de_archivo(self, carpeta: str, archivo: str) -> None:
        path = Path(READ_FOLDER, carpeta, archivo)

        with path.open(mode="r", encoding="utf-8") as file:
            for line in file:
                id, hasFlowerText, canEditText, childsText = line.strip().split(",")

                hasFlower = hasFlowerText == "T"
                canEdit = canEditText == "T"
                childs = childsText.split(";")

                node = [id, hasFlower, canEdit, childs]

                self.estructura.append(node)

    def visualizar_bonsai(
        self, orientacion: str, emojis: bool, guardar_archivo: bool
    ) -> None:
        visualization = utilidades.visualizar_bonsai(
            self.estructura, orientacion, emojis, guardar_archivo
        )

        # Nothing to save, visualization is None
        if not guardar_archivo:
            return

        path = Path(WRITE_FOLDER, f"{self.identificador}.txt")

        with path.open(mode="w+", encoding="utf-8") as file:
            file.write(visualization)

    def find_node_index(self, id: int) -> int | None:
        for i in range(len(self.estructura)):
            if self.estructura[i][0] == id:
                return i

        return None

    def find_node(self, id: str) -> list | None:
        for node in self.estructura:
            if node[0] == id:
                return node

        return None

    def find_parent(self, id: str) -> list | None:
        for node in self.estructura:
            if id in node[3]:
                return node

        return None

    def remove_node(self, id: str) -> None:
        index = self.find_node_index(id)

        self.estructura.pop(index)

        parent = self.find_parent(id)

        if parent is None:
            return

        for i in range(2):
            if parent[3][i] == id:
                parent[3][i] = "0"

    def copy(self):
        tree = Bonsai(self.identificador, self.costo_corte, self.costo_flor, [])

        for *data, childs in self.estructura:
            tree.estructura.append([*data, [*childs]])

        return tree


class DCCortaRamas:
    def modificar_nodo(self, bonsai: Bonsai, identificador: str) -> str:
        node = bonsai.find_node(identificador)

        if node is None:
            return NOT_FOUND

        if not node[2]:
            return NOT_ALLOWED

        node[1] = not node[1]
        return DONE

    def quitar_nodo(self, bonsai: Bonsai, identificador: str) -> str:
        to_search = [identificador]
        nodes_to_remove = set()

        while to_search:
            node_id_to_remove = to_search.pop()

            if node_id_to_remove == "0":
                continue

            nodes_to_remove.add(node_id_to_remove)

            node = bonsai.find_node(node_id_to_remove)

            if node is None:
                return NOT_FOUND

            if not node[2]:
                return NOT_ALLOWED

            to_search.extend(node[3])

        for node_id in nodes_to_remove:
            bonsai.remove_node(node_id)

        return DONE

    def es_simetrico(self, bonsai: Bonsai) -> bool:
        cost = self.balance(bonsai)[0]

        return cost == 0

    def can_remove_node(self, bonsai: Bonsai, node_id: str) -> bool:
        return self.quitar_nodo(bonsai.copy(), node_id) == DONE

    def upper_bound_to_balance(self, bonsai: Bonsai) -> int:
        return max(1, max(bonsai.costo_corte, bonsai.costo_flor) * len(bonsai.estructura))

    def balance(self, bonsai: Bonsai) -> list:
        upper_bound = self.upper_bound_to_balance(bonsai)

        def merge_solutions(a: list, b: list):
            return [a[0] + b[0], [*a[1], *b[1]]]

        def search(node_a: list | None, node_b: list | None):
            if node_a is None and node_b is None:
                return [0, []]

            if node_a is None and node_b is not None:
                if not self.can_remove_node(bonsai.copy(), node_b[0]):
                    return [upper_bound, []]

                return [bonsai.costo_corte, [[REMOVE_NODE, node_b[0]]]]

            if node_b is None and node_a is not None:
                if not self.can_remove_node(bonsai.copy(), node_a[0]):
                    return [upper_bound, []]

                return [bonsai.costo_corte, [[REMOVE_NODE, node_a[0]]]]

            left_a, right_a = node_a[3]
            left_b, right_b = node_b[3]

            left_child_a = bonsai.find_node(left_a)
            right_child_a = bonsai.find_node(right_a)

            left_child_b = bonsai.find_node(left_b)
            right_child_b = bonsai.find_node(right_b)

            best_solution = [upper_bound, []]

            subtree_solution = merge_solutions(
                search(left_child_a, right_child_b), search(right_child_a, left_child_b)
            )

            if node_a[1] == node_b[1]:
                best_solution = min(best_solution, subtree_solution)

            if node_a[1] != node_b[1]:
                if node_a[2]:
                    solution = merge_solutions(
                        [bonsai.costo_flor, [[MODIFY_FLOWER, node_a[0]]]],
                        subtree_solution,
                    )

                    best_solution = min(best_solution, solution)

                elif node_b[2]:
                    solution = merge_solutions(
                        [bonsai.costo_flor, [[MODIFY_FLOWER, node_b[0]]]],
                        subtree_solution,
                    )

                    best_solution = min(best_solution, solution)

            copy = bonsai.copy()
            can_remove = self.can_remove_node(copy, node_a[0]) and self.can_remove_node(
                copy, node_b[0]
            )

            if can_remove:
                solution = [
                    2 * bonsai.costo_corte,
                    [[REMOVE_NODE, node_a[0]], [REMOVE_NODE, node_b[0]]],
                ]

                best_solution = min(best_solution, solution)

            return best_solution

        root = bonsai.find_node("1")

        left = bonsai.find_node(root[3][0])
        right = bonsai.find_node(root[3][1])

        return search(left, right)

    def emparejar_bonsai(self, bonsai: Bonsai) -> list:
        cost, instrucctions = self.balance(bonsai)

        if cost >= self.upper_bound_to_balance(bonsai):
            return [False, []]

        return [True, instrucctions]

    def emparejar_bonsai_ahorro(self, bonsai: Bonsai) -> list:
        cost, instrucctions = self.balance(bonsai)

        if cost >= self.upper_bound_to_balance(bonsai):
            return [False, []]

        return [True, cost, instrucctions]

    def comprobar_solucion(self, bonsai: Bonsai, instrucciones: list) -> list:
        copy = bonsai.copy()

        cost = 0

        for type, id in instrucciones:
            if type == MODIFY_FLOWER:
                if self.modificar_nodo(copy, id) != DONE:
                    return [False, 0]

                cost += copy.costo_flor

            elif type == REMOVE_NODE:
                if self.quitar_nodo(copy, id) != DONE:
                    return [False, 0]

                cost += copy.costo_corte

        if not self.es_simetrico(copy):
            return [False, 0]

        return [True, cost]
