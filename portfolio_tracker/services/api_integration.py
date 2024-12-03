#1.2 Servicios de Integración de APIs 

import requests
import yfinance as yf
import ccxt
from typing import Optional, Dict, Any
import logging

class APIIntegrationService:
    """Servicio centralizado para integración de APIs financieras"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.exchange_clients = {
            'binance': ccxt.binance(),
            # Añadir más exchanges según sea necesario
        }
    
    def get_real_time_price(self, symbol: str, source: str = 'yahoo') -> Optional[float]:
        """
        Obtiene el precio en tiempo real de un activo
        
        Args:
            symbol: Símbolo del activo (ej. AAPL, BTC)
            source: Fuente de datos (yahoo, binance, etc)
        
        Returns:
            Precio actual o None si falla
        """
        try:
            if source == 'yahoo':
                ticker = yf.Ticker(symbol)
                return ticker.history(period='1d')['Close'][-1]
            
            elif source == 'binance':
                exchange = self.exchange_clients['binance']
                ticker = exchange.fetch_ticker(symbol)
                return ticker['last']
            
            else:
                self.logger.warning(f"Fuente no soportada: {source}")
                return None
        
        except Exception as e:
            self.logger.error(f"Error obteniendo precio para {symbol}: {e}")
            return None
    
    def fetch_historical_data(
        self, 
        symbol: str, 
        start_date: str, 
        end_date: str, 
        source: str = 'yahoo'
    ) -> Optional[Dict[str, Any]]:
        """
        Obtiene datos históricos de un activo
        
        Args:
            symbol: Símbolo del activo
            start_date: Fecha de inicio (YYYY-MM-DD)
            end_date: Fecha de fin (YYYY-MM-DD)
            source: Fuente de datos
        
        Returns:
            Diccionario con datos históricos o None
        """
        try:
            if source == 'yahoo':
                ticker = yf.Ticker(symbol)
                historical = ticker.history(start=start_date, end=end_date)
                return {
                    'open': historical['Open'].tolist(),
                    'close': historical['Close'].tolist(),
                    'high': historical['High'].tolist(),
                    'low': historical['Low'].tolist(),
                    'volume': historical['Volume'].tolist()
                }
            
            else:
                self.logger.warning(f"Fuente no soportada: {source}")
                return None
        
        except Exception as e:
            self.logger.error(f"Error obteniendo histórico para {symbol}: {e}")
            return None
    
    def convert_currency(
        self, 
        amount: float, 
        from_currency: str, 
        to_currency: str
    ) -> Optional[float]:
        """
        Convierte monedas usando tasas en tiempo real
        
        Args:
            amount: Monto a convertir
            from_currency: Moneda de origen
            to_currency: Moneda de destino
        
        Returns:
            Monto convertido o None
        """
        try:
            # Ejemplo simplificado, usar API de conversión real
            url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
            response = requests.get(url)
            rates = response.json()['rates']
            
            converted_amount = amount * rates.get(to_currency, 1)
            return converted_amount
        
        except Exception as e:
            self.logger.error(f"Error convirtiendo moneda: {e}")
            return None