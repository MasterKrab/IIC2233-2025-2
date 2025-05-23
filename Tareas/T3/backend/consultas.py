from typing import Generator, Iterable
from pathlib import Path
from utilidades import (
    Usuarios,
    Productos,
    Ordenes,
    OrdenesItems,
    Proveedor,
    ProveedoresProductos,
)


def readFormat(text: str, separator: str, typing: list):
    return map(
        lambda tuple: tuple[1](tuple[0]), zip(text.strip().split(separator), typing)
    )


def dateToDays(date: str, separator: str = "-"):
    years, months, days = map(int, date.split(separator))

    return years * 60 * 60 + months * 60 + days


def cargar_usuarios(path: str) -> Generator:
    with Path(path).open("r", encoding="utf-8") as file:
        next(file)

        for line in file:
            data = line.strip().split(";")
            yield Usuarios(*data)


def cargar_productos(path: str) -> Generator:
    with Path(path).open("r", encoding="utf-8") as file:
        next(file)

        for line in file:
            data = readFormat(line, ";", [str, str, float, int, str, str, str, str])
            yield Productos(*data)


def cargar_ordenes(path: str) -> Generator:
    with Path(path).open("r", encoding="utf-8") as file:
        next(file)

        for line in file:
            data = line.strip().split(";")
            yield Ordenes(*data)


def cargar_ordenes_items(path: str) -> Generator:
    with Path(path).open("r", encoding="utf-8") as file:
        next(file)

        for line in file:
            data = readFormat(line, ";", [str, str, int])
            yield OrdenesItems(*data)


def cargar_proveedores(path: str) -> Generator:
    with Path(path).open("r", encoding="utf-8") as file:
        next(file)

        for line in file:
            data = line.strip().split(";")
            yield Proveedor(*data)


def cargar_proveedores_productos(path: str) -> Generator:
    with Path(path).open("r", encoding="utf-8") as file:
        next(file)

        for line in file:
            data = line.strip().split(";")
            yield ProveedoresProductos(*data)


# CONSULTAS


# CONSULTAS SIMPLES (1 GENERADOR)


def productos_desde_fecha(
    generador_productos: Generator, fecha: str, inverso: bool
) -> Generator:
    days = dateToDays(fecha)

    def is_date_in_range(product: Productos):
        current_days = dateToDays(product.fecha_modificacion)

        return current_days == days or inverso ^ (current_days > days)

    return filter(is_date_in_range, generador_productos)


def buscar_orden_por_contenido(
    generador_ordenes_items: Generator, id_producto: str, cantidad: int
) -> Generator:
    return map(
        lambda item: item.id_base_datos_orden,
        filter(
            lambda item: item.id_base_datos_producto == id_producto
            and item.cantidad_productos == cantidad,
            generador_ordenes_items,
        ),
    )


def proveedores_por_estado(generador_proveedores: Generator, estado: str) -> Generator:
    return map(
        lambda supplier: supplier.nombre_proveedor,
        filter(lambda supplier: supplier.estado == estado, generador_proveedores),
    )


def ordenes_segun_estado_orden(
    generador_ordenes: Generator, estado_orden: str
) -> Generator:
    return filter(lambda order: order.estado_orden == estado_orden, generador_ordenes)


def ordenes_entre_fechas(
    generador_ordenes: Generator, fecha_inicial: str, fecha_final: str
) -> Generator:
    start = -float("inf") if fecha_inicial == "-" else dateToDays(fecha_inicial)
    end = float("inf") if fecha_final == "-" else dateToDays(fecha_final)

    return filter(
        lambda order: start <= dateToDays(order.fecha_creacion) <= end,
        generador_ordenes,
    )


# TODO: Ask if _asdict() is bad practice
def modificar_estado_orden_ordenes_previas_fecha(
    generador_ordenes: Generator, fecha: str, cambio_estados: dict
) -> Generator:
    days = dateToDays(fecha)

    return map(
        lambda order: Ordenes(
            **{
                **order._asdict(),
                **{"estado_orden": cambio_estados[order.estado_orden]},
            }
        ),
        filter(
            lambda order: dateToDays(order.fecha_creacion) < days
            and order.estado_orden in cambio_estados,
            generador_ordenes,
        ),
    )


# CONSULTAS COMPLEJAS (2 o 3 GENERADORES)


def producto_mas_popular(
    generador_productos: Generator,
    generador_ordenes: Generator,
    generador_ordenes_items: Generator,
    fecha_inicial: str,
    fecha_final: str,
    ranking: int,
) -> Iterable:
    pass


def ordenes_usuario(
    generador_productos: Generator,
    generador_ordenes: Generator,
    generador_ordenes_items: Generator,
    ids_usuario: list,
) -> dict:
    pass


def valor_orden(
    generador_productos: Generator, generador_ordenes_items: Generator, id_orden: str
) -> float:
    pass


def proveedores_segun_precio_productos(
    generador_productos: Generator,
    generador_proveedores: Generator,
    generador_proveedor_producto: Generator,
    precio: float,
) -> list:
    pass


def precio_promedio_segun_estado_orden(
    generador_ordenes: Generator,
    generador_ordenes_items: Generator,
    generador_productos: Generator,
    estado_orden: str,
) -> float:
    pass


def cantidad_vendida_productos(
    generador_productos: Generator,
    generador_ordenes_items: Generator,
    ids_productos: list,
) -> dict:
    pass


def ordenes_dirigidas_al_estado(
    generador_ordenes: Generator, generador_usuarios: Generator, estado: str
) -> Generator:
    pass


def ganancias_dadas_por_clientes(
    generador_productos: Generator,
    generador_ordenes: Generator,
    generador_ordenes_items: Generator,
    ids_usuarios: list,
) -> dict:
    pass


def modificar_estados_ordenes_dirigidas_al_estado(
    generador_ordenes: Generator,
    generador_usuarios: Generator,
    estado: str,
    cambio_estados_ordenes: dict,
) -> Generator:
    pass


def agrupar_items_por_maximo_pedido(
    generador_productos: Generator, generador_ordenes_items: Generator
) -> Generator:
    pass
