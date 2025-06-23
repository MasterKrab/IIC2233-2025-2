import socket
from queue import Queue
from threading import Thread, Lock
from time import time
import requests

from servidor.utils.id import create_id_generator
from servidor.utils.config import get_api_url
from servidor.user import UserThread
from servidor.game import Game
from servidor.parametros import TIEMPO_MAXIMO_BUSQUEDA_PARTIDA, TOKEN_AUTENTICACION
from utils.game_sets import get_game_sets
from utils.log import log
from utils.find import find
from parametros import CUSTOM


class Server:
    def __init__(self, port: int, host: str) -> None:
        self.host = host
        self.port = port

        self.users = {}
        self.users_lock = Lock()

        self.generate_user_id = create_id_generator()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.game_sets = [set["name"] for set in get_game_sets()] + [CUSTOM]

        self.searching_game_queue = Queue()

        self.waiting_game_groups = []

        self.waiting_game_thread = Thread(target=self.create_game, daemon=True)

        self.disconnect_users_thread = Thread(target=self.disconnect_users, daemon=True)
        self.disconnect_users_thread.start()

        self.games = []

    def run(self) -> None:
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        log(f"Server listening in {self.host}:{self.port}")

        self.waiting_game_thread.start()

        while True:
            socket, address = self.socket.accept()
            user_id = self.generate_user_id()

            thread = UserThread(
                user_id, socket, self.game_sets, self.searching_game_queue
            )

            with self.users_lock:
                self.users[user_id] = thread

                log(f"[id: {user_id}] Connection: {socket} {address}")

                thread.start()

    def create_game(self):
        while True:
            while not self.searching_game_queue.empty():
                user, game_set = self.searching_game_queue.get()

                group = find(
                    lambda group: group["game_set"] == game_set,
                    self.waiting_game_groups,
                )

                if group is None:
                    group = {
                        "game_set": game_set,
                        "users": [],
                        "start_time": time(),
                    }
                    self.waiting_game_groups.append(group)

                group["users"].append(user)

                self.searching_game_queue.task_done()

            remaing_groups = []

            for group in self.waiting_game_groups:
                game_set = group["game_set"]
                users = group["users"]
                start_time = group["start_time"]

                difference_time = time() - start_time

                if difference_time < TIEMPO_MAXIMO_BUSQUEDA_PARTIDA:
                    remaing_groups.append(group)
                    continue

                for user in users:
                    user.is_searching_game = False
                    user.pending_messages.put(
                        {
                            "type": "game-found",
                            "message": f"Game successfully found with {len(users)} players",
                            "game_set": game_set,
                        }
                    )

                response = requests.post(
                    f"{get_api_url()}/game-id",
                    headers={"token": TOKEN_AUTENTICACION},
                )
                
                data = response.json()

                game_id = data["id"]

                game_thread = Game(game_id, users, game_set, self.users_lock)
                game_thread.start()

                self.games.append(game_thread)

            self.waiting_game_groups = remaing_groups

    def disconnect_users(self):
        while True:

            with self.users_lock:
                for id, user_thread in list(self.users.items()):
                    if user_thread.is_connected:
                        continue

                    if user_thread.name is not None:
                        requests.patch(
                            f"{get_api_url()}/users",
                            params={"name": user_thread.name, "online": False},
                            headers={"token": TOKEN_AUTENTICACION},
                        )

                    for group in self.waiting_game_groups:
                        if user_thread in group["users"]:
                            group["users"].remove(user_thread)

                    del self.users[id]

                    log(f"(User {id}): Disconnected")
