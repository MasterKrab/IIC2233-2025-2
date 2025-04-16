def erase_terminal():
    print("\n" * 100)


def print_title(title: str, lateral_space: int = 10):

    bar = "-" * (len(title) + 2 * lateral_space)

    lateral_space_text = " " * lateral_space

    print(bar)
    print(f"{lateral_space_text}{title}{lateral_space_text}")
    print(bar)


def create_table(
    table: list[str, str],
):
    largest_size = max(len(row[0]) for row in table) + len(str(len(table)))

    rows = []

    for i in range(len(table)):
        separation = " " * (largest_size - len(table[i][0]) - len(str(i + 1)))

        rows.append(f"[{i+1}] {table[i][0]} {separation}: {table[i][1]}")

    return "\n".join(rows)


def continue_input():
    input("Presiona ENTER para continuar...")
