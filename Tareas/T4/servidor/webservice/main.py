from wsgiref.simple_server import make_server
from flask import Flask, Response, request
from typing import Callable
from functools import wraps
import json


from servidor.utils.read_sets import read_sets
from servidor.database.files import (
    read_users,
    update_users,
    read_games,
    update_games,
    read_user_games,
    update_user_games,
    generate_game_id,
)
from servidor.database.rankings import calculate_rankings
from servidor.parametros import TOKEN_AUTENTICACION
from utils.find import find
from utils.log import log
from utils.duration import is_valid_duration
from parametros import RANKINGS, CUSTOM


app = Flask(__name__)


def create_answer(data: dict, status_code: int) -> Response:
    """
    Function "create_answer" extracted doing modifications from "Actividad 8",
    retrieved on June 14, 2025, from
    https://github.com/IIC2233/Syllabus/tree/main/Actividades/AC8
    """

    return Response(
        response=json.dumps(data),
        status=status_code,
        content_type="application/json",
    )


def protected(route: Callable) -> Callable:
    """
    Function extracted doing modifications from
    "How to Write a Decorator in Python Flask to Check Logged In Status",
    retrieved on June 22, 2025, from
    https://medium.com/geekculture/
    how-to-write-a-decorator-for-python-flask-to-check-logged-in-status-3689872f6635
    """

    @wraps(route)
    def decorated(*args, **kwargs):
        token = request.headers.get("token")

        if token != TOKEN_AUTENTICACION:
            return create_answer({"error": "Not allowed"}, 401)

        return route(*args, **kwargs)

    return decorated


@app.route("/check")
def check() -> Response:
    return create_answer({"message": "Web service is working!"}, 200)


@app.route("/rankings")
def get_rankings():
    name = request.args.get("nombre")

    if not name:
        return create_answer({"message": "Name parameter is required"}, 400)

    if name.strip().lower() not in RANKINGS:
        return create_answer({"message": "Invalid ranking name"}, 400)

    game_set = request.args.get("conjunto")

    if game_set is not None:
        games_sets = [game_set["name"] for game_set in read_sets()] + [CUSTOM]

        if game_set not in games_sets:
            return create_answer({"message": "Invalid game set"}, 400)

    amount_text = request.args.get("cantidad")

    if not amount_text.isdigit():
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
@protected
def get_users() -> Response:
    name = request.args.get("name")

    user = find(lambda user: user["name"] == name, read_users())

    if user is None:
        return create_answer({"message": "User not found"}, 404)

    return create_answer(user, 200)


@app.route("/users", methods=["POST"])
@protected
def create_user() -> Response:
    name_value = request.args.get("name")

    if name_value is None or not name_value.strip():
        return create_answer({"message": "Name is required"}, 400)

    name = name_value.strip()

    if "," in name or "\n" in name:
        return create_answer({"message": "Invalid name"}, 400)

    users = read_users()

    already_exists = name in [user["name"] for user in users]

    if already_exists:
        return create_answer({"message": "User already exists"}, 400)

    users.append({"name": name, "online": True})

    update_users(users)

    return create_answer({"message": "User created successfully"}, 201)


@app.route("/users", methods=["PATCH"])
@protected
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


@app.route("/game-id", methods=["POST"])
@protected
def create_game_id() -> Response:
    return create_answer(
        {"message": "Game id created successfully", "id": generate_game_id()}, 201
    )


@app.route("/games", methods=["POST"])
@protected
def create_game() -> Response:
    body = request.get_json(force=True)

    print(body)

    game_id = body.get("id_partida")
    game_set = body.get("nombre_conjunto").strip()
    players = body.get("usuarios")

    users_names = set(user["name"] for user in read_users())
    players_names = set(player["nombre"] for player in players)

    # Check if all players exists
    if players_names - users_names:
        return create_answer({"message": "Invalid users"}, 400)

    games_sets = [game_set["name"] for game_set in read_sets()] + [CUSTOM]

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
        {
            "id": game_id,
            "duration": duration,
            "game_set": game_set,
            "winner": winner["nombre"],
        }
    )

    update_games(games)

    user_games = read_user_games()

    user_games.append({"id_partida": game_id, "usuarios": players})
    print(user_games)

    update_user_games(user_games)

    return create_answer({"message": "Game created successfully"}, 201)


def init_webservice(port: int, host: str):
    with make_server(host, port, app) as httpd:
        try:
            log(f"Starting web server: http://{host}:{port}")
            httpd.serve_forever()
        except KeyboardInterrupt:
            log("Closing web server")
            httpd.shutdown()
