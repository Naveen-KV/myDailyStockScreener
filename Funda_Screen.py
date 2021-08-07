
from bs4 import BeautifulSoup
import requests

def fun_analysis(rpi):
    rpi.insert(loc=1, column='quarter_opm', value="0")
    rpi.insert(loc=2, column='quarter_opm_change', value="0")
    rpi.insert(loc=3, column='year_opm', value="0")
    rpi.insert(loc=4, column='year_opm_change', value="0")
    rpi.insert(loc=5, column='ROCE', value="0")
    rpi.insert(loc=6, column='ROE', value="0")
    rpi.insert(loc=7, column='PROMOTER HOLDING %', value="0")
    rpi.insert(loc=8, column='PROMOTER HOLDING change %', value="0")
    rpi.insert(loc=9, column='SALES_10YR GROWTH %', value="0")
    rpi.insert(loc=10, column='SALES_5YR GROWTH %', value="0")
    rpi.insert(loc=11, column='SALES_3YR GROWTH %', value="0")
    rpi.insert(loc=12, column='SALES_TTM GROWTH %', value="0")
    rpi.insert(loc=13, column='PROFIT_10YR GROWTH %', value="0")
    rpi.insert(loc=14, column='PROFIT_5YR GROWTH %', value="0")
    rpi.insert(loc=15, column='PROFIT_3YR GROWTH %', value="0")
    rpi.insert(loc=16, column='TTM PROFIT GROWTH %', value="0")
    rpi.insert(loc=17, column='BORROWINGS', value="0")
    rpi.insert(loc=18, column='BORROWINGS (prev)', value="0")
    rpi.insert(loc=19, column='FIXED ASSETS', value="0")
    rpi.insert(loc=20, column='FIXED ASSETS (prev)', value="0")

    my_stock_list = rpi.iloc[:, 0]

    for i in range(0, len(my_stock_list)):
        inv_url = 'https://www.screener.in/company/' + rpi.iloc[i, 0] + '/consolidated/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}  # This is chrome, you can set whatever browser you like
        response = requests.get(inv_url, headers=headers).text
        soup = BeautifulSoup(response)
        # tables = pd.read_html(requests.get(inv_url, headers=headers).text)
        roce = soup.findAll("table")[8].findAll("tr")[1]
        checkn = roce.findAll('td')[-1].text.strip()
        #print(checkn)
        if (checkn == "ROCE %"):
            url_stand = 'https://www.screener.in/company/' + rpi.iloc[i, 0] + '/'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}  # This is chrome, you can set whatever browser you like
            response_stand = requests.get(url_stand, headers=headers).text
            soup_stand = BeautifulSoup(response_stand)
            # tables_stand = pd.read_html(requests.get(url_stand, headers=headers).text)
            #print(rpi.iloc[i, 0])
            #print(':\n')
            #print(url_stand)

            # OPM_QUARTER
            try:
                opm_q = soup_stand.findAll("table")[0].findAll("tr")[4]
                rpi.iloc[i, 1] = opm_q.findAll('td')[-1].text
            except:
                rpi.iloc[i, 1] = 0

            # OPM_QUARTER_CHANGE
            try:
                opm_q_c = soup_stand.findAll("table")[0].findAll("tr")[4]
                rpi.iloc[i, 2] = opm_q_c.findAll('td')[-2].text
            except:
                rpi.iloc[i, 2] = 0

            # OPM_SALES
            try:
                opm_s = soup_stand.findAll("table")[1].findAll("tr")[4]
                rpi.iloc[i, 3] = opm_s.findAll('td')[-1].text
            except:
                rpi.iloc[i, 3] = 0

            # OPM_SALES_CHANGE
            try:
                opm_s_c = soup_stand.findAll("table")[1].findAll("tr")[4]
                rpi.iloc[i, 4] = opm_s_c.findAll('td')[-2].text
            except:
                rpi.iloc[i, 4] = 0

            # ROCE
            try:
                roce = soup_stand.findAll("table")[8].findAll("tr")[1]
                rpi.iloc[i, 5] = roce.findAll('td')[-1].text
            except:
                rpi.iloc[i, 5] = 0

            # ROE
            try:
                roe = soup_stand.findAll("table")[5].findAll("tr")[4]
                rpi.iloc[i, 6] = roe.findAll('td')[-1].text
            except:
                rpi.iloc[i, 6] = 0

            # PROMOTER SKIN IN THE GAME
            try:
                prom_share = soup_stand.findAll("table")[9].findAll("tr")[1]
                promon = prom_share.findAll('td')[-1].text
                prom_n = float(promon)
                promoy = prom_share.findAll('td')[-2].text
                prom_y = float(promoy)
                rpi.iloc[i, 7] = promon
                rpi.iloc[i, 8] = prom_n - prom_y
            except:
                rpi.iloc[i, 7] = 0
                rpi.iloc[i, 8] = 0

            # SALES GROWTH
            try:
                sales_10yr = soup_stand.findAll("table")[2].findAll("tr")[1]
                rpi.iloc[i, 9] = sales_10yr.findAll('td')[1].text
                sales_5yr = soup_stand.findAll("table")[2].findAll("tr")[2]
                rpi.iloc[i, 10] = sales_5yr.findAll('td')[1].text
                sales_3yr = soup_stand.findAll("table")[2].findAll("tr")[3]
                rpi.iloc[i, 11] = sales_3yr.findAll('td')[1].text
                sales_ttm = soup_stand.findAll("table")[2].findAll("tr")[4]
                rpi.iloc[i, 12] = sales_ttm.findAll('td')[1].text
            except:
                rpi.iloc[i, 9] = 0
                rpi.iloc[i, 10] = 0
                rpi.iloc[i, 11] = 0
                rpi.iloc[i, 12] = 0

            # PROFIT GROWTH
            try:
                pro_10yr = soup_stand.findAll("table")[3].findAll("tr")[1]
                rpi.iloc[i, 13] = pro_10yr.findAll('td')[1].text
                pro_5yr = soup_stand.findAll("table")[3].findAll("tr")[2]
                rpi.iloc[i, 14] = pro_5yr.findAll('td')[1].text
                pro_3yr = soup_stand.findAll("table")[3].findAll("tr")[3]
                rpi.iloc[i, 15] = pro_3yr.findAll('td')[1].text
                pro_ttm = soup_stand.findAll("table")[3].findAll("tr")[4]
                rpi.iloc[i, 16] = pro_ttm.findAll('td')[1].text
            except:
                rpi.iloc[i, 13] = 0
                rpi.iloc[i, 14] = 0
                rpi.iloc[i, 15] = 0
                rpi.iloc[i, 16] = 0

            # DEBT REDUCTION
            # soup = BeautifulSoup(response_consol)
            try:
                borro = soup_stand.findAll("table")[6].findAll("tr")[3]
                rpi.iloc[i, 17] = borro.findAll('td')[-1].text
                rpi.iloc[i, 18] = borro.findAll('td')[-2].text
            except:
                rpi.iloc[i, 17] = 0
                rpi.iloc[i, 18] = 0

            # CAPEX
            try:
                fac = soup_stand.findAll("table")[6].findAll("tr")[6]
                rpi.iloc[i, 19] = fac.findAll('td')[-1].text
                rpi.iloc[i, 20] = fac.findAll('td')[-2].text
            except:
                rpi.iloc[i, 19] = 0
                rpi.iloc[i, 20] = 0

            #print(rpi.iloc[i, 0])
        else:
            url_consol = 'https://www.screener.in/company/' + rpi.iloc[i, 0] + '/consolidated/'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}  # This is chrome, you can set whatever browser you like
            response_consol = requests.get(url_consol, headers=headers).text
            soup_consol = BeautifulSoup(response_consol)
            # tables_consol = pd.read_html(requests.get(url_consol, headers=headers).text)
            #print(rpi.iloc[i, 0])
            #print(':\n')
            #print(url_consol)

            # OPM_QUARTER
            try:
                opm_q = soup_consol.findAll("table")[0].findAll("tr")[4]
                rpi.iloc[i, 1] = opm_q.findAll('td')[-1].text
            except:
                rpi.iloc[i, 1] = 0

            # OPM_QUARTER_CHANGE
            try:
                opm_q_c = soup_consol.findAll("table")[0].findAll("tr")[4]
                rpi.iloc[i, 2] = opm_q_c.findAll('td')[-2].text
            except:
                rpi.iloc[i, 2] = 0

            # OPM_SALES
            try:
                opm_s = soup_consol.findAll("table")[1].findAll("tr")[4]
                rpi.iloc[i, 3] = opm_s.findAll('td')[-1].text
            except:
                rpi.iloc[i, 3] = 0

            # OPM_SALES_CHANGE
            try:
                opm_s_c = soup_consol.findAll("table")[1].findAll("tr")[4]
                rpi.iloc[i, 4] = opm_s_c.findAll('td')[-2].text
            except:
                rpi.iloc[i, 4] = 0

            # ROCE
            try:
                roce = soup_consol.findAll("table")[8].findAll("tr")[1]
                rpi.iloc[i, 5] = roce.findAll('td')[-1].text
            except:
                rpi.iloc[i, 5] = 0

            # ROE
            try:
                roe = soup_consol.findAll("table")[5].findAll("tr")[4]
                rpi.iloc[i, 6] = roe.findAll('td')[-1].text
            except:
                rpi.iloc[i, 6] = 0

            # PROMOTER SKIN IN THE GAME
            try:
                prom_share = soup_consol.findAll("table")[9].findAll("tr")[1]
                promon = prom_share.findAll('td')[-1].text
                prom_n = float(promon)
                promoy = prom_share.findAll('td')[-2].text
                prom_y = float(promoy)
                rpi.iloc[i, 7] = promon
                rpi.iloc[i, 8] = prom_n - prom_y
            except:
                rpi.iloc[i, 7] = 0
                rpi.iloc[i, 8] = 0

            # SALES GROWTH
            try:
                sales_10yr = soup_consol.findAll("table")[2].findAll("tr")[1]
                rpi.iloc[i, 9] = sales_10yr.findAll('td')[1].text
                sales_5yr = soup_consol.findAll("table")[2].findAll("tr")[2]
                rpi.iloc[i, 10] = sales_5yr.findAll('td')[1].text
                sales_3yr = soup_consol.findAll("table")[2].findAll("tr")[3]
                rpi.iloc[i, 11] = sales_3yr.findAll('td')[1].text
                sales_ttm = soup_consol.findAll("table")[2].findAll("tr")[4]
                rpi.iloc[i, 12] = sales_ttm.findAll('td')[1].text
            except:
                rpi.iloc[i, 9] = 0
                rpi.iloc[i, 10] = 0
                rpi.iloc[i, 11] = 0
                rpi.iloc[i, 12] = 0

            # PROFIT GROWTH
            try:
                pro_10yr = soup_consol.findAll("table")[3].findAll("tr")[1]
                rpi.iloc[i, 13] = pro_10yr.findAll('td')[1].text
                pro_5yr = soup_consol.findAll("table")[3].findAll("tr")[2]
                rpi.iloc[i, 14] = pro_5yr.findAll('td')[1].text
                pro_3yr = soup_consol.findAll("table")[3].findAll("tr")[3]
                rpi.iloc[i, 15] = pro_3yr.findAll('td')[1].text
                pro_ttm = soup_consol.findAll("table")[3].findAll("tr")[4]
                rpi.iloc[i, 16] = pro_ttm.findAll('td')[1].text
            except:
                rpi.iloc[i, 13] = 0
                rpi.iloc[i, 14] = 0
                rpi.iloc[i, 15] = 0
                rpi.iloc[i, 16] = 0

            # DEBT REDUCTION
            # soup = BeautifulSoup(response_consol)
            try:
                borro = soup_consol.findAll("table")[6].findAll("tr")[3]
                rpi.iloc[i, 17] = borro.findAll('td')[-1].text
                rpi.iloc[i, 18] = borro.findAll('td')[-2].text
            except:
                rpi.iloc[i, 17] = 0
                rpi.iloc[i, 18] = 0

            # CAPEX
            try:
                fac = soup_consol.findAll("table")[6].findAll("tr")[6]
                rpi.iloc[i, 19] = fac.findAll('td')[-1].text
                rpi.iloc[i, 20] = fac.findAll('td')[-2].text
            except:
                rpi.iloc[i, 19] = 0
                rpi.iloc[i, 20] = 0

            #print(rpi.iloc[i, 0])

    return rpi

def final_screen(rpi, qopm_val, yopm_val, promc_val, borrow_val, fassets_val, prom_val):
    check_list = rpi.copy()
    rpi.drop(columns = ["quarter_opm_change", "year_opm_change", "ROCE", "ROE", "SALES_10YR GROWTH %","SALES_5YR GROWTH %", "SALES_3YR GROWTH %", "SALES_TTM GROWTH %"], axis = 1, inplace = True)
    rpi.drop(columns =["PROFIT_10YR GROWTH %", "PROFIT_5YR GROWTH %", "PROFIT_3YR GROWTH %", "TTM PROFIT GROWTH %", "BORROWINGS (prev)", "FIXED ASSETS (prev)"], axis=1, inplace=True)
    if qopm_val == 0:
        rpi.drop(columns = ["quarter_opm"], axis = 1, inplace= True)
    if yopm_val == 0:
        rpi.drop(columns=["year_opm"], axis=1, inplace=True)
    if promc_val == 0:
        rpi.drop(columns=["PROMOTER HOLDING change %"], axis=1, inplace=True)
    if borrow_val == 0:
        rpi.drop(columns=["BORROWINGS"], axis=1, inplace=True)
    if fassets_val == 0:
        rpi.drop(columns=["FIXED ASSETS"], axis=1, inplace=True)
    if prom_val == 0:
        rpi.drop(columns=["PROMOTER HOLDING %"], axis=1, inplace=True)
    return rpi
