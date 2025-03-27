from abc import ABC


class Vehiculo(ABC):
    identificador = 0

    def __init__(
        self, rendimiento: int, marca: str, energia=111.5, *args, **kwargs
    ) -> None:
        self.rendimiento = rendimiento
        self.marca = marca
        self.energia_privada = max(energia, 0)
        self.identificador = Vehiculo.identificador
        Vehiculo.identificador += 1

    @property
    def autonomia(self) -> float:
        return self.energia_privada * self.rendimiento

    @property
    def energia(self) -> float:
        return round(self.energia_privada, 1)

    @energia.setter
    def energia(self, valor: float):
        self.energia_privada = max(0, valor)


class MotorElectrico(ABC):
    def __init__(self, vida_util_bateria: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.vida_util_bateria = vida_util_bateria

    def usar_bateria(self) -> bool:
        if self.vida_util_bateria <= 0:
            return False

        self.vida_util_bateria -= 1
        return True


class Auto(Vehiculo):
    def __init__(
        self, rendimiento: int, marca: str, energia: 111.5, *args, **kwargs
    ) -> None:
        super().__init__(rendimiento, marca, energia, *args, **kwargs)
        self.kilometraje = 0

    def recorrer(self, kilometros: float) -> str:
        recorrido = float(round(min(self.autonomia, kilometros), 1))
        gasto = recorrido / self.rendimiento

        self.kilometraje += recorrido
        self.energia -= gasto

        return (
            f"Anduve en auto {recorrido}Km y eso consume {round(gasto, 1)}L de bencina"
        )


class AutoElectrico(MotorElectrico, Auto):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def recorrer(self, kilometros: float) -> str:
        if not self.usar_bateria():
            return "La bateria del auto electrico no funciona"

        recorrido = float(round(min(self.autonomia, kilometros), 1))
        gasto = recorrido / self.rendimiento

        self.kilometraje += recorrido
        self.energia -= gasto

        return f"Anduve en auto electrico {recorrido}Km y eso consume {gasto}W de energia electrica"


class Bicicleta(Vehiculo):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def recorrer(self, kilometros: float) -> str:
        kilometros = float(round(kilometros, 1))

        return f"Anduve en bicicleta {kilometros}Km y eso no consume bencina ni energia electrica"


class BicicletaElectrica(MotorElectrico, Bicicleta):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def recorrer(self, kilometros: float):
        kilometros = float(round(kilometros, 1))

        if not self.usar_bateria():
            return f"La bateria de la bicicleta electrica no funciona, tuve que pedalear {kilometros}Km"

        recorrido = float(round(min(self.autonomia, kilometros), 1))
        gasto = recorrido / self.rendimiento

        self.energia -= gasto

        if recorrido == kilometros:
            return f"Anduve en bicicleta electrica {recorrido}Km y eso consume {gasto}W de energia electrica"

        restante = kilometros - recorrido

        return f"Anduve en bicicleta electrica {recorrido}Km y eso consume {gasto}W de energia electrica, los {restante}Km restantes los tuve que pedalear"
