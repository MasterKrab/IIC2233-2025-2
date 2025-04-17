from pathlib import Path
from abc import ABC

from parametros import (
    DATA_FOLDER,
    POSITIVE_MODIFIER_FILE,
    NEGATIVE_MODIFIER_FILE,
)


class Modificador(ABC):
    def __init__(self, nombre: str, ataque: int, defensa: float, vida_maxima: int):
        self.nombre = nombre
        self.ataque = ataque
        self.defensa = defensa
        self.vida_maxima = vida_maxima


class ModificadorPositivo(Modificador):
    def __init__(self, nombre: str):
        with Path(DATA_FOLDER, POSITIVE_MODIFIER_FILE).open() as file:
            for line in file:
                if not line.startswith(nombre):
                    continue

                ataque, defensa, vida_maxima, precio = map(float, line.split(";")[1:])

                super().__init__(nombre, ataque, defensa, vida_maxima)

                self.precio = int(precio)

                break

    @staticmethod
    def get_modifiers() -> list[str]:
        names = []

        with Path(DATA_FOLDER, POSITIVE_MODIFIER_FILE).open() as file:
            for line in file:
                name = line.split(";")[:1][0]
                names.append(name)

        return names


class ModificadorNegativo(Modificador):
    def __init__(self, nombre: str):
        with Path(DATA_FOLDER, NEGATIVE_MODIFIER_FILE).open() as file:
            for line in file:
                if not line.startswith(nombre):
                    continue

                ataque, defensa, vida_maxima = map(float, line.split(";")[1:])

                super().__init__(nombre, ataque, defensa, vida_maxima)
                return

    @staticmethod
    def get_modifiers() -> list[str]:
        names = []

        with Path(DATA_FOLDER, NEGATIVE_MODIFIER_FILE).open() as file:
            for line in file:
                name = line.split(";")[:1][0]
                names.append(name)

        return names
