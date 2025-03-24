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

    return input(f"Indique su opción ({numbers}): ")


def erase_prints():
    print("\n" * 100)


def print_tree_change(before: Bonsai, after: Bonsai):
    print()
    print("Bonsái original:")
    print()

    before.visualizar_bonsai("Vertical", True, False)

    print()
    print("Bonsái modificado:")
    print()

    after.visualizar_bonsai("Vertical", True, False)

    print()


def ask_yes_no(question: str) -> bool:
    print()

    while True:
        answer = input(f"{question} (Si/No): ").strip().lower()

        if answer == "s" or answer == "si":
            return True

        if answer == "n" or answer == "no":
            return False

        print("Respuesta no válida.")


def ask_non_negative_number(question: str) -> int:

    while True:
        answer = input(f"{question}: ").strip()

        if answer.isdigit():
            if int(answer) < 0:
                print("El número debe ser no negativo.")
                continue

            return int(answer)

        print("Respuesta no válida.")


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

    tree = Bonsai("1", 1, 1, [])
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
            if corta_ramas.es_simetrico(tree):
                print("El bonsái ya está podado.")
            else:

                with_min_cost = ask_yes_no("¿Podar con el costo mínimo?")

                tree_copy = tree.copy()

                if with_min_cost:
                    cut_cost = ask_non_negative_number("Ingrese el costo de corte")
                    flower_cost = ask_non_negative_number(
                        "Ingrese el costo de modificar una flor"
                    )

                    tree.costo_corte = cut_cost
                    tree.costo_flor = flower_cost

                    solution = corta_ramas.emparejar_bonsai_ahorro(tree)

                    tree.costo_corte = 1
                    tree.costo_flor = 1

                    was_balanced = solution[0]

                    if was_balanced:
                        cost, changes = solution[1:]

                        corta_ramas.apply_solution(tree, changes)

                        print(
                            f"El bonsái fue podado con costo mínimo de {cost}", end=""
                        )

                        print(f"y {len(changes)} cambios")

                        print_tree_change(tree_copy, tree)
                    else:
                        print("No es posible podar el bonsái.")
                else:
                    was_balanced, changes = corta_ramas.emparejar_bonsai(tree)

                    if was_balanced:
                        print(f"El bonsái fue podado con {len(changes)} cambios")

                        corta_ramas.apply_solution(tree, changes)

                        print_tree_change(tree_copy, tree)
                    else:
                        print("No es posible podar el bonsái.")

        print()

        if 1 <= answer <= 5:
            input("Presione enter para volver al menu. ")
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
