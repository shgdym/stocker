import baostock as bs
import pandas as pd

# login
lg = bs.login()
# show login info
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

# get base info
rs = bs.query_stock_basic(code="sh.600000")
# rs = bs.query_stock_basic(code_name="浦发银行")
print('query_stock_basic respond error_code:'+rs.error_code)
print('query_stock_basic respond  error_msg:'+rs.error_msg)

# print result
data_list = []
while (rs.error_code == '0') & rs.next():

    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)

print(result)

# logout
bs.logout()