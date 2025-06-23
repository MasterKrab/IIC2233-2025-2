from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QMessageBox,
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont


class WelcomeWindow(QWidget):
    submit_name = pyqtSignal(str)
    open_main_window = pyqtSignal()

    def __init__(
        self, title: str = "DCCaída de palabras", x: int = 0, y: int = 0
    ) -> None:
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(x, y, 600, 300)

        self.layout = QVBoxLayout()

        self.label = QLabel(title)
        self.label.setFont(QFont("Arial", 20))
        self.label.setAlignment(Qt.AlignCenter)

        self.name_label = QLabel("Ingresa el nombre de usuario")
        self.name_label.setFont(QFont("Arial", 12))
        self.name_label.setFixedWidth(410)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ejemplo: Masterkrab")
        self.name_input.setFixedWidth(325)

        self.button = QPushButton("Ingresar")
        self.button.clicked.connect(self.submit)
        self.button.setFixedWidth(75)

        self.layout_form_bottom = QHBoxLayout()

        self.layout_form_bottom.addStretch(1)
        self.layout_form_bottom.addWidget(self.name_input)
        self.layout_form_bottom.addWidget(self.button)
        self.layout_form_bottom.addStretch(1)

        self.layout.addStretch(1)
        self.layout.addWidget(self.label)
        self.layout.addStretch(1)
        self.layout.addWidget(self.name_label, alignment=Qt.AlignCenter)
        self.layout.addLayout(self.layout_form_bottom)
        self.layout.addStretch(1)

        self.setLayout(self.layout)

    def submit(self) -> None:
        name = self.name_input.text().strip()

        if not name:
            return

        if "," in name or "\n" in name:
            QMessageBox.critical(
                self,
                "Error",
                "El nombre no puede tener comas ni saltos de línea.",
            )
            return

        self.button.setEnabled(False)
        self.submit_name.emit(name)

    def handle_name_answer(self, ok: bool, name: str):

        if ok:
            QMessageBox.information(
                self,
                "Nombre seleccionado",
                f"El nombre {name} fue exitosamente seleccionado, bienvenido.",
            )

            self.close()
            self.open_main_window.emit()

        else:
            QMessageBox.critical(
                self,
                "Error",
                "El nombre ya esta usado, elije otro.",
            )
            self.button.setEnabled(True)
