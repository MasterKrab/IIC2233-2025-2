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


class DCCortaRamas:
    def modificar_nodo(self, bonsai: Bonsai, identificador: str) -> str:
        for node in bonsai.estructura:
            # not target node
            if node[0] != identificador:
                continue

            # Can't edit
            if not node[2]:
                return NOT_ALLOWED

            node[1] = not node[1]
            return DONE

        return NOT_FOUND

    def quitar_nodo(self, bonsai: Bonsai, identificador: str) -> str:
        pass

    def es_simetrico(self, bonsai: Bonsai) -> bool:
        pass

    def emparejar_bonsai(self, bonsai: Bonsai) -> list:
        pass

    def emparejar_bonsai_ahorro(self, bonsai: Bonsai) -> list:
        pass

    def comprobar_solucion(self, bonsai: Bonsai, instrucciones: list) -> list:
        pass
