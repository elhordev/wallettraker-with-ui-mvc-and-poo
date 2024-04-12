import tkinter as tk
from resources.constants import TITLE

class AppUi(tk.Tk):
    
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)


        # Configuracion de la ventana Root.
        self.title('WallettrakerUI by elhor')
        self.geometry('1920x1080')
        self.resizable(False,False)
        
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

        # Creamos frame para el label y el reloj
        frame_superior = tk.Frame(self)

        # Creamos el label.
        cabecera = tk.Label(frame_superior, text=TITLE)
        cabecera.config(font=('Terminal', 25))
        cabecera.grid(row=0, column=0)

        # Creamos el label para el reloj.
        reloj = tk.Label(frame_superior, text='')
        reloj.grid(row=0, column=1, columnspan=1)

        frame_superior.grid(row=0, column=0)

        # Creamos frame para opciones de compra y venta.

        frame_opciones = tk.Frame(self)
        frame_opciones.grid(row=1, column=1)

app = AppUi()

app.mainloop()

