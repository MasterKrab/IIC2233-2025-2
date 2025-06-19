def read_format(types: list, separator: str, text: str = None) -> list[tuple]:
    """ "
    Function extracted doing modifications from my "Tarea 2"; that is, a function by
    Enzo Vivallo (GitHub: Masterkrab), retrieved on June 16, 2025, from
    https://github.com/IIC2233/MasterKrab-iic2233-2025-1/blob/main/Tareas/T2/utils/input.py
    """
    if text is None:
        text = input()

    values = text.strip().split(separator)

    result = []

    for i in range(len(values)):
        if types[i] is str:
            values[i] = values[i].strip()

        result.append(types[i](values[i]))

    return result
