from pathlib import Path
from typing import Self
from abc import ABC
from clases.modificador import Modificador, ModificadorNegativo
from utils.choice import event_happens
from random import choice

from parametros import (
    DATA_FOLDER,
    BRANCHES_FILE,
    DINERO_CACTOOS,
)


class Rama(ABC):
    def __init__(self, nombre: str, id: int, ramas_hijas: list[Self] = None):
        self.nombre = nombre
        self.ramas_hijas = ramas_hijas or []
        self.id = id

        self.modificadores = []

        with Path(DATA_FOLDER, BRANCHES_FILE).open() as file:
            for line in file:
                if not line.startswith(nombre):
                    continue

                puntos_de_vida, defensa, dano_base, resistencia_a_plagas = map(
                    float, line.split(";")[1:]
                )

                self._vitalidad_maxima = int(puntos_de_vida)
                self._salud = int(puntos_de_vida)

                self._defensa = defensa

                self.dano_base = int(dano_base)

                self.resistencia_a_plagas = resistencia_a_plagas

                break

    @property
    def vitalidad_maxima(self) -> int:
        value = self._vitalidad_maxima

        for modificador in self.modificadores:
            value += modificador.vida_maxima

        return value

    @property
    def defensa(self) -> int:
        value = self._defensa

        for modificador in self.modificadores:
            value += modificador.defensa

        return max(-0.5, min(value, 0.5))

    @defensa.setter
    def defensa(self, defensa: int) -> int:
        self._defensa = max(-0.5, min(defensa, 0.5))

    @property
    def salud(self) -> int:
        return self._salud

    @salud.setter
    def salud(self, salud: int):
        self._salud = max(0, min(salud, self.vitalidad_maxima))

    def cargar_modificador(self, modificador: Modificador):
        self.modificadores = [modificador]

    @property
    def all_subtree_branches(self) -> list[Self]:

        def get_branches(rama: Rama):
            branches = [rama]

            for rama_hija in rama.ramas_hijas:
                branches = [*branches, *get_branches(rama_hija)]

            return branches

        return get_branches(self)[1:]

    def atacar(self) -> int:
        damage = self.dano_base

        for branch in self.all_subtree_branches:
            damage += branch.atacar()

        amount = len(self.all_subtree_branches) + 1

        real_damage = round(damage / amount)

        for modificador in self.modificadores:
            real_damage += modificador.ataque

        return real_damage

    def recibir_dano(self, daño: int) -> int:
        daño_verdadero = round(daño * (1 - self.defensa))

        diferencia = abs(self.salud - daño_verdadero)

        self.salud -= daño_verdadero

        if self.salud == 0:
            return diferencia

        return 0

    def pasar_ronda(self):
        has_new_negative_modifer = event_happens(1 - self.resistencia_a_plagas)

        if not has_new_negative_modifer:
            return

        name = choice(ModificadorNegativo.get_modifiers())

        self.cargar_modificador(ModificadorNegativo(name))

        print("")

    def presentarse(self):
        return f"{self.nombre}, Vida: {self.salud}/{self.vitalidad_maxima}, Daño base: {self.dano_base}, Defensa: {self.defensa}."

    def __str__(self) -> str:
        return self.presentarse()

    def __repr__(self) -> str:
        return self.presentarse()


class Ficus(Rama):
    efecto = "Cada vez que transcurre una ronda, esta rama y sus hijas recuperan 4% de la salud faltante."
    nombre = "Ficus"

    def __init__(self, *args, **kwargs):
        super().__init__(self.nombre, *args, **kwargs)

    def pasar_ronda(self):
        super().pasar_ronda()

        self.salud += int((self.vitalidad_maxima - self.salud) * 0.04)

        for rama in self.ramas_hijas:
            self.salud += int((rama.vitalidad_maxima - rama.salud) * 0.04)


class Celery(Rama):
    efecto = "Por cada ronda que esta rama no ataque ni forme parte de un ataque, su daño base aumenta un 1%."
    nombre = "Celery"

    def __init__(self, *args, **kwargs):
        super().__init__(self.nombre, *args, **kwargs)

        self.bonus = True

    def pasar_ronda(self):
        super().pasar_ronda()

        if self.bonus:
            self.dano_base += int(self.dano_base * 0.01)

        self.bonus = True

    def atacar(self) -> int:
        self.bonus = False

        return super().atacar()

    def recibir_dano(self, daño) -> int:
        self.bonus = False

        return super().recibir_dano(daño)


class Hyedrid(Rama):
    efecto = "Esta rama se puede equipar dos objetos Modificador en lugar de uno. Para la mecánica de reemplazo, se debe considerar el órden en que ingresan los objetos. Debe seguir una secuencia FIFO."
    nombre = "Hyedrid"

    def __init__(self, *args, **kwargs):
        super().__init__(self.nombre, *args, **kwargs)

    def cargar_modificador(self, modificador: Modificador):
        if len(self.modificadores) >= 2:
            self.modificadores.pop(0)

        self.modificadores.append(modificador)


class Paalm(Rama):
    efecto = (
        "Cada vez que esta rama recibe daño y no muere, su defensa aumenta en 0.02."
    )
    nombre = "Paalm"

    def __init__(self, *args, **kwargs):
        super().__init__(self.nombre, *args, **kwargs)

    def recibir_daño(self, daño: int):
        super().recibir_daño(daño)

        if self.salud > 0:
            self.defensa += 0.02


class Alovelis(Rama):
    efecto = "Sin efectos adicionales."
    nombre = "Alovelis"

    def __init__(self, *args, **kwargs):
        super().__init__(self.nombre, *args, **kwargs)


class Pine(Rama):
    efecto = (
        "Si esta rama muere por un ataque, anula el daño de penetración hacia su padre."
    )
    nombre = "Pine"

    def __init__(self, *args, **kwargs):
        super().__init__(self.nombre, *args, **kwargs)

    def recibir_dano(self, daño):
        daño_restante = super().recibir_dano(daño)

        if self.salud == 0:
            return 0

        return daño_restante


class Cactoos(Rama):
    efecto = f"Si no ataca ni recibe daño durante una ronda, genera {DINERO_CACTOOS} de dinero por cada rama hija."
    nombre = "Cactoos"

    def __init__(self, *args, **kwargs):
        super().__init__(self.nombre, *args, **kwargs)

        self.money = 0

    def pasar_ronda(self):
        super().pasar_ronda()

        times = 1 + len(self.ramas_hijas)

        self.money += DINERO_CACTOOS * times

    def extract_money(self):
        money = self.money

        self.money = 0

        return money
