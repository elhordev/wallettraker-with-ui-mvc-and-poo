# Logica de scrapp y filtrado y creacion de lista de objetos de realtime.
# Con la funcion url content, descargamos el codigo HTML de la pagina, luego con la funcion scrapurl, filtramos y
# limpiamos todas las variables de saltos de lineas y tabulaciones, para posterior mente instanciar los objetos.


import requests
from bs4 import BeautifulSoup

from controller.stocks import Stocks, realtime


def urlcontent(url):
    return requests.get(url)


def scrapurl(web):
    realtime.clear()
    url_content = BeautifulSoup(web.content, "html.parser")
    acc_scrap = url_content.find_all(class_="ellipsis-short")
    price_scrap = url_content.find_all(class_="tv-price")
    time_scrap = url_content.find_all(class_="tv-time")
    close_scrap = url_content.find_all(class_="tv-close")
    var_scrap = url_content.find_all(class_="tv-change-percent")
    more_or_less_scrap = url_content.find_all(class_="tv-change-abs")

    stocks_names = [stock.text.strip() for stock in acc_scrap]
    indexes = [n for n in range(len(stocks_names))]
    prices_stocks = [float(price.text.strip().replace(',', '.')) for price in price_scrap
                     if '\nPrecio\n' not in price.text]
    time_stocks = [time.text.strip() for time in time_scrap if "\nÚLTIMA ACTUALIZACIÓN\n" not in time.text]
    close_stocks = [float(close.text.strip().replace(',', '.')) for close in close_scrap if
                    '\nPRECIO DE CIERRE\n' not in close.text]
    var_stocks = [var.text.strip() for var in var_scrap if "\n%\n" not in var.text]
    diff_stock = [diff.text.strip() for diff in more_or_less_scrap if "\n+/-" not in diff.text]

    for stock, prices, time, close, var, diff, index in zip(stocks_names, prices_stocks, time_stocks, close_stocks,
                                                            var_stocks, diff_stock, indexes):
        new_stock = Stocks(stock, prices, time, close, var, diff, index)
        realtime.append(new_stock)
        print(new_stock)
