from typing import Self
from socket import socket
from queue import Queue
from threading import Thread
import requests
import time

from servidor.utils.config import get_api_url
from servidor.parametros import TOKEN_AUTENTICACION
from utils.bytes import receive_bytes, receive_message, create_chunks
from utils.crypto import xor_cipher
from utils.log import log
from parametros import MINIMO_PALABRAS_CONJUNTO, CUSTOM


class UserThread(Thread):
    def __init__(
        self,
        id: int,
        socket: socket,
        game_sets: list[str],
        searching_game_queue: Queue[Self, str],
    ) -> None:
        super().__init__(daemon=True)

        self.id = id
        self.name = None
        self.socket = socket
        self.is_connected = True
        self.is_searching_game = False
        self.game_sets = game_sets
        self.game_actions_queue = None
        self.custom_words = []

        self.daemon = True

        self.searching_game_queue = searching_game_queue

        self.pending_messages = Queue()

        self.pending_messages_thread = Thread(target=self.send_messages, daemon=True)

        self.check_connection_thread = Thread(target=self.check_connection, daemon=True)

    def check_connection(self):
        while self.is_connected:
            time.sleep(5)
            self.pending_messages.put({"type": "check-connection"})

    def send_messages(self):
        while self.is_connected:
            message = self.pending_messages.get()

            try:
                size, chunks = create_chunks(message)

                self.socket.sendall(size)

                for i, chunk in chunks:
                    self.socket.sendall(chunk)

                self.pending_messages.task_done()

            except BrokenPipeError:
                self.pending_messages.task_done()
                self.disconnect()
                log(f"(User {self.id}): Send message failed due to broken pipe.")
                break

    def run(self) -> None:
        self.pending_messages_thread.start()
        self.check_connection_thread.start()

        log(f"(User {self.id}): Start running")

        while self.is_connected:
            try:
                received = receive_bytes(self.socket, 4, 4)

                if not received:
                    break

                size = int.from_bytes(xor_cipher(received), "little")

                print(f"(User {self.id}): Received size {size}")

                if size == 0:
                    break
            except OSError as error:
                log(f"(User {self.id}): OSError {error}")
                self.disconnect()
                break

            message = receive_message(self.socket, size)

            self.process_message(message)

        self.disconnect()

    def process_message(self, message: dict) -> None:
        try:
            if message["action"] == "select-name":
                if not message["name"].strip():
                    self.pending_messages.put(
                        {
                            "ok": False,
                            "type": "error",
                            "message": "Name is required",
                        }
                    )
                    return

                self.select_name(message["name"].strip())

            elif message["action"] == "search-game":
                game_set = message["game_set"].strip()

                # Get words for personalized game set
                words = message["words"] if game_set == CUSTOM else None

                if words is not None and len(words) < MINIMO_PALABRAS_CONJUNTO:
                    self.pending_messages.put(
                        {
                            "ok": False,
                            "type": "error",
                            "message": f"Game set must have >= {MINIMO_PALABRAS_CONJUNTO} words",
                        }
                    )
                    return

                self.search_game(message["game_set"].strip(), words)
            elif message["action"] == "game":
                if self.game_actions_queue is None:
                    self.pending_messages.put(
                        {
                            "ok": False,
                            "type": "error",
                            "message": "User is not in a game",
                        }
                    )
                    return

                self.game_actions_queue.put(
                    {
                        **message,
                        "user-id": self.id,
                    }
                )
        except KeyError as error:
            log(f"(User {self.id}): KeyError {error}")

            self.pending_messages.put(
                {
                    "ok": False,
                    "type": "error",
                    "message": "Invalid message data",
                }
            )

    def select_name(self, name: str) -> None:
        response = requests.get(
            f"{get_api_url()}/users",
            params={"name": name, "online": True},
            headers={"token": TOKEN_AUTENTICACION},
        )

        if response.status_code == 404:
            requests.post(
                f"{get_api_url()}/users",
                params={"name": name},
                headers={"token": TOKEN_AUTENTICACION},
            )

        if response.status_code == 200:
            data = response.json()

            if data["online"]:
                self.pending_messages.put(
                    {
                        "ok": False,
                        "type": "used-name",
                        "message": f"User {name} is already connected",
                        "name": name,
                    }
                )
                return

            requests.patch(
                f"{get_api_url()}/users",
                params={"name": name, "online": True},
                headers={"token": TOKEN_AUTENTICACION},
            )

        self.name = name
        self.pending_messages.put(
            {
                "ok": True,
                "type": "selected-name",
                "message": "Successfully connected",
                "name": name,
            }
        )

    def search_game(self, game_set: str, words: list[str] | None) -> None:
        if self.is_searching_game:
            self.pending_messages.put(
                {
                    "ok": False,
                    "type": "error",
                    "message": "Already searching for a game",
                }
            )
            return

        if game_set not in self.game_sets:
            self.pending_messages.put(
                {
                    "ok": False,
                    "type": "error",
                    "message": f"Invalid game set: {game_set}",
                }
            )

        self.searching_game_queue.put((self, game_set))

        self.is_searching_game = True
        self.custom_words = words if game_set == CUSTOM else []

        self.pending_messages.put(
            {
                "ok": True,
                "type": "searching-game",
                "message": f"Searching game with game set: {game_set}",
            }
        )

    def disconnect(self) -> None:
        if not self.is_connected:
            return

        self.is_connected = False
        self.socket.close()

        log(f"(User {self.id}): Socket closed")
