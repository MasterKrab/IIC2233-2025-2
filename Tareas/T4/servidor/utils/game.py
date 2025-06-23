from random import randint
from math import e as euler, log2
import requests

from servidor.utils.config import get_api_url
from servidor.parametros import TOKEN_AUTENTICACION
from servidor.parametros import (
    TIEMPO_APARICION_MAXIMO,
    TIEMPO_APARICION_MINIMO,
    TIEMPO_CAIDA_MAXIMO,
)
from utils.duration import seconds_to_duration


def generate_spawn_interval(current_dificulty: int) -> int:
    return randint(
        max(
            TIEMPO_APARICION_MINIMO,
            round((TIEMPO_APARICION_MAXIMO - current_dificulty) / 2),
        ),
        max(
            TIEMPO_APARICION_MINIMO, round(TIEMPO_APARICION_MAXIMO - current_dificulty)
        ),
    )


def calculate_fall_time(current_dificulty: int) -> int:
    divisor = 1 + euler ** (0.08 * (current_dificulty - 50))
    return int(TIEMPO_CAIDA_MAXIMO / divisor)


def calculate_points(word: str, current_dificulty: int, streak: int) -> int:
    return len(word) * log2(1 + current_dificulty) * log2(2 + streak)


def save_game(game_id: int, game_set: str, data: dict):
    users = list(data.values())

    users.sort(key=lambda user: user["supervivencia"], reverse=True)

    for user in users:
        user["supervivencia"] = seconds_to_duration(int(user["supervivencia"]))

    data = {"id_partida": game_id, "nombre_conjunto": game_set, "usuarios": users}

    requests.post(
        f"{get_api_url()}/games",
        headers={"token": TOKEN_AUTENTICACION},
        json=data,
    )
