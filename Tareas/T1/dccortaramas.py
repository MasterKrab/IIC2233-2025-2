import utilidades
from pathlib import Path


# Files constants
READ_FOLDER = "data"
WRITE_FOLDER = "visualizaciones"

# Messages
NOT_ALLOWED = "No permitido"
DONE = "Realizado"
NOT_FOUND = "No encontrado"
FAILS = "Falla"

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
                id, has_flower_text, can_edit_text, childs_text = line.strip().split(
                    ","
                )

                has_flower = has_flower_text == "T"
                can_edit = can_edit_text == "T"
                childs = childs_text.split(";")

                node = [id, has_flower, can_edit, childs]

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
        """
        Search node by id and return its index in the structure
        """

        for i in range(len(self.estructura)):
            if self.estructura[i][0] == id:
                return i

        return None

    def find_node(self, id: str) -> list | None:
        """
        Search node by id and return it
        """
        for node in self.estructura:
            if node[0] == id:
                return node

        return None

    def find_parent(self, id: str) -> list | None:
        """
        Search parent of a node by id and return it
        """
        for node in self.estructura:
            if id in node[3]:
                return node

        return None

    def remove_node(self, id: str) -> None:
        """
        Remove node by id and do the necessary changes in the structure
        """
        index = self.find_node_index(id)

        self.estructura.pop(index)

        parent = self.find_parent(id)

        if parent is None:
            return

        for i in range(2):
            if parent[3][i] == id:
                parent[3][i] = "0"

    def copy(self):
        """
        Return a copy of the bonsai
        """
        tree = Bonsai(self.identificador, self.costo_corte, self.costo_flor, [])

        for *data, childs in self.estructura:
            tree.estructura.append([*data, [*childs]])

        return tree

    def get_nodes(self):
        """
        Return a set of the nodes
        """

        nodes = set()

        for node in self.estructura:
            nodes.add(node[0])
            nodes.update(node[3])

        nodes.discard("0")

        return nodes


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
        # A stack to search the nodes to remove
        to_search = [identificador]

        nodes_to_remove = set()

        while to_search:
            node_id_to_remove = to_search.pop()

            # Node not exists
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

    def can_remove_node(self, bonsai: Bonsai, node_id: str) -> bool:
        """
        Return a bool indicating if a node can be removed
        """

        # Copy the bonsai and try to remove the node to check if it can be removed
        return self.quitar_nodo(bonsai.copy(), node_id) == DONE

    def balance(self, bonsai: Bonsai) -> list:
        """
        Return the cost and instructions to balance the bonsai. If it's not possible return
        [float("inf"), []], if it's already balanced return [0, []] and if it's possible
        return the cost and instructions.
        """

        def merge_solutions(a: list, b: list):
            return [a[0] + b[0], [*a[1], *b[1]]]

        # Recursive function to find the best solution by exploring the tree while accounting
        # for symmetric nodes. It calculates the cost of three possible actions: modifying the
        # flower, removing both nodes, or doing nothing (if the nodes are symmetric). It checks
        # all meaningful changes, so it's guaranteed to find the best solution.
        def search(node_a: list | None, node_b: list | None):
            if node_a is None and node_b is None:
                return [0, []]

            # If node_a is None, we only can remove node_b
            if node_a is None and node_b is not None:
                if not self.can_remove_node(bonsai.copy(), node_b[0]):
                    return [float("inf"), []]

                return [bonsai.costo_corte, [[REMOVE_NODE, node_b[0]]]]

            # If node_b is None, we only can remove node_a
            if node_b is None and node_a is not None:
                if not self.can_remove_node(bonsai.copy(), node_a[0]):
                    return [float("inf"), []]

                return [bonsai.costo_corte, [[REMOVE_NODE, node_a[0]]]]

            left_a, right_a = node_a[3]
            left_b, right_b = node_b[3]

            left_child_a = bonsai.find_node(left_a)
            right_child_a = bonsai.find_node(right_a)

            left_child_b = bonsai.find_node(left_b)
            right_child_b = bonsai.find_node(right_b)

            best_solution = [float("inf"), []]

            # Solution to balance both subtrees
            subtree_solution = merge_solutions(
                search(left_child_a, right_child_b), search(right_child_a, left_child_b)
            )

            # If the nodes are symmetric, we can do nothing
            if node_a[1] == node_b[1]:
                best_solution = min(best_solution, subtree_solution)

            # If the nodes are not symmetric, we can try to modify the flower
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

            # Checks if we can remove both nodes
            copy = bonsai.copy()
            can_remove = self.can_remove_node(copy, node_a[0]) and self.can_remove_node(
                copy, node_b[0]
            )

            # If we can remove both nodes, we can try to remove them
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

    def es_simetrico(self, bonsai: Bonsai) -> bool:
        if not bonsai.estructura:
            return True

        cost, instrucctions = self.balance(bonsai)

        # If the cost is 0 and there are no instructions, the bonsai is already symetric
        return cost == 0 and not instrucctions

    def emparejar_bonsai(self, bonsai: Bonsai) -> list:
        cost, instrucctions = self.balance(bonsai)

        # If the cost is infinite, then it's not possible
        if cost == float("inf"):
            return [False, []]

        return [True, instrucctions]

    def calculate_cost(self, bonsai: Bonsai, instrucciones: list) -> int:
        """
        Calculate the cost of a solution
        """
        cost = 0

        for instruccion in instrucciones:
            type = instruccion[0]

            if type == MODIFY_FLOWER:
                cost += bonsai.costo_flor

            elif type == REMOVE_NODE:
                cost += bonsai.costo_corte

        return cost

    def apply_solution(self, bonsai: Bonsai, instrucciones: list) -> str:
        """
        Apply the changes of a solution to a bonsai, return DONE if it's possible,
        FAILS otherwise
        """
        for type, id in instrucciones:
            if type == MODIFY_FLOWER:
                if self.modificar_nodo(bonsai, id) != DONE:
                    return FAILS

            elif type == REMOVE_NODE:
                if self.quitar_nodo(bonsai, id) != DONE:
                    return FAILS

        if not self.es_simetrico(bonsai):
            return FAILS

        return DONE

    def emparejar_bonsai_ahorro(self, bonsai: Bonsai) -> list:
        cost, instrucctions = self.balance(bonsai)

        # If the cost is infinite, then it's not possible
        if cost == float("inf"):
            return [False, []]

        return [True, cost, instrucctions]

    def comprobar_solucion(self, bonsai: Bonsai, instrucciones: list) -> list:
        # Checks if the solution is correct
        if self.apply_solution(bonsai.copy(), instrucciones) == DONE:
            return [True, self.calculate_cost(bonsai, instrucciones)]

        return [False, 0]
