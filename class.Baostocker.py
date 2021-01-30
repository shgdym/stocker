import baostock as bs
import pandas as pd

def getKData(code, startdate, enddate):

    rs = bs.query_history_k_data(code,
                                 "date,code,high,close,low,tradeStatus",
                                 start_date=startdate, end_date=enddate,
                                 frequency="d", adjustflag="3")
    result_list = []

    while (rs.error_code == '0') & rs.next():
        result_list.append(rs.get_row_data())
        df_init = pd.DataFrame(result_list, columns=rs.fields)

        df_status = df_init[df_init['tradeStatus'] == '1']
        low = df_status['low'].astype(float)
        del df_status['low']
        df_status.insert(0, 'low', low)
        high = df_status['high'].astype(float)
        del df_status['high']
        df_status.insert(0, 'high', high)
        close = df_status['close'].astype(float)
        del df_status['close']
        df_status.insert(0, 'close', close)

    df_data = pd.DataFrame()
    df_data['date'] = df_status['date'].values
    df_data.index = df_status['date'].values
    df_data.index.name = 'date'

    # # 删除空数据
    # df_data = df_data.dropna()
    # # 计算KDJ指标金叉、死叉情况
    # df_data['x'] = ''
    #
    # kdj_position = df_data['K'] > df_data['D']
    #
    # df_data.loc[kdj_position[(kdj_position == True) & (kdj_position.shift() == False)].index, 'x'] = 'j'
    # df_data.loc[kdj_position[(kdj_position == False) &(kdj_position.shift() == True)].index, 'x'] = 's'

    return (df_data)