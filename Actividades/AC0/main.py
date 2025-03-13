from pathlib import Path
from entities import Item, Usuario
from utils.pretty_print import print_usuario, print_items, print_canasta, print_usuario


def cargar_items() -> list:
    items = []

    path = Path("utils", "items.dcc")

    with path.open(mode="r") as file:
        for line in file:
            name, price, points = line.split(",")

            new_item = Item(name, int(price), int(points))

            items.append(new_item)

    return items


def crear_usuario(tiene_suscripcion: bool) -> Usuario:
    user = Usuario(tiene_suscripcion)

    print_usuario(user)

    return user


if __name__ == "__main__":
    user = crear_usuario(True)

    items = cargar_items()

    print_items(items)

    for item in items:
        user.agregar_item(item)

    print_canasta(user)

    user.comprar()

    print_usuario(user)
