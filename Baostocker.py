import baostock as bs
import pandas as pd


class Baostocker:
    def __init__(self):
        self.login()

    @staticmethod
    def login():
        lg = bs.login()
        print('login respond error_code:' + lg.error_code)
        print('login respond  error_msg:' + lg.error_msg)

    @staticmethod
    def getKData(code, startdate, enddate):
        rs = bs.query_history_k_data(code,
                                     "date,code,high,close,low,tradeStatus",
                                     start_date=startdate, end_date=enddate,
                                     frequency="d", adjustflag="3")
        result_list = []
        while (rs.error_code == '0') & rs.next():
            result_list.append(rs.get_row_data())

        return result_list
