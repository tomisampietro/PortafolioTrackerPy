# -*- coding: utf-8 -*-


import json
import os

from Entidades.models import Asset, AssetType
from dashboard.Portfolio import Portfolio


class DashboardModel:
    def __init__(self):
        self.portfolio = Portfolio()
        self.data_file = "portfolio_data.json"
        self.load_saved_assets()

    def load_saved_assets(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                for asset_data in data:
                    asset_type = AssetType(name=asset_data['type'])
                    asset = Asset(
                        symbol=asset_data['symbol'],
                        name=asset_data['name'],
                        type=asset_type,
                        quantity=asset_data['quantity'],
                        current_price=asset_data['current_price']
                    )
                    self.portfolio.assets.append(asset)

    def get_portfolio_performance(self):
        # Ejemplo de datos de rendimiento
        performance = [1000, 1050, 1100, 1080, 1150]
        dates = ["Lun", "Mar", "Mie", "Jue", "Vie"]
        return dates, performance

    def get_asset_distribution(self):
        # Datos ficticios para prototipo
        labels = ['Acciones', 'Bonos', 'Efectivo', 'Criptomonedas']
        sizes = [40, 30, 20, 10]
        colors = ['#ff69b4', '#00ffcc', '#ff9800', '#4caf50']
        return labels, sizes, colors

    def get_asset_composition(self):
        # Datos ficticios de composición
        categories = ['Dinero Liquido', 'Conservadores', 'Medios', 'Arriesgados', 'Ultra Arriesgados']
        values = [10000, 30000, 20000, 25000, 15000]  # Valores en dólares
        colors = ['#00ffcc', '#4caf50', '#ff9800', '#ff69b4', '#ff4444']
        return categories, values, colors
