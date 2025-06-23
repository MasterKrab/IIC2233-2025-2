from pathlib import Path
from time import time
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QMessageBox
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

        self.pixmap = QPixmap(
            str(Path(SPRITES_PATH, "bloque-normal.png"))
        ).scaledToHeight(25)

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
        self.position_x = x
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


class GameWindow(QWidget):
    send_typed_word = pyqtSignal(str)
    end_game = pyqtSignal()

    def __init__(
        self, title: str = "DCCaída de palabras", x: int = 0, y: int = 0
    ) -> None:
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(x, y, 1000, 700)
        self.setFixedSize(self.width(), self.height())

        self.lives = VIDAS_INICIALES
        self.points = 0
        self.is_running = True

        self.words_labels = []

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_game)
        self.update_timer.start(30)

        self.horizontal_offset = 100
        self.words_width = self.width() - 2 * self.horizontal_offset

        self.top_bar_height = 50

        self.words_height = self.height() - self.top_bar_height

        self.current_word = QLineEdit(self)
        self.current_word.setAlignment(Qt.AlignCenter)
        self.current_word.setStyleSheet("border: none; background: transparent")

        self.current_word.setFont(QFont(get_font(), 16))
        self.current_word.setGeometry(
            int(self.width() / 4), 0, int(self.width() / 2), self.top_bar_height
        )
        self.current_word.setPlaceholderText("Escribe aquí")
        self.current_word.returnPressed.connect(self.type_current_word)

        self.current_word.show()

        self.lives_label = QLabel(f"Vidas: {VIDAS_INICIALES}", self)
        self.lives_label.setAlignment(Qt.AlignCenter)
        self.lives_label.setGeometry(0, 0, int(self.width() / 4), self.top_bar_height)
        self.lives_label.setFont(QFont(get_font(), 16))
        self.lives_label.show()

        self.score_label = QLabel("Puntaje: 0", self)
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setGeometry(
            int(3 * self.width() / 4), 0, int(self.width() / 4), self.top_bar_height
        )
        self.score_label.setFont(QFont(get_font(), 16))
        self.score_label.show()

    def type_current_word(self) -> None:
        text = self.current_word.text().strip()

        if not text:
            return

        self.send_typed_word.emit(text)
        self.current_word.clear()

    def update_game(self) -> None:
        if not self.is_running:
            return

        for label in self.words_labels:
            label.update()

    def receive_game_message(self, message: dict) -> None:
        action = message["action"]

        if not self.is_running:
            return

        if action == "state":
            self.lives = message["lives"]
            self.score = message["score"]

            self.lives_label.setText(f"Vidas: {self.lives}")
            self.score_label.setText(f"Puntaje: {self.score:.2f}")
        elif action == "new-word":
            word = message["word"]

            text = word["word"]

            position_x = (
                int(word["horizontal-position"] * self.words_width)
                + self.horizontal_offset
            )
            start_time = word["start-time"]
            fall_time = word["fall-time"]

            label = Word(
                self,
                text,
                start_time,
                fall_time,
                self.words_height,
                position_x,
                self.top_bar_height,
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
