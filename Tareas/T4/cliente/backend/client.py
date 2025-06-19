import socket
from PyQt5.QtCore import QThread, pyqtSignal
from utils.log import log
from utils.bytes import receive_bytes, receive_message, create_chunks
from utils.crypto import xor_cipher


class Client(QThread):
    select_name_answer = pyqtSignal(bool, str)

    def __init__(self, port: int, host: str) -> None:
        super().__init__()

        self.port = port
        self.host = host
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None

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

            if message["type"] == "used-name":
                self.select_name_answer.emit(False, self.name)
            elif message["type"] == "selected-name":
                self.name = message["name"]
                self.select_name_answer.emit(True, self.name)

    def send_message(self, message: dict) -> None:
        log("Sending message to server")

        size, chunks = create_chunks(message)

        self.socket.sendall(size)

        log(f"Sending {len(chunks)} chunks to server")

        for i, chunk in chunks:
            self.socket.sendall(chunk)
            log(f"Sending chunk {i} to server")
