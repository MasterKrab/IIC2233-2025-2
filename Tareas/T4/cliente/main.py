import sys
import json
from pathlib import Path
from cliente.backend.client import Client
from cliente.frontend.welcome import WelcomeWindow
from cliente.frontend.main_window import MainWindow
from cliente.utils.config import get_socket_config
from PyQt5.QtWidgets import QApplication, QMessageBox


class MainHandler:
    def __init__(self, host: str, port: int):
        self.client = Client(port, host)

        self.welcome_window = WelcomeWindow(x=100, y=100)
        self.welcome_window.submit_name.connect(self.select_name)

        self.main_window = MainWindow()
        self.welcome_window.open_main_window.connect(self.main_window.show)

        self.client.select_name_answer.connect(self.welcome_window.handle_name_answer)

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
