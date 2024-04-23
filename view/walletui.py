import tkinter as tk
import time
from tkinter import ttk
from controller.realtime import urlcontent, scrapurl, realtime
from resources.constants import TITLE, URL


class AppUi(tk.Tk):

    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk",
                 useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)

        # Configuracion de la ventana Root.
        self.title('WallettrakerUI by elhor')
        self.geometry('1920x1080')
        self.resizable(False, False)

        self.menu_bar()
        self.mostrar_datos_tabulares()
        self.scale_refresh_rate()
        self.frame_label()
        self.show_wallet_data()
        self.frame_label_sell_buy_opcions()
        self.clock_refresh()
    @staticmethod
    def show_tiempo_real():
        result = urlcontent(URL)
        scrapurl(result)

    def menu_bar(self):
        # Crear la barra de menu.
        menu_bar = tk.Menu(self)

        # Creamos menu archivo
        archivo_menu = tk.Menu(menu_bar, tearoff=False)
        archivo_menu.add_command(label='Cargar cartera')
        archivo_menu.add_command(label='Guardar cartera')
        archivo_menu.add_separator()
        archivo_menu.add_command(label='Salir', command=self.quit)

        # Agregar el menu archivo a la barra_menu
        menu_bar.add_cascade(label='Archivo', menu=archivo_menu)
        self.config(menu=menu_bar)

    def frame_label(self):
        # Creamos frame para el label y el reloj
        frame_superior = tk.Frame(self)

        # Creamos el label.
        cabecera = tk.Label(frame_superior, text=TITLE)
        cabecera.config(font=('Terminal', 25))
        cabecera.grid(row=0, column=0)

        frame_superior.grid(row=0, column=0)

    def frame_label_sell_buy_opcions(self):
        # Creamos frame para opciones de compra y venta.
        frame_opciones = tk.Frame(self)
        frame_opciones.grid(row=1, column=1)

        # Variable de control para los Radiobutton de las opciones.
        opcion = tk.StringVar(value='venta')
        opcion_tobin = tk.BooleanVar()

        # Variables de control
        control_opcion = tk.IntVar()
        control_qty = tk.IntVar()
        control_expense = tk.DoubleVar()
        control_price = tk.DoubleVar()
        control_index = tk.IntVar()

        # Creamos opciones dentro de frame.
        opcion_radio_tobin = tk.Checkbutton(frame_opciones, text='Tobin', font=('Terminal', 16), variable=opcion_tobin)
        opcion_venta = tk.Radiobutton(frame_opciones, text='Venta ', font=('Terminal', 16), variable=opcion,
                                      value='venta'''',
                                              command=color_boton''')
        opcion_venta.pack()

        opcion_compra = tk.Radiobutton(frame_opciones, text='Compra ', font=('Terminal', 16), variable=opcion,
                                       value='compra'''',
                                               command=color_boton''')
        opcion_compra.pack()

        label_stock = tk.Label(frame_opciones, text='Valor: ', font=('Terminal', 16))
        label_info_stock = tk.Label(frame_opciones,
                                    text='*Recuerda que para una venta,\n tienes que poner el indice de tu wallet.',
                                    font=('Terminal', 7))
        label_qty = tk.Label(frame_opciones, text='Cantidad: ', font=('Terminal', 16))
        label_expense = tk.Label(frame_opciones, text='Gastos operacion: ', font=('Terminal', 16))
        label_price = tk.Label(frame_opciones, text='Precio valor: ', font=('Terminal', 16))

        entry_stock = tk.Entry(frame_opciones, textvariable=control_opcion)
        entry_qty = tk.Entry(frame_opciones, textvariable=control_qty)
        entry_expense = tk.Entry(frame_opciones, textvariable=control_expense)
        entry_price = tk.Entry(frame_opciones, textvariable=control_price)

        boton_ejecutar = tk.Button(frame_opciones, text='Ejecutar', font=('Terminal', 14), bg='green'
                                   )  # ,command=aniadir_compra

        label_stock.pack(padx=10, pady=5)
        entry_stock.pack(padx=10, pady=5)
        label_info_stock.pack()

        label_price.pack(padx=10, pady=5)
        entry_price.pack(padx=10, pady=5)

        label_qty.pack(padx=10, pady=5)
        entry_qty.pack(padx=10, pady=5)

        label_expense.pack(padx=10, pady=5)
        entry_expense.pack(padx=10, pady=5)

        opcion_radio_tobin.pack(padx=10, pady=5)

        boton_ejecutar.pack(padx=10, pady=5)

    def scale_refresh_rate(self):
        # Creamos un tk.scale para controlar la actualizacion.
        frame_scale = tk.Frame(self)
        frame_scale.grid(row=2, column=1)

        freq_actualizacion_var_control = tk.IntVar(value=10)

        label_slide = tk.Label(frame_scale, text='\n\nFrecuencia de actualizacion', font=('Terminal', 10))
        label_bajo_slide = tk.Label(frame_scale, text='Segundos', font=('Terminal', 8))
        slide = tk.Scale(frame_scale, from_=3, to=20, orient='horizontal', resolution=1,
                         variable=freq_actualizacion_var_control, sliderlength=10)  # command=control_freq_actualizacion
        '''
        label_slide.pack()
        slide.pack()
        label_bajo_slide.pack()
        '''

    def show_wallet_data(self):

        # Creamos tabla de wallet.
        wallet_tabular = ttk.Treeview(self, height=35)
        wallet_tabular.grid(row=3, column=0)

        # Label wallet
        label_wallet = tk.Label(self, text='Wallet Personal', font=('Terminal', 20))
        label_wallet.grid(row=2, column=0)

    def mostrar_datos_tabulares(self):
        # Creamos tabla.
        self.show_tiempo_real()

        columns = ['Stock', 'Precio', 'Hora', 'Var', 'Close', 'Differencia']
        realtime_tabular = ttk.Treeview(self, height=35)
        realtime_tabular.grid(row=1, column=0)
        realtime_tabular['columns'] = columns

        for col in columns:
            realtime_tabular.column(col, anchor="center")
            realtime_tabular.heading(col, text=col)

        for item in realtime_tabular.get_children():
            realtime_tabular.delete(item)

        for stock in realtime:
            realtime_tabular.insert('', 'end', values=(stock.stock, stock.realtime_price, stock.time,
                                                       stock.var, stock.close, stock.more_or_less))
        print('Actualizando tiempo real cada 5 segundos')

        self.after(5000, func=self.mostrar_datos_tabulares)

    def clock_refresh(self):
        # Creamos el label para el reloj.
        # Con su actualizacion
        clock_frame = tk.Frame()
        clock_frame.grid(row=0, column=1)
        clock = tk.Label(clock_frame, text='')
        clock.grid(row=0, column=1, columnspan=1)
        clock.config(text=time.strftime('\t%H:%M:%S'), font=('Terminal', 25))

        self.after(1000, self.clock_refresh)


app = AppUi()

app.mainloop()
