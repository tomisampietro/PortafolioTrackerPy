# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QScrollArea
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from dashboard.dashboardModel import DashboardModel
from dashboard.Portfolio import Portfolio  # Importa la clase Portfolio
from Entidades.models import Asset, AssetType  # Importa las clases Asset y AssetType
import json
import os
import mplcursors

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.portfolio = Portfolio()
        self.data_file = "portfolio_data.json"
        self.load_saved_assets()
        self.init_ui()

    def load_saved_assets(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                for asset_data in data:
                    asset_type = AssetType[asset_data['type']]
                    asset = Asset(
                        symbol=asset_data['symbol'],
                        name=asset_data['name'],
                        type=asset_type,
                        quantity=asset_data['quantity'],
                        current_price=asset_data['current_price']
                    )
                    self.portfolio.assets.append(asset)

    def init_ui(self):
        layout = QVBoxLayout()

        # Estilo general
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: #00ffcc;
            }
            QLabel {
                font-family: 'Roboto Mono';
                font-size: 18px;
                color: #ffffff;
            }
            QComboBox {
                background-color: #2d2d3d;
                color: #ffffff;
                border: 1px solid #00ffcc;
                padding: 5px;
                font-size: 14px;
            }
        """)

        # Título del Dashboard
        title_label = QLabel("Dashboard del Portafolio")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ff69b4;")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Selección de Período
        period_layout = QHBoxLayout()
        period_label = QLabel("Período de Análisis:")
        self.period_selector = QComboBox()
        self.period_selector.addItems(["Hoy", "Última Semana", "Último Mes", "Últimos 6 Meses", "Último Año"])
        self.period_selector.currentIndexChanged.connect(self.update_dashboard)
        period_layout.addWidget(period_label)
        period_layout.addWidget(self.period_selector)
        layout.addLayout(period_layout)

        # Scroll Area para gráficos
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Gráfico principal (rendimiento)
        self.figure_performance = Figure(facecolor='#1e1e2f')
        self.canvas_performance = FigureCanvas(self.figure_performance)
        self.canvas_performance.setMinimumHeight(400)
        scroll_layout.addWidget(self.canvas_performance)

        # Gráfico de distribución de activos
        self.figure_distribution = Figure(facecolor='#1e1e2f')
        self.canvas_distribution = FigureCanvas(self.figure_distribution)
        self.canvas_distribution.setMinimumHeight(400)
        scroll_layout.addWidget(self.canvas_distribution)

        # Gráfico de composición de activos
        self.figure_composition = Figure(facecolor='#1e1e2f')
        self.canvas_composition = FigureCanvas(self.figure_composition)
        self.canvas_composition.setMinimumHeight(400)
        scroll_layout.addWidget(self.canvas_composition)

        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)

        self.setLayout(layout)
        self.update_dashboard()

    def plot_portfolio_performance(self):
        """Gráfico de rendimiento del portafolio a lo largo del tiempo."""
        self.figure_performance.clear()
        ax = self.figure_performance.add_subplot(111)
        ax.set_facecolor("#1e1e2f")
        ax.tick_params(axis='x', colors='#ffffff', labelsize=12)
        ax.tick_params(axis='y', colors='#ffffff', labelsize=12)
        ax.spines['bottom'].set_color('#ffffff')
        ax.spines['top'].set_color('#ffffff')
        ax.spines['right'].set_color('#ffffff')
        ax.spines['left'].set_color('#ffffff')

        # Ejemplo de datos de rendimiento
        self.performance = [1000, 1050, 1100, 1080, 1150]
        self.dates = ["Lun", "Mar", "Mié", "Jue", "Vie"]

        line, = ax.plot(self.dates, self.performance, color='#00ffcc', linewidth=3, marker='o', markersize=8)
        ax.set_title('Rendimiento del Portafolio', color='#ffffff', fontsize=16)
        ax.set_ylabel("Valor ($)", color='#ffffff', fontsize=14)

        # Hacer el gráfico interactivo
        mplcursors.cursor(line, hover=True).connect("add", lambda sel: sel.annotation.set_text(f"{self.dates[sel.index]}: ${self.performance[sel.index]:.2f}"))

        self.canvas_performance.draw()

    def plot_asset_distribution(self):
        """Gráfico circular de distribución de activos."""
        self.figure_distribution.clear()
        ax = self.figure_distribution.add_subplot(111)
        ax.set_facecolor("#1e1e2f")

        # Datos ficticios para prototipo
        labels = ['Acciones', 'Bonos', 'Efectivo', 'Criptomonedas']
        sizes = [40, 30, 20, 10]
        colors = ['#ff69b4', '#00ffcc', '#ff9800', '#4caf50']

        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, autopct='%1.1f%%',
            startangle=140, colors=colors,
            textprops={'color': '#ffffff', 'fontsize': 12}
        )
        ax.set_title('Distribución de Activos', color='#ffffff', fontsize=16)

        # Hacer el gráfico interactivo
        mplcursors.cursor(wedges, hover=True).connect(
            "add", lambda sel: sel.annotation.set_text(f"{labels[sel.index]}: {sizes[sel.index]}%")
        )

        self.canvas_distribution.draw()

    def plot_asset_composition(self):
        """Gráfico de composición de activos con valores en dólares alineados a la derecha dentro de las barras."""
        self.figure_composition.clear()
        ax = self.figure_composition.add_subplot(111)
        ax.set_facecolor("#1e1e2f")

        # Datos ficticios de composición
        categories = ['Dinero Líquido', 'Conservadores', 'Medios', 'Arriesgados', 'Ultra Arriesgados']
        values = [10000, 30000, 20000, 25000, 15000]  # Valores en dólares
        colors = ['#00ffcc', '#4caf50', '#ff9800', '#ff69b4', '#ff4444']

        bars = ax.barh(categories, values, color=colors)

        # Agregar valores alineados a la derecha dentro de las barras
        for bar, value in zip(bars, values):
            ax.text(
                bar.get_width() - 500,  # Ajuste para posicionar dentro del borde derecho de la barra
                bar.get_y() + bar.get_height() / 2,  # Posición vertical (centro de la barra)
                f"${value:,}",  # Texto formateado con separador de miles
                ha='right', va='center', color='#ffffff', fontsize=12, weight='bold'
            )

        ax.set_title('Composición por Categorías', color='#ffffff', fontsize=20)
        ax.set_xlabel('Valor ($)', color='#ffffff', fontsize=16)
        ax.tick_params(axis='x', colors='#ffffff', labelsize=12)
        ax.tick_params(axis='y', colors='#ffffff', labelsize=14)
        for spine in ax.spines.values():
            spine.set_color('#ffffff')

        # Hacer el gráfico interactivo
        mplcursors.cursor(bars, hover=True).connect(
            "add", lambda sel: sel.annotation.set_text(f"{categories[sel.index]}: ${values[sel.index]:,.2f}")
        )

        self.canvas_composition.draw()

    def update_dashboard(self):
        """Actualizar gráficos según el período seleccionado."""
        self.plot_portfolio_performance()
        self.plot_asset_distribution()
        self.plot_asset_composition()
