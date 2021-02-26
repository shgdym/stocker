import baostock as bs
import pandas as pd


class Baostocker:
    def __init__(self):
        self.login()

    def login(self):
        lg = bs.login()

    @staticmethod
    def getKData(code, startdate, enddate):
        rs = bs.query_history_k_data(code,
                                     "date,code,high,close,low,tradeStatus,pctChg,open",
                                     start_date=startdate, end_date=enddate,
                                     frequency="d", adjustflag="3")
        return rs
