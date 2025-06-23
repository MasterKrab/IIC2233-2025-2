from PyQt5.QtCore import QThread, pyqtSignal
import socket

from utils.log import log
from utils.bytes import receive_bytes, receive_message, create_chunks
from utils.crypto import xor_cipher
from parametros import CUSTOM


class Client(QThread):
    select_name_answer = pyqtSignal(bool, str)
    connect_to_game = pyqtSignal()
    receive_game_message = pyqtSignal(dict)

    def __init__(self, port: int, host: str) -> None:
        super().__init__()

        self.port = port
        self.host = host
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.searching_time_start = None

    def connect(self) -> dict:
        try:
            self.socket.connect((self.host, self.port))

            log("Connected succesfully")

            return {"ok": True, "message": "Succesfully connected"}

        except ConnectionError:
            log("Could not connect to the server")

            return {"ok": False, "message": "Connection error"}

    def run(self) -> None:
        while True:
            size = int.from_bytes(
                xor_cipher(receive_bytes(self.socket, 4, 4)), "little"
            )

            if size == 0:
                log("Closing connection")
                break

            message = receive_message(self.socket, size)

            log(f"Received message: {message}")

            type = message["type"]

            if type == "used-name":
                self.select_name_answer.emit(False, self.name)
            elif type == "selected-name":
                self.name = message["name"]
                self.select_name_answer.emit(True, self.name)
            elif type == "game-found":
                self.connect_to_game.emit()
            elif type == "game-state":
                self.receive_game_message.emit(message)

    def send_message(self, message: dict) -> None:
        log("Sending message to server")

        size, chunks = create_chunks(message)

        self.socket.sendall(size)

        log(f"Sending {len(chunks)} chunks to server")

        for i, chunk in chunks:
            self.socket.sendall(chunk)
            log(f"Sending chunk {i} to server")

    def search_game(self, game_set: str, words: list[str]) -> None:
        data = {"action": "search-game", "game_set": game_set}

        if game_set == CUSTOM:
            data["words"] = words

        self.send_message(data)

    def send_typed_word(self, word: str) -> None:
        self.send_message(
            {
                "action": "game",
                "game-action": "word-typed",
                "word": word,
            }
        )
