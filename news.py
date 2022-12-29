# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 09:55:30 2022

@author: User
"""
import db
import requests
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()




def img(link):
    page='https://www.cpbl.com.tw'+link
    rq=requests.get(page,verify=False).text
    bs=BeautifulSoup(rq,'html.parser')
    image=bs.find('div','imgcenter img_bg').find('img').get('src')
    return image

url="https://www.cpbl.com.tw/xmdoc"
rq=requests.get(url,verify=False).text
bs=BeautifulSoup(rq,'html.parser')
item=bs.find_all('div',class_='item')

cursor=db.conn.cursor()

for i in item:
    try:
        link=i.find('a').get('href')
        title=i.find('div','title').text.strip()
        postdate=i.find('div','date').text
        photo=img(link)
        alllink='https://www.cpbl.com.tw'+link
        
        print('連結:',alllink)
        print('標題:',title)
        print('日期:',postdate)
        print('圖片:',photo)
        print()
        sql="select * from news where link='{}'".format(alllink)
        cursor.execute(sql)
        db.conn.commit()
        if cursor.rowcount == 0:
            pass
            sql="insert into news(link,title,photo,postdate) values('{}','{}','{}','{}')".format(alllink,title,photo,postdate)
        
            cursor.execute(sql)
            db.conn.commit()
    except:
        pass
