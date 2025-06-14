import socket
from servidor.utils.id import create_id_generator
from servidor.user import UserThread
from utils.log import log


class Server:
    def __init__(self, port: int, host: str) -> None:
        self.host = host
        self.port = port
        self.users = {}
        self.generate_id = create_id_generator()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.names = set()

    def run(self) -> None:
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        log(f"Server listening in {self.host}:{self.port}")

        while True:
            socket, address = self.socket.accept()
            user_id = self.generate_id()

            thread = UserThread(user_id, socket, self.names)
            self.users[user_id] = thread

            log(f"[id: {user_id}] Connection: {socket} {address}")

            thread.start()
