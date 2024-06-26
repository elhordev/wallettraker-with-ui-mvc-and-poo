import os
import tkinter as tk
import time
from tkinter import ttk, filedialog

from PIL import Image, ImageTk

from controller.realtime import urlcontent, scrapurl
from resources.constants import TITLE, URL, PATH_ERROR_IMAGE
from controller.stocks import realtime, StocksBuy, wallet
from model.wallet_manager import upload_wallet, save_wallet
from controller.alerts import Alerts


# To do: Add colors to the alarm window depend on if below or above
# Add config popup metbod
class AppUi(tk.Tk):

    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk",
                 useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)

        # Root window setup.

        self.title('WallettrakerUI by elhor')
        self.geometry('1920x1080')
        self.resizable(False, False)

        # Create the frames.
        superior_frame = tk.Frame(self)
        option_frame = tk.Frame(self)
        # Create control variables.
        self.execute_button = tk.Button(option_frame, text='Execute', font=('Terminal', 14), bg='green',
                                        command='')

        self.option = tk.StringVar(value='sell')
        self.refresh_var_control = tk.IntVar(value=20)
        self.clock = tk.Label(option_frame, text='')
        self.option_control = tk.IntVar()
        self.qty_control = tk.IntVar()
        self.expense_control = tk.DoubleVar()
        self.price_control = tk.DoubleVar()
        index_control = tk.IntVar()
        self.tobin_option = tk.BooleanVar()
        self.entry_qty = tk.Entry(option_frame, textvariable=self.qty_control)
        self.entry_expense = tk.Entry(option_frame, textvariable=self.expense_control)
        self.entry_price = tk.Entry(option_frame, textvariable=self.price_control)
        self.option_radio_tobin = tk.Checkbutton(option_frame, text='Tobin', font=('Terminal', 16),
                                                 variable=self.tobin_option)

        # Initializing functions on the instance.

        self.button_color()
        self.show_market_data()
        self.show_wallet_data()
        self.clock_refresh()
        self.check_alerts()
        # Creating MenuBar

        menu_bar = tk.Menu(self)

        # Creating File menu

        file_menu = tk.Menu(menu_bar, tearoff=False)
        file_menu.add_command(label='Load Wallet', command=self.open_file)
        file_menu.add_command(label='Save Wallet', command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.quit)

        # Add File menu to Menu Bar

        menu_bar.add_cascade(label='File', menu=file_menu)

        # Creating Alert menu

        alert_menu = tk.Menu(menu_bar, tearoff=False)
        add_alert_menu = tk.Menu(alert_menu, tearoff=False)
        add_alert_menu.add_command(label='Descendent Price', command=self.add_alert_pop_up_bellow)
        add_alert_menu.add_command(label='Ascendent Price', command=self.add_alert_pop_up_above)
        alert_menu.add_cascade(label='Add Alert', menu=add_alert_menu)
        alert_menu.add_command(label='Show Alerts', command=self.show_alerts_pop_up)

        # Add Alert menu to Menu Bar

        menu_bar.add_cascade(label='Alerts', menu=alert_menu)
        self.config(menu=menu_bar)

        # Creating the frame for the label and the clock

        superior_frame.grid(row=0, column=0)
        # Create the label

        header = tk.Label(superior_frame, text=TITLE)
        header.config(font=('Terminal', 25))
        header.grid(row=0, column=0)

        # Create the clock label

        self.clock.pack()

        # Create the option frame and sell/buy

        option_frame.grid(row=1, column=1)

        # Create label for refresh control.

        label_slide = tk.Label(option_frame, text='\n\nFrecuencia de actualizacion', font=('Terminal', 10))
        label_info_slide = tk.Label(option_frame, text='Seconds', font=('Terminal', 8))
        slide = tk.Scale(option_frame, from_=3, to=29, orient='horizontal',
                         resolution=1, variable=self.refresh_var_control,
                         command=self.conn_refresh, sliderlength=10)

        # Create options inside the frame.

        sell_option = tk.Radiobutton(option_frame, text='Sell', font=('Terminal', 16),
                                     variable=self.option, value='sell',
                                     command=self.button_color)
        sell_option.pack()

        buy_option = tk.Radiobutton(option_frame, text='Buy', font=('Terminal', 16),
                                    variable=self.option, value='buy',
                                    command=self.button_color)
        buy_option.pack()

        label_stock = tk.Label(option_frame, text='Stock: ', font=('Terminal', 16))
        label_info_stock = tk.Label(option_frame, text='Recuerda que para una venta, \n tienes que poner el indice de '
                                                       'tu wallet.', font=('Terminal', 7))

        label_qty = tk.Label(option_frame, text='Cantidad: ', font=('Terminal', 16))
        label_expense = tk.Label(option_frame, text='Gastos operacion: ', font=('Terminal', 16))
        label_price = tk.Label(option_frame, text='Precio valor: ', font=('Terminal', 16))
        entry_stock = tk.Entry(option_frame, textvariable=self.option_control)

        label_stock.pack(padx=10, pady=5)
        entry_stock.pack(padx=10, pady=5)
        label_info_stock.pack()

        label_price.pack(padx=10, pady=5)
        self.entry_price.pack(padx=10, pady=5)

        label_qty.pack(padx=10, pady=5)
        self.entry_qty.pack(padx=10, pady=5)

        label_expense.pack(padx=10, pady=5)
        self.entry_expense.pack(padx=10, pady=5)

        self.option_radio_tobin.pack(padx=10, pady=5)

        self.execute_button.pack(padx=10, pady=5)

        label_slide.pack()
        slide.pack()
        label_info_slide.pack()

    def clock_refresh(self):
        self.clock.config(text=time.strftime('%H:%M:%S\n'), font=('Terminal', 25))
        self.after(1000, self.clock_refresh)

    def conn_refresh(self, value):
        self.refresh_var_control.set(value)
        print(f'Refreshing in {self.refresh_var_control.get()} seconds.')

    def show_pop_up_sell(self):
        pop_up_sell = tk.Toplevel(self)
        pop_up_sell.title('Sell')
        pop_up_sell.geometry('250x80')

        sell_label = tk.Label(pop_up_sell, text='Successfully sale!!\n')
        close_button = tk.Button(pop_up_sell, text='Close', command=pop_up_sell.destroy)

        sell_label.pack()
        close_button.pack()

    def show_pop_up_buy(self):

        pop_up_buy = tk.Toplevel(self)
        pop_up_buy.title('Buy')
        pop_up_buy.geometry('250x80')

        sell_label = tk.Label(pop_up_buy, text='Successfully Buy!!\n')
        close_button = tk.Button(pop_up_buy, text='Close', command=pop_up_buy.destroy)

        sell_label.pack()
        close_button.pack()

    def button_color(self):
        if self.option.get() == 'sell':
            self.execute_button.config(bg='green', command=lambda: StocksBuy.add_sell(self))
            self.entry_qty.config(state='disabled')
            self.entry_price.config(state='disabled')
            self.entry_expense.config(state='disabled')
            self.option_radio_tobin.config(state='disabled')

        elif self.option.get() == 'buy':
            self.execute_button.config(bg='red', command=lambda: StocksBuy.add_stock_to_wallet(self))
            self.entry_qty.config(state='normal')
            self.entry_price.config(state='normal')
            self.entry_expense.config(state='normal')
            self.option_radio_tobin.config(state='normal')

    @staticmethod
    def show_tiempo_real():
        result = urlcontent(URL)
        scrapurl(result)

    def show_market_data(self):
        # Creamos tabla.
        self.show_tiempo_real()

        columns = ['Index', 'Stock', 'Price', 'Time', 'Variation', 'Close', 'Difference']
        realtime_tabular = ttk.Treeview(self, height=35)
        realtime_tabular.grid(row=1, column=0)
        realtime_tabular['columns'] = columns

        for col in columns:
            realtime_tabular.column(col, anchor="center")
            realtime_tabular.heading(col, text=col)

        for item in realtime_tabular.get_children():
            realtime_tabular.delete(item)
        realtime_tabular.column('#0', width=0)
        for stock in realtime:
            realtime_tabular.insert('', 'end', values=(stock.index, stock.stock, stock.realtime_price, stock.time,
                                                       stock.close, stock.var, stock.more_or_less))
        print('\nRefreshing in {} seconds\n'.format(self.refresh_var_control.get()))

        self.after(self.refresh_var_control.get() * 1000, func=self.show_market_data)

    def show_wallet_data(self):
        index_wallet = -1
        # Creamos tabla de wallet.
        wallet_tabular = ttk.Treeview(self, height=35)
        wallet_tabular.grid(row=3, column=0)

        # Label wallet
        label_wallet = tk.Label(self, text='Wallet Personal', font=('Terminal', 20))
        label_wallet.grid(row=2, column=0)

        columns = ['Index', 'Stock', 'Buy Price', 'Quantity', 'Expense', 'Tobin', 'Balance', 'Account Charge']
        wallet_tabular['columns'] = columns
        wallet_tabular.column('#0', width=0)
        for col in columns:
            wallet_tabular.column(col, anchor='center')
            wallet_tabular.heading(col, text=col)

        for item in wallet_tabular.get_children():
            wallet_tabular.delete(item)

        for buy in wallet:
            index_wallet += 1
            buy.index = index_wallet
            for stock in realtime:
                if stock.stock == buy.stock:
                    buy.balance = '{}'.format(round((stock.realtime_price * buy.qty) - buy.accountcharge), 2)
            wallet_tabular.insert('', 'end', values=(buy.index,
                                                     buy.stock, buy.buyprice, buy.qty, buy.expense, buy.tobin,
                                                     buy.balance, buy.accountcharge))
        self.after(self.refresh_var_control.get() * 1000, func=self.show_wallet_data)

    def show_pop_up_error(self):
        popup_error_entry = tk.Toplevel(self)
        popup_error_entry.title('Error')
        popup_error_entry.geometry('600x450')

        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(current_dir, PATH_ERROR_IMAGE)
        print(img_path)
        if os.path.exists(img_path):
            image = Image.open(img_path)
            image_tk = ImageTk.PhotoImage(image)
            image_label = tk.Label(popup_error_entry, image=image_tk, anchor=tk.CENTER)
            image_label.image = image_tk
            image_label.pack()

        else:
            print('Error: Image file don''t found on the directory')

        label_error = tk.Label(popup_error_entry,
                               text='\n\nError al Introducir datos, recuerda que:\n\n-Valor son enteros.\n\n- '
                                    'Cantidad son'
                                    'enteros.\n\n- Gastos pueden ser decimales, usando el punto.\n\n- Precio igual que '
                                    'gastos.\n\n')
        label_error.config(font=('Terminal', 15))
        label_error.pack()

        boton_cerrar = tk.Button(popup_error_entry, text='OK', command=popup_error_entry.destroy)
        boton_cerrar.pack()

    def show_pop_up_error_range(self):

        popup_error_entry = tk.Toplevel(self)
        popup_error_entry.title('Error')
        popup_error_entry.geometry('400x350')

        if os.path.exists(PATH_ERROR_IMAGE):
            image = Image.open(PATH_ERROR_IMAGE)
            image_tk = ImageTk.PhotoImage(image)
            image_label = tk.Label(popup_error_entry, image=image_tk, anchor=tk.CENTER)
            image_label.pack()

        else:
            print('Error: Image file don''t found on the directory')

        label_error = tk.Label(popup_error_entry,
                               text=f'Stock entry out\n of range, you have to\nselect from 0 to {len(realtime)}\n')
        label_error.config(font=('Terminal', 15))
        label_error.pack()

        boton_cerrar = tk.Button(popup_error_entry, text='OK', command=popup_error_entry.destroy)
        boton_cerrar.pack()

    def open_file(self):

        try:
            file = filedialog.askopenfile('r', filetypes=[('CSV files', '*.csv')])
            print(file.name)
            load_window = tk.Toplevel(self)
            load_window.title('Loading wallet...')
            load_window.geometry('270x120')
            load_label = tk.Label(load_window, text='Wallet Loaded Succesfully\n')
            load_button = tk.Button(load_window, text='Ok', command=load_window.destroy)
            load_label.pack()
            load_button.pack()
            upload_wallet(file_name=file.name)
        except AttributeError:
            print('No selected file')

    def save_file(self):
        save_window = tk.Toplevel(self)
        save_window.title('Guardado')
        save_window.geometry('450x250')
        save_label = tk.Label(save_window, text='\n Do you want to save your wallet?\nWith which '
                                                'name?\n\nWARNING!\nIf you save a'
                                                'wallet,\n with the same name than an existing wallet it will overwrite'
                                                'it\n!')
        save_entry = tk.Entry(save_window)
        save_label.pack()
        save_button = tk.Button(save_window, text='Ok', command=lambda: save_wallet(save_entry.get()))
        save_entry.pack()
        save_button.pack()

    def add_alert_pop_up_above(self):
        direction = 'above'

        add_alert_window_above = tk.Toplevel(self, background='green')
        add_alert_window_above.title('Add Alert')
        add_alert_window_above.geometry('450x250')
        add_alert_label_above = tk.Label(add_alert_window_above, text='If the stock rises alert:\n', background='green')
        add_alert_index_entry = tk.Entry(add_alert_window_above)
        add_alert_index_entry.insert(0, 'Index')
        add_alert_price_entry = tk.Entry(add_alert_window_above)
        add_alert_price_entry.insert(0, 'Price')

        add_alert_button_above = tk.Button(add_alert_window_above, text='Create Alert',
                                           command=lambda: Alerts.add_alert(index=int(add_alert_index_entry.get()),
                                                                            price=float(add_alert_price_entry.get()),
                                                                            direction=direction))

        add_close_top_level_button = tk.Button(add_alert_window_above, text='Exit',
                                               command=add_alert_window_above.destroy)

        add_alert_label_above.pack()
        add_alert_index_entry.pack()
        add_alert_price_entry.pack()
        add_alert_button_above.pack()
        add_close_top_level_button.pack()

    def add_alert_pop_up_bellow(self):
        direction = 'below'

        add_alert_window_bellow = tk.Toplevel(self, background='red')
        add_alert_window_bellow.title('Add Alert')
        add_alert_window_bellow.geometry('450x250')
        add_alert_label_above = tk.Label(add_alert_window_bellow, text='If the stock decreases alert:\n',
                                         background='red')
        add_alert_index_entry = tk.Entry(add_alert_window_bellow)
        add_alert_index_entry.insert(0, 'Index')
        add_alert_price_entry = tk.Entry(add_alert_window_bellow)
        add_alert_price_entry.insert(0, 'Price')

        add_alert_button_bellow = tk.Button(add_alert_window_bellow, text='Create Alert',
                                            command=lambda: Alerts.add_alert(index=int(add_alert_index_entry.get()),
                                                                             price=float(add_alert_price_entry.get()),
                                                                             direction=direction))
        add_close_top_level_button = tk.Button(add_alert_window_bellow, text='Exit',
                                               command=add_alert_window_bellow.destroy)

        add_alert_label_above.pack()
        add_alert_index_entry.pack()
        add_alert_price_entry.pack()
        add_alert_button_bellow.pack()
        add_close_top_level_button.pack()

    def show_alerts_pop_up(self):

        show_alerts = tk.Toplevel(self)
        show_alerts.title('Alerts')
        show_alerts.geometry('400x300')
        if Alerts.alerts:
            for i, alert in enumerate(Alerts.alerts):
                alert_label = tk.Label(show_alerts,
                                       text=f'{i}. If {alert.stock} {alert.direction} from {alert.price}€\n')
                alert_label.pack()
            delete_alerts = tk.Button(show_alerts, text='Delete Alert', command=self.pop_up_delete_alert)
            delete_alerts.pack()
        else:
            no_alerts_label = tk.Label(show_alerts, text='No alerts to show.')
            no_alerts_label.pack()

        show_alerts_button = tk.Button(show_alerts, text='Close', command=show_alerts.destroy)
        show_alerts_button.pack()

    def check_alerts(self):
        print('Checking Alerts...')
        Alerts.check_alerts(Alerts, self)
        self.after(self.refresh_var_control.get() * 1000, func=self.check_alerts)

    def pop_up_alerts(self, alert_info, alert_direction):

        pop_up_alert = tk.Toplevel(self)
        pop_up_alert.geometry('300x100')
        pop_up_alert.title('ALERT!!')

        pop_up_alert_label = tk.Label(pop_up_alert, text=alert_info)
        pop_up_alert_button = tk.Button(pop_up_alert, text='Close', command=pop_up_alert.destroy)
        if alert_direction == 'above':
            pop_up_alert.config(background='green')
            pop_up_alert_label.config(background='green')

        else:
            pop_up_alert.config(background='red')
            pop_up_alert_label.config(background='red')

        pop_up_alert_label.pack()
        pop_up_alert_button.pack()

    def pop_up_delete_alert(self):
        pop_up_delete_alert = tk.Toplevel(self)
        pop_up_delete_alert.geometry('300x300')
        pop_up_delete_alert.title('Delete Alert')

        if Alerts.alerts:
            for i, alert in enumerate(Alerts.alerts):
                alert_label = tk.Label(pop_up_delete_alert,
                                       text=f'{i}. If {alert.stock} {alert.direction} from {alert.price}€\n')
                alert_label.pack()

            delete_alert_label = tk.Label(pop_up_delete_alert, text='Which alert do you want to delete ?\n')
            delete_alert_label.pack()

            delete_alert_entry = tk.Entry(pop_up_delete_alert)
            delete_alert_entry.pack()

            delete_alert_button = tk.Button(pop_up_delete_alert, text='Delete',
                                            command=lambda: Alerts.delete_alert(Alerts, delete_alert_entry.get()))
            delete_alert_button.pack()

        else:
            no_alerts_label = tk.Label(pop_up_delete_alert, text='No alerts to show.')
            no_alerts_label.pack()
