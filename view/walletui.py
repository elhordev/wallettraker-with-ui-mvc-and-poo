import os
import tkinter as tk
import time
from tkinter import ttk, filedialog


from PIL import Image, ImageTk

from controller.realtime import urlcontent, scrapurl
from resources.constants import TITLE, URL, PATH_ERROR_IMAGE
from controller.stocks import realtime, StocksBuy
from model.wallet_manager import wallet, upload_wallet, save_wallet


# TO DO:
# Pintar el balance ,calculandolo antes de insertarlo en la tabla ttk del wallet.
# Aniadir un indice al tiempo real para la compra.
# Crear un popup error en caso de salirme del rango de la lista de compra
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
        self.execute_button = tk.Button(option_frame, text='Ejecutar', font=('Terminal', 14), bg='green',
                                        command=None)

        self.option = tk.StringVar(value='sell')
        self.refresh_var_control = tk.IntVar(value=20)
        self.clock = tk.Label(superior_frame, text='')
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

        # Creating MenuBar

        menu_bar = tk.Menu(self)

        # Creating File menu

        file_menu = tk.Menu(menu_bar, tearoff=False)
        file_menu.add_command(label='Load Wallet',command=self.open_file)
        file_menu.add_command(label='Save Wallet',command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.quit)

        # Add File menu to Menu Bar

        menu_bar.add_cascade(label='File', menu=file_menu)
        self.config(menu=menu_bar)

        # Creating the frame for the label and the clock

        superior_frame.grid(row=0, column=0)
        # Create the label

        header = tk.Label(superior_frame, text=TITLE)
        header.config(font=('Terminal', 25))
        header.grid(row=0, column=0)

        # Create the clock label

        self.clock.grid(row=0, column=1, columnspan=1)

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
        self.clock.config(text=time.strftime('\t%H:%M:%S'), font=('Terminal', 25))
        self.after(1000, self.clock_refresh)

    def conn_refresh(self, value):
        self.refresh_var_control.set(value)
        print(self.refresh_var_control.get())

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

        columns = ['Index', 'Stock', 'Price', 'Time', 'Var', 'Close', 'Difference']
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
                                                       stock.var, stock.close, stock.more_or_less))
        print('Actualizando tiempo real cada {} segundos'.format(self.refresh_var_control.get()))

        self.after(self.refresh_var_control.get() * 1000, func=self.show_market_data)

    def show_wallet_data(self):
        index_wallet = -1
        # Creamos tabla de wallet.
        wallet_tabular = ttk.Treeview(self, height=35)
        wallet_tabular.grid(row=3, column=0)

        # Label wallet
        label_wallet = tk.Label(self, text='Wallet Personal', font=('Terminal', 20))
        label_wallet.grid(row=2, column=0)

        columns = ['Index', 'Stock', 'Buy Price', 'Qty', 'Expense', 'Tobin', 'Balance', 'Account Charge']
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

        if os.path.exists(PATH_ERROR_IMAGE):
            image = Image.open(PATH_ERROR_IMAGE)
            image_tk = ImageTk.PhotoImage(image)
            image_label = tk.Label(popup_error_entry, image=image_tk, anchor=tk.CENTER)
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

        file = filedialog.askopenfile('r',filetypes=[('CSV files','*.csv')])
        upload_wallet(file=file)

    def save_file(self):
        save_window = tk.Toplevel(self)
        save_window.title('Guardado')
        save_window.geometry('400x350')
        save_label = tk.Label(save_window, text='\n Do you want to save your wallet?\nWith which name?\n')
        save_entry = tk.Entry(save_window)
        save_label.pack()
        save_button = tk.Button(save_window, text='Ok', command=lambda: save_wallet(save_entry.get()))
        save_entry.pack()
        save_button.pack()



        
        