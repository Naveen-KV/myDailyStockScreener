


def calculate_ema(prices, days, smoothing=2):
    ema = [sum(prices[:days]) / days]
    for price in prices[days:]:
        ema.append((price * (smoothing / (1 + days))) + ema[-1] * (1 - (smoothing / (1 + days))))
    return ema

def Find_Ema(complete_data, stock_trend, stockcodes, ema_select):

    stock_trend["ema13"] = 0
    stock_trend["ema21"] = 0
    stock_trend["ema51"] = 0




    for i in range(0, len(stockcodes)):
        try:
            ema_51 = calculate_ema(complete_data[stockcodes[i]].iloc[:, 5], 51)
            stock_trend.iloc[i, -1] = round(ema_51[-1], 2)
            ema_21 = calculate_ema(complete_data[stockcodes[i]].iloc[:, 5], 21)
            stock_trend.iloc[i, -2] = round(ema_21[-1], 2)
            ema_13 = calculate_ema(complete_data[stockcodes[i]].iloc[:, 5], 13)
            stock_trend.iloc[i, -3] = round(ema_13[-1], 2)
        except:
            pass

    ema21_list = stock_trend.copy()


    if ema_select == 51:
        ema21_list = stock_trend[(stock_trend["Price"] > stock_trend["ema13"]) & (stock_trend["Price"] > stock_trend["ema21"])]
    elif ema_select == 13:
        ema21_list = stock_trend[stock_trend["Price"] > stock_trend["ema13"]]
    elif ema_select == 21:
        ema21_list = stock_trend[(stock_trend["Price"] > stock_trend["ema21"])]
    else:
        pass

    cols = ["VOL X", "Price", "% Change", "52W_HIGH", "sma30", "sma50", "sma100", "ema13", "ema21", "ema51"]
    my_stock_list_21ema = ema21_list.drop(columns = cols, axis = 1)

    return my_stock_list_21ema
