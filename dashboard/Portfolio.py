# -*- coding: utf-8 -*-
import uuid
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from Entidades.models import Asset, Transaction, AssetType  # Asegúrate de importar las clases necesarias

@dataclass
class Portfolio:
    """Contenedor de portafolio de inversiones."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = 'Mi Portafolio'
    assets: List[Asset] = field(default_factory=list)
    transactions: List[Transaction] = field(default_factory=list)

    def add_asset(self, asset: Asset):
        """
        Añade un nuevo activo al portafolio.
        :param asset: Instancia de Asset a añadir.
        """
        if not isinstance(asset, Asset):
            raise TypeError("El objeto añadido debe ser una instancia de Asset.")
        self.assets.append(asset)

    def remove_asset(self, asset_id: str):
        """
        Elimina un activo del portafolio por su ID.
        :param asset_id: ID del activo a eliminar.
        """
        original_count = len(self.assets)
        self.assets = [a for a in self.assets if a.id != asset_id]
        if len(self.assets) == original_count:
            raise ValueError(f"No se encontró un activo con el ID {asset_id} para eliminar.")

    @property
    def total_value(self) -> float:
        """
        Calcula el valor total del portafolio.
        :return: Valor total (float).
        """
        return round(sum(asset.total_value for asset in self.assets), 2)

    @property
    def performance_metrics(self) -> Dict[str, float]:
        """
        Calcula métricas de rendimiento básicas del portafolio.
        :return: Diccionario con las métricas.
        """
        return {
            'total_value': self.total_value,
            'asset_count': len(self.assets),
            'diversification': self._calculate_diversification()
        }

    def _calculate_diversification(self) -> Dict[str, Dict[str, float]]:
        """
        Calcula la diversificación del portafolio por tipo de activo.
        :return: Diccionario con los datos de diversificación por AssetType.
        """
        diversification = {}
        for asset_type in AssetType:
            type_assets = [a for a in self.assets if a.type == asset_type]
            if type_assets:
                diversification[asset_type.name] = {
                    'count': len(type_assets),
                    'total_value': round(sum(a.total_value for a in type_assets), 2)
                }
        return diversification

    def find_asset(self, asset_id: str) -> Optional[Asset]:
        """
        Busca un activo por su ID.
        :param asset_id: ID del activo a buscar.
        :return: Instancia de Asset si se encuentra, None en caso contrario.
        """
        for asset in self.assets:
            if asset.id == asset_id:
                return asset
        return None

    def add_transaction(self, transaction: Transaction):
        """
        Añade una transacción al portafolio.
        :param transaction: Instancia de Transaction a añadir.
        """
        if not isinstance(transaction, Transaction):
            raise TypeError("El objeto añadido debe ser una instancia de Transaction.")
        self.transactions.append(transaction)
