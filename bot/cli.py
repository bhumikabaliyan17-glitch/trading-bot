#!/usr/bin/env python3
import sys
from .orders import OrderManager
from .logging_config import setup_logging

logger = setup_logging()

def print_banner():
    print("\n" + "=" * 50)
    print("   🤖 BINANCE FUTURES TRADING BOT")
    print("   Testnet Mode (USDT-M)")
    print("=" * 50 + "\n")

def print_order_summary(symbol, side, order_type, quantity, price=None):
    print("\n" + "=" * 50)
    print("ORDER REQUEST SUMMARY")
    print("=" * 50)
    print(f"Symbol: {symbol.upper()}")
    print(f"Side: {side.upper()}")
    print(f"Type: {order_type.upper()}")
    print(f"Quantity: {quantity}")
    if price:
        print(f"Price: {price}")
    print("=" * 50)

def print_order_result(result):
    if result.get('success'):
        print("\n✅ ORDER SUCCESSFUL")
        print(f"Order ID: {result.get('order_id')}")
        print(f"Status: {result.get('status')}")
        print(f"Executed Quantity: {result.get('executed_qty')}")
        if result.get('avg_price'):
            print(f"Average Price: {result.get('avg_price')}")
    else:
        print("\n❌ ORDER FAILED")
        print(f"Error: {result.get('error_message', 'Unknown error')}")
    print("=" * 50 + "\n")

def get_user_input(prompt, required=True):
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("⚠️ This field is required. Please enter a value.")

def main():
    print_banner()
    order_manager = OrderManager()
    
    print("📝 Enter order details:\n")
    
    symbol = get_user_input("Enter symbol (e.g., BTCUSDT): ")
    side = get_user_input("Enter side (BUY/SELL): ")
    order_type = get_user_input("Enter order type (MARKET/LIMIT): ")
    quantity = get_user_input("Enter quantity (e.g., 0.001): ")
    
    price = None
    if order_type.upper() == 'LIMIT':
        price = get_user_input("Enter price (e.g., 50000): ")
    
    print_order_summary(symbol, side, order_type, quantity, price)
    
    confirm = input("Confirm order? (yes/no): ").lower()
    if confirm != 'yes':
        print("\n❌ Order cancelled by user.")
        sys.exit(0)
    
    logger.info(f"Attempting {side} {order_type} order: {quantity} {symbol}")
    result = order_manager.place_order(symbol, side, order_type, quantity, price)
    
    if result.get('success'):
        logger.info(f"Order successful: {result.get('order_id')}")
    else:
        logger.error(f"Order failed: {result.get('error_message')}")
    
    print_order_result(result)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Bot stopped by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
