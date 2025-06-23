from typing import Optional

from servidor.database.files import (
    read_users,
    read_user_games,
    users_games_by_set,
)
from utils.duration import duration_text_to_seconds, seconds_to_duration
from utils.find import find
from parametros import (
    MINIMO_ENTRADAS_CLASIFICACION,
    RANKINGS,
    RANKING_SUPERVIVENCIA,
    RANKING_SUPERVIVENCIA_LENGUAJE,
    RANKING_PUNTAJES,
    RANKING_PUNTAJES_LENGUAJE,
    RANKING_ADICCION,
)


def supervivencia_ranking(game_set: Optional[str] = None):
    users = read_users()

    users_data = []
    user_by_name = dict()

    for user in users:
        name = user["name"]

        users_data.append({"name": name, "max_time": 0})
        user_by_name[name] = users_data[-1]

    users_games = (
        read_user_games() if game_set is None else users_games_by_set(game_set)
    )

    for game in users_games:
        for user_results in game["usuarios"]:
            user = user_by_name[user_results["nombre"]]

            time = duration_text_to_seconds(user_results["supervivencia"])

            user["max_time"] = max(user["max_time"], time)

    users_data.sort(key=lambda user: user["max_time"], reverse=True)

    return [
        {
            "nombre": user["name"],
            "supervivencia-maxima": seconds_to_duration(user["max_time"]),
        }
        for user in users_data
    ]


def puntajes_ranking(game_set: Optional[str] = None):
    users = read_users()

    users_data = []
    user_by_name = dict()

    for user in users:
        name = user["name"]

        users_data.append({"name": name, "puntaje-maximo": 0})
        user_by_name[name] = users_data[-1]

    users_games = (
        read_user_games() if game_set is None else users_games_by_set(game_set)
    )

    for game in users_games:
        for user_results in game["usuarios"]:
            user = user_by_name[user_results["nombre"]]

            user["puntaje-maximo"] = max(
                user["puntaje-maximo"], user_results["puntaje"]
            )

    users_data.sort(key=lambda user: user["puntaje-maximo"], reverse=True)

    return [
        {
            "nombre": user["name"],
            "puntaje-maximo": user["puntaje-maximo"],
        }
        for user in users_data
    ]


def addiccion():
    users = read_users()

    users_games = read_user_games()

    users_data = []
    user_by_name = dict()

    for user in users:
        name = user["name"]

        users_data.append({"name": name, "games": 0})
        user_by_name[name] = users_data[-1]

    for game in users_games:
        for user_results in game["usuarios"]:
            user = user_by_name[user_results["nombre"]]

            user["games"] += 1

    users_data.sort(key=lambda user: user["games"], reverse=True)

    return [{"nombre": user["name"], "partidas": user["games"]} for user in users_data]


def victorias():
    users = read_users()

    users_games = read_user_games()

    users_data = []
    user_by_name = dict()

    for user in users:
        name = user["name"]

        users_data.append({"name": name, "wins": 0})
        user_by_name[name] = users_data[-1]

    for game in users_games:
        max_time = max(
            user_results["supervivencia"] for user_results in game["usuarios"]
        )

        user = find(
            lambda user_results: user_results["supervivencia"] == max_time,
            game["usuarios"],
        )

        user_data = user_by_name[user["nombre"]]

        user_data["wins"] += 1

    users_data.sort(key=lambda user: user["wins"], reverse=True)

    return [{"nombre": user["name"], "victorias": user["wins"]} for user in users_data]


def calculate_rankings(
    name, amount=MINIMO_ENTRADAS_CLASIFICACION, game_set: Optional[str] = None
):
    formatted_name = name.lower().strip()

    if formatted_name not in RANKINGS:
        raise ValueError("Ranking name is not valid")

    if formatted_name == RANKING_SUPERVIVENCIA:
        return supervivencia_ranking()[:amount]

    if formatted_name == RANKING_SUPERVIVENCIA_LENGUAJE:
        return supervivencia_ranking(game_set)[:amount]

    if formatted_name == RANKING_PUNTAJES:
        return puntajes_ranking()[:amount]

    if formatted_name == RANKING_PUNTAJES_LENGUAJE:
        return puntajes_ranking(game_set)[:amount]

    if formatted_name == RANKING_ADICCION:
        return addiccion()[:amount]

    return victorias()[:amount]
