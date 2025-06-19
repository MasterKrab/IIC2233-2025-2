from pathlib import Path

import json

from utils.read_format import read_format
from servidor.parametros import USERS_FILE, GAMES_FILE, USERS_GAMES_FILE


def check_file(file_path: Path) -> None:
    if not file_path.exists():
        file_path.touch()


def read_users() -> list[dict]:
    check_file(USERS_FILE)

    with USERS_FILE.open("r", encoding="utf-8") as file:
        lines = file.readlines()

    users = [
        {"name": name, "online": online == "True"}
        for name, online in (line.strip().split(",") for line in lines)
    ]

    return users


def update_users(users: list[dict]) -> None:
    check_file(USERS_FILE)

    with USERS_FILE.open("w", encoding="utf-8") as file:
        for user in users:
            file.write(f"{user['name']},{user['online']}\n")


def read_games():
    check_file(GAMES_FILE)

    with GAMES_FILE.open("r", encoding="utf-8") as file:
        lines = file.readlines()

    games = []

    for line in lines:
        id, duration, game_set, winner = read_format(
            [int, str, str, str], ",", line.strip()
        )

        games.append(
            {
                "id": id,
                "duration": duration,
                "game_set": game_set.strip(),
                "winner": winner.strip(),
            }
        )

    return games


def update_games(games: list[dict]) -> None:
    check_file(GAMES_FILE)

    with GAMES_FILE.open("w", encoding="utf-8") as file:
        for game in games:
            values = [game["id"], game["duration"], game["game_set"], game["winner"]]

            file.write(f"{','.join(map(str, values))}\n")


def read_user_games() -> dict:
    check_file(USERS_GAMES_FILE)

    with USERS_GAMES_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def update_user_games(user_games: dict) -> None:
    check_file(USERS_GAMES_FILE)

    with USERS_GAMES_FILE.open("w", encoding="utf-8") as file:
        json.dump(user_games, file)


def get_game_set_by_id():
    game_set_by_id = dict()
    games = read_games()

    for game in games:
        game_set_by_id[game["id"]] = game["game_set"]

    return game_set_by_id


def users_games_by_set(game_set: str):
    game_set_by_id = get_game_set_by_id()

    users_games = read_user_games()

    users_games = filter(
        lambda game: game_set == game_set_by_id[game["id_partida"]],
        users_games,
    )

    return list(users_games)
