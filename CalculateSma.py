

def Find_Sma(complete_data, stock_trend, stockcodes):
    """ Finding Moving Averages """
    ma_30 = 30
    ma_50 = 50
    ma_100 = 100
    sma30 = "Sma" + str(ma_30)
    sma50 = "Sma" + str(ma_50)
    sma100 = "Sma" + str(ma_100)

    for i in range(0, len(stockcodes)):
        try:

            complete_data[stockcodes[i]][sma30] = complete_data[stockcodes[i]].iloc[:, 4].rolling(window=ma_30).mean()
            complete_data[stockcodes[i]][sma50] = complete_data[stockcodes[i]].iloc[:, 4].rolling(window=ma_50).mean()
            complete_data[stockcodes[i]][sma100] = complete_data[stockcodes[i]].iloc[:, 4].rolling(window=ma_100).mean()
        except:
            pass

    stock_trend.insert(loc=5, column='sma30', value='0')
    stock_trend.insert(loc=6, column='sma50', value='0')
    stock_trend.insert(loc=7, column='sma100', value='0')

    for i in range(0, len(stockcodes)):
        try:
            stock_trend.iloc[i, -3] = round(complete_data[stockcodes[i]].iloc[-1, -3], 2)
            stock_trend.iloc[i, -2] = round(complete_data[stockcodes[i]].iloc[-1, -2], 2)
            stock_trend.iloc[i, -1] = round(complete_data[stockcodes[i]].iloc[-1, -1], 2)
        except:
            pass

    return stock_trend