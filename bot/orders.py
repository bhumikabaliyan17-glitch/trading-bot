from .client import BinanceFuturesClient
from .validators import (
    validate_symbol, validate_side, validate_order_type,
    validate_quantity, validate_price
)

class OrderManager:
    
    def __init__(self):
        self.client = BinanceFuturesClient()
    
    def validate_order_inputs(self, symbol, side, order_type, quantity, price=None):
        valid, msg = validate_symbol(symbol)
        if not valid:
            return False, msg
        valid, msg = validate_side(side)
        if not valid:
            return False, msg
        valid, msg = validate_order_type(order_type)
        if not valid:
            return False, msg
        valid, msg = validate_quantity(quantity)
        if not valid:
            return False, msg
        valid, msg = validate_price(price, order_type)
        if not valid:
            return False, msg
        return True, ""
    
    def place_order(self, symbol, side, order_type, quantity, price=None):
        valid, error_msg = self.validate_order_inputs(
            symbol, side, order_type, quantity, price
        )
        if not valid:
            return {'success': False, 'error_message': error_msg}
        
        return self.client.place_order(symbol, side, order_type, quantity, price)
