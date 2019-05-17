# -*- coding: utf-8 -*-
import codecs
import json
import os
import re
import sqlite3
import time
import base64

import requests
from bs4 import BeautifulSoup
from lxml import etree

# 网址List
sites = []

# 从sitemap中获取新闻
def getSiteList(id=0):
    # 基础网址
    baseSitemap = "http://www.thepaper.cn/sitemap/newsDetail-number.xml"
    # 真正网址（一般为1-10）
    sitemap_url = baseSitemap.replace('number', str(id))
    # 解析网址
    html = requests.get(sitemap_url, timeout=10)
    html.encoding = html.apparent_encoding
    try:
        # 此处用正则表达式匹配，因为使用lxml的etree无法匹配
        pattern = re.compile(r"<loc>(.+?)</loc>")
        for site in pattern.findall(html.text):
            sites.append(site.strip())
    except Exception:
        pass

# 从robots获取当天的新闻
def getRobotsList(robotsUrl="https://www.thepaper.cn/robots.txt"):
    # 解析网址
    html = requests.get(robotsUrl, timeout=10)
    html.encoding = html.apparent_encoding
    try:
        # 此处用正则表达式匹配
        pattern = re.compile(r"Disallow:(.+?\d+)")
        for site in pattern.findall(html.text):
            sites.append("https://www.thepaper.cn" + site)
    except Exception:
        pass

# 读取对应网站页面和内容
def getPageContent(url):
    try:
        req = requests.get(url, timeout=10)
        req.encoding = req.apparent_encoding
        page = req.text

        if "此文章已下线" in page:
            return

        fa = etree.HTML(page)
        soup = BeautifulSoup(page, "html.parser")
        title = soup.find('h1', 'news_title').string
        tuple = (url, title, "".join(fa.xpath(
            '//div[@class="news_txt"]//text()')))
        return tuple
        '''
        fil = codecs.open("./content/" + title + '.txt', "a+", 'utf-8')
        for i in fa.xpath(
                '//div[@class="news_txt"]//text()'):
            fil.write(i + '\r\n')
        fil.close()
        '''
    except Exception:
        pass

#创建SQL数据库
def createSQL(Sqlname='ThePaper.db'):
     # 创建数据库
    sql = sqlite3.connect(Sqlname)
    sql.execute("""
                create table if not exists paper(
                link varchar PRIMARY KEY ,
                title varchar DEFAULT NULL,
                content varchar DEFAULT NULL)""")
    return sql

if __name__ == '__main__':
    getRobotsList()
    for i in range(1, 11):
        getSiteList(i)
    # 对列表去重
    sites = list(set(sites))
    #创建一个新的Sql存储我们的网站
    paperSql = createSQL()
    time0 = time.time()
    id = 0
    for url in sites:
        tuple = getPageContent(url)
        command = "insert into paper (link,title,content) values (?,?,?);"
        try:
            paperSql.execute(command, tuple)
            paperSql.commit()
            time1 = time.time()
            print("\r已爬取{0}个网页 ，总花费时间:{1:.2f}s".format(id, time1 - time0), end="")
        except Exception as e:
            print(e, tuple)

'''
    # 将网站保存为txt(也可以保存在sql中)
    f = codecs.open('site.txt', "a+", 'utf-8')
    time0 = time.time()
    id = 0
    for url in sites:
        getPageContent(url)
        f.write(url + "\r\n")
        id = id+1
        time1 = time.time()
        print("\r已爬取{0}个网页 ，总花费时间:{1:.2f}s".format(
            id, time1 - time0), end="")
    f.close()
'''
