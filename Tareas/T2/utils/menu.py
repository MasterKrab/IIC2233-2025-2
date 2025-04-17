from utils.terminal import create_table


def get_number_in_range(text: str, min: int, max: int) -> int:
    while True:
        number = input(text)

        try:
            number = int(number)
        except ValueError:
            print("El valor ingresado no es un número.")
            continue

        if number < min or number > max:
            print(f"El número debe estar entre {min} y {max} inclusive.")
            continue

        return number


def get_number_in_set(text: str, numbers: set[int]) -> int:
    numbers_text = []

    for number in numbers:
        numbers_text.append(str(number))

    while True:
        number = input(text)

        try:
            number = int(number)
        except ValueError:
            print("El valor ingresado no es un número.")
            continue

        if number not in numbers:
            print("El valor ingresado no esta en el conjunto de números válidos.")
            print(f"Los números válidos son: {', '.join(numbers_text)}.")
            continue

        return number


def print_menu(
    table: list[str, str] | list[str],
    choose_text: str,
    min: int,
    max: int,
    exit_text: str = None,
):

    if isinstance(table[0], str):
        for i in range(len(table)):
            print(f"[{i+1}] {table[i]}")
    else:
        print(create_table(table))

    if exit_text:
        print(f"[{len(table) + 1}] {exit_text}")

    print()

    while True:
        answer = input(choose_text)

        try:
            number = int(answer)
        except ValueError:
            print("El valor ingresado no es un número.")
            continue

        number = int(answer)

        if number < min or number > max:
            print(f"El número debe estar entre {min} y {max} inclusive.")
            continue

        return number
