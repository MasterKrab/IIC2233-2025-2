from typing import Generator
from os.path import join

from utilidades import fecha_actual

from frontend.table import Table

from backend.consultas import (
    cargar_usuarios,
    cargar_productos,
    cargar_ordenes,
    cargar_ordenes_items,
    cargar_proveedores,
    cargar_proveedores_productos,
    productos_desde_fecha,
    buscar_orden_por_contenido,
    proveedores_por_estado,
    ordenes_segun_estado_orden,
    ordenes_entre_fechas,
    ordenes_entre_fechas,
    modificar_estado_orden_ordenes_previas_fecha,
    producto_mas_popular,
    ordenes_usuario,
    valor_orden,
    proveedores_segun_precio_productos,
    precio_promedio_segun_estado_orden,
    cantidad_vendida_productos,
    ordenes_dirigidas_al_estado,
    ganancias_dadas_por_clientes,
    modificar_estados_ordenes_dirigidas_al_estado,
    agrupar_items_por_maximo_pedido,
)

from utils.format import formatNamedtuples, formatDicts
from utils.state import extract_state

from constants import (
    USERS_FILE,
    PRODUCTS_FILE,
    ORDERS_FILE,
    ITEMS_ORDERS_FILE,
    SUPPLIERS_PRODUCTS_FILE,
    SUPPLIERS_FILE,
)


def handle_productos_desde_fecha(path: str) -> Generator:
    products = cargar_productos(join(path, PRODUCTS_FILE))

    return productos_desde_fecha(products, fecha_actual(), False)


def handle_buscar_orden_por_contenido(path: str) -> Generator:
    order_items = cargar_ordenes_items(join(path, ITEMS_ORDERS_FILE))
    order_items_copy = cargar_ordenes_items(join(path, ITEMS_ORDERS_FILE))

    order = next(order_items_copy)

    id = order.id_base_datos_producto
    amount = order.cantidad_productos

    for item in buscar_orden_por_contenido(order_items, id, amount):
        yield {"id_base_datos_orden": item}


def handle_proveedores_por_estado(path: str) -> Generator:
    for item in proveedores_por_estado(
        cargar_proveedores(join(path, SUPPLIERS_FILE)), "VI"
    ):
        yield {
            "nombre_proveedor": item,
        }


def handle_ordenes_segun_estado_orden(path: str) -> Generator:
    return ordenes_segun_estado_orden(
        cargar_ordenes(join(path, ORDERS_FILE)), "shipped"
    )


def handle_ordenes_entre_fechas(path: str) -> Generator:
    return ordenes_entre_fechas(
        cargar_ordenes(join(path, ORDERS_FILE)), "2022-05-08", "2023-11-24"
    )


def handle_modificar_estado_orden_ordenes_previas_fecha(path: str) -> Generator:
    return modificar_estado_orden_ordenes_previas_fecha(
        cargar_ordenes(join(path, ORDERS_FILE)),
        "2022-05-08",
        {"pending": "shipped", "shipped": "delivered"},
    )


def handle_producto_mas_popular(path: str) -> Generator:
    products = cargar_productos(join(path, PRODUCTS_FILE))
    orders = cargar_ordenes(join(path, ORDERS_FILE))
    items_orders = cargar_ordenes_items(join(path, ITEMS_ORDERS_FILE))

    for name in producto_mas_popular(
        products, orders, items_orders, "2022-05-08", "2023-11-24", 10
    ):
        yield {"nombre_producto": name}


def handle_ordenes_usuario(path: str) -> Generator:
    produts = cargar_productos(join(path, PRODUCTS_FILE))
    orders = cargar_ordenes(join(path, ORDERS_FILE))
    items_orders = cargar_ordenes_items(join(path, ITEMS_ORDERS_FILE))

    users = cargar_usuarios(join(path, USERS_FILE))

    ids = []

    for user in users:
        if len(ids) >= 10:
            break

        ids.append(user.id_base_datos)

    user_orders = ordenes_usuario(produts, orders, items_orders, ids)

    for user_id, values in user_orders.items():
        for product_id, amount in values.items():
            yield {
                "id_base_datos_usuario": user_id,
                "id_base_datos_producto": product_id,
                "cantidad_productos": amount,
            }


def handle_valor_orden(path: str) -> Generator:
    products = cargar_productos(join(path, PRODUCTS_FILE))
    orders = cargar_ordenes(join(path, ORDERS_FILE))
    items_orders = cargar_ordenes_items(join(path, ITEMS_ORDERS_FILE))

    order = next(orders)
    id = order.id_base_datos

    value = valor_orden(products, items_orders, id)

    yield {"id_base_datos_orden": id, "valor_total_orden": value}


def handle_proveedores_segun_precio_productos(path: str) -> Generator:
    products = cargar_productos(join(path, PRODUCTS_FILE))
    suppliers = cargar_proveedores(join(path, SUPPLIERS_FILE))
    suppliers_products = cargar_proveedores_productos(
        join(path, SUPPLIERS_PRODUCTS_FILE)
    )

    for supplier, amount in proveedores_segun_precio_productos(
        products, suppliers, suppliers_products, 1000
    ):
        yield {**supplier._asdict(), "cantidad_productos": amount}


def handle_precio_promedio_segun_estado_orden(path: str) -> Generator:
    products = cargar_productos(join(path, PRODUCTS_FILE))
    orders = cargar_ordenes(join(path, ORDERS_FILE))
    items_orders = cargar_ordenes_items(join(path, ITEMS_ORDERS_FILE))

    price = precio_promedio_segun_estado_orden(
        orders, items_orders, products, "shipped"
    )

    yield {"precio_promedio": price}


def handle_cantidad_vendida_productos(path: str) -> Generator:
    products = cargar_productos(join(path, PRODUCTS_FILE))
    items_orders = cargar_ordenes_items(join(path, ITEMS_ORDERS_FILE))

    products_copy = cargar_productos(join(path, PRODUCTS_FILE))

    ids = []

    for product in products_copy:
        if len(ids) >= 10:
            break

        ids.append(product.id_base_datos)

    for product_id, amount in cantidad_vendida_productos(
        products, items_orders, ids
    ).items():
        yield {
            "id_base_datos_producto": product_id,
            "cantidad_vendida": amount,
        }


def handle_ordenes_dirigidas_al_estado(path: str) -> Generator:
    orders = cargar_ordenes(join(path, ORDERS_FILE))
    users = cargar_usuarios(join(path, USERS_FILE))

    users = cargar_usuarios(join(path, USERS_FILE))

    user = next(users)
    state = extract_state(user.direccion)

    return ordenes_dirigidas_al_estado(orders, users, state)


def handle_ganancias_dadas_por_clientes(path: str) -> Generator:
    products = cargar_productos(join(path, PRODUCTS_FILE))
    orders = cargar_ordenes(join(path, ORDERS_FILE))
    items_orders = cargar_ordenes_items(join(path, ITEMS_ORDERS_FILE))

    users = cargar_usuarios(join(path, USERS_FILE))

    ids = []

    for user in users:
        if len(ids) >= 10:
            break

        ids.append(user.id_base_datos)

    for user_id, income in ganancias_dadas_por_clientes(
        products, orders, items_orders, ids
    ).items():
        yield {
            "id_base_datos": user_id,
            "ganancia": income,
        }


def handle_modificar_estados_ordenes_dirigidas_al_estado(path: str) -> Generator:
    orders = cargar_ordenes(join(path, ORDERS_FILE))
    users = cargar_usuarios(join(path, USERS_FILE))

    users_copy = cargar_usuarios(join(path, USERS_FILE))

    user = next(users_copy)
    state = extract_state(user.direccion)

    return modificar_estados_ordenes_dirigidas_al_estado(
        orders,
        users,
        state,
        {"pending": "shipped", "shipped": "delivered"},
    )


def handle_agrupar_items_por_maximo_pedido(path: str) -> Generator:
    products = cargar_productos(join(path, PRODUCTS_FILE))
    items_orders = cargar_ordenes_items(join(path, ITEMS_ORDERS_FILE))

    return agrupar_items_por_maximo_pedido(products, items_orders)


QUERIES_HANDLES = {
    "productos_desde_fecha": handle_productos_desde_fecha,
    "buscar_orden_por_contenido": handle_buscar_orden_por_contenido,
    "proveedores_por_estado": handle_proveedores_por_estado,
    "ordenes_segun_estado_orden": handle_ordenes_segun_estado_orden,
    "ordenes_entre_fechas": handle_ordenes_entre_fechas,
    "modificar_estado_orden_ordenes_previas_fecha": handle_modificar_estado_orden_ordenes_previas_fecha,
    "producto_mas_popular": handle_producto_mas_popular,
    "ordenes_usuario": handle_ordenes_usuario,
    "valor_orden": handle_valor_orden,
    "proveedores_segun_precio_productos": handle_proveedores_segun_precio_productos,
    "precio_promedio_segun_estado_orden": handle_precio_promedio_segun_estado_orden,
    "cantidad_vendida_productos": handle_cantidad_vendida_productos,
    "ordenes_dirigidas_al_estado": handle_ordenes_dirigidas_al_estado,
    "ganancias_dadas_por_clientes": handle_ganancias_dadas_por_clientes,
    "modificar_estados_ordenes_dirigidas_al_estado": handle_modificar_estados_ordenes_dirigidas_al_estado,
    "agrupar_items_por_maximo_pedido": handle_agrupar_items_por_maximo_pedido,
}


def make_query(path: str, query: str) -> Generator:
    if not query in QUERIES_HANDLES:
        raise ValueError(f"Query '{query}' not found.")

    result = QUERIES_HANDLES[query](path)

    while True:
        data = []

        for i in range(100):
            try:
                data.append(next(result))
            except StopIteration:
                break

        if not data:
            raise StopIteration()

        if isinstance(data[0], dict):
            header, rows = formatDicts(data)
        elif isinstance(data[0], tuple):
            header, rows = formatNamedtuples(data)

        yield Table(header, rows)
