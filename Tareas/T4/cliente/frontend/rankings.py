from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QComboBox,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
from threading import Thread
import requests

from cliente.utils.config import get_api_url, get_font
from cliente.utils.pretty import pretty
from utils.game_sets import get_game_sets
from utils.find import find
from parametros import RANKINGS, RANKINGS_WITH_GAME_SET, CUSTOM


class RankingsTable(QTableWidget):
    update_data = pyqtSignal(list)

    def __init__(self) -> None:
        super().__init__()
        self.setFont(QFont(get_font(), 12))
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.update_data.connect(self.update)
        self.setFixedHeight(400)

    def update(self, data: list) -> None:
        headers = [key for key in data[0].keys()]
        pretty_headers = [pretty(header) for header in headers]

        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(pretty_headers)
        self.setRowCount(len(data))

        for row, value in enumerate(data):
            for column, header in enumerate(headers):
                cell_value = value[header]

                text = (
                    f"{cell_value:.2f}"
                    if isinstance(cell_value, float)
                    else str(cell_value)
                )

                self.setItem(row, column, QTableWidgetItem(text))

        self.resizeColumnsToContents()
        self.resizeRowsToContents()


class Rankings(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.game_sets = [game_set["name"] for game_set in get_game_sets()] + [CUSTOM]

        self.label = QLabel("Rankings")
        self.label.setFont(QFont(get_font(), 18))
        self.label.setAlignment(Qt.AlignCenter)

        self.drop_down_query = QComboBox()

        self.rankings = [(ranking, pretty(ranking)) for ranking in RANKINGS]

        self.drop_down_query.addItems([pretty(ranking) for ranking in RANKINGS])
        self.drop_down_query.currentTextChanged.connect(self.query_selection)

        self.drop_down_game_set = QComboBox()
        self.drop_down_game_set.addItems(self.game_sets)
        self.drop_down_game_set.currentTextChanged.connect(self.query_selection)

        self.loading_label = QLabel()
        self.loading_label.setFont(QFont(get_font(), 12))

        self.table = RankingsTable()

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.drop_down_query)
        self.layout.addWidget(self.drop_down_game_set)
        self.layout.addWidget(self.loading_label)
        self.layout.addWidget(self.table)
        self.layout.addStretch()

        self.setLayout(self.layout)

        self.query_selection()

    def get_current_ranking(self) -> str:
        text = self.drop_down_query.currentText()

        ranking = find(
            lambda ranking: pretty(ranking[0]) == text,
            self.rankings,
        )

        return ranking[0]

    def query_selection(self):
        enabled = self.get_current_ranking() in RANKINGS_WITH_GAME_SET
        self.drop_down_game_set.setEnabled(enabled)

        self.loading_label.setText("Cargando rankings...")
        self.update_data_thread = Thread(target=self.update_data, daemon=True)
        self.update_data_thread.start()

    def update_data(self) -> None:
        ranking = self.get_current_ranking()

        data = {
            "nombre": ranking,
            "cantidad": 25,
        }

        if ranking in RANKINGS_WITH_GAME_SET:
            data["conjunto"] = self.drop_down_game_set.currentText()

        response = requests.get(f"{get_api_url()}/rankings", params=data)

        data = response.json()

        self.table.update_data.emit(data)
        self.loading_label.setText("")
