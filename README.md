# myDailyStockScreener
A daily Stock Screener to screen stocks based on price volume action, technical analysis and fundamental analysis. 

Daily price volume action of all the main stocks listed in NSE are captured using Google Finance API via Google Sheets.
The gathered data is processed based on price and volume action parameters selected by the user using web API developed 
using FLask framework.

The shortlisted stocks are put to technical analysis parameters selected again by the user using web API and the parameters are calculated using 
web scraping and pandas data processing.

The shortlisted stocks are again filtered using fundamental analysis parameters again input by the user and fundamental parameters collected using web scraping.

The final list is made available to the user for final decision
