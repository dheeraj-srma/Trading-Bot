from binance.enums import *
from bot.logging_config import logger


def place_market_order(client, symbol, side, quantity):

    logger.info(
        f"MARKET order | {symbol} | {side} | qty={quantity}"
    )

    order = client.futures_create_order(
        symbol=symbol,
        side=side,
        type=FUTURE_ORDER_TYPE_MARKET,
        quantity=quantity
    )

    logger.info(order)

    return order


def place_limit_order(client,
                      symbol,
                      side,
                      quantity,
                      price):

    logger.info(
        f"LIMIT order | {symbol} | {side} | qty={quantity} | price={price}"
    )

    order = client.futures_create_order(
        symbol=symbol,
        side=side,
        type=FUTURE_ORDER_TYPE_LIMIT,
        quantity=quantity,
        price=price,
        timeInForce="GTC"
    )

    logger.info(order)

    return order