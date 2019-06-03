# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 18:16:22 2019

@author: swang
"""

import pandas as pd
import urllib
import time
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


from bs4 import BeautifulSoup
from songs_tool import codb

co = codb.conndb()

host = "https://www.instagram.com/accounts/login/?source=auth_switcher"
exe_path = r"C:\Users\swang\Downloads\webdrivers\chromedriver74.exe"

table_name = 'Instagram'
username = 'swang115'
password = 'Astro328'
browser = webdriver.Chrome(exe_path)
browser.get(host)

# loggin in
browser.find_element_by_tag_name('form').find_element_by_tag_name('input').send_keys(username, Keys.TAB, password)

time.sleep(3)
browser.find_element_by_xpath("//button[contains(.,'Log In')]").click()
time.sleep(3)
try:
    browser.find_element_by_xpath("//button[contains(.,'Not Now')]").click()
except:
    pass

# jump to the explore page
browser.find_element_by_tag_name('nav').find_elements_by_tag_name('a')[1].click()
time.sleep(2)

# set current explore page as our main page
main_window = browser.current_window_handle

# get scroll height
PAUSE = 1
height = browser.execute_script("return document.body.scrollHeight")
actions = ActionChains(browser)


output = {
        'poster_dict': [], 'poster_cap_dict': [], 'poster_likes_dict': [],
        'resp_dict': [], 'resp_likes_dict': []
        }
poster_dict = {}
poster_cap_dict = {}
poster_likes_dict = {}
resp_dict = {}
resp_likes_dict = {}

for i, post in enumerate(browser.find_element_by_tag_name('article').find_elements_by_tag_name('a')):
    # scroll down to the bottom of the page once per 9 posts
    if (i+1)%9 == 0:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(PAUSE)
        new_height = browser.execute_script("return document.body.scrollHeight")
        last_height = new_height

    post.click()

    # poster -- text() to make there is a valid value after title attribute
    poster = post.find_element_by_xpath("//a[@title = text()]").text
    
    # poster's caption
    main_post = post.find_elements_by_xpath("//span[@title = text()]")[0].text
    
    # top 12 liked reponses
    resp_list = []
    likes_list = []
    for revs in post.find_elements_by_xpath("//li[@role = 'menuitem']")[1:]:
        resp_list += [revs.find_element_by_tag_name('span').text]
        likes_list += revs.find_element_by_tag_name('button').text.split(' ')[0]
        
    poster_list = [poster for i in range(len(resp_list))]
    poster_caption_list = [main_post for i in range(len(resp_list))]
    poster_likes_list = []
    for item in post.find_elements_by_xpath("//button[@type = 'button']"):
        try:
            poster_likes = item.find_element_by_tag_name('span').text
            break
        except:
            continue
    poster_likes_list = [poster_likes for i in range(len(resp_list))]
    post.find_element_by_xpath("//button[contains(.,'Close')]").click()
    
    poster_dict['poster_dict'] += poster_list
    poster_dict['poster_cap_dict'] += poster_caption_list
    poster_dict['poster_likes_dict'] += poster_likes_list
    poster_dict['resp_dict'] += resp_list
    poster_dict['resp_likes_dict'] += likes_list

df = pd.DataFrame.from_dict(output)
codb.upload_table('Instagram', df, co)