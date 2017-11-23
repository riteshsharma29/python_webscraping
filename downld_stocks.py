#! /usr/bin/env python
# -*- coding: utf-8 -*-

#https://adesquared.wordpress.com/2013/06/16/using-python-beautifulsoup-to-scrape-a-wikipedia-table/
#http://srome.github.io/Parsing-HTML-Tables-in-Python-with-BeautifulSoup-and-pandas/

# Import required modules
import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib2,cookielib,codecs,sys
import pandas as pd
from pandas import ExcelWriter
import pandas as pd
import html5lib,csv,sys

wiki = "https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?"
#to avoid 4.3 Forbidden error
header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
req = urllib2.Request(wiki,headers=header)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page,"html.parser")

#find table using class attribute
table = soup.find_all("table")

#Find number of tables and then select your desired table
#print table[2]
#sys.exit()

#For eg let's select 1st table and decode its contents into utf-8
new_table = str(table[2]).decode('utf-8')

#generate html file from a of webtable html

convstr = codecs.open("test.html", "w", encoding="utf8")
convstr.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">' + '\n')
convstr.write('<html xmlns="http://www.w3.org/1999/xhtml">' + '\n')
convstr.write('<head>' + '\n')
convstr.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />' + '\n')
convstr.write(new_table + '\n')
convstr.write('</html>' + '\n')

#Lets read the downloaded html file into Pandas Dataframe and dump it into xls

dfs = pd.read_html('test.html',header =0, flavor = 'bs4')

#print dfs[0].dropna()

writer = ExcelWriter('nse.xlsx')
	
dfs[0].to_excel(writer,'Sheet1')
	
writer.save()	
