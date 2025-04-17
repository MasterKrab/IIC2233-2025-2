from utils.input import read_input

from parametros import (
    DATA_FOLDER,
    POSITIVE_MODIFIER_FILE,
    NEGATIVE_MODIFIER_FILE,
)

from pathlib import Path
from abc import ABC, abstractmethod


class Modificador(ABC):
    def __init__(self, nombre: str, ataque: int, defensa: float, vida_maxima: int):
        self.nombre = nombre
        self.ataque = ataque
        self.defensa = defensa
        self.vida_maxima = vida_maxima

    @abstractmethod
    def get_modifiers() -> list[str]:
        pass

    @abstractmethod
    def __str__(self):
        pass


class ModificadorPositivo(Modificador):
    def __init__(self, nombre: str):
        with Path(DATA_FOLDER, POSITIVE_MODIFIER_FILE).open() as file:
            for line in file:
                if not line.startswith(nombre):
                    continue

                ataque, defensa, vida_maxima, precio = read_input(
                    [str, int, float, int, int], ";", line
                )[1:]

                super().__init__(nombre, ataque, defensa, vida_maxima)

                self.precio = int(precio)

                break

    @staticmethod
    def get_modifiers() -> list[str]:
        """
        Returns a list of all positive modifiers names.
        """
        names = []

        with Path(DATA_FOLDER, POSITIVE_MODIFIER_FILE).open() as file:
            for line in file:
                name = line.split(";")[:1][0]
                names.append(name)

        return names

    def __str__(self):
        return f"{self.nombre} (Positivo)"


class ModificadorNegativo(Modificador):
    def __init__(self, nombre: str):
        with Path(DATA_FOLDER, NEGATIVE_MODIFIER_FILE).open() as file:
            for line in file:
                if not line.startswith(nombre):
                    continue

                ataque, defensa, vida_maxima = read_input(
                    [str, int, float, int], ";", line
                )[1:]

                super().__init__(nombre, ataque, defensa, vida_maxima)
                return

    @staticmethod
    def get_modifiers() -> list[str]:
        """
        Returns a list of all negative modifiers names.
        """
        names = []

        with Path(DATA_FOLDER, NEGATIVE_MODIFIER_FILE).open() as file:
            for line in file:
                name = line.split(";")[:1][0]
                names.append(name)

        return names

    def __str__(self):
        return f"{self.nombre} (Negativo)"
