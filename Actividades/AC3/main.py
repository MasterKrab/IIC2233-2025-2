import json
import os

from utils import Conductor, PatenteError


class CargadorArchivos:

    @staticmethod
    def cargar_registro_oficial(path_registro_oficial: str) -> dict:
        registro_oficial = dict()
        with open(path_registro_oficial, "r") as file:
            registros = json.load(file)
            for nombre_conductor, patente in registros.items():
                registro_oficial[nombre_conductor] = patente
        return registro_oficial

    @staticmethod
    def cargar_conductores(path_conductores: str) -> list:
        conductores = list()
        with open(path_conductores, "r", encoding="latin-1") as file:
            for line in file:
                conductor = Conductor(*line.strip().split(","))
                conductores.append(conductor)
        return conductores

    def cargar_datos(self, path_registro_oficial: str, path_conductores: str) -> tuple:
        registro_oficial = None
        conductores = None

        try:
            registro_oficial = self.cargar_registro_oficial(path_registro_oficial)
        except FileNotFoundError:
            print(f"El archivo {path_registro_oficial} no existe.")

        try:
            conductores = self.cargar_conductores(path_conductores)
        except FileNotFoundError:
            print(f"El archivo {path_conductores} no existe.")

        return registro_oficial, conductores


class DCConductor:

    def __init__(self, registro_oficial: dict, conductores: list) -> None:
        self.registro_oficial = registro_oficial
        self.conductores = conductores
        self.seleccionados = list()

    def chequear_rut(self, conductor: Conductor) -> None:
        if "." in conductor.rut:
            raise ValueError(f"El rut {conductor.rut} contiene puntos.")

        if conductor.rut[-2] != "-":
            raise ValueError(
                f"El rut {conductor.rut} no contiene el guión en la penultima posicion."
            )

    def chequear_celular(self, conductor: Conductor) -> None:
        if not conductor.celular.isdigit():
            raise ValueError(
                f"El celular {conductor.celular} contiene caracteres no numericos."
            )

        if conductor.celular[0] != "9":
            raise ValueError(f"El celular {conductor.celular} no comienza con 9.")

        if len(conductor.celular) != 9:
            raise ValueError(
                f"El celular {conductor.celular} no tiene el largo correcto."
            )

    def chequear_nombre(self, conductor: Conductor) -> None:
        if conductor.nombre not in self.registro_oficial:
            raise KeyError(f"El conductor {conductor.nombre} no esta en el registro.")

    def chequear_patente(self, conductor: Conductor) -> None:
        if self.registro_oficial[conductor.nombre] != conductor.patente:
            raise PatenteError(conductor)

    def chequear_conductores_app(self) -> str:
        if self.registro_oficial and self.conductores:
            cantidad_errores = 0

            for conductor in self.conductores:
                try:
                    self.chequear_rut(conductor)
                except ValueError as error:
                    print(error)

                    cantidad_errores += 1
                    continue

                try:
                    self.chequear_celular(conductor)
                except ValueError as error:
                    print(error)

                    cantidad_errores += 1
                    continue

                try:
                    self.chequear_nombre(conductor)
                except KeyError as error:
                    print(error)

                    cantidad_errores += 1
                    continue

                try:
                    self.chequear_patente(conductor)
                except PatenteError as error:
                    print(error.mensaje)

                    cantidad_errores += 1
                    continue

                self.seleccionados.append(conductor)

            return f"La cuenta de datos erroneos fue: {cantidad_errores}."

        return "Falta parte de los datos necesarios para hacer la revision."


if __name__ == "__main__":
    cargador_archivos = CargadorArchivos()

    print(" CASO 1 ".center(50, "-"))
    registro_oficial, conductores = cargador_archivos.cargar_datos(
        os.path.join("data", "regiztro_ofizial.json"),
        os.path.join("data", "conductores.csv"),
    )
    dcconductor = DCConductor(registro_oficial, conductores)
    print(dcconductor.chequear_conductores_app(), "\n")

    print(" CASO 2 ".center(50, "-"))
    registro_oficial, conductores = cargador_archivos.cargar_datos(
        os.path.join("data", "registro_oficial.json"),
        os.path.join("data", "conductores.hvs"),
    )
    dcconductor = DCConductor(registro_oficial, conductores)
    print(dcconductor.chequear_conductores_app(), "\n")

    print(" CASO 3 ".center(50, "-"))
    registro_oficial, conductores = cargador_archivos.cargar_datos(
        os.path.join("data", "registro_oficial.json"),
        os.path.join("data", "conductores.csv"),
    )
    dcconductor = DCConductor(registro_oficial, conductores)
    print(dcconductor.chequear_conductores_app())
