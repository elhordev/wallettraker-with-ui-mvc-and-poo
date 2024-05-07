import tkinter as tk

realtime = []
wallet = []


class Stocks:
    def __init__(self, stock: str, realtime_price: float, time: str, var: str, close: float, more_or_less: float
                 , index: int):
        self.stock = stock
        self.realtime_price = realtime_price
        self.time = time
        self.var = var
        self.close = close
        self.more_or_less = more_or_less
        self.index = index

    def __str__(self):
        return f'Loading {self.stock} at {self.time}'


class StocksBuy(Stocks):
    def __init__(self, stock: str, buyprice: float, qty: int, expense: float, tobin: bool):
        super().__init__(stock, None, None, None, None, None, 0)

        self.buyprice = buyprice
        self.qty = qty
        self.expense = expense
        self.tobin = tobin
        self.balance = 0
        self.accountcharge = (buyprice * qty) + expense

    def __str__(self):
        return (f'Buy of {self.qty} stocks of {self.stock} with a price of {self.buyprice} for a total value with '
                f'expenses of {self.accountcharge}')

    def calcular_tobin(self):
        if self.tobin:
            self.tobin = f'{round(self.accountcharge * 0.002, 2)}€'

    @staticmethod
    def add_stock_to_wallet(app):
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
            print(buy)
            app.show_pop_up_buy()
        except tk.TclError:
            app.show_pop_up_error()
        except IndexError:
            app.show_pop_up_error_range()

    @staticmethod
    def add_sell(app):
        try:
            delete_wallet = app.option_control.get()
            wallet.pop(delete_wallet)
            app.show_pop_up_sell()
        except IndexError:
            app.show_pop_up_error()
        except tk.TclError:
            app.show_pop_up_error()
