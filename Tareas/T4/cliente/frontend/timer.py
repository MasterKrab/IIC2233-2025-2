from time import time

from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import QTimer

from utils.duration import seconds_to_duration


class Timer(QWidget):
    """
    Code extracted doing modifications from "PyQt5 - Create a digital clock"; that is, a class by
    GeeksForGeeks, retrieved on June 19, 2025, from
    https://www.geeksforgeeks.org/python/pyqt5-create-a-digital-clock/
    """

    def __init__(self, label: QLabel, text: str = "{}") -> None:
        super().__init__()

        self.label = label

        self.timer = QTimer(self)
        self.text = text
        self.start_time = time()

        self.timer.timeout.connect(self.showTime)

    def start(self, interval: int = 1000) -> None:

        self.start_time = time()
        self.timer.start(interval)

    def showTime(self):
        current_time = time() - self.start_time
        text = self.text.format(seconds_to_duration(int(current_time)))

        self.label.setText(text)
