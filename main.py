# -*- coding: utf-8 -*-
"""
Created on Thu May 23 22:23:01 2019

@author: swang
"""

import pandas as pd
#import numpy as np
import urllib
import json

from bs4 import BeautifulSoup
from songs_tool import codb

co = codb.conndb()

host = "na.op.gg"
header_qry = "SELECT * FROM MYHEADERS"

headers = {'User-Agent': pd.read_sql(header_qry, co).iloc[0][0],
           'Host': host}

parser = {'name': 'English'}
data = bytes(urllib.parse.urlencode(parser), encoding='utf-8')

# get all summoners name
for i in range(100):
    url = "https://na.op.gg/ranking/ladder/page={}".format(i+1)
    opgg = urllib.request.Request(url=url,
                                  data=data,
                                  headers=headers, method='POST')
    response = urllib.request.urlopen(opgg)
    # parse the output

    soup = BeautifulSoup(response.read().decode('utf-8'))
    
    # 1 --> summoner name
    # 2 --> tier
    # 3 --> lp
    # 4 --> level
    # 5 --> winratio
    
    this_name = soup.find_all('td')[i+7].text
    this_tier = soup.find_all('td')[i+8].text.replace('\t', '').replace('\n', '')
    this_winrate = soup.find_all('td')[i+11].text[-3:]
    
    # search this summoner
    
    url = "https://na.op.gg/summoner/userName={}".format(this_name)
    opgg = urllib.request.Request(url=url,
                                  data=data,
                                  headers=headers, method='POST')
    
    one = ':'.join(soup.find_all('script')[43].text.split(',')[7].split(':')[1:])
    two = ', '.join(soup.find_all('script')[43].text.split(',')[8:-15])
    games = one[1:] + ',' + two[:-1]
    games = games[:games.index('championsList')-4]
    json.loads(games)