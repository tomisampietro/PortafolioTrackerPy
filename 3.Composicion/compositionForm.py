from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QHBoxLayout,
    QDialog,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QDialogButtonBox,
    QMessageBox,
    QHeaderView
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QDateTime

class Transaction:
    def __init__(self, date_time, quantity, price, platform, transaction_type):
        self.date_time = date_time
        self.quantity = quantity
        self.price = price
        self.platform = platform
        self.transaction_type = transaction_type

class Asset:
    def __init__(self, symbol, name, asset_type, quantity, current_price, platform, risk_type):
        self.symbol = symbol
        self.name = name
        self.type = asset_type
        self.quantity = quantity
        self.current_price = current_price
        self.platform = platform
        self.risk_type = risk_type
        self.transactions = []

    @property
    def total_value(self):
        return self.quantity * self.current_price

class Composition(QWidget):
    def __init__(self):
        super().__init__()
        self.portfolio = []  # Lista para manejar los activos
        self.init_ui()
        self.load_sample_assets()  # Cargar datos de ejemplo

    def init_ui(self):
        layout = QVBoxLayout()
        self.setStyleSheet("""
            QWidget {
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #1e1e2f, stop: 1 #1a1a26
                );
            }
        """)

        # Título de la Composición del Portafolio
        title_label = QLabel("Composición del Portafolio")
        title_label.setStyleSheet("""
            font-size: 28px; 
            font-weight: bold; 
            color: #00ffcc; 
            padding-bottom: 10px;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Filtros
        filter_layout = QHBoxLayout()
        self.symbol_filter = QLineEdit()
        self.symbol_filter.setPlaceholderText("Filtrar por Símbolo")
        self.symbol_filter.textChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.symbol_filter)

        self.name_filter = QLineEdit()
        self.name_filter.setPlaceholderText("Filtrar por Nombre")
        self.name_filter.textChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.name_filter)

        self.type_filter = QComboBox()
        self.type_filter.addItem("Todos")
        self.type_filter.addItem("Acciones")
        self.type_filter.addItem("Criptomoneda")
        self.type_filter.currentIndexChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.type_filter)

        self.risk_type_filter = QComboBox()
        self.risk_type_filter.addItem("Todos")
        self.risk_type_filter.addItem("Dinero Líquido")
        self.risk_type_filter.addItem("Conservadores")
        self.risk_type_filter.addItem("Medios")
        self.risk_type_filter.addItem("Arriesgados")
        self.risk_type_filter.addItem("Ultra Arriesgados")
        self.risk_type_filter.currentIndexChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.risk_type_filter)

        layout.addLayout(filter_layout)

        # Tabla de Activos
        self.assets_table = QTableWidget()
        self.assets_table.setColumnCount(8)
        self.assets_table.setHorizontalHeaderLabels([
            "Símbolo", "Nombre", "Tipo", "Cantidad",
            "Precio", "Valor Total", "Plataforma", "Tipo de Riesgo"
        ])
        self.assets_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.assets_table.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #222244; 
                color: #ff69b4; 
                font-weight: bold; 
                font-size: 14px; 
                border-bottom: 2px solid #00ffcc;
            }
        """)
        self.assets_table.setStyleSheet("""
            QTableWidget {
                background-color: #2d2d2d;
                color: #00ffcc;
                gridline-color: #555555;
                font-family: "Roboto Mono";
            }
        """)
        self.assets_table.cellDoubleClicked.connect(self.show_transaction_history)
        layout.addWidget(self.assets_table)

        # Tabla de Transacciones
        self.transactions_table = QTableWidget()
        self.transactions_table.setColumnCount(5)
        self.transactions_table.setHorizontalHeaderLabels([
            "Fecha y Hora", "Cantidad", "Precio", "Plataforma", "Tipo de Transacción"
        ])
        self.transactions_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.transactions_table.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #222244; 
                color: #ff69b4; 
                font-weight: bold; 
                font-size: 14px; 
                border-bottom: 2px solid #00ffcc;
            }
        """)
        self.transactions_table.setStyleSheet("""
            QTableWidget {
                background-color: #2d2d2d;
                color: #00ffcc;
                gridline-color: #555555;
                font-family: "Roboto Mono";
            }
        """)
        layout.addWidget(self.transactions_table)

        # Botones de agregar y eliminar activos
        button_layout = QHBoxLayout()
        add_button = QPushButton("Agregar Activo")
        add_button.setStyleSheet("background-color: #4caf50; color: white; font-size: 16px; padding: 10px;")
        add_button.clicked.connect(self.add_asset)
        button_layout.addWidget(add_button)

        remove_button = QPushButton("Eliminar Activo")
        remove_button.setStyleSheet("background-color: #f44336; color: white; font-size: 16px; padding: 10px;")
        remove_button.clicked.connect(self.remove_asset)
        button_layout.addWidget(remove_button)

        layout.addLayout(button_layout)

        self.load_composition()
        self.setLayout(layout)

    def load_sample_assets(self):
        # Datos de ejemplo
        sample_assets = [
            Asset("AAPL", "Apple Inc.", "Acciones", 10, 150.00, "NYSE", "Conservadores"),
            Asset("GOOGL", "Alphabet Inc.", "Acciones", 5, 2800.00, "NASDAQ", "Conservadores"),
            Asset("BTC", "Bitcoin", "Criptomoneda", 2, 45000.00, "Binance", "Ultra Arriesgados"),
            Asset("ETH", "Ethereum", "Criptomoneda", 10, 3000.00, "Coinbase", "Arriesgados")
        ]

        # Agregar transacciones de ejemplo para AAPL
        aapl_transactions = [
            Transaction(QDateTime.currentDateTime(), 5, 145.00, "NYSE", "Compra"),
            Transaction(QDateTime.currentDateTime().addDays(-1), 3, 148.00, "NYSE", "Compra"),
            Transaction(QDateTime.currentDateTime().addDays(-2), 2, 150.00, "NYSE", "Venta")
        ]
        sample_assets[0].transactions.extend(aapl_transactions)

        self.portfolio.extend(sample_assets)
        self.load_composition()

    def load_composition(self):
        # Limpiar tabla actual
        self.assets_table.setRowCount(0)

        # Cargar activos del portafolio
        distribution_data = []
        labels = []
        for asset in self.portfolio:
            row = self.assets_table.rowCount()
            self.assets_table.insertRow(row)

            self.assets_table.setItem(row, 0, QTableWidgetItem(asset.symbol))
            self.assets_table.setItem(row, 1, QTableWidgetItem(asset.name))
            self.assets_table.setItem(row, 2, QTableWidgetItem(asset.type))
            self.assets_table.setItem(row, 3, QTableWidgetItem(str(asset.quantity)))
            self.assets_table.setItem(row, 4, QTableWidgetItem(f"${asset.current_price:.2f}"))
            self.assets_table.setItem(row, 5, QTableWidgetItem(f"${asset.total_value:.2f}"))
            self.assets_table.setItem(row, 6, QTableWidgetItem(asset.platform))
            self.assets_table.setItem(row, 7, QTableWidgetItem(asset.risk_type))

            # Para el gráfico circular
            distribution_data.append(asset.total_value)
            labels.append(asset.name)

        # Actualizar el gráfico
        self.update_distribution_chart(distribution_data, labels)

    def update_distribution_chart(self, distribution_data, labels):
        # Aquí puedes implementar la lógica para actualizar el gráfico de distribución de activos
        pass

    def apply_filters(self):
        symbol_filter = self.symbol_filter.text().lower()
        name_filter = self.name_filter.text().lower()
        type_filter = self.type_filter.currentText()
        risk_type_filter = self.risk_type_filter.currentText()

        for row in range(self.assets_table.rowCount()):
            symbol_item = self.assets_table.item(row, 0)
            name_item = self.assets_table.item(row, 1)
            type_item = self.assets_table.item(row, 2)
            risk_type_item = self.assets_table.item(row, 7)

            symbol_match = symbol_filter in symbol_item.text().lower()
            name_match = name_filter in name_item.text().lower()
            type_match = (type_filter == "Todos") or (type_filter == type_item.text())
            risk_type_match = (risk_type_filter == "Todos") or (risk_type_filter == risk_type_item.text())

            self.assets_table.setRowHidden(row, not (symbol_match and name_match and type_match and risk_type_match))

    def add_asset(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Activo")
        layout = QFormLayout(dialog)

        symbol_input = QLineEdit()
        name_input = QLineEdit()
        type_input = QLineEdit()
        quantity_input = QLineEdit()
        price_input = QLineEdit()
        platform_input = QLineEdit()
        risk_type_input = QLineEdit()

        layout.addRow("Símbolo:", symbol_input)
        layout.addRow("Nombre:", name_input)
        layout.addRow("Tipo:", type_input)
        layout.addRow("Cantidad:", quantity_input)
        layout.addRow("Precio:", price_input)
        layout.addRow("Plataforma:", platform_input)
        layout.addRow("Tipo de Riesgo:", risk_type_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec_() == QDialog.Accepted:
            try:
                symbol = symbol_input.text()
                name = name_input.text()
                type_name = type_input.text()
                quantity = int(quantity_input.text())
                price = float(price_input.text())
                platform = platform_input.text()
                risk_type = risk_type_input.text()

                asset_type = type_name  # Assuming type_name is a string representing the asset type
                new_asset = Asset(symbol, name, asset_type, quantity, price, platform, risk_type)
                self.portfolio.append(new_asset)
                self.load_composition()
            except ValueError:
                QMessageBox.warning(self, "Error", "Cantidad y precio deben ser numéricos.")

    def remove_asset(self):
        selected_rows = self.assets_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Error", "Por favor seleccione un activo para eliminar.")
            return

        for selected_row in selected_rows:
            row_index = selected_row.row()
            symbol = self.assets_table.item(row_index, 0).text()  # Cambiar a la columna correcta
            asset_to_remove = next((a for a in self.portfolio if a.symbol == symbol), None)
            if asset_to_remove:
                self.portfolio.remove(asset_to_remove)

        self.load_composition()

    def show_transaction_history(self, row, column):
        symbol = self.assets_table.item(row, 0).text()
        asset = next((a for a in self.portfolio if a.symbol == symbol), None)
        if asset:
            self.transactions_table.setRowCount(0)
            for transaction in asset.transactions:
                row = self.transactions_table.rowCount()
                self.transactions_table.insertRow(row)
                self.transactions_table.setItem(row, 0, QTableWidgetItem(transaction.date_time.toString()))
                self.transactions_table.setItem(row, 1, QTableWidgetItem(str(transaction.quantity)))
                self.transactions_table.setItem(row, 2, QTableWidgetItem(f"${transaction.price:.2f}"))
                self.transactions_table.setItem(row, 3, QTableWidgetItem(transaction.platform))
                self.transactions_table.setItem(row, 4, QTableWidgetItem(transaction.transaction_type))