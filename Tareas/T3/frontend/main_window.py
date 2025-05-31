from os.path import isdir, exists, join
from os import listdir, getcwd

from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
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
from constants import DATA_FOLDER, DATA_FILES


from frontend.input import QueryInput
from frontend.handlers import make_query


class MainWindow(QWidget):
    def __init__(
        self, title: str = "Programa de Consultas", x: int = 0, y: int = 0
    ) -> None:
        super().__init__()

        self.setWindowTitle(title)
        self.setGeometry(x, y, 1024, 600)
        self.setMinimumSize(800, 400)

        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 24))
        self.title_label.setFixedHeight(50)

        self.results_label = QLabel("Resultados de la consulta")
        self.results_label.setFont(QFont("Arial", 16))
        self.results_label.setAlignment(Qt.AlignCenter)

        self.next_button = QPushButton("Siguiente")
        self.next_button.clicked.connect(self.paginate)
        self.next_button.setFixedWidth(100)
        self.next_button.setEnabled(False)

        self.input_section = QueryInput()
        self.input_section.submit_query_signal.connect(self.handle_query)

        self.result_table = None

        self.right_layout = QVBoxLayout()

        self.results_top_layout = QHBoxLayout()
        self.results_top_layout.addWidget(self.results_label)
        self.results_top_layout.addWidget(self.next_button, alignment=Qt.AlignRight)

        self.right_layout.addLayout(self.results_top_layout)
        self.right_layout.addStretch(1)

        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(20)

        self.content_layout = QHBoxLayout()
        self.content_layout.addWidget(self.input_section, stretch=1)
        self.content_layout.addLayout(self.right_layout, stretch=3)

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addLayout(self.content_layout)

        self.setLayout(self.main_layout)

    def handle_query(self, path: str, query: str) -> None:
        self.result_generator = make_query(path, query)
        self.next_button.setEnabled(True)

        self.paginate()

    def paginate(self):
        if not self.result_generator:
            return

        try:
            if self.result_table:
                self.right_layout.removeWidget(self.result_table)
                self.right_layout.addStretch(1)
                self.result_table = None

            self.result_table = next(self.result_generator)

            self.right_layout.removeItem(self.right_layout.itemAt(1))
            self.right_layout.addWidget(self.result_table)

        except RuntimeError as error:
            if "StopIteration" not in str(error):
                raise error

            self.next_button.setEnabled(False)
            self.result_generator = None
            self.result_table = None

            QMessageBox.information(
                self, "Consulta finalizada", "No hay más resultados."
            )
