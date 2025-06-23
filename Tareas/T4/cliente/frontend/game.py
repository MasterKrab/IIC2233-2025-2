from pathlib import Path
from time import time
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QGridLayout,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap

from cliente.utils.config import get_font
from cliente.parametros import SPRITES_PATH
from parametros import VIDAS_INICIALES


class Word(QWidget):
    def __init__(
        self,
        parent: QWidget,
        text: str,
        start_time: int,
        fall_time: int,
        window_height: int,
        x: int,
        y: int,
    ) -> None:
        super().__init__(parent)

        self.setStyleSheet("border: none")

        self.label = QLabel(text, self)
        self.label.setFont(QFont(get_font(), 20))
        self.label.setGeometry(0, 0, self.width(), self.height())
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: white")

        self.padding = 25

        self.pixmap = QPixmap(str(Path(SPRITES_PATH, "bloque-normal.png"))).scaled(
            self.label.width() + 2 * self.padding,
            self.label.height() + 2 * self.padding,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )

        self.label_pixmap = QLabel(self)
        self.label_pixmap.setGeometry(0, 0, self.pixmap.width(), self.pixmap.height())
        self.label_pixmap.setPixmap(self.pixmap)

        self.label = QLabel(text, self)
        self.label.setGeometry(0, 0, self.pixmap.width(), self.pixmap.height())
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont(get_font(), 16))
        self.label.setStyleSheet("color: white")

        self.text = text
        self.start_time = start_time
        self.fall_time = fall_time
        self.position_x = min(parent.width() - self.pixmap.width(), x)
        self.position_y = y
        self.start_y = y
        self.window_height = window_height

        self.update()

    def update(self) -> None:

        difference = time() - self.start_time

        factor = (difference * 1e3) / self.fall_time

        if factor > 1:
            self.close()
            return

        delta_y = int(factor * self.window_height)

        self.position_y = self.start_y + delta_y

        self.move(self.position_x, self.position_y)


class PlayersTable(QTableWidget):
    def __init__(
        self,
    ) -> None:
        super().__init__()

        self.setFont(QFont(get_font(), 12))
        self.setEditTriggers(QTableWidget.NoEditTriggers)

        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Nombre", "Puntaje", "Vidas", "Racha"])

    def update_data(self, players: list[dict], name: str) -> None:
        players.sort(
            key=lambda x: (x["score"], x["lives"], x["streak"]),
            reverse=True,
        )

        self.setRowCount(len(players))

        for row, participant in enumerate(players):
            name_item = QTableWidgetItem(participant["name"])

            if participant["name"] == name:
                name_item.setFont(QFont(get_font(), 12, QFont.Bold))

            self.setItem(row, 0, name_item)
            self.setItem(row, 1, QTableWidgetItem(f"{participant['score']:.2f}"))
            self.setItem(row, 2, QTableWidgetItem(str(participant["lives"])))
            self.setItem(row, 3, QTableWidgetItem(str(participant["streak"])))

        self.resizeColumnsToContents()
        self.resizeRowsToContents()


class GameWindow(QWidget):
    send_typed_word = pyqtSignal(str)
    end_game = pyqtSignal()

    def __init__(
        self, title: str = "DCCaída de palabras", x: int = 0, y: int = 0
    ) -> None:
        super().__init__()
        self.setWindowTitle(title)

        self.setGeometry(self.screen().geometry())
        self.showFullScreen()

        self.lives = VIDAS_INICIALES
        self.score = 0
        self.streak = 0
        self.name = ""
        self.is_running = True
        self.horizontal_offset = 0
        self.words_labels = []

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_game)
        self.update_timer.start(30)

        self.current_word = QLineEdit()
        self.current_word.setAlignment(Qt.AlignCenter)
        self.current_word.setStyleSheet("border: none; background: transparent")

        self.current_word.setFont(QFont(get_font(), 16))
        self.current_word.setPlaceholderText("Escribe aquí")
        self.current_word.returnPressed.connect(self.type_current_word)
        self.current_word.setFont(QFont(get_font(), 20))

        self.current_word.show()

        self.stats_label = QLabel()
        self.stats_label.setFont(QFont(get_font(), 14))
        self.update_stats()

        self.players_table = PlayersTable()

        self.words_panel = QWidget()
        self.words_panel.setStyleSheet(
            "border-top: 2px solid; border-bottom: 2px solid;"
        )

        self.layout = QGridLayout()

        self.layout.addWidget(self.stats_label, 0, 0, 1, 1)
        self.layout.addWidget(self.players_table, 1, 0, 1, 1)
        self.layout.addWidget(self.current_word, 0, 1, 1, 3)
        self.layout.addWidget(self.words_panel, 1, 1, 2, 2)

        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 6)

        self.layout.setColumnStretch(0, 2)
        self.layout.setColumnStretch(1, 5)

        self.setLayout(self.layout)

    def update_stats(self) -> None:
        lines = [
            f"Jugador: {self.name}",
            f"Vidas: {self.lives}",
            f"Puntaje: {self.score:.2f}",
            f"Racha: {self.streak}",
        ]

        self.stats_label.setText("\n".join(lines))

    def type_current_word(self) -> None:
        text = self.current_word.text().strip()

        if not text:
            return

        self.send_typed_word.emit(text)
        self.current_word.clear()

    def update_game(self) -> None:
        if not self.is_running:
            return

        self.current_word.setFocus()

        for label in self.words_labels:
            label.update()

    def receive_game_message(self, message: dict) -> None:
        action = message["action"]

        if not self.is_running:
            return

        if action == "state":
            self.name = message["name"]
            self.lives = message["lives"]
            self.score = message["score"]
            self.streak = message["streak"]
            self.players = message["players"]

            self.update_stats()
            self.players_table.update_data(self.players, self.name)
        elif action == "new-word":
            word = message["word"]

            text = word["word"]

            position_x = int(
                word["horizontal-position"]
                * (self.words_panel.width() - self.horizontal_offset)
            )
            start_time = word["start-time"]
            fall_time = word["fall-time"]

            label = Word(
                self.words_panel,
                text,
                start_time,
                fall_time,
                self.words_panel.height(),
                position_x,
                0,
            )

            self.words_labels.append(label)
            label.show()
        elif action == "word-typed":
            word = message["word"]

            self.remove_word(word)
        elif action == "win":
            self.is_running = False
            QMessageBox.information(
                self,
                "Juego terminado",
                "Has ganado :)",
            )
            self.end_game.emit()

        elif action == "loose":
            self.is_running = False
            QMessageBox.information(
                self,
                "Juego terminado",
                "Has perdido :(",
            )
            self.end_game.emit()

    def remove_word(self, word: str) -> None:
        for label in self.words_labels:
            if label.text == word:
                label.deleteLater()
                self.words_labels.remove(label)
                break
