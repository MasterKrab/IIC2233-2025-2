def read_format(text: str, separator: str, typing: list):
    return map(
        lambda tuple: tuple[1](tuple[0]), zip(
            text.strip().split(separator), typing)
    )
