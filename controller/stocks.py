import tkinter as tk
from main import app
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

    def add_stock_to_wallet(self):

        try:
            buy = StocksBuy(stock=realtime[app.frame_label_sell_buy_opcions.control_opcion.get()][self.stock],
                            buyprice=app.frame_label_sell_buy_opcions.control_price.get(),
                            qty=app.frame_label_sell_buy_opcions.control_qty.get(),
                            expense=app.frame_label_sell_buy_opcions.control_expense.get(),
                            tobin=app.frame_label_sell_buy_opcions.opcion_tobin.get())

            if app.frame_label_sell_buy_opcions.opcion_tobin.get():
                StocksBuy.calcular_tobin()

            wallet.append(buy)
            print(wallet)
        except tk.TclErrorl:
            app.show_error_popup()
