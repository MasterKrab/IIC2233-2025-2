from __future__ import annotations
from copy import deepcopy
from utils import NodoUrgencia, Urgencia


class ListaUrgencias:
    def __init__(self) -> None:
        self.cabeza = None

    def __repr__(self) -> str:
        return f"{self.cabeza}"

    def __iter__(self) -> IteradorListarUrgencias:
        copy = ListaUrgencias()

        copy.cabeza = NodoUrgencia(self.cabeza.urgencia)

        last = copy.cabeza
        current = self.cabeza.siguiente

        while current:
            last.siguiente = NodoUrgencia(current.urgencia)
            current = current.siguiente

        return IteradorListarUrgencias(copy)

    # nodes = []

    # current = self.cabeza

    # while current:
    #     nodes.append(current)
    #     current = current.siguiente

    # return IteradorListarUrgencias(nodes)

    def agregar_urgencia(self, urgencia: Urgencia) -> None:
        node = NodoUrgencia(urgencia)

        if not self.cabeza:
            self.cabeza = node
            return

        if node.urgencia >= self.cabeza.urgencia:
            node.siguiente = self.cabeza
            self.cabeza = node
            return

        last = self.cabeza

        while True:
            current = last.siguiente

            if current is None:
                last.siguiente = node
                break

            if node.urgencia > current.urgencia:
                last.siguiente = node
                node.siguiente = current
                break

            last = current

    def quitar_urgencia(self, paciente: str) -> Urgencia:
        if self.cabeza is None:
            raise ValueError(f"ListaUrgencias no contiene a {paciente}")

        if self.cabeza.urgencia.paciente == paciente:
            node = self.cabeza
            self.cabeza = node.siguiente
            return node.urgencia

        last = self.cabeza

        while True:
            current = last.siguiente

            if current is None:
                raise ValueError(f"ListaUrgencias no contiene a {paciente}")

            if current.urgencia.paciente == paciente:
                last.siguiente = current.siguiente
                return current.urgencia

            last = current


class IteradorListarUrgencias:
    def __init__(self, lista_urgencias: ListaUrgencias) -> None:
        self.lista_urgencias = ListaUrgencias()

        current = lista_urgencias.cabeza

        while current:
            self.lista_urgencias.agregar_urgencia(current.urgencia)
            current = current.siguiente

    def __iter__(self) -> IteradorListarUrgencias:
        return self

    def __next__(self) -> Urgencia:
        if not self.lista_urgencias.cabeza:
            raise StopIteration

        head = self.lista_urgencias.cabeza.urgencia.paciente

        return self.lista_urgencias.quitar_urgencia(head)


if __name__ == "__main__":
    # PARTE I: agregar urgencia

    # Lista vacía
    lista_urgencias = ListaUrgencias()
    print(lista_urgencias)

    # Agregar elemento a la lista vacía
    urg_agr_1 = Urgencia("Paciente1", 17.2)
    lista_urgencias.agregar_urgencia(urg_agr_1)
    print(lista_urgencias)

    # Agregar elemento a una lista con más elementos
    n2 = NodoUrgencia(Urgencia("Paciente2", 13.0))
    n3 = NodoUrgencia(Urgencia("Paciente3", 7.0))
    n4 = NodoUrgencia(Urgencia("Paciente4", 3.2))
    n5 = NodoUrgencia(Urgencia("Paciente5", 1.2))

    lista_urgencias.cabeza.siguiente = n2
    n2.siguiente = n3
    n3.siguiente = n4
    n4.siguiente = n5

    urg_agr_6 = Urgencia("Paciente6", 5.0)
    lista_urgencias.agregar_urgencia(urg_agr_6)

    print(lista_urgencias)

    # -----------------------------------------
    # PARTE I: agregar quitar

    # Lista de la parte anterior
    print(lista_urgencias)

    # Quitar paciente de la lista
    urg_quit_1 = lista_urgencias.quitar_urgencia("Paciente6")
    print(urg_quit_1)
    print(lista_urgencias)

    # Quitar paciente que no esta en la lista
    try:
        urg_quit_2 = lista_urgencias.quitar_urgencia("Paciente7")
        print(urg_quit_2)
        print(lista_urgencias)
    except ValueError as error:
        print(error)

    # -----------------------------------------
    # PARTE II: Iterable e iterador

    # Lista desordenada
    lista_urgencias = ListaUrgencias()

    n1 = NodoUrgencia(Urgencia("Paciente1", 17.2))
    n2 = NodoUrgencia(Urgencia("Paciente3", 7.0))
    n3 = NodoUrgencia(Urgencia("Paciente5", 1.2))
    n4 = NodoUrgencia(Urgencia("Paciente4", 3.2))
    n5 = NodoUrgencia(Urgencia("Paciente2", 13.0))

    n1.siguiente = n2
    n2.siguiente = n3
    n3.siguiente = n4
    n4.siguiente = n5

    lista_urgencias.cabeza = n1
    print(lista_urgencias)

    for urg in lista_urgencias:
        print(urg)
