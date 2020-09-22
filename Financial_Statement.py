# import plot package
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
params = {'legend.fontsize': 'x-large',
          'figure.figsize': (7.5, 7),
          'axes.labelsize': 'x-large',
          'axes.titlesize':'x-large',
          'xtick.labelsize':'x-large',
          'ytick.labelsize':'x-large'}
pylab.rcParams.update(params)
plt.rcParams.update({'font.size': 10})
# import numerical python library
import numpy as np
# import HTTP library
import requests
# import 表格 library
import pandas as pd


BalanceSheetURL = "https://mops.twse.com.tw/mops/web/ajax_t164sb03";  # 資產負債表
ProfitAndLoseURL = "https://mops.twse.com.tw/mops/web/ajax_t164sb04";  # 綜合損益表
CashFlowStatementURL = "https://mops.twse.com.tw/mops/web/ajax_t164sb05";  # 現金流量表
EquityStatementURL = "https://mops.twse.com.tw/mops/web/ajax_t164sb06"; # 權益變動表


def crawl_financial_report(url, stock_number, year, season):
    form_data = {
        'encodeURIComponent': 1,
        'step': 1,
        'firstin': 1,
        'off': 1,
        'co_id': stock_number,
        'year': year,
        'season': season,
    }

    r = requests.post(url, form_data)
    html_df = pd.read_html(r.text)[1].fillna("")
    return html_df


# 爬取目標網站
year = 108
season = 1
stock_number = 3056

# 結果
Data = crawl_financial_report(BalanceSheetURL, 3056, year, season)

print('(1): 所有資料')
print(Data)
# 直行橫列
print('(2): 第一列(row)')
print(Data.iloc[1])
print('(3): 第二列(row)')
print(Data.iloc[2])
print('(4): 第一列(row)且第一行(column)的元素（第一季結尾3/31的現金及約當現金的“金額”）')
print(Data.iloc[1, 1])
print('(5): 第一列(row)且第二行(column)的元素（第一季結尾3/31的現金及約當現金的“金額%數”）')
print(Data.iloc[1, 2])
print('(6): 第一列(row)且第一行(column)的元素（第一季結尾3/31的現金及約當現金的“金額”）')
print(Data.iloc[1][1])
print('(7): 行表頭（column header）')
print(Data.columns)
print('(8): 第一個行表頭（column header）')
print(Data.columns[0])
print('(9): 第二個行表頭（column header）')
print(Data.columns[1])
print('(10): 第三個行表頭（column header）')
print(Data.columns[2])
print('(11): 第二個行表頭且“第三層”')
print(Data.columns[1][2])

Date = []
Cash_and_equivalents = []

for yr in np.arange(102, 109, 1):
    tmp_Data = crawl_financial_report(BalanceSheetURL, 3056, yr, season)
    Date.append(tmp_Data.columns[1][2][0:3])
    Cash_and_equivalents.append(tmp_Data.iloc[1, 1])

print(Date)
print(Cash_and_equivalents)

plt.figure(1)
plt.plot(Date, Cash_and_equivalents, '-bo')
plt.xlabel('Year')
plt.ylabel('Cash and equivalents')
plt.grid()
plt.title('Stock: 3056')
plt.show()
