from mysqlExt import MySql

objMysql = MySql()


class StockerDB(object):
    def __init__(self):
        self.objMysql = MySql()


    def get_dsz_symbol(self):
        sql = "select * from `baostock`.`300yi`"
        rows = self.objMysql.getRows(sql)

        return rows

    def __del__(self):
        del self.objMysql