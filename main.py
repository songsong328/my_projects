# -*- coding: utf-8 -*-
"""
Created on Thu May 23 22:23:01 2019

@author: swang
"""

import pandas as pd
#import numpy as np
import urllib
import time
from selenium import webdriver

from bs4 import BeautifulSoup
from songs_tool import codb

co = codb.conndb()

host = "na.op.gg"
header_qry = "SELECT * FROM MYHEADERS"
exe_path = r"C:\Users\swang\Downloads\webdrivers\chromedriver74.exe"
grandmaster = 5
diamond2 = 51
headers = {'User-Agent': pd.read_sql(header_qry, co).iloc[0][0],
           'Host': host}
parser = {'name': 'English'}
data = bytes(urllib.parse.urlencode(parser), encoding='utf-8')
table_name = 'Gaming'
# urllib
# get all summoners name
browser = webdriver.Chrome(exe_path)

output = {'Summoner': [], 'Ranking': [], 'Win_Ratio': [],
          'Champion': [], 'Game_Type': [], 'Game_Length': [],
          'Kill': [], 'Death': [], 'Assist': [], 'KDA': [], 'CS': []
          }
for i in range(grandmaster, diamond2):
    # locate ladder ranking page
    url = "https://na.op.gg/ranking/ladder/page={}".format(i+1)
    
    # jump to that page
    browser.get(url)
    soup = BeautifulSoup(browser.page_source)
    content_wrap = soup.find_all('div', {'class': 'ContentWrap'})[0]
    ranking_table = content_wrap.find('table', {'class':'ranking-table'})
    
    # find the matching info of all the users on the ranking page
    for i, users in enumerate(ranking_table.find_all('tr', {'class':'ranking-table__row'})):
        
        # get this summoner's name
        user = ranking_table.find_all('tr', {'class':'ranking-table__row'})[i].a.text
        # get this summoner's rank
        rank = ranking_table.find_all('tr', {'class':'ranking-table__row'})[i].find('td', {'class': 'ranking-table__cell ranking-table__cell--tier'}).text.strip()
        # get this summoner's win ratio
        w_ratio = ranking_table.find_all('tr', {'class':'ranking-table__row'})[i].find('span', {'class': 'winratio__text'}).text
        url_user = "https://na.op.gg/summoner/userName={}".format(user)

        browser.get(url_user)
        
        # show the latest maxium of 50 games
        for _ in range(5):
            try:
                browser.find_element_by_css_selector('.GameMoreButton.Box').click()
                time.sleep(3)
            except:
                pass
            soup_user = BeautifulSoup(browser.page_source)
            
            # get that particular summoner's game infos
            for game in soup_user.find_all('div', {'class': 'GameItemWrap'}):
                output['Summoner'] += [user]
                output['Ranking'] += [rank]
                output['Win_Ratio'] += [w_ratio]
                
                champ = game.find('div', {'class': 'ChampionName'}).a.text
                game_type = game.find('div', {'class': 'GameType'}).text.strip()
                game_len = game.find('div', {'class': 'GameLength'}).text
                kill = game.find('div', {'class': 'KDA'}).find('span', {'class': 'Kill'}).text
                death = game.find('div', {'class': 'KDA'}).find('span', {'class': 'Death'}).text
                assist = game.find('div', {'class': 'KDA'}).find('span', {'class': 'Assist'}).text
                if int(death) != 0:
                    kda = '{:.2f}'.format((int(kill) + int(assist)) / int(death))
                else:
                    kda = 'Perfect'
                cs = game.find('span', {'class': 'CS'}).text
                
                output['Champion'] += [champ]
                output['Game_Type'] += [game_type]
                output['Game_Length'] += [game_len]
                output['Kill'] += [kill]
                output['Death'] += [death]
                output['Assist'] += [assist]
                output['KDA'] += [kda]
                output['CS'] += [cs]

df = pd.DataFrame().from_dict(output)
codb.upload_table(table_name, df, co)

print(pd.read_sql("SELECT * FROM {}".format(table_name), co))