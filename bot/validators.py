import re

def validate_symbol(symbol):
    if not symbol or not isinstance(symbol, str):
        return False, "Symbol must be a non-empty string"
    if not re.match(r'^[A-Z]+USDT$', symbol):
        return False, "Symbol must end with USDT (e.g., BTCUSDT)"
    return True, ""

def validate_side(side):
    if side.upper() not in ['BUY', 'SELL']:
        return False, "Side must be BUY or SELL"
    return True, ""

def validate_order_type(order_type):
    if order_type.upper() not in ['MARKET', 'LIMIT']:
        return False, "Order type must be MARKET or LIMIT"
    return True, ""

def validate_quantity(quantity):
    try:
        qty = float(quantity)
        if qty <= 0:
            return False, "Quantity must be greater than 0"
        if qty > 100:
            return False, "Quantity too high for testnet (max 100)"
        return True, ""
    except ValueError:
        return False, "Quantity must be a valid number"

def validate_price(price, order_type):
    if order_type.upper() == 'MARKET':
        return True, ""
    try:
        p = float(price)
        if p <= 0:
            return False, "Price must be greater than 0"
        return True, ""
    except ValueError:
        return False, "Price must be a valid number"
