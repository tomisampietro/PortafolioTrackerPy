from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QTableWidget, QTableWidgetItem, QLabel, QHeaderView, QPushButton,
    QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox, QScrollArea, QComboBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
import random


class MoneySources(QWidget):
    def on_graph_click(self, event):
        """Maneja eventos de clic en el gráfico."""
        if event.inaxes:
            QMessageBox.information(self, "Información del Gráfico", f"Has hecho clic en el punto: ({event.xdata:.2f}, {event.ydata:.2f})")
    def add_entry_dialog(self, table, color):
        """Abre un cuadro de diálogo para agregar una nueva entrada a la tabla."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Entrada")
        layout = QFormLayout(dialog)

        description_input = QLineEdit()
        value_input = QLineEdit()
        date_input = QLineEdit()
        date_input.setPlaceholderText("YYYY-MM-DD")

        layout.addRow("Descripción:", description_input)
        layout.addRow("Valor:", value_input)
        layout.addRow("Fecha:", date_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec() == QDialog.Accepted:
            description = description_input.text()
            value = value_input.text()
            date = date_input.text()

            if description and value and date:
                try:
                    value = float(value)
                    new_row = (description, f"{value:,.2f}", date)
                    self.add_data_to_table(table, [new_row], color)
                except ValueError:
                    QMessageBox.warning(self, "Error", "El valor debe ser un número válido.")
            else:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
    def update_totals(self):
        """Actualiza los totales de todas las tablas."""
        self.assets_total_label.setText(f"${self.calculate_total(self.assets_table):,.2f}")
        self.liabilities_total_label.setText(f"${self.calculate_total(self.liabilities_table):,.2f}")
        self.net_worth_total_label.setText(f"${self.calculate_total(self.net_worth_table):,.2f}")
    def __init__(self):
        super().__init__()
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year
        self.init_ui()

    def init_ui(self):
        # Crear layout principal para la ventana
        main_layout = QVBoxLayout(self)

        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Contenedor para el contenido desplazable
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Título y Filtros
        self.title_label = QLabel(f"Fuentes de dinero: {self.get_month_name(self.current_month)} {self.current_year}")
        self.title_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        scroll_layout.addWidget(self.title_label)

        # Filtros de selección de mes y año
        filters_layout = QHBoxLayout()
        self.month_combo = QComboBox()
        self.month_combo.addItems([self.get_month_name(i) for i in range(1, 13)])
        self.month_combo.setCurrentIndex(self.current_month - 1)
        self.month_combo.currentIndexChanged.connect(self.update_metrics)

        self.year_combo = QComboBox()
        self.year_combo.addItems([str(y) for y in range(self.current_year - 10, self.current_year + 11)])
        self.year_combo.setCurrentText(str(self.current_year))
        self.year_combo.currentIndexChanged.connect(self.update_metrics)

        filters_layout.addWidget(QLabel("Mes:"))
        filters_layout.addWidget(self.month_combo)
        filters_layout.addWidget(QLabel("Año:"))
        filters_layout.addWidget(self.year_combo)
        scroll_layout.addLayout(filters_layout)

        # GroupBox para Patrimonio Neto
        net_worth_groupbox = QGroupBox("Patrimonio Neto")
        net_worth_groupbox.setMinimumHeight(400)
        net_worth_layout = QVBoxLayout()
        self.net_worth_table = QTableWidget()
        self.net_worth_table.setColumnCount(3)
        self.net_worth_table.setHorizontalHeaderLabels(["Descripción", "Valor", "Fecha"])
        self.net_worth_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.net_worth_table.horizontalHeader().setStyleSheet("font-weight: bold; font-size: 12px; color: black;")
        self.net_worth_table.setStyleSheet("""
            QTableWidget {
                background-color: #d0e7ff; /* Celeste claro para fondo de la tabla */
            }
            QTableWidget::item {
                color: black; /* Color del texto de las tablas */
            }
        """)
        net_worth_layout.addWidget(self.net_worth_table)

        # Botón y Total para Patrimonio Neto
        net_worth_controls_layout = QHBoxLayout()
        add_net_worth_button = QPushButton("Agregar Patrimonio Neto")
        add_net_worth_button.setStyleSheet("background-color: #e0f7fa; color: black; font-size: 14px;")
        add_net_worth_button.clicked.connect(lambda: self.add_entry_dialog(self.net_worth_table, "#e0f7fa"))
        net_worth_controls_layout.addWidget(add_net_worth_button)
        self.net_worth_total_label = QLabel("$0,00")
        self.net_worth_total_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.net_worth_total_label.setAlignment(Qt.AlignRight)
        net_worth_controls_layout.addWidget(self.net_worth_total_label)
        net_worth_layout.addLayout(net_worth_controls_layout)

        net_worth_groupbox.setLayout(net_worth_layout)
        scroll_layout.addWidget(net_worth_groupbox)

        # Añadir espacio después del GroupBox de Patrimonio Neto
        scroll_layout.addSpacing(20)

        # Layout horizontal para Activos y Pasivos
        assets_liabilities_layout = QHBoxLayout()

        # GroupBox para Activos
        assets_groupbox = QGroupBox("Activos")
        assets_groupbox.setMinimumHeight(400)
        assets_layout = QVBoxLayout()
        self.assets_table = QTableWidget()
        self.assets_table.setColumnCount(3)
        self.assets_table.setHorizontalHeaderLabels(["Descripción", "Valor", "Fecha"])
        self.assets_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.assets_table.horizontalHeader().setStyleSheet("font-weight: bold; font-size: 12px; color: black;")
        self.assets_table.setStyleSheet("""
            QTableWidget::item {
                color: black; /* Color del texto de las tablas */
            }
        """)
        assets_layout.addWidget(self.assets_table)

        # Botón y Total para Activos
        assets_controls_layout = QHBoxLayout()
        add_assets_button = QPushButton("Agregar Activo")
        add_assets_button.setStyleSheet("background-color: #d0f0c0; color: black; font-size: 14px;")
        add_assets_button.clicked.connect(lambda: self.add_entry_dialog(self.assets_table, "#d0f0c0"))
        assets_controls_layout.addWidget(add_assets_button)
        self.assets_total_label = QLabel("$0,00")
        self.assets_total_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.assets_total_label.setAlignment(Qt.AlignRight)
        assets_controls_layout.addWidget(self.assets_total_label)
        assets_layout.addLayout(assets_controls_layout)

        assets_groupbox.setLayout(assets_layout)
        assets_liabilities_layout.addWidget(assets_groupbox)

        # GroupBox para Pasivos
        liabilities_groupbox = QGroupBox("Pasivos")
        liabilities_groupbox.setMinimumHeight(400)
        liabilities_layout = QVBoxLayout()
        self.liabilities_table = QTableWidget()
        self.liabilities_table.setColumnCount(3)
        self.liabilities_table.setHorizontalHeaderLabels(["Descripción", "Valor", "Fecha"])
        self.liabilities_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.liabilities_table.horizontalHeader().setStyleSheet("font-weight: bold; font-size: 12px; color: black;")
        self.liabilities_table.setStyleSheet("""
            QTableWidget::item {
                color: black; /* Color del texto de las tablas */
            }
        """)
        liabilities_layout.addWidget(self.liabilities_table)

        # Botón y Total para Pasivos
        liabilities_controls_layout = QHBoxLayout()
        add_liabilities_button = QPushButton("Agregar Pasivo")
        add_liabilities_button.setStyleSheet("background-color: #f8d7da; color: black; font-size: 14px;")
        add_liabilities_button.clicked.connect(lambda: self.add_entry_dialog(self.liabilities_table, "#f8d7da"))
        liabilities_controls_layout.addWidget(add_liabilities_button)
        self.liabilities_total_label = QLabel("$0,00")
        self.liabilities_total_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.liabilities_total_label.setAlignment(Qt.AlignRight)
        liabilities_controls_layout.addWidget(self.liabilities_total_label)
        liabilities_layout.addLayout(liabilities_controls_layout)

        liabilities_groupbox.setLayout(liabilities_layout)
        assets_liabilities_layout.addWidget(liabilities_groupbox)

        scroll_layout.addLayout(assets_liabilities_layout)

        # Añadir espacio después del GroupBox de Activos y Pasivos
        scroll_layout.addSpacing(20)

        # Métricas adicionales
        self.metrics_label = QLabel("")
        self.metrics_label.setFont(QFont("Arial", 16))
        self.update_metrics()
        self.update_totals()  # Inicializa las métricas
        scroll_layout.addWidget(self.metrics_label)

        # Gráfico de evolución
        # Añadir un contenedor para el gráfico
        graph_groupbox = QGroupBox("Gráfico de Evolución de Activos y Pasivos")
        graph_groupbox.setMinimumHeight(500)
        graph_layout = QVBoxLayout()
        self.figure, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        graph_layout.addWidget(self.toolbar)
        graph_layout.addWidget(self.canvas)
        self.canvas.mpl_connect('button_press_event', self.on_graph_click)
        graph_groupbox.setLayout(graph_layout)
        scroll_layout.addWidget(graph_groupbox)
        self.plot_evolution_chart()

        # Configurar Scroll Area
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        # Agregar valores de ejemplo a las tablas
        self.add_example_data()

    def get_month_name(self, month):
        """Devuelve el nombre del mes dado un índice."""
        return [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ][month - 1]

    def update_metrics(self):
        """Actualiza las métricas de beneficio y ahorro."""
        """Actualiza las métricas de beneficio y ahorro."""
        selected_month = self.month_combo.currentIndex() + 1
        selected_year = int(self.year_combo.currentText())
        total_assets = self.calculate_total(self.assets_table)
        total_liabilities = self.calculate_total(self.liabilities_table)
        net_benefit = total_assets - total_liabilities
        self.metrics_label.setText(
            f"En {self.get_month_name(selected_month)} {selected_year}, he tenido un beneficio de ${net_benefit:,.2f} disponibles para ahorrar."
        )

    def plot_evolution_chart(self):
        """Genera un gráfico de la evolución de activos y pasivos totales por mes/año."""
        months = [self.get_month_name(i) for i in range(1, 13)]
        assets_data = [random.randint(50000, 200000) for _ in range(12)]  # Datos ficticios de activos
        liabilities_data = [random.randint(20000, 100000) for _ in range(12)]  # Datos ficticios de pasivos

        self.ax.clear()
        self.ax.plot(months, assets_data, label="Activos Totales", marker="o")
        self.ax.plot(months, liabilities_data, label="Pasivos Totales", marker="o")
        self.ax.set_title("Evolución de Activos y Pasivos")
        self.ax.set_xlabel("Mes")
        self.ax.set_ylabel("Monto ($)")
        self.ax.legend()
        self.canvas.draw()

    def calculate_total(self, table):
        """Calcula el total de una tabla."""
        """Calcula el total de una tabla."""
        total = 0
        for row in range(table.rowCount()):
            value_item = table.item(row, 1)
            if value_item:
                value = float(value_item.text().replace("$", "").replace(",", ""))
                total += value
        return total

    def add_example_data(self):
        """Agrega datos ficticios a las tablas y calcula los totales."""
        net_worth_data = [("Cuenta Ahorro", "50000", "2023-01-01"), ("Inversiones", "150000", "2023-02-01")]
        self.add_data_to_table(self.net_worth_table, net_worth_data, "#d0e7ff")
        assets_data = [("Acciones", "120000", "2023-01-01"), ("Propiedades", "300000", "2023-01-01")]
        liabilities_data = [("Hipoteca", "200000", "2023-01-01"), ("Préstamo Auto", "15000", "2023-01-01")]
        self.add_data_to_table(self.assets_table, assets_data, "#d0f0c0")
        self.add_data_to_table(self.liabilities_table, liabilities_data, "#f8d7da")
        self.update_metrics()

    def add_data_to_table(self, table, data, color):
        """Agrega datos a una tabla y actualiza el total."""
        """Agrega datos a una tabla."""
        for row_data in data:
            row = table.rowCount()
            table.insertRow(row)
            for column, value in enumerate(row_data):
                item = QTableWidgetItem(f"${float(value):,.2f}" if column == 1 else value)
                item.setBackground(QColor(color))
                table.setItem(row, column, item)
        self.update_totals()
