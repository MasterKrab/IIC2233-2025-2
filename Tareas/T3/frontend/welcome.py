from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont


class WelcomeWindow(QWidget):
    open_main_window_signal = pyqtSignal()

    def __init__(self, title: str = "¡Bienvenido!", x: int = 0, y: int = 0) -> None:
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(x, y, 400, 250)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(35)

        self.label = QLabel("¡Bienvenido a la aplicación!")
        self.label.setFont(QFont("Arial", 20))
        self.label.setAlignment(Qt.AlignCenter)

        self.button = QPushButton("Ingresar a la ventana principal")
        self.button.setFixedWidth(200)
        self.button.clicked.connect(self.open_main_window)

        self.layout.addStretch(1)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button, alignment=Qt.AlignCenter)
        self.layout.addStretch(1)

        self.setLayout(self.layout)
        self.show()

    def open_main_window(self) -> None:
        self.hide()
        self.open_main_window_signal.emit()
