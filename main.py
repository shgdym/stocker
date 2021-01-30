from StockerDB import StockerDB
from Baostocker import Baostocker
from win10toast import ToastNotifier
import _thread as thread

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

for stockerInfo in stockerList:
    stocke_code = stockerInfo[0]
    stocke_name = stockerInfo[1]
    stocke_price = stockerInfo[2]

    stocke_code = stocke_code.replace('SH', 'sh.')
    stocke_code = stocke_code.replace('SZ', 'sz.')

    res = objBaostocker.getKData(stocke_code, '2021-01-03', '2021-01-10')
    print(res)
    exit()

