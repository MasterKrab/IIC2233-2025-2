from dccortaramas import Bonsai, DCCortaRamas, DONE, READ_FOLDER
from pathlib import Path


def print_top():
    print("¡Bienvenido a DCCortaramas!")
    print("*** Menú de Inicio ***")
    print()


def print_menu(options: list[str]) -> int:
    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")

    numbers = str(list(range(1, len(options) + 1)))[1:-1]

    return input(f"Indique su opción ({numbers}):")


def erase_prints():
    print("\n" * 100)


def main():
    print_top()

    while True:
        answer = int(print_menu(["Cargar bonsái", "Salir del programa"]))

        if answer == 2:
            return

        if answer == 1:
            break

        print("Opción no válida.")

    folder = input("Ingrese la carpeta donde se encuentra el archivo: ")
    filename = input("Ingrese el nombre del archivo: ")

    if not Path(READ_FOLDER, folder, filename).exists():
        print("El archivo no existe en la carpeta indicada.")
        return

    tree = Bonsai("1", 0, 0, [])
    corta_ramas = DCCortaRamas()
    tree.cargar_bonsai_de_archivo(folder, filename)

    while True:
        erase_prints()
        print_top()

        answer = int(
            print_menu(
                [
                    "Visualizar bonsái",
                    "Modificar Hoja",
                    "Cortar Rama",
                    "Verificar Simetría",
                    "Podar Bonsái",
                    "Salir del programa",
                ]
            )
        )

        if answer == 6:
            return

        if answer == 1:
            tree.visualizar_bonsai("Vertical", True, False)

        if answer == 2:
            id = input("Ingrese el nodo a modificar del Bonsái: ").strip()

            if corta_ramas.modificar_nodo(tree, id) != DONE:
                print("No se pudo modificar el nodo.")

            else:
                has_flower = tree.find_node(id)[1]

                if has_flower:
                    print("Se ha agregado la flor al nodo .")
                else:
                    print("Se ha removido la flor al nodo.")

        if answer == 3:
            id = input("Ingrese el nodo a eliminar del Bonsái: ").strip()

            if corta_ramas.quitar_nodo(tree, id) == DONE:
                print("Se ha eliminado el nodo.")
            else:
                print("No se pudo eliminar el nodo.")

        if answer == 4:
            if corta_ramas.es_simetrico(tree):
                print("El bonsái es simétrico.")
            else:
                print("El bonsái no es simétrico.")

        if answer == 5:
            print("Aún no esta implementado.")

        if 1 <= answer <= 5:
            input("Presione enter para volver al menu.")
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
