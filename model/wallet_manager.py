import csv
from controller.stocks import StocksBuy, wallet


def upload_wallet(file_name):
    with open(file_name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        wallet.clear()
        print(f'Loading the wallet {file_name}...\nWait a seconds...\n')
        for buy in reader:

            stock_instance = StocksBuy(stock=buy[0], buyprice=float(buy[1]), qty=int(buy[2]),
                                       expense=float(buy[3]), tobin=buy[4])
            if stock_instance.tobin == 'False':
                stock_instance.tobin = False
            else:
                stock_instance.calcular_tobin()
            wallet.append(stock_instance)


def save_wallet(file_name):
    with open(f'{file_name}.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for buy in wallet:
            writer.writerow([buy.stock, buy.buyprice, buy.qty, buy.expense,
                             buy.tobin, buy.balance, buy.accountcharge])

    print('Wallet saved succesfully')
