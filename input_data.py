
"""IMPORTING NECESSARY LIBRARIES"""

import pandas as pd
import numpy as np

from datetime import datetime, timedelta
import requests

from io import StringIO

from bs4 import BeautifulSoup



def Read_Data():

    """ read data from google sheet"""
    google_sheet_url = "https://docs.google.com/spreadsheets/d/1Lt9-MCpStCoqxnoVuCkqJ4OQRqhZ4nv0-XNIiC9J1zI/edit#gid=0"
    url_1 = google_sheet_url.replace( "edit#gid","export?format=csv&gid")
    stock_list = pd.read_csv(url_1)
    return stock_list


def Missing_Data(stock_list):

    """Delete rows with missing values"""
    stock_list.dropna(axis=0, how="any", inplace=True)
    return stock_list

def Price_Vol_Action(stock_list, price, pchange, volx):

    """Select Stocks with Price Volume Action"""
    today_list = stock_list[(stock_list["Price"] > price) & (stock_list["VOL X"] >= volx) & (stock_list["% Change"] > pchange)]
    return today_list


def Data_Selection(today_list):

    """Select only desired columns"""
    cols = ["SYMBOL", "VOL X", "Price", "% Change", "52W_HIGH"]
    stock_trend = today_list[cols]
    stockcodes = today_list.iloc[:, 0].values
    return stock_trend, stockcodes

def Get_Historical_Data(stockcodes):
    """ Get Historical price data"""
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

    complete_data = {}
    for i in range(0, len(stockcodes)):
        url = 'https://query1.finance.yahoo.com/v7/finance/download/' + stockcodes[i] + '.NS?period1=' + start_date + '&period2=' + end_date + '&interval=' + interval + '&events=' + events
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        r = requests.get(url, headers=headers)

        if r.ok:
            data = r.content.decode('utf8')
            complete_data[stockcodes[i]] = pd.read_csv(StringIO(data), skip_blank_lines=True)
            complete_data[stockcodes[i]].dropna(axis=0, how="any", inplace=True)

    return complete_data



    

    


    

    

    

    

   

    

    

