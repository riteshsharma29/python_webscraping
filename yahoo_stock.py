#!/usr/bin/python
# coding: utf-8 -*-

import pandas as pd
import pandas_datareader as pdr
from datetime import datetime
import ConfigParser
import codecs

'''https://ntguardian.wordpress.com/2016/09/19/introduction-stock-market-data-python-1/
https://pypi.python.org/pypi/pandas-datareader'''

config = ConfigParser.ConfigParser()
config.read("stocks.txt")

stocks = ""

def fetch_list(mylist):

# read config items
    for section in config.sections():
        for option in config.options(section):
            mylist = config.get(section, option)
            stocks = mylist
            return stocks

stocklst = fetch_list(stocks)

dflst = []

def extract():
    
    for stock in stocklst.split(","):
        stock = stock.strip()
        #start = datetime(2017,12,1)
        start = datetime.today()
        end = datetime.today()
        myseries = pd.Series(stock)
        myseries.name = "Stock"
        df = pdr.get_data_yahoo(stock,start, end)
        #add a column where 1st param is column number, 2nd param is columnname, 3rd param is stock name
        df.insert(0,'StockName',stock)
        dflst.append(df)
    #concatenate all the individual stockinfo into 1 DataFrame and export it to excel
    maindf=pd.concat(dflst)
    maindf.to_excel("mystock.xls")

extract()

logfile = codecs.open("done.txt","w",encoding='utf-8')
logfile.write("done !!! stock info downloaded in mystock.xls")
