from StockerDB import StockerDB
from Baostocker import Baostocker
from win10toast import ToastNotifier
import _thread as thread
import datetime
import json

toaster = ToastNotifier()
objBaostocker = Baostocker()
objStockerDB = StockerDB()


def win_toast(toast_title, toast_content):
    toaster.show_toast(toast_title,
                       toast_content,
                       duration=7200)

def run_export(toast_content):
    print(toast_content)
# thread.start_new_thread(win_toast, ("Thread-1", "Thread-1", ))
# thread.start_new_thread(run_export, ("Thread-1", ))

stockerList = objStockerDB.get_dsz_symbol()

today = datetime.date.today()
start_date = today - datetime.timedelta(days=20)

for stockerInfo in stockerList:
    stocke_symbol = stockerInfo[0]
    stocke_name = stockerInfo[1]
    stocke_price = stockerInfo[2]

    stocke_code = stocke_symbol.replace('SH', 'sh.')
    stocke_code = stocke_code.replace('SZ', 'sz.')

    k_data = objBaostocker.getKData(stocke_code, str(start_date), str(today))
    k_dict = {}
    for item in k_data:
        k_dict[item[0]] = item
    json_str = json.dumps(k_dict)

    objStockerDB.update_k_data(stocke_symbol, json_str)

print("update k data success! ")



