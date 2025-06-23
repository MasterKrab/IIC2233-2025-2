from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QFileDialog,
    QMessageBox,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from time import time
from pathlib import Path

from parametros import MINIMO_PALABRAS_CONJUNTO
from cliente.frontend.rankings import Rankings
from cliente.frontend.game_sets_table import GameSetsTable
from cliente.frontend.timer import Timer
from cliente.utils.salute import salute
from cliente.utils.config import get_font
from utils.game_sets import get_game_sets
from utils.find import find


class MainWindow(QWidget):
    search_game = pyqtSignal(str, list)

    def __init__(
        self, title: str = "DCCaída de palabras", x: int = 0, y: int = 0
    ) -> None:
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(x, y, 950, 600)

        self.is_searching_game = False

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.rankings = Rankings()

        self.name_label = QLabel("")
        self.name_label.setFont(QFont(get_font(), 18))

        self.button_game_set = QPushButton("Importar conjunto")
        self.button_game_set.clicked.connect(self.import_game_set)

        self.game_sets_label = QLabel("Conjuntos de palabras")
        self.game_sets_label.setFont(QFont(get_font(), 14))

        self.game_sets = [{"custom": False, **game_set} for game_set in get_game_sets()]

        self.game_sets_table = GameSetsTable(self.game_sets)
        self.game_sets_table.setMaximumHeight(300)

        self.drop_down_game_set = QComboBox()
        self.drop_down_game_set.addItems(
            [game_set["name"] for game_set in self.game_sets]
        )

        self.button_search_game = QPushButton("Buscar partida")
        self.button_search_game.clicked.connect(self.handle_search_game)

        self.search_game_label = QLabel(
            "Elije un conjunto de palabras para buscar una partida"
        )
        self.search_game_label.setFont(QFont(get_font(), 12))

        self.timer = Timer(
            self.search_game_label, text="Buscando partida, tiempo buscando: {}"
        )

        self.layout.addWidget(self.rankings, 0, 3, 6, 2)

        self.layout.addWidget(self.name_label, 0, 0, 1, 3, Qt.AlignCenter)

        self.layout.addWidget(self.game_sets_label, 1, 0, 1, 2)
        self.layout.addWidget(self.button_game_set, 1, 2, 1, 1)

        self.layout.addWidget(self.game_sets_table, 2, 0, 1, 3)

        self.layout.addWidget(self.drop_down_game_set, 3, 0, 1, 2, Qt.AlignBottom)

        self.layout.addWidget(self.button_search_game, 3, 2, 1, 1, Qt.AlignBottom)

        self.layout.addWidget(self.search_game_label, 4, 0, 2, 3, Qt.AlignTop)

    def show_window(self, name: str) -> None:
        self.name_label.setText(salute(name))
        self.show()

    def handle_search_game(self):
        game_set = self.drop_down_game_set.currentText()

        game_set_data = find(lambda set: set["name"] == game_set, self.game_sets)

        is_custom = game_set_data["custom"]

        name = "personalizado" if is_custom else game_set
        words = game_set_data["words"] if is_custom else []

        self.search_game.emit(name, words)

        self.button_search_game.setEnabled(False)
        self.drop_down_game_set.setEnabled(False)
        self.timer.start(time())

    def import_game_set(self):
        dialog = QFileDialog(self)
        dialog.setNameFilter("*.txt")

        if not dialog.exec_():
            QMessageBox.critical(
                self,
                "Error",
                "No se pudo abrir la ventana de importar conjunto",
            )
            return

        path = dialog.selectedFiles()[0]

        with Path(path).open("r", encoding="utf-8") as file:
            lines = list(map(str.strip, file.readlines()))

        if len(lines) - 1 < MINIMO_PALABRAS_CONJUNTO:
            QMessageBox.critical(
                self,
                "Error",
                f"El conjunto debe tener al menos {MINIMO_PALABRAS_CONJUNTO} palabras",
            )
            return

        name = Path(path).stem
        description = lines[0]
        words = list(lines)[1:]

        self.game_sets.append(
            {
                "name": name,
                "description": description,
                "words_amount": len(words),
                "words": words,
                "custom": True,
            }
        )

        self.game_sets_table.update_data(self.game_sets)

        self.drop_down_game_set.addItem(name)

        QMessageBox.information(
            self,
            "Conjunto importado",
            f"Conjunto {name} importado correctamente",
        )

    def close(self) -> None:
        self.is_searching_game = False
        self.button_search_game.setEnabled(True)
        self.drop_down_game_set.setEnabled(True)

        self.timer.stop()
        self.search_game_label.setText(
            "Elije un conjunto de palabras para buscar una partida"
        )
        super().close()
