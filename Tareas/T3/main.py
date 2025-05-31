from frontend.welcome import WelcomeWindow
from frontend.main_window import MainWindow

from PyQt5.QtWidgets import QApplication

import sys


def main():
    def hook(type, value, traceback) -> None:
        print(type)
        print(traceback)

    sys.__excepthook__ = hook

    app = QApplication([])
    welcome_window = WelcomeWindow(x=100, y=100)
    main_window = MainWindow()

    welcome_window.open_main_window_signal.connect(main_window.show)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
