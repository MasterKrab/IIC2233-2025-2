def read_input(types: list[str, float, int], separator: str, text: str = None):
    if text is None:
        text = input()

    values = text.strip().split(separator)

    result = []

    for i in range(len(values)):
        if types[i] == str:
            values[i] = values[i].strip()

        result.append(types[i](values[i]))

    return result


def read_inputs(type: str | float | int, separator: str, text: str = None):
    if text is None:
        text = input()

    values = text.strip().split(separator)

    result = []

    for i in range(len(values)):
        if type == str:
            values[i] = values[i].strip()

        result.append(type(values[i]))

    return result
