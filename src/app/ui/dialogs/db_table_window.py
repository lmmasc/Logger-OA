from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt
from app.db.queries import fetch_all
from app.utils.file_manager import get_db_path
from app.translation import tr


class DBTableWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("db_table"))
        self.setWindowFlag(Qt.Window)
        layout = QVBoxLayout()
        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        db_path = get_db_path()
        # Ejemplo: obtener todas las filas de una tabla llamada 'datos'
        query = "SELECT * FROM datos"  # Cambia 'datos' por el nombre real de tu tabla
        data = fetch_all(db_path, query)
        if not data:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            return
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data[0]))
        # Opcional: establecer encabezados si los tienes
        # self.table.setHorizontalHeaderLabels([...])
        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    # ...existing code...
