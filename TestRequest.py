import requests
from bs4 import BeautifulSoup
import re
import json
import pandas
from mpl_test import Crawler


# crawler = Crawler('http://api.zhuanlan.sina.com.cn/api/article/get_list.json?article_ids=64889,64888,64887,64885,64884,64882,64879,64878,64876,64875,64872,64871,64870,64873,,&callback=jQuery110207573210913066464_1511753267296&_=1511753267297')
# newsdetail = crawler.parserData()
#
# df = pandas.DataFrame(newsdetail)

import sqlite3
with sqlite3.connect('news.sqlite') as db:
   df2 = pandas.read_sql_query('SELECT * FROM news', con = db)
   print(df2)