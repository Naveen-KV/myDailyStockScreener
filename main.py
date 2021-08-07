# THIS IS THE ENTRY POINT OF THE CODE


from flask import Flask, render_template, request

import os

from input_data import Read_Data, Missing_Data, Price_Vol_Action, Data_Selection, Get_Historical_Data
from CalculateSma import Find_Sma
from CalculateEma import Find_Ema
from CalculateADX import Find_ADX
from Funda_Screen import fun_analysis, final_screen

app = Flask(__name__)

@app.route("/", methods = ["GET"])
def home():

    return render_template("index.html")


@app.route("/values", methods=["POST"])
def home1():
    price = int(request.form["price"])
    pchange = int(request.form["pchange"])
    volx = int(request.form["volx"])
    adx = int(request.form["adx"])
    ema = request.form["EMA"]
    ema_select = 0
    if ema == 'EMA13':
        ema_select = 13
    elif ema == 'EMA21':
        ema_select = 21
    elif ema == 'EMA51':
        ema_select = 51

    qopm = request.form["qopm"]
    yopm = request.form["yopm"]
    promc = request.form["promc"]
    borrow= request.form["borrow"]
    fassets = request.form["fassets"]
    if qopm == "on":
        qopm_val = 1
    else:
        qopm_val = 0
    if yopm == "on":
        yopm_val = 1
    else:
        yopm_val = 0
    if promc == "on":
        promc_val = 1
    else:
        promc_val = 0
    if borrow== "on":
        borrow_val = 1
    else:
        borrow_val = 0
    if fassets == "on":
        fassets_val = 1
    else:
        fassets_val = 0
    print(promc_val)
    stock_list = Read_Data()
    stock_list = Missing_Data(stock_list)
    today_list = Price_Vol_Action(stock_list, price, pchange, volx)
    stock_trend, stockcodes = Data_Selection(today_list)
    complete_data = Get_Historical_Data(stockcodes)
    stock_trend = Find_Sma(complete_data, stock_trend, stockcodes)
    my_stock_list_ema = Find_Ema(complete_data, stock_trend, stockcodes, ema_select)
    rpi = Find_ADX(my_stock_list_ema, adx)
    rpi = fun_analysis(rpi)
    rpi = final_screen(rpi, qopm_val, yopm_val, promc_val, borrow_val, fassets_val)
    final = rpi.to_html(index=False)



    print("Success")
    if (os.path.isfile('templates/final.html')):
        os.remove('templates/final.html')
    else :
        print(" no deletion")

    with open('templates/final.html', 'w') as myFile:
        myFile.write(final)
        """
        #myFile.write('<body>')
        #myFile.write('<table>')



        for i in output:
            myFile.write('<tr><td>' + i + '</td>')

        myFile.write('</tr>')
        myFile.write('</table>')
        myFile.write('</body>')
        myFile.write('</html>')
        """

        myFile.close()

    return render_template("final.html")




if __name__ == '__main__':
    app.run(debug = True)