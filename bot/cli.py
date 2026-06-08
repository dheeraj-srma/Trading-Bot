import argparse

from rich.console import Console

from bot.client import get_client
from bot.orders import (
    place_market_order,
    place_limit_order
)
from bot.validators import validate_order

console = Console()


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", required=True)
    parser.add_argument("--type", required=True)
    parser.add_argument("--quantity",
                        type=float,
                        required=True)
    parser.add_argument("--price",
                        type=float)

    args = parser.parse_args()

    

    try:

        validate_order(
            args.symbol,
            args.side,
            args.type,
            args.quantity,
            args.price
        )

        client = get_client()

        console.print(
            f"\n[cyan]Symbol:[/cyan] {args.symbol}"
        )

        console.print(
            f"[cyan]Side:[/cyan] {args.side}"
        )

        console.print(
            f"[cyan]Type:[/cyan] {args.type}"
        )

        if args.type.upper() == "MARKET":

            result = place_market_order(
                client,
                args.symbol,
                args.side,
                args.quantity
            )

        else:

            result = place_limit_order(
                client,
                args.symbol,
                args.side,
                args.quantity,
                args.price
            )

        console.print(f"Order ID: {result.get('orderId')}")
        console.print(f"Status: {result.get('status')}")
        console.print(f"Original Qty: {result.get('origQty')}")
        console.print(f"Executed Qty: {result.get('executedQty')}")
        console.print(f"Price: {result.get('price')}")

    except Exception as e:

        console.print(
            f"[red]ERROR:[/red] {e}"
        )


if __name__ == "__main__":
    main()