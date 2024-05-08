from controller.stocks import realtime
import tkinter as tk


# Make all the logic for the email send
# Manaage exceptions for the tk.Tclerror
class Alerts:
    alerts = []

    def __init__(self, stock: str, price: float, direction: str):
        self.stock = stock
        self.price = price
        self.direction = direction

    @staticmethod
    def add_alert(index, price, direction):
        stock = realtime[index]
        try:
            alert = Alerts(stock=stock.stock,
                           price=float(price),
                           direction=direction)
            print(alert.stock, alert.price, alert.direction)
            Alerts.alerts.append(alert)
        except tk.TclError as e:

            print(f'{e}')

    def delete_alert(self):
        pass

    def check_alerts(self, AppUi):
        alerts_to_delete = []
        if self.alerts:
            print('There are alerts')
            for alert in self.alerts:
                for stock in realtime:
                    if alert.stock == stock.stock and alert.direction == 'above' and stock.realtime_price >= alert.price:

                        alert_text = f'{stock.stock} is now above {alert.price}'
                        print(alert_text)
                        alerts_to_delete.append(alert)
                        print('PopUp 1 Send')
                        AppUi.pop_up_alerts(alert_text)
                    elif alert.stock == stock.stock and alert.direction == 'below' and stock.realtime_price <= alert.price:

                        alert_text_2 = f'{stock.stock} is now below {alert.price}'
                        print(alert_text_2)
                        alerts_to_delete.append(alert)
                        print('PopUp 2 send')
                        AppUi.pop_up_alerts(alert_text_2)
            for alert in alerts_to_delete:
                self.alerts.remove(alert)

        else:
            print('No alerts to check')

    def send_alerts(self):
        pass
