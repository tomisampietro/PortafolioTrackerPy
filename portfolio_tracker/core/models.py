
#1.1 Modelos de Datos

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import List, Optional

class AssetType(Enum):
    """Tipos de activos financieros"""
    STOCK = auto()
    CRYPTO = auto()
    BOND = auto()
    CEDEAR = auto()
    FUND = auto()
    COMMODITY = auto()

class TransactionType(Enum):
    """Tipos de transacciones"""
    BUY = auto()
    SELL = auto()
    DIVIDEND = auto()
    TRANSFER = auto()

@dataclass
class Asset:
    """Representa un activo financiero"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    symbol: str = ''
    name: str = ''
    type: AssetType = AssetType.STOCK
    category: Optional[str] = None
    
    # Detalles de inversión
    purchase_price: float = 0.0
    quantity: float = 0.0
    current_price: float = 0.0
    currency: str = 'USD'
    
    # Metadata adicional
    exchange: Optional[str] = None
    country: Optional[str] = None
    
    @property
    def total_value(self) -> float:
        """Calcula el valor total del activo"""
        return self.quantity * self.current_price
    
    @property
    def unrealized_gain_loss(self) -> float:
        """Calcula la ganancia/pérdida no realizada"""
        return (self.current_price - self.purchase_price) * self.quantity

@dataclass
class Transaction:
    """Registro de transacciones financieras"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    asset_id: str = ''
    type: TransactionType = TransactionType.BUY
    date: datetime = field(default_factory=datetime.now)
    price: float = 0.0
    quantity: float = 0.0
    fees: float = 0.0
    notes: Optional[str] = None

@dataclass
class Portfolio:
    """Contenedor de portafolio de inversiones"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = 'Mi Portafolio'
    assets: List[Asset] = field(default_factory=list)
    transactions: List[Transaction] = field(default_factory=list)
    
    def add_asset(self, asset: Asset):
        """Añade un nuevo activo al portafolio"""
        self.assets.append(asset)
    
    def remove_asset(self, asset_id: str):
        """Elimina un activo del portafolio"""
        self.assets = [a for a in self.assets if a.id != asset_id]
    
    @property
    def total_value(self) -> float:
        """Calcula el valor total del portafolio"""
        return sum(asset.total_value for asset in self.assets)
    
    @property
    def performance_metrics(self) -> dict:
        """Calcula métricas de rendimiento básicas"""
        return {
            'total_value': self.total_value,
            'asset_count': len(self.assets),
            'diversification': self._calculate_diversification()
        }
    
    def _calculate_diversification(self) -> dict:
        """Calcula la diversificación por tipo de activo"""
        diversification = {}
        for asset_type in AssetType:
            type_assets = [a for a in self.assets if a.type == asset_type]
            if type_assets:
                diversification[asset_type] = {
                    'count': len(type_assets),
                    'total_value': sum(a.total_value for a in type_assets)
                }
        return diversification

@dataclass
class PortfolioCategory:
    """Categorías personalizables para agrupar activos"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ''
    description: Optional[str] = None
    assets: List[str] = field(default_factory=list)  # Lista de asset IDs