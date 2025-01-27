# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QVBoxLayout, 
    QHBoxLayout, 
    QWidget, 
    QPushButton, 
    QLabel,
    QStackedWidget
)
from PyQt5.QtCore import Qt

# Asegurarse de que el directorio raíz esté en sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar módulos directamente
from dashboard.dashboardForm import Dashboard
from Composicion.compositionForm import Composition
from FuentesDeDinero.FuentesDeDineroForm import MoneySources

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Portfolio Tracker")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #1e1e1e; color: #f3f3f3;")

        # Crear un widget central y un layout principal
        central_widget = QWidget()
        main_layout = QHBoxLayout()

        # Menú de navegación
        nav_menu = QVBoxLayout()
        nav_menu.setAlignment(Qt.AlignTop)
        nav_menu.setContentsMargins(20, 20, 20, 20)
        title_label = QLabel("Menú de Navegación")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        nav_menu.addWidget(title_label)

        buttons = [
            ("Resumen del Portafolio", self.show_portfolio_summary),
            ("Composición de Portafolio", self.show_composition),
            ("Fuentes de dinero", self.show_money_sources),
            ("Configuración", self.show_settings)
        ]

        for text, handler in buttons:
            button = QPushButton(text)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #3a3d41; 
                    color: white; 
                    font-size: 16px; 
                    padding: 10px; 
                    margin: 10px;
                    border: 1px solid #555555;
                }
                QPushButton:hover {
                    background-color: #4a4d51;
                }
            """)
            button.clicked.connect(handler)
            nav_menu.addWidget(button)

        main_layout.addLayout(nav_menu)

        # Crear un QStackedWidget para cambiar entre diferentes pantallas
        self.stacked_widget = QStackedWidget()

        # Agregar Dashboard, Composición y Fuentes de dinero al stacked widget
        self.dashboard = Dashboard()
        self.composition = Composition()
        self.money_sources = MoneySources()
        self.stacked_widget.addWidget(self.dashboard)  # Index 0
        self.stacked_widget.addWidget(self.composition)  # Index 1
        self.stacked_widget.addWidget(self.money_sources)  # Index 2

        main_layout.addWidget(self.stacked_widget)

        # Establecer el layout en el widget central
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Mostrar la pantalla de "Composición de Portafolio" al iniciar
        self.stacked_widget.setCurrentIndex(1)

    def show_portfolio_summary(self):
        # Cambiar al Dashboard
        self.stacked_widget.setCurrentIndex(0)

    def show_composition(self):
        # Cambiar a la pantalla de Composición de Portafolio
        self.stacked_widget.setCurrentIndex(1)

    def show_money_sources(self):
        # Cambiar a la pantalla de Fuentes de dinero
        self.stacked_widget.setCurrentIndex(2)

    def show_settings(self):
        print("Mostrar configuración")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
