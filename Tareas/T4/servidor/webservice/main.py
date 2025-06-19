import json
from flask import Flask, Response, request
from wsgiref.simple_server import make_server

from servidor.utils.read_sets import read_sets
from servidor.database.read import (
    read_users,
    update_users,
    read_games,
    update_games,
    read_user_games,
    update_user_games,
)
from servidor.database.rankings import calculate_rankings
from utils.find import find
from utils.log import log
from utils.duration import is_valid_duration
from parametros import RANKINGS

app = Flask(__name__)


def create_answer(data: dict, status_code: int) -> Response:
    """
    Function "create_answer" extracted doing modifications from "Actividad 8", retrieved on June 14, 2025, from
    https://github.com/IIC2233/Syllabus/tree/main/Actividades/AC8
    """

    return Response(
        response=json.dumps(data),
        status=status_code,
        content_type="application/json",
    )


@app.route("/rankings")
def get_rankings():
    name = request.args.get("nombre")

    if not name:
        return create_answer({"message": "Name parameter is required"}, 400)

    if name.strip().lower() not in RANKINGS:
        return create_answer({"message": "Invalid ranking name"}, 400)

    game_set = request.args.get("conjunto")

    if game_set is not None:
        games_sets = [game_set["name"] for game_set in read_sets()] + ["personalizado"]

        if game_set not in games_sets:
            return create_answer({"message": "Invalid game set"}, 400)

    amount_text = request.args.get("cantidad")

    if not amount.isdigit():
        return create_answer({"message": "Invalid amount"}, 400)

    amount = int(amount_text)

    if amount < 0:
        return create_answer({"message": "Invalid amount"}, 400)

    rankings = calculate_rankings(name, amount, game_set)

    return create_answer(rankings, 200)


@app.route("/conjuntos")
def sets() -> Response:
    sets = read_sets()
    return create_answer(sets, 200)


@app.route("/users")
def get_users() -> Response:
    name = request.args.get("name")

    user = find(lambda user: user["name"] == name, read_users())

    if user is None:
        return create_answer({"message": "User not found"}, 404)

    return create_answer(user, 200)


@app.route("/users", methods=["POST"])
def create_user() -> Response:
    name = request.args.get("name")

    users = read_users()

    already_exists = name in [user["name"] for user in users]

    if already_exists:
        return create_answer({"message": "User already exists"}, 400)

    users.append({"name": name, "online": True})

    update_users(users)

    return create_answer({"message": "User created successfully"}, 201)


@app.route("/users", methods=["PATCH"])
def edit_user() -> Response:
    name = request.args.get("name")
    online = request.args.get("online")

    users = read_users()

    user = find(lambda user: user["name"] == name, users)

    if user is None:
        return create_answer({"message": "User not found"}, 404)

    if online.lower() not in ["true", "false"]:
        return create_answer({"message": "Invalid online value"}, 400)

    user["online"] = online.lower() == "true"

    update_users(users)

    return create_answer({"message": "User status changed"}, 200)


@app.route("/games", methods=["POST"])
def create_game() -> Response:
    body = request.get_json(force=True)

    game_id = body.get("id_partida")
    game_set = body.get("nombre_conjunto").strip()
    players = body.get("usuarios")

    users_names = set(user["name"] for user in read_users())
    players_names = set(player["nombre"] for player in players)

    # Check if all players exists
    if players_names - users_names:
        return create_answer({"message": "Invalid users"}, 400)

    games_sets = [game_set["name"] for game_set in read_sets()] + ["personalizado"]

    game_set_exists = game_set in games_sets

    if not game_set_exists:
        return create_answer({"message": "Invalid game set"}, 400)

    for player in players:
        if not is_valid_duration(player["supervivencia"]):
            return create_answer({"message": "Invalid duration"}, 400)

    duration = max(player["supervivencia"] for player in players)

    games = read_games()

    game_already_exists = game_id in [game["id"] for game in games]

    if game_already_exists:
        return create_answer({"message": "Game already exists"}, 400)

    winner = find(lambda player: player["supervivencia"] == duration, players)

    games.append(
        {"id": game_id, "duration": duration, "game_set": game_set, "winner": winner}
    )

    update_games(games)

    user_games = read_user_games()

    user_games.append({"id_partida": game_id, "usuarios": players})

    update_user_games(user_games)

    return create_answer({"message": "Game created successfully"}, 201)


def init_webservice(port: int, host: str):
    with make_server(host, port, app) as httpd:
        try:
            log(f"Iniciando servidor web: http://{host}:{port}")
            httpd.serve_forever()
        except KeyboardInterrupt:
            log("Apagando servidor web")
            httpd.shutdown()
