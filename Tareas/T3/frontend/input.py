from os.path import isdir, exists, join
from os import listdir, getcwd

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QCompleter,
    QMessageBox,
)

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from utils.folders import search_folders
from utils.path import normalize_path
from utils.format import format_field

from constants import DATA_FOLDER, DATA_FILES
from frontend.handlers import QUERIES_HANDLES


class QueryInput(QWidget):
    submit_query_signal = pyqtSignal(str, str)

    def __init__(self) -> None:
        super().__init__()

        self.title_label = QLabel("Entrada de consultas")
        self.title_label.setFont(QFont("Arial", 16))

        self.path_label = QLabel("Ruta a carpeta de datos")

        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Ejemplo: M")

        self.query = QComboBox()

        self.query_fields = {
            format_field(query): query for query in QUERIES_HANDLES.keys()
        }

        self.query.addItems(self.query_fields.keys())

        self.completer_folders = QCompleter(search_folders(DATA_FOLDER))
        self.completer_folders.setCaseSensitivity(Qt.CaseInsensitive)
        self.path_input.setCompleter(self.completer_folders)

        self.button = QPushButton("Realizar consulta")
        self.button.clicked.connect(self.submit_query)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.path_label)
        self.layout.addWidget(self.path_input)
        self.layout.addWidget(self.query)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def submit_query(self) -> None:
        normalized_path = normalize_path(self.path_input.text())

        if not normalized_path:
            QMessageBox.critical(
                self,
                "Error",
                "Debe ingresar una ruta válida.",
            )
            return

        entire_path = join(getcwd(), DATA_FOLDER, normalized_path)

        if not exists(entire_path) or not isdir(entire_path):
            QMessageBox.critical(
                self,
                "Error",
                "La ruta ingresada no existe o no es una carpeta.",
            )
            return

        items = listdir(entire_path)

        for file in DATA_FILES:
            if file in items:
                continue

            if isdir(join(entire_path, file)):
                continue

            QMessageBox.critical(
                self,
                "Error",
                "La carpeta no contiene todos los archivos necesarios.",
            )
            return

        query = self.query_fields[self.query.currentText()]

        self.submit_query_signal.emit(entire_path, query)
