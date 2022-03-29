import yfinance as yf
import numpy as np
import datetime
import re
from itertools import combinations
import matplotlib.pyplot as plt

tik_f = open('tiker.txt')
tickers = list((tik_f.readline().split()))

shares_data = dict()
sharesOutstanding_data = dict()

startDate = datetime.datetime(2017, 1, 1)
endDate = datetime.datetime(2019, 12, 1)

temp_dates = yf.Ticker(tickers[0]).history(start=startDate, end=endDate, interval='3mo').index.values
dates = []
for elem in temp_dates:
    dates.append(re.findall(r'[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]', str(elem))[0])
print(dates)

for tiker in tickers:
    shares_data[tiker] = yf.Ticker(tickers[0]).history(start=startDate, end=endDate, interval='1mo')


def get_mat_cap(tiker, data):
    shares_price = data[tiker][0]
    sharesOutstanding = sharesOutstanding_data[tiker]
    return shares_price * sharesOutstanding


def get_corrcoef(ar1):
    return np.corrcoef(ar1)[0][1]


def get_data(startDate, endDate):
    startDate = startDate
    endDate = endDate
    shares_data_t = dict()
    for tiker in tickers:
        data = yf.Ticker(tiker)
        shares_data_t[tiker] = list(data.history(start=startDate, end=endDate, interval='1d')['Close'])
    return shares_data_t


def get_shares_price(shares_data, date):
    return shares_data['Close'][date]


def get_positive_trend_company(data):
    temp = []
    for ticker in tickers:
        if data[ticker][0] <= data[ticker][-1]:
            temp.append(ticker)
    return temp


def calculate_correlation_3comany(com_combin, data):
    temp = dict()
    for i in com_combin:
        ar1 = data[i[0]][:min(len(data[i[0]]), len(data[i[1]]), len(data[i[2]])) - 1]
        ar2 = data[i[1]][:min(len(data[i[0]]), len(data[i[1]]), len(data[i[2]])) - 1]
        ar3 = data[i[2]][:min(len(data[i[0]]), len(data[i[1]]), len(data[i[2]])) - 1]

        temp[i] = get_corrcoef([ar1, ar2, ar3])
    return temp


print(len(get_data(dates[0], dates[1])['GAZP.ME']))
start = 10 * 10 ** 6
tol = [start]
bor = [start]
Zhe = [start]

com_combin = combinations(tickers, 3)


def calculate_tol(com, data, its_first=False):
    global tol
    company = min(com, key=com.get)
    if data[company[0]][0] and data[company[1]][0] and data[company[2]][0]:
        if its_first:
            com_1 = (tol[0] / 3) // data[company[0]][0]
            com_2 = (tol[0] / 3) // data[company[1]][0]
            com_3 = (tol[0] / 3) // data[company[2]][0]
            ost = tol[0] - (com_1 * data[company[0]][0] + com_2 * data[company[1]][0] + com_3 * data[company[2]][0])
            stock = (com_1 * data[company[0]][0] + com_2 * data[company[1]][0] + com_3 * data[company[2]][0]) + ost
            tol = [ost, [company[0], com_1], [company[1], com_2], [company[2], com_3], stock]
        else:
            profit = data[tol[1][0]][-1] * tol[1][1] + data[tol[2][0]][-1] * tol[2][1] + data[tol[3][0]][-1] * tol[3][1]
            tol[0] += profit
            com_1 = (tol[0] / 3) // data[company[0]][0]
            com_2 = (tol[0] / 3) // data[company[1]][0]
            com_3 = (tol[0] / 3) // data[company[2]][0]
            ost = tol[0] - (com_1 * data[company[0]][0] + com_2 * data[company[1]][0] + com_3 * data[company[2]][0])
            print('Data = ', com_1, com_2, com_3, data[company[0]][0])
            stock = (com_1 * data[company[0]][0] + com_2 * data[company[1]][0] + com_3 * data[company[2]][0]) + ost
            tol = [ost, [company[0], com_1], [company[1], com_2], [company[2], com_3], stock]


def calculate_bor(com, data, its_first=False):
    global bor
    company = max(com, key=com.get)
    if data[company[0]][0] and data[company[1]][0] and data[company[2]][0]:

        if its_first:
            com_1 = (bor[0] / 3) // data[company[0]][0]
            com_2 = (bor[0] / 3) // data[company[1]][0]
            com_3 = (bor[0] / 3) // data[company[2]][0]
            ost = bor[0] - (com_1 * data[company[0]][0] + com_2 * data[company[1]][0] + com_3 * data[company[2]][0])
            stock = (com_1 * data[company[0]][0] + com_2 * data[company[1]][0] + com_3 * data[company[2]][0]) + ost
            bor = [ost, [company[0], com_1], [company[1], com_2], [company[2], com_3], stock]
        else:
            profit = data[bor[1][0]][-1] * bor[1][1] + data[bor[2][0]][-1] * bor[2][1] + data[bor[3][0]][-1] * bor[3][1]
            bor[0] += profit

            com_1 = (bor[0] / 3) // data[company[0]][0]
            com_2 = (bor[0] / 3) // data[company[1]][0]
            com_3 = (bor[0] / 3) // data[company[2]][0]
            ost = bor[0] - (com_1 * data[company[0]][0] + com_2 * data[company[1]][0] + com_3 * data[company[2]][0])
            stock = (com_1 * data[company[0]][0] + com_2 * data[company[1]][0] + com_3 * data[company[2]][0]) + ost
            bor = [ost, [company[0], com_1], [company[1], com_2], [company[2], com_3], stock]


def calculate_Zhe(data, its_first=False):
    global Zhe
    if its_first and np.nan not in data:
        full_cap = 0
        for tiker in tickers:
            full_cap += get_mat_cap(tiker, data)
        volume_in_full = dict()
        for tiker in tickers:
            volume_in_full[tiker] = get_mat_cap(tiker, data) / full_cap

        volume_buy_share = dict()
        for tiker in tickers:
            volume_buy_share[tiker] = (volume_in_full[tiker] * Zhe[0]) // data[tiker][0]

        temp = 0
        for elem in volume_buy_share:
            temp += volume_buy_share[elem] * data[elem][0]
        ost = Zhe[0] - temp
        Zhe = [Zhe[0], volume_buy_share, temp]
    elif np.nan not in data:
        temp = 0
        for elem in Zhe[1]:
            temp += Zhe[1][elem] * data[elem][0]
        Zhe[0] += temp

        full_cap = 0
        for tiker in tickers:
            full_cap += get_mat_cap(tiker, data)
        volume_in_full = dict()
        for tiker in tickers:
            volume_in_full[tiker] = get_mat_cap(tiker, data) / full_cap

        volume_buy_share = dict()
        for tiker in tickers:
            volume_buy_share[tiker] = (volume_in_full[tiker] * Zhe[0]) // data[tiker][0]

        temp = 0
        for elem in volume_buy_share:
            temp += volume_buy_share[elem] * data[elem][0]
        ost = Zhe[0] - temp
        Zhe = [ost, volume_buy_share, temp]


chart_data = dict()
chart_data["Anatoly"] = []
chart_data["Boris"] = []
chart_data["Evgeny"] = []
chart_data["Date"] = []
for i in range(len(dates) - 1):
    cur_data = get_data(dates[i], dates[i + 1])
    positive_trend_company = get_positive_trend_company(cur_data)
    com_combin = list(combinations(positive_trend_company, 3))

    com_coref = calculate_correlation_3comany(com_combin, cur_data)
    if i == 0:
        calculate_tol(com_coref, cur_data, its_first=True)
        calculate_bor(com_coref, cur_data, its_first=True)
        calculate_Zhe(cur_data, its_first=True)
    else:
        calculate_tol(com_coref, cur_data)
        calculate_bor(com_coref, cur_data)
        calculate_Zhe(cur_data)
    chart_data["Anatoly"].append(tol[-1])
    chart_data["Boris"].append(bor[-1])
    chart_data["Evgeny"].append(Zhe[-1])
    chart_data["Date"].append(dates[i])

fig, ax = plt.subplots(figsize=(12, 7))
ax.set_title("Рост портфеля")
ax.set_ylabel("Стоимость портфеля")
ax.set_xlabel("Дата")

ax.plot(chart_data["Date"], chart_data["Anatoly"], label='Anatoly')
ax.plot(chart_data["Date"], chart_data["Boris"], label='Boris')
ax.plot(chart_data["Date"], chart_data["Evgeny"], label='Evgeny')

legend = ax.legend(loc='best', shadow=True, fontsize='x-large')

plt.show()