from controller.stocks import realtime
import tkinter as tk
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Alerts:
    alerts = []

    # If you have SMTP service just put yout credentials and data below ,
    # and the functioncall

    # Config SMTP y credentials
    smtp_server = ''
    smtp_port = None  # Port of TLS
    sender_email = 'Your mail'
    password = 'Your mail password'
    password2 = 'Esto_esdeprueba1992'  # Ignore that
    # Config of the message
    subject = ''
    body = ''
    mail_to_account = ''

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

    def delete_alert(self, alert):

        try:
            self.alerts.pop(int(alert))
            print(f'Alert deleted succesfully')
        except tk.TclError as e:

            print(f'{e}')

    def check_alerts(self, AppUi):
        alerts_to_delete = []

        if self.alerts:
            print('There are alerts')
            for alert in self.alerts:
                for stock in realtime:
                    if (alert.stock == stock.stock and alert.direction == 'above'
                            and stock.realtime_price >= alert.price):

                        alert_text = f'{stock.stock} is now above {alert.price}\n'
                        print(alert_text)
                        alerts_to_delete.append(alert)
                        print('PopUp 1 Send')

                        AppUi.pop_up_alerts(alert_text, alert.direction)
                    elif (alert.stock == stock.stock and alert.direction == 'below'
                          and stock.realtime_price <= alert.price):

                        alert_text_2 = f'{stock.stock} is now below {alert.price}\n'
                        print(alert_text_2)
                        alerts_to_delete.append(alert)
                        print('PopUp 2 send')

                        AppUi.pop_up_alerts(alert_text_2, alert.direction)
            for alert in alerts_to_delete:
                self.alerts.remove(alert)

        else:
            print('No alerts to check')

    def send_alerts(self):

        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = self.mail_to_account
        message['Subject'] = self.subject
        message.attach(MIMEText(self.body, 'plain'))
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        try:

            server.starttls()
            server.login(self.sender_email, self.password)
            text = message.as_string()
            # Sending mail
            server.sendmail(self.sender_email, self.subject, text)
            print('Mail send!')

        except Exception as e:
            print(e)

        finally:
            server.quit()
