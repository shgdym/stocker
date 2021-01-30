from mysqlExt import MySql

objMysql = MySql()


class StockerDB(object):
    def __init__(self):
        self.objMysql = MySql()


    def get_dsz_symbol(self):
        sql = "select * from `baostock`.`300yi`"
        rows = self.objMysql.getRows(sql)

        return rows

    def update_k_data(self, stocker_symbol, json_data):
        sql = "update `baostock`.`300yi` set k_data='{}' where symbol = '{}' limit 1".format(json_data, stocker_symbol)
        objMysql.query(sql)

    def __del__(self):
        del self.objMysql