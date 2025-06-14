from PyQt5.QtWidgets import QWidget, QLabel


class MainWindow(QWidget):
    def __init__(
        self, title: str = "DCCaída de palabras", x: int = 0, y: int = 0
    ) -> None:
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(x, y, 600, 300)

        self.label = QLabel(title, self)
