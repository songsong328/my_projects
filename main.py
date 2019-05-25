# -*- coding: utf-8 -*-
"""
Created on Thu May 23 22:23:01 2019

@author: swang
"""

import pandas as pd
import numpy as np
import requests
import urllib
from songs_tool import codb
#co = codb.conndb()

url = "https://na.op.gg/summoner/userName=NoFaith"
headers = {'User-Agent': """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36""",
           'Host': "na.op.gg"}

parser = {'name': 'English'}

data = bytes(urllib.parse.urlencode(parser), encoding='utf-8')
opgg = urllib.request.Request(url=url, data=data, headers=headers, method='POST')
response = urllib.request.urlopen(quora)


print(response.read().decode('utf-8'))


