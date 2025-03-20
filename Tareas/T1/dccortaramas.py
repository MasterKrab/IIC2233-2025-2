import utilidades
from pathlib import Path

# Files constants
READ_FOLDER = "data"
WRITE_FOLDER = "visualizaciones"

# Messages
NOT_ALLOWED = "No permitido"
DONE = "Realizado"
NOT_FOUND = "No encontrado"


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


def find_node_index(bonsai: Bonsai, id: int) -> int | None:
    for i in range(len(bonsai.estructura)):
        if bonsai.estructura[i][0] == id:
            return i

    return None


def find_node(bonsai: Bonsai, id: int) -> list | None:
    index = find_node_index(bonsai, id)

    if index is None:
        return None

    return bonsai.estructura[index]


class DCCortaRamas:
    def modificar_nodo(self, bonsai: Bonsai, identificador: str) -> str:
        node = find_node(bonsai, identificador)

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

            node = find_node(bonsai, node_id_to_remove)

            if node is None:
                return NOT_FOUND

            if not node[2]:
                return NOT_ALLOWED

            to_search.extend(node[3])

        # Remove nodes
        for node_id in nodes_to_remove:
            index = find_node(bonsai, node_id)
            bonsai.estructura.remove(index)

        # Remove nodes from child lists
        for node in bonsai.estructura:
            for i in range(2):
                if node[3][i] in nodes_to_remove:
                    node[3][i] = "0"

        return DONE

    def es_simetrico(self, bonsai: Bonsai) -> bool:
        pass

    def emparejar_bonsai(self, bonsai: Bonsai) -> list:
        pass

    def emparejar_bonsai_ahorro(self, bonsai: Bonsai) -> list:
        pass

    def comprobar_solucion(self, bonsai: Bonsai, instrucciones: list) -> list:
        pass
