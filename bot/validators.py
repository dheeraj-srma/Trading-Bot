def validate_order(symbol, side, order_type, quantity, price=None):

    side = side.upper()
    order_type = order_type.upper()

    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")

    if order_type not in ["MARKET", "LIMIT"]:
        raise ValueError("Order type must be MARKET or LIMIT")

    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero")

    if order_type == "LIMIT" and price is None:
        raise ValueError("LIMIT order requires price")

    return True