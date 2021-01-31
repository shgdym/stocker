from StockerDB import StockerDB
from Baostocker import Baostocker
from win10toast import ToastNotifier
import pandas as pd
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
start_date = today - datetime.timedelta(days=25)
date_range = -4
for stockerInfo in stockerList:
    stocke_symbol = stockerInfo[0]
    stocke_name = stockerInfo[1]
    stocke_price = stockerInfo[2]

    stocke_code = stocke_symbol.replace('SH', 'sh.')
    stocke_code = stocke_code.replace('SZ', 'sz.')

    rs = objBaostocker.getKData(stocke_code, str(start_date), str(today))

    result_list = []
    while (rs.error_code == '0') & rs.next():
        row_data = rs.get_row_data()
        # 剔除停牌
        if row_data[5] == '0':
            continue
        result_list.append(row_data)

    if len(result_list) == 0:
        continue

    fc_list = result_list[date_range::]
    df_init = pd.DataFrame(result_list, columns=rs.fields)

    y_hight = 0
    b_match = True
    for i in range(len(fc_list)):
        t_hight = fc_list[i][2]
        if y_hight != 0 and t_hight > y_hight:
            b_match = False
            break

        y_hight = t_hight
    if not b_match:
        continue

    # 个头差不多 小阴小阳 -2.782000 0.837100
    y_pctChg = float(result_list[-2][6])
    t_pctChg = float(result_list[-1][6])
    if y_pctChg > 0.0 or y_pctChg > 5.0:
        continue
    if t_pctChg < 0.0 or y_pctChg > 5.0:
        continue

    if abs(abs(t_pctChg) - abs(y_pctChg)) > 1.5:
        continue
    print(fc_list[0][1])






    # print(df_init)
    # exit()
    #
    # k_dict = {}
    # for item in k_data:
    #     k_dict[item[0]] = item
    # json_str = json.dumps(k_dict)
    #
    # objStockerDB.update_k_data(stocke_symbol, json_str)

print("update k data success! ")



