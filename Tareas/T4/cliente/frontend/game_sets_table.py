from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QFont

from cliente.utils.config import get_font


class GameSetsTable(QTableWidget):
    def __init__(self, game_sets: list[dict]) -> None:
        super().__init__()

        self.setFont(QFont(get_font(), 12))
        self.setEditTriggers(QTableWidget.NoEditTriggers)

        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(
            ["Nombre", "Cantidad de palabras", "Descripción", "Personalizado"]
        )

        self.update_data(game_sets)

    def update_data(self, game_sets: list[dict]) -> None:
        self.setRowCount(len(game_sets))

        for row, game_set in enumerate(game_sets):
            self.setItem(row, 0, QTableWidgetItem(game_set["name"]))
            self.setItem(row, 1, QTableWidgetItem(str(game_set["words_amount"])))
            self.setItem(row, 2, QTableWidgetItem(game_set["description"]))
            self.setItem(row, 3, QTableWidgetItem("Sí" if game_set["custom"] else "No"))

        self.resizeColumnsToContents()
        self.resizeRowsToContents()
