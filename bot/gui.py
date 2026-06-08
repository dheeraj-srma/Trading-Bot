import tkinter as tk
from tkinter import ttk, messagebox

from bot.client import get_client
from bot.orders import (
    place_market_order,
    place_limit_order
)
from bot.validators import validate_order


BG = "#1e1e1e"
CARD = "#252526"
FG = "white"
GREEN = "#16c60c"
RED = "#e81123"


class TradingBotUI:

    def __init__(self, root):

        self.root = root
        self.root.title("Binance Futures Trading Bot")
        self.root.geometry("700x700")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        title = tk.Label(
            root,
            text="Binance Futures Testnet Trading Bot",
            font=("Segoe UI", 20, "bold"),
            bg=BG,
            fg="white"
        )

        title.pack(pady=15)

        form = tk.Frame(
            root,
            bg=BG
        )

        form.pack()

        # Symbol

        tk.Label(
            form,
            text="Symbol",
            bg=BG,
            fg=FG,
            font=("Segoe UI", 10)
        ).pack()

        self.symbol_entry = tk.Entry(
            form,
            width=25,
            font=("Segoe UI", 11)
        )

        self.symbol_entry.insert(
            0,
            "BTCUSDT"
        )

        self.symbol_entry.pack(pady=5)

        # Side

        tk.Label(
            form,
            text="Side",
            bg=BG,
            fg=FG,
            font=("Segoe UI", 10)
        ).pack()

        self.side_var = tk.StringVar(
            value="BUY"
        )

        self.side_combo = ttk.Combobox(
            form,
            textvariable=self.side_var,
            values=["BUY", "SELL"],
            state="readonly",
            width=22
        )

        self.side_combo.pack(pady=5)

        # Order Type

        tk.Label(
            form,
            text="Order Type",
            bg=BG,
            fg=FG,
            font=("Segoe UI", 10)
        ).pack()

        self.type_var = tk.StringVar(
            value="MARKET"
        )

        self.type_combo = ttk.Combobox(
            form,
            textvariable=self.type_var,
            values=["MARKET", "LIMIT"],
            state="readonly",
            width=22
        )

        self.type_combo.pack(pady=5)

        self.type_combo.bind(
            "<<ComboboxSelected>>",
            self.toggle_price
        )

        # Quantity

        tk.Label(
            form,
            text="Quantity",
            bg=BG,
            fg=FG,
            font=("Segoe UI", 10)
        ).pack()

        self.quantity_entry = tk.Entry(
            form,
            width=25,
            font=("Segoe UI", 11)
        )

        self.quantity_entry.insert(
            0,
            "0.001"
        )

        self.quantity_entry.pack(pady=5)

        # Price

        tk.Label(
            form,
            text="Price (LIMIT only)",
            bg=BG,
            fg=FG,
            font=("Segoe UI", 10)
        ).pack()

        self.price_entry = tk.Entry(
            form,
            width=25,
            font=("Segoe UI", 11)
        )

        self.price_entry.pack(pady=5)

        self.price_entry.config(
            state="disabled"
        )

        # Button

        self.place_btn = tk.Button(
            form,
            text="Place Order",
            command=self.place_order,
            bg=GREEN,
            fg="white",
            font=("Segoe UI", 11, "bold"),
            width=20
        )

        self.place_btn.pack(
            pady=15
        )

        # Status

        self.status_label = tk.Label(
            root,
            text="Ready",
            bg=BG,
            fg=GREEN,
            font=("Segoe UI", 10)
        )

        self.status_label.pack()

        # Response Label

        tk.Label(
            root,
            text="Response",
            bg=BG,
            fg=FG,
            font=("Segoe UI", 11, "bold")
        ).pack(pady=10)

        # Response Box

        self.response_box = tk.Text(
            root,
            width=80,
            height=15,
            bg=CARD,
            fg="white",
            insertbackground="white",
            font=("Consolas", 10),
            bd=0
        )

        self.response_box.pack(
            padx=20,
            pady=10
        )

    def toggle_price(self, event=None):

        if self.type_var.get() == "MARKET":

            self.price_entry.delete(
                0,
                tk.END
            )

            self.price_entry.config(
                state="disabled"
            )

        else:

            self.price_entry.config(
                state="normal"
            )

    def place_order(self):

        try:

            symbol = self.symbol_entry.get().upper()

            side = self.side_var.get()

            order_type = self.type_var.get()

            quantity = float(
                self.quantity_entry.get()
            )

            price = None

            if (
                order_type == "LIMIT"
                and
                self.price_entry.get()
            ):

                price = float(
                    self.price_entry.get()
                )

            validate_order(
                symbol,
                side,
                order_type,
                quantity,
                price
            )

            client = get_client()

            if order_type == "MARKET":

                result = place_market_order(
                    client,
                    symbol,
                    side,
                    quantity
                )

            else:

                result = place_limit_order(
                    client,
                    symbol,
                    side,
                    quantity,
                    price
                )

            output = (
                f"SUCCESS\n\n"
                f"Order ID      : {result.get('orderId')}\n"
                f"Status        : {result.get('status')}\n"
                f"Symbol        : {result.get('symbol')}\n"
                f"Side          : {result.get('side')}\n"
                f"Type          : {result.get('type')}\n"
                f"Original Qty  : {result.get('origQty')}\n"
                f"Executed Qty  : {result.get('executedQty')}\n"
                f"Price         : {result.get('price')}"
            )

            self.response_box.delete(
                "1.0",
                tk.END
            )

            self.response_box.insert(
                tk.END,
                output
            )

            self.status_label.config(
                text="Order Submitted Successfully",
                fg=GREEN
            )

        except Exception as e:

            self.status_label.config(
                text="Order Failed",
                fg=RED
            )

            messagebox.showerror(
                "Error",
                str(e)
            )


if __name__ == "__main__":

    root = tk.Tk()

    app = TradingBotUI(root)

    root.mainloop()