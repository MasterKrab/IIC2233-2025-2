from typing import Generator, Iterable
from pathlib import Path
from typing import Callable, Generator, TypeVar, Optional
from collections import defaultdict
from utilidades import (
    Usuarios,
    Productos,
    Ordenes,
    OrdenesItems,
    Proveedor,
    ProveedoresProductos,
    fecha_actual,
    cambio_unidad_medida,
)


def readFormat(text: str, separator: str, typing: list):
    return map(
        lambda tuple: tuple[1](tuple[0]), zip(text.strip().split(separator), typing)
    )


def dateToDays(date: str, separator: str = "-"):
    years, months, days = map(int, date.split(separator))

    return years * 60 * 60 + months * 60 + days


Item = TypeVar("Item")


def find(callback: Callable[[Item], bool], generator: Generator) -> Optional[Item]:
    for item in generator:
        if callback(item):
            return item

    return None


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


def extract_state(text: str) -> str:
    return text.split(" ")[::-1][1].strip().upper()


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
    valid_orders_ids = set(
        map(
            lambda order: order.id_base_datos,
            ordenes_entre_fechas(generador_ordenes, fecha_inicial, fecha_final),
        )
    )

    valid_items = filter(
        lambda item: item.id_base_datos_orden in valid_orders_ids,
        generador_ordenes_items,
    )

    products_scores = dict()

    for item in valid_items:
        id = item.id_base_datos_producto
        products_scores[id] = products_scores.get(id, 0) + item.cantidad_productos

    products = sorted(
        filter(
            lambda product: products_scores.get(product.id_base_datos, 0) > 0,
            generador_productos,
        ),
        key=lambda product: (
            -products_scores.get(product.id_base_datos, 0),
            product.id_base_datos,
        ),
    )

    return map(lambda product: product.nombre, products[:ranking])


def ordenes_usuario(
    generador_productos: Generator,
    generador_ordenes: Generator,
    generador_ordenes_items: Generator,
    ids_usuario: list,
) -> dict:
    amount_products_by_id = dict()

    for product in generador_productos:
        amount_products_by_id[product.id_base_datos] = product.cantidad_por_unidad

    user_id_by_order_id = dict()

    for order in generador_ordenes:
        user_id_by_order_id[order.id_base_datos] = order.id_base_datos_usuario

    result = dict()

    for id in ids_usuario:
        result[id] = dict()

    for item in generador_ordenes_items:
        amount = (
            item.cantidad_productos * amount_products_by_id[item.id_base_datos_producto]
        )

        user_id = user_id_by_order_id[item.id_base_datos_orden]

        if user_id not in ids_usuario:
            continue

        result[user_id][item.id_base_datos_producto] = (
            result[user_id].get(item.id_base_datos_producto, 0) + amount
        )

    return result


def valor_orden(
    generador_productos: Generator, generador_ordenes_items: Generator, id_orden: str
) -> float:
    products_price_by_id = dict()

    for product in generador_productos:
        products_price_by_id[product.id_base_datos] = product.precio

    orders = filter(
        lambda order: order.id_base_datos_orden == id_orden, generador_ordenes_items
    )

    total = 0.0

    for order in orders:
        total += (
            products_price_by_id[order.id_base_datos_producto]
            * order.cantidad_productos
        )

    return total


def proveedores_segun_precio_productos(
    generador_productos: Generator,
    generador_proveedores: Generator,
    generador_proveedor_producto: Generator,
    precio: float,
) -> list:
    supplier_name_by_supplier_product_id = dict()
    products_amount_by_supplier_name = dict()

    for supplier_product in generador_proveedor_producto:
        suplier_id = supplier_product.identificador_del_proveedor
        supplier_name = supplier_product.nombre_proveedor

        supplier_name_by_supplier_product_id[suplier_id] = supplier_name
        products_amount_by_supplier_name[supplier_name] = 0

    max_cost_by_supplier_name = defaultdict(int)

    for product in generador_productos:
        supplier_id = product.identificador_del_proveedor

        if supplier_id not in supplier_name_by_supplier_product_id:
            continue

        supplier_name = supplier_name_by_supplier_product_id[supplier_id]

        last_price = max_cost_by_supplier_name[supplier_name]

        max_cost_by_supplier_name[supplier_name] = max(product.precio, last_price)

        last_amount = products_amount_by_supplier_name[supplier_name]

        products_amount_by_supplier_name[supplier_name] = last_amount + 1

    suppliers = filter(
        lambda supplier: max_cost_by_supplier_name.get(
            supplier.nombre_proveedor, float("inf")
        )
        < precio,
        generador_proveedores,
    )

    result = []

    for supplier in suppliers:
        result.append(
            (supplier, products_amount_by_supplier_name[supplier.nombre_proveedor])
        )

    return result


def precio_promedio_segun_estado_orden(
    generador_ordenes: Generator,
    generador_ordenes_items: Generator,
    generador_productos: Generator,
    estado_orden: str,
) -> float:
    price_by_product_id = dict()

    for product in generador_productos:
        price_by_product_id[product.id_base_datos] = product.precio

    price_by_order_id = defaultdict(int)

    for order in generador_ordenes_items:
        price_by_order_id[order.id_base_datos_orden] += (
            price_by_product_id[order.id_base_datos_producto] * order.cantidad_productos
        )

    total = 0.0
    count = 0.0

    for order in ordenes_segun_estado_orden(generador_ordenes, estado_orden):
        total += price_by_order_id[order.id_base_datos]
        count += 1

    if count == 0:
        return 0.0

    return round(total / count, 2)


def cantidad_vendida_productos(
    generador_productos: Generator,
    generador_ordenes_items: Generator,
    ids_productos: list,
) -> dict:
    unit_amount_by_product_id = dict()

    for product in generador_productos:
        unit_amount_by_product_id[product.id_base_datos] = product.cantidad_por_unidad

    ids_products = set(ids_productos)

    amount_by_product_id = dict()

    ids_products = set(ids_productos)

    for id in ids_products:
        amount_by_product_id[id] = 0

    for order in generador_ordenes_items:
        if order.id_base_datos_producto not in ids_products:
            continue

        current = (
            unit_amount_by_product_id[order.id_base_datos_producto]
            * order.cantidad_productos
        )

        amount_by_product_id[order.id_base_datos_producto] += current

    return amount_by_product_id


def ordenes_dirigidas_al_estado(
    generador_ordenes: Generator, generador_usuarios: Generator, estado: str
) -> Generator:
    user_state_by_user_id = dict()

    for user in generador_usuarios:
        user_state_by_user_id[user.id_base_datos] = extract_state(user.direccion)

    formatted_state = estado.strip().upper()

    return filter(
        lambda order: user_state_by_user_id[order.id_base_datos_usuario]
        == formatted_state,
        generador_ordenes,
    )


def ganancias_dadas_por_clientes(
    generador_productos: Generator,
    generador_ordenes: Generator,
    generador_ordenes_items: Generator,
    ids_usuarios: list,
) -> dict:
    user_id_by_order_id = dict()

    for order in generador_ordenes:
        user_id_by_order_id[order.id_base_datos] = order.id_base_datos_usuario

    product_price_by_product_id = dict()

    for product in generador_productos:
        product_price_by_product_id[product.id_base_datos] = product.precio

    ids_users = set(ids_usuarios)

    income_by_user_id = dict()

    for id in ids_usuarios:
        income_by_user_id[id] = 0

    for order in generador_ordenes_items:
        if order.id_base_datos_orden not in user_id_by_order_id:
            continue

        user_id = user_id_by_order_id[order.id_base_datos_orden]

        if user_id not in ids_users:
            continue

        current = (
            order.cantidad_productos
            * product_price_by_product_id[order.id_base_datos_producto]
        )

        income_by_user_id[user_id] += current

    return income_by_user_id


def modificar_estados_ordenes_dirigidas_al_estado(
    generador_ordenes: Generator,
    generador_usuarios: Generator,
    estado: str,
    cambio_estados_ordenes: dict,
) -> Generator:
    for order in ordenes_dirigidas_al_estado(
        generador_ordenes, generador_usuarios, estado
    ):
        if order.estado_orden not in cambio_estados_ordenes:
            yield order
            continue

        yield Ordenes(
            **{
                **order._asdict(),
                **{"estado_orden": cambio_estados_ordenes[order.estado_orden]},
            }
        )


def agrupar_items_por_maximo_pedido(
    generador_productos: Generator, generador_ordenes_items: Generator
) -> Generator:
    max_order_by_product_id = defaultdict(int)

    for item in generador_ordenes_items:
        current = item.cantidad_productos
        last = max_order_by_product_id[item.id_base_datos_producto]

        max_order_by_product_id[item.id_base_datos_producto] = max(current, last)

    def transform_product(product: Productos):
        max_order = max_order_by_product_id[product.id_base_datos]

        if max_order == 1:
            return product

        changes = {
            "unidad_de_medida": cambio_unidad_medida(product.unidad_de_medida),
            "cantidad_por_unidad": max_order * product.cantidad_por_unidad,
            "precio": max_order * product.precio,
            "fecha_modificacion": fecha_actual(),
        }

        new_data = {
            **product._asdict(),
            **changes,
        }

        return Productos(**new_data)

    return map(transform_product, generador_productos)


# Revisar tests: 10, 7
