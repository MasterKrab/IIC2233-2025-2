import utilidades
from pathlib import Path

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
                node, hasFlowerText, canEditText, childsText = line.strip().split(",")

                hasFlower = hasFlowerText == "T"
                canEdit = canEditText == "T"
                childs = childsText.split(";")

                self.estructura.append([node, hasFlower, canEdit, childs])

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

    def find_node(self, id: int) -> list | None:
        index = self.find_node_index(id)

        if index is None:
            return None

        return self.estructura[index]

    def remove_node(self, id: int) -> None:
        index = self.find_node_index(id)
        self.estructura.pop(index)

        for node in self.estructura:
            for i in range(2):
                if node[3][i] == id:
                    node[3][i] = "0"
                    break

    def copy(self):
        tree = Bonsai(self.identificador, self.costo_corte, self.costo_flor, [])

        for *data, childs in self.estructura:
            tree.estructura.append([*data, childs.copy()])

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
        def search(node: list | None, swap: bool):
            if node is None:
                return ()

            left, right = node[3]

            if swap:
                left, right = right, left

            left_child = bonsai.find_node(left)
            right_right = bonsai.find_node(right)

            return (node[1], search(left_child, swap), search(right_right, swap))

        root = bonsai.estructura[0]

        left_child = bonsai.find_node(root[3][0])
        right_child = bonsai.find_node(root[3][1])

        return search(left_child, True) == search(right_child, False)

    def emparejar_bonsai(self, bonsai: Bonsai) -> list:
        pass
        # Remove nodes

    def emparejar_bonsai_ahorro(self, bonsai: Bonsai) -> list:
        pass

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
