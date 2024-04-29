import tkinter as tk
from model.wallet_manager import wallet

realtime = []


class Stocks:
    def __init__(self, stock: str, realtime_price: float, time: str, var: str, close: float, more_or_less: float):
        self.stock = stock
        self.realtime_price = realtime_price
        self.time = time
        self.var = var
        self.close = close
        self.more_or_less = more_or_less

    def __str__(self):
        return f'Cargando {self.stock} at {self.time}'


class StocksBuy(Stocks):
    def __init__(self, stock: str, buyprice: float, qty: int, expense: float, tobin: bool):
        super().__init__(stock, None, None, None, None, None)

        self.buyprice = buyprice
        self.qty = qty
        self.expense = expense
        self.tobin = tobin
        self.balance = 0
        self.accountcharge = (buyprice * qty) + expense

    def __str__(self):
        return (f'Compra de {self.qty} acciones de {self.stock} a un precio de {self.buyprice} por un valor en cuenta '
                f'despues de gastos de {self.accountcharge}')

    def calcular_tobin(self):
        if self.tobin:
            self.tobin = f'{round(self.accountcharge * 0.002, 2)}€'

    @staticmethod
    def add_stock_to_wallet(app):
        print('Miau')
        try:
            stock_position = realtime[app.option_control.get()]
            buy = StocksBuy(stock=stock_position.stock,
                            buyprice=app.price_control.get(),
                            qty=app.qty_control.get(),
                            expense=app.expense_control.get(),
                            tobin=app.tobin_option.get())

            if app.tobin_option.get():
                buy.calcular_tobin()

            wallet.append(buy)
            print(wallet[0])
        except tk.TclError:
            app.show_popup_error()

    @staticmethod
    def add_sell(app):
        print('Guau')
