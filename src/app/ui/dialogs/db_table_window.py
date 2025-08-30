from PySide6.QtWidgets import QDialog, QVBoxLayout, QTableWidget
from app.db.queries import get_table_data
from app.translation import tr


class DBTableWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("db_table"))
        layout = QVBoxLayout()
        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        data = get_table_data()
        # Aquí deberías poblar la tabla con los datos obtenidos
        # self.table.setRowCount(len(data))
        # self.table.setColumnCount(len(data[0]) if data else 0)
        # ...
