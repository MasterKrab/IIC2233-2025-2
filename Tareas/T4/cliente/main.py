import sys
from cliente.backend.client import Client
from cliente.frontend.welcome import WelcomeWindow
from cliente.frontend.main_window import MainWindow
from cliente.frontend.game import GameWindow
from cliente.utils.config import get_socket_config
from PyQt5.QtWidgets import QApplication, QMessageBox

GameWindow


class MainHandler:
    def __init__(self, host: str, port: int):
        self.client = Client(port, host)

        self.welcome_window = WelcomeWindow(x=100, y=100)
        self.welcome_window.submit_name.connect(self.select_name)

        self.welcome_window.open_main_window.connect(
            lambda: self.main_window.show_window(self.client.name)
        )

        self.client.select_name_answer.connect(self.welcome_window.handle_name_answer)

        self.main_window = MainWindow()
        self.main_window.search_game.connect(self.client.search_game)
        self.client.connect_to_game.connect(self.start_game)

    def run(self):
        while True:
            is_connected = self.client.connect()["ok"]

            if not is_connected:
                QMessageBox.critical(
                    self.welcome_window,
                    "Error",
                    "No se pudo conectar al servidor",
                )

                answer = QMessageBox.question(
                    self.welcome_window,
                    "",
                    "¿Quieres volver a intentar a conectar?",
                    QMessageBox.Yes | QMessageBox.No,
                )

                if answer == QMessageBox.No:
                    exit()

                continue

            break

        self.client.start()
        self.welcome_window.show()

    def select_name(self, name: str):
        self.client.send_message({"action": "select-name", "name": name})

    def start_game(self):
        self.main_window.close()

        self.game_window = GameWindow()
        self.game_window.show()
        self.client.receive_game_message.connect(self.game_window.receive_game_message)
        self.game_window.send_typed_word.connect(self.client.send_typed_word)
        self.game_window.end_game.connect(self.end_game)

    def end_game(self):
        self.game_window.close()
        self.main_window.show()


def main():
    def hook(type, value, traceback) -> None:
        print(type)
        print(traceback)

    sys.__excepthook__ = hook

    app = QApplication([])

    port, host = get_socket_config()

    main_handler = MainHandler(host, port)

    main_handler.run()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
