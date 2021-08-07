import pandas as pd
from datetime import datetime, timedelta
import requests
from io import StringIO

def get_adx(high, low, close, lookback):
    plus_dm = high.diff()
    minus_dm = low.diff()
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm > 0] = 0

    tr1 = pd.DataFrame(high - low)
    tr2 = pd.DataFrame(abs(high - close.shift(1)))
    tr3 = pd.DataFrame(abs(low - close.shift(1)))
    frames = [tr1, tr2, tr3]
    tr = pd.concat(frames, axis=1, join='inner').max(axis=1)
    atr = tr.rolling(lookback).mean()

    plus_di = 100 * (plus_dm.ewm(alpha=1 / lookback).mean() / atr)
    minus_di = abs(100 * (minus_dm.ewm(alpha=1 / lookback).mean() / atr))
    dx = (abs(plus_di - minus_di) / abs(plus_di + minus_di)) * 100
    adx = ((dx.shift(1) * (lookback - 1)) + dx) / lookback
    adx_smooth = adx.ewm(alpha=1 / lookback).mean()
    return plus_di, minus_di, adx_smooth


def Find_ADX(my_stock_list, adx):

    my_stock_list["adx"] = 0
    stockcodes_adx = my_stock_list.iloc[:, 0].values

    N = 1000  # No. of days for historical price data

    end_date = str(int(datetime.now().timestamp()))
    date_N_days_ago = datetime.now() - timedelta(days=N)
    start_date = str(int(date_N_days_ago.timestamp()))

    # Select time frame

    # interval = '1d'
    interval = '1wk'
    # interval = '1mo'

    events = 'history'
    # events = 'div'
    # events = 'split'

    for i in range(0, len(stockcodes_adx)):
        #print(stockcodes_adx[i])
        url_adx = 'https://query1.finance.yahoo.com/v7/finance/download/' + stockcodes_adx[i] + '.NS?period1=' + start_date + '&period2=' + end_date + '&interval=' + interval + '&events=' + events
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        r = requests.get(url_adx, headers = headers )

        if r.ok:
            try:

                data = r.content.decode('utf8')
                pricol_y = pd.read_csv(StringIO(data))
                pricol_y.dropna(axis=0, how="any", inplace=True)
                pricol_y.drop("Adj Close", axis=1, inplace=True)
                aapl = pricol_y.copy()
                aapl['plus_di'] = pd.DataFrame(get_adx(aapl['High'], aapl['Low'], aapl['Close'], 14)[0]).rename(columns={0: 'plus_di'})
                aapl['minus_di'] = pd.DataFrame(get_adx(aapl['High'], aapl['Low'], aapl['Close'], 14)[1]).rename(columns={0: 'minus_di'})
                aapl['adx'] = pd.DataFrame(get_adx(aapl['High'], aapl['Low'], aapl['Close'], 14)[2]).rename(columns={0: 'adx'})
                aapl = aapl.dropna()
                #aapl.tail()

                my_stock_list.iloc[i, -1] = round(aapl.iloc[-1, -1], 2)
                #print(my_stock_list.iloc[i, -1])
            except:

                my_stock_list.iloc[i, -1] = 0

    check_list = my_stock_list[my_stock_list["adx"] > adx]
    cols = ["adx"]
    check_list.drop(columns = cols, axis = 1, inplace = True)
    return check_list