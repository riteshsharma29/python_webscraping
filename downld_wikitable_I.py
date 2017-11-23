#!/usr/bin/python

#http://coderscrowd.com/app/public/codes/view/139
#https://www.youtube.com/watch?v=wT66i7jeyL8

from pandas import ExcelWriter
import pandas as pd
import html5lib,csv

url = "https://en.wikipedia.org/wiki/List_of_Nobel_laureates"

dfs = pd.read_html(url,header =0, flavor = 'bs4')

writer = ExcelWriter('noble.xlsx')
	
dfs[0].to_excel(writer,'Sheet1')
	
writer.save()	