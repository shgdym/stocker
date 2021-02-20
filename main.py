from config import global_config
import datetime
import json
import json2csv
import pandas as pd

json2csv.updateList()

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
for stockerInfo in stockerList:
    if Flag:
        Flag = False
        continue
    print(stockerInfo)
    exit()
    stocke_symbol = stockerInfo[1]
    stocke_name = stockerInfo[3]
    stocke_price = stockerInfo[2]
    result_dict = json.loads(stockerInfo[4])

    result_list = []
    for (k, v) in result_dict.items():
        if v[5] == '0':
            continue
        result_list.append(v)
    if len(result_list) == 0:
        continue
    stocke_code = stocke_symbol.replace('SH', 'sh.')
    stocke_code = stocke_code.replace('SZ', 'sz.')

    fc_list = result_list[date_range::]
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
    stocke_code = stocke_code.replace('.', '')
    url = "http://image.sinajs.cn/newchart/daily/n/"+stocke_code+".gif"
    res_list.append(fc_list[0][1]+" "+result_list[-1][2]+" "+url)
if len(res_list) > 0:
    file = 'result.txt'
    file_handle = open(file, mode='w')
    for i in range(len(res_list)):
        file_handle.write(res_list[i]+'\n')
    file_handle.close()
