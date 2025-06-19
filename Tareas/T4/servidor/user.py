from socket import socket
from queue import Queue
import threading
import requests
import time

from utils.bytes import receive_bytes, receive_message, create_chunks
from utils.crypto import xor_cipher
from utils.log import log
from servidor.utils.config import get_api_url


class UserThread(threading.Thread):
    def __init__(self, id: int, socket: socket) -> None:
        super().__init__()

        self.id = id
        self.name = None
        self.socket = socket
        self.is_connected = True

        self.daemon = True

        self.pending_messages = Queue()

        self.pending_messages_thread = threading.Thread(
            target=self.send_messages, daemon=True
        )

        self.check_connection_thread = threading.Thread(
            target=self.check_connection, daemon=True
        )

    def check_connection(self):
        while self.is_connected:
            time.sleep(5)

            try:
                size, chunks = create_chunks({"type": "check-connection"})

                self.socket.sendall(size)

                for i, chunk in chunks:
                    self.socket.sendall(chunk)

            except BrokenPipeError:
                log(f"(User {self.id}) broken pipe error.")
                self.disconnect()
                break
            except Exception as error:
                log(f"Error user {self.id}: {error}")
                self.disconnect()
                break

    def send_messages(self):
        while self.is_connected:
            message = self.pending_messages.get()

            log(f"(User {self.id}): Sending message")

            try:
                size, chunks = create_chunks(message)

                self.socket.sendall(size)

                for i, chunk in chunks:
                    self.socket.sendall(chunk)
                    log(f"Sending chunk {i} to user {self.id}")

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

            try:
                message = receive_message(self.socket, size)

                self.process_message(message)

            except Exception as error:
                log(f"(User {self.id}): Sending message error {error}")
                break

        self.disconnect()

    def process_message(self, message: dict) -> None:
        print(message)
        if message["action"] == "select-name":
            self.select_name(message["name"].strip())

    def select_name(self, name: str) -> None:
        response = requests.get(
            f"{get_api_url()}/users",
            params={"name": name, "online": True},
        )

        if response.status_code == 404:
            requests.post(
                f"{get_api_url()}/users",
                params={"name": name},
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

    def disconnect(self) -> None:
        if not self.is_connected:
            return

        log(f"(User {self.id}): Disconnecting")

        self.is_connected = False

        self.socket.close()

        if self.name is not None:
            requests.patch(
                f"{get_api_url()}/users", params={"name": self.name, "online": False}
            )
