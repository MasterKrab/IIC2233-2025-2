from socket import socket
from queue import Queue
import threading
from PyQt5.QtCore import pyqtSignal
from utils.bytes import receive_bytes, receive_message, create_chunks
from utils.crypto import xor_cipher
from utils.log import log


class UserThread(threading.Thread):
    def __init__(self, id: int, socket: socket, names: set) -> None:
        super().__init__()

        self.id = id
        self.names = names
        self.name = None
        self.socket = socket

        self.daemon = True

        self.pending_messages = Queue()

        self.pending_messages_thread = threading.Thread(
            target=self.send_messages, daemon=True
        )

    def send_messages(self):
        while True:
            message = self.pending_messages.get()

            log(f"Sending message to user {self.id}")

            try:
                size, chunks = create_chunks(message)

                self.socket.sendall(size)

                for i, chunk in chunks:
                    self.socket.sendall(chunk)
                    log(f"Sending chunk {i} to user {self.id}")

                self.pending_messages.task_done()

            except BrokenPipeError:
                self.pending_messages.task_done()
                log(f"Send message failed for user {self.id} due to broken pipe.")
                break

    def run(self) -> None:

        self.pending_messages_thread.start()

        log(f"(User {self.id}): Start running")

        while True:
            size = int.from_bytes(
                xor_cipher(receive_bytes(self.socket, 4, 4)), "little"
            )

            if size == 0:
                log(f"(User {self.id}): disconnected")
                break

            try:
                message = receive_message(self.socket, size)

                self.process_message(message)

            except Exception as error:
                log(f"(User {self.id}): Disconnected because of error {error}")
                break

        self.names.remove(self.name)

    def process_message(self, message: dict) -> None:
        if message["action"] == "select-name":
            self.select_name(message["name"].strip())

    def select_name(self, name: str) -> None:
        if name in self.names:

            self.pending_messages.put(
                {
                    "ok": False,
                    "type": "duplicated-name",
                    "message": f"Name {name} is already used",
                    "name": name,
                }
            )
        else:
            self.names.add(name)
            self.name = name

            self.pending_messages.put(
                {
                    "ok": True,
                    "type": "selected-name",
                    "message": "Name succesfully slected",
                    "name": name,
                }
            )
