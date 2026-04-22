from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv
import os

load_dotenv()

class BinanceFuturesClient:
    
    def __init__(self):
        self.api_key = os.getenv('API_KEY')
        self.api_secret = os.getenv('API_SECRET')
        
        if not self.api_key or not self.api_secret:
            raise ValueError("API_KEY and API_SECRET must be set in .env file")
        
        self.client = Client(self.api_key, self.api_secret, testnet=True)
        self.client.API_URL = 'https://testnet.binancefuture.com/fapi'
    
    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            if order_type.upper() == 'MARKET':
                order = self.client.futures_create_order(
                    symbol=symbol.upper(),
                    side=side.upper(),
                    type='MARKET',
                    quantity=float(quantity)
                )
            else:
                order = self.client.futures_create_order(
                    symbol=symbol.upper(),
                    side=side.upper(),
                    type='LIMIT',
                    quantity=float(quantity),
                    price=str(price),
                    timeInForce='GTC'
                )
            
            return {
                'success': True,
                'order_id': order.get('orderId'),
                'status': order.get('status'),
                'executed_qty': order.get('executedQty'),
                'avg_price': order.get('avgPrice'),
                'raw_response': order
            }
            
        except BinanceAPIException as e:
            return {
                'success': False,
                'error_code': e.code,
                'error_message': e.message
            }
        except Exception as e:
            return {
                'success': False,
                'error_message': str(e)
            }
