from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class Table(QTableWidget):
    def __init__(self, header: list[str], values: list[list[str]]) -> None:
        super().__init__()

        self.setColumnCount(len(header))
        self.setHorizontalHeaderLabels(header)

        self.setRowCount(len(values))

        for row, value in enumerate(values):
            for column, item in enumerate(value):
                self.setItem(row, column, QTableWidgetItem(item))

        self.resizeColumnsToContents()
