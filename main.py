from config import global_config
from Baostocker import Baostocker
import datetime
import json
import json2csv
import pandas as pd

Baostocker = Baostocker()
if global_config.getRaw('config', 'UPDATE_STOCKER') != "NO":
    day_Week = datetime.datetime.now().weekday()
    if day_Week == 1:
        json2csv.updateList()
else:
    json2csv.updateList()
pf = pd.read_csv('dsz.csv', header=None, sep=' ')

# TODO update k_data

stockerList = pf.values.tolist()
today = datetime.date.today()
start_date = today - datetime.timedelta(days=25)
date_range = -int(global_config.getRaw('config', 'DATE_RANGE'))
res_list = []

Flag = True
for stocker in stockerList:
    if Flag:
        Flag = False
        continue

    stockerBaseInfo = stocker[0].split(",")
    bao_code = stockerBaseInfo[1].replace('SH', 'sh.')
    bao_code = bao_code.replace('SZ', 'sz.')
    rs = Baostocker.getKData(bao_code, str(start_date), str(today))
    k_list = []
    while (rs.error_code == '0') & rs.next():
        row_data = rs.get_row_data()
        # 剔除停牌时的数据
        if row_data[5] == '0':
            continue
        k_list.append(row_data)

    stocke_symbol = stockerBaseInfo[1]
    stocke_name = stockerBaseInfo[3]
    stocke_price = stockerBaseInfo[2]
    # result_dict = json.loads(stockerInfo[4])

    result_list = []
    for v in k_list:
        if v[5] == '0':
            continue
        result_list.append(v)
    if len(result_list) == 0:
        continue

    stocker_code = stocke_symbol.replace('SH', 'sh.')
    stocker_code = stocker_code.replace('SZ', 'sz.')

    fc_list = result_list[date_range::]
    y_high = 0
    b_match = True
    for i in range(len(fc_list)):
        t_high = fc_list[i][2]
        if y_high != 0 and t_high > y_high:
            b_match = False
            break

        y_high = t_high
    if not b_match:
        continue
    # 个头差不多 小阴小阳 -2.782000 0.837100
    # 两日涨幅
    # y_pctChg = float(result_list[-2][6])
    # t_pctChg = float(result_list[-1][6])
    # # 涨幅差太多 continue
    # if abs(abs(t_pctChg) - abs(y_pctChg)) > 2.5:
    #     continue
    #
    # # 两日收盘价与开盘价差
    # y_stat = float(result_list[-2][3]) - float(result_list[-2][7])
    # t_stat = float(result_list[-1][3]) - float(result_list[-1][7])
    # # 收盘开盘价 差太多 continue
    # if y_stat > 0.0 or y_pctChg > 5.0:
    #     continue
    # if t_stat < 0.0 or t_pctChg > 5.0:
    #     continue
    #
    # # 两日最低价与最高价
    # y_low = float(result_list[-2][3])
    # t_low = float(result_list[-1][7])
    # y_high = float(result_list[-2][7])
    # t_high = float(result_list[-1][3])
    #
    # t_price = float(result_list[-1][3])
    #
    # high_diff = abs(t_high - y_high) / t_price
    # low_diff = abs(t_low - y_low) / t_price
    # #
    # if high_diff > 0.02 or low_diff > 0.02:
    #     continue

    y_low = float(result_list[-2][4])
    y_high = float(result_list[-2][2])
    y_open = float(result_list[-2][7])
    y_close = float(result_list[-2][3])
    y_diff = (y_open - y_close) / y_close
    y_pctChg = float(result_list[-2][6])

    t_pctChg = float(result_list[-1][6])
    t_low = float(result_list[-1][4])
    t_high = float(result_list[-1][2])
    t_open = float(result_list[-1][7])
    t_close = float(result_list[-1][3])
    t_diff = (t_close - t_open) / t_close

    high_diff = abs(t_high - y_high) / t_close

    low_diff = abs(t_low - y_low) / t_close

    y_stat = float(y_close) - float(y_open)
    t_stat = float(t_close) - float(t_open)

    if y_stat > 0.0 or t_stat < 0.0:
        continue

    # if t_diff < 0 or y_diff > 0:
    #     continue
    if abs(abs(t_pctChg) - abs(y_pctChg)) > 2:
        continue

    if abs(t_high - y_high) / t_close > 0.02:
        continue

    if abs(t_low - y_low) / t_close > 0.02:
        continue

    if abs(t_close - y_open) / t_close > 0.017:
        continue

    if high_diff > 0.02 or low_diff > 0.02:
        continue

    stocker_code = stocker_code.replace('.', '')

    url = "http://image.sinajs.cn/newchart/daily/n/" + stocker_code + ".gif"
    res_list.append(fc_list[0][1]+" "+result_list[-1][2]+" "+url)
    # print(y_stat)
    # print(t_stat)
    # print(abs(abs(t_pctChg) - abs(y_pctChg)))
    # print(abs(t_high - y_high) / t_close)
    # print(abs(t_low - y_low) / t_close)
    # print(high_diff)
    # print(low_diff)
    # print(res_list)
    # exit()
print(res_list)
exit()
if len(res_list) > 0:
    file = 'result.txt'
    file_handle = open(file, mode='w')
    for i in range(len(res_list)):
        file_handle.write(res_list[i]+'\n')
    file_handle.close()
