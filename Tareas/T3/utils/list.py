def flatten(values: list) -> list:
    result = []

    for item in values:
        if isinstance(item, list):
            result = [*result, *flatten(item)]
        else:
            result = [*result, item]

    return result
