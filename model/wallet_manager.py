import csv
# to do:
# Top level error para gestionar duplicados de cartera con el mismo nombre o hacer un
# wallet succesfully
# Aniadir funcion de upload_wallet

wallet = []

def upload_wallet(file):
    pass
    

def save_wallet(file_name):

    with open(f'{file_name}.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        for buy in wallet:
            writer.writerow([buy.index, buy.stock, buy.qty, buy.expense,
                              buy.tobin, buy.balance, buy.accountcharge])
            

    print('Wallet saved succesfully')




