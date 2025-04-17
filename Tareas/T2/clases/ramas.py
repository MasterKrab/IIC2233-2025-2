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
    DEFENSA_MINIMA,
    DEFENSA_MAXIMA,
)


class Rama(ABC):
    def __init__(self, nombre: str, id: int, ramas_hijas: list[Self] = None):
        self.nombre = nombre
        self.ramas_hijas = ramas_hijas or []

        self.id = id
        self.modificador = None

        self._vitalidad_maxima = 0
        self._salud = 0
        self._defensa = 0
        self.resistencia_a_plagas = 0
        self.started_attack = False

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

        return int(value)

    @property
    def defensa(self) -> int:
        value = self._defensa

        for modificador in self.modificadores:
            value += modificador.defensa

        return max(DEFENSA_MINIMA, min(value, DEFENSA_MAXIMA))

    @defensa.setter
    def defensa(self, defensa: int) -> int:
        self._defensa = max(DEFENSA_MINIMA, min(defensa, DEFENSA_MAXIMA))

    @property
    def salud(self) -> int:
        # Make sure it not more than max health
        self._salud = max(0, min(self._salud, self.vitalidad_maxima))

        return self._salud

    @salud.setter
    def salud(self, salud: int):
        # Make sure it not more than max health
        self._salud = max(0, min(salud, self.vitalidad_maxima))

    def cargar_modificador(self, modificador: Modificador):
        if self.modificador:
            print(
                f"En la rama [{self.id}] {self.nombre} el modificador {self.modificadores[0].nombre} ha sido reemplazado por el modificador {modificador.nombre}."
            )
        else:
            print(
                f"En la rama [{self.id}] {self.nombre} se ha cargado el modificador:",
                modificador.nombre,
            )

        self.modificador = modificador

    @property
    def all_subtree_branches(self) -> list[Self]:

        def get_branches(rama: Rama):
            branches = [rama]

            for rama_hija in rama.ramas_hijas:
                branches = [*branches, *get_branches(rama_hija)]

            return branches

        return get_branches(self)[1:]

    @property
    def modificadores(self) -> list[Modificador]:
        if self.modificador is not None:
            return [self.modificador]

        return []

    def atacar(self, started_attack: bool = False) -> int:
        damage = self.dano_base
        self.started_attack = started_attack

        for branch in self.all_subtree_branches:
            damage += branch.atacar()

        amount = len(self.all_subtree_branches) + 1

        real_damage = round(damage / amount)

        for modificador in self.modificadores:
            real_damage += modificador.ataque

        return real_damage

    def recibir_dano(self, dano: int) -> int:
        real_damage = round(dano * (1 - self.defensa))

        print(f"La rama [{self.id}] {self.nombre} ha recidido {real_damage} de daño")

        diferencia = abs(self.salud - real_damage)

        self.salud -= real_damage

        if self.salud == 0:
            return diferencia

        return 0

    def pasar_ronda(self):
        has_new_negative_modifer = event_happens(1 - self.resistencia_a_plagas)

        if not has_new_negative_modifer:
            return

        name = choice(ModificadorNegativo.get_modifiers())

        print(f"La rama [{self.id}] {self.nombre} se ha contagiado de {name}.")

        self.cargar_modificador(ModificadorNegativo(name))

        self.started_attack = False

    def presentarse(self):
        if self.modificadores:
            modifiers_names = [modifier.nombre for modifier in self.modificadores]

            return f"{self.nombre}, Vida: {self.salud}/{self.vitalidad_maxima}, Daño base: {self.dano_base}, Defensa: {self.defensa}, Resistencia a plagas: {self.resistencia_a_plagas}, Modificadores: {', '.join(modifiers_names)}."

        return f"{self.nombre}, Vida: {self.salud}/{self.vitalidad_maxima}, Daño base: {self.dano_base}, Defensa: {self.defensa}, Resistencia a plagas: {self.resistencia_a_plagas}."

    def __str__(self) -> str:
        return self.presentarse()

    def __repr__(self) -> str:
        return self.presentarse()

    @staticmethod
    def get_branches() -> list[str]:
        names = []

        with Path(DATA_FOLDER, BRANCHES_FILE).open() as file:
            for line in file:
                name = line.split(";")[0]
                names.append(name)

        return names


class Ficus(Rama):
    efecto = "Cada vez que transcurre una ronda, esta rama y sus hijas recuperan 4% de la salud faltante."
    nombre = "Ficus"

    def __init__(self, *args, **kwargs):
        super().__init__(self.nombre, *args, **kwargs)

    def pasar_ronda(self):
        super().pasar_ronda()

        self.salud += int(abs(self.vitalidad_maxima - self.salud) * 0.04)

        for rama in self.ramas_hijas:
            rama.salud += int(abs(rama.vitalidad_maxima - rama.salud) * 0.04)


class Celery(Rama):
    efecto = "Por cada ronda que esta rama no ataque ni forme parte de un ataque, su dano base aumenta un 1%."
    nombre = "Celery"

    def __init__(self, *args, **kwargs):
        super().__init__(self.nombre, *args, **kwargs)

        self.bonus = True

    def pasar_ronda(self):
        super().pasar_ronda()

        if self.bonus:
            self.dano_base += int(self.dano_base * 0.01)

        self.bonus = True

    def atacar(self, started_attack: bool = False) -> int:
        self.bonus = False

        return super().atacar(started_attack)


class Hyedrid(Rama):
    efecto = "Esta rama se puede equipar dos objetos Modificador en lugar de uno. Para la mecánica de reemplazo, se debe considerar el órden en que ingresan los objetos. Debe seguir una secuencia FIFO."
    nombre = "Hyedrid"

    def __init__(self, *args, **kwargs):
        super().__init__(self.nombre, *args, **kwargs)
        self._modificadores = []

    def cargar_modificador(self, modificador: Modificador):
        if len(self.modificadores) >= 2:
            removed = self._modificadores.pop(0)
            print(
                f"En la rama [{self.id}] {self.nombre} el modificador {removed.nombre} ha sido descartado."
            )

        print(
            f"En la rama [{self.id}] {self.nombre} el modificador {modificador.nombre} ha sido añadido."
        )

        self._modificadores.append(modificador)

    @property
    def modificadores(self) -> list[Modificador]:
        return self._modificadores


class Paalm(Rama):
    efecto = (
        "Cada vez que esta rama recibe daño y no muere, su defensa aumenta en 0.02."
    )
    nombre = "Paalm"

    def __init__(self, *args, **kwargs):
        super().__init__(self.nombre, *args, **kwargs)

    def recibir_dano(self, dano: int) -> int:
        dano_restante = super().recibir_dano(dano)

        if self.salud > 0:
            self.defensa += 0.02

        return dano_restante


class Alovelis(Rama):
    efecto = "Sin efectos adicionales."
    nombre = "Alovelis"

    def __init__(self, *args, **kwargs):
        super().__init__(self.nombre, *args, **kwargs)


class Pine(Rama):
    efecto = (
        "Si esta rama muere por un ataque, anula el dano de penetración hacia su padre."
    )
    nombre = "Pine"

    def __init__(self, *args, **kwargs):
        super().__init__(self.nombre, *args, **kwargs)

    def recibir_dano(self, dano):
        dano_restante = super().recibir_dano(dano)

        if self.salud == 0:
            return 0

        return dano_restante


class Cactoos(Rama):
    efecto = f"Si no ataca ni recibe dano durante una ronda, genera {DINERO_CACTOOS} de dinero por cada rama hija."
    nombre = "Cactoos"

    def __init__(self, *args, **kwargs):
        super().__init__(self.nombre, *args, **kwargs)

        self.money = 0
        self.bonus = True

    def atacar(self, started_attack: bool = False) -> int:
        self.bonus = not started_attack

        return super().atacar(started_attack)

    def recibir_dano(self, dano) -> int:
        self.bonus = False

        return super().recibir_dano(dano)

    def pasar_ronda(self):
        super().pasar_ronda()

        if self.bonus:
            self.money += DINERO_CACTOOS * len(self.ramas_hijas)

        self.bonus = True

    def extract_money(self):
        money = self.money

        self.money = 0

        return money


def get_branch_class(name: str) -> Rama:
    for branch in (Ficus, Celery, Hyedrid, Paalm, Alovelis, Pine, Cactoos):
        if branch.nombre.strip().lower() == name.lower():
            return branch
