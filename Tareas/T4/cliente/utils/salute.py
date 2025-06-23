from random import choice

SALUTES = [
    "¡Hola, {}!",
    "¡Bienvenido, {}!",
    "¡Saludos, {}!",
    "¡Es un agrado verte, {}!",
    "!Eres el mejor, {}!",
]


def salute(name: str) -> str:
    return choice(SALUTES).format(name)
