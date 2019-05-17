
# -*- coding: utf-8 -*-
import base64
import codecs
import json
import os
import re
import sqlite3
import time

import requests
from bs4 import BeautifulSoup
from lxml import etree
from urllib import parse
from urllib import request
from urllib.parse import urljoin

sites = []

titles = []
links = []
date = []
writer = []
content = []


# 获取新闻网站列表
def GetSite(baseSitemap=r"http://hqhr.hqu.edu.cn/sylj/", nextbaseSitemap=r"http://hqhr.hqu.edu.cn/sylj/mtgz.htm"):
    sites.append(nextbaseSitemap)
    try:
        # 解析网址
        html = requests.get(nextbaseSitemap, timeout=100)
        html.encoding = html.apparent_encoding
        page = html.text

        get = etree.HTML(page)

        nextbaseSitemap = urljoin(baseSitemap,
                                  "".join(get.xpath('//td[@align="left"]/div/a[@class="Next"][1]//@href')))
        if(nextbaseSitemap == baseSitemap):
            return "解析完毕"
        GetSite(nextbaseSitemap, nextbaseSitemap)
    except Exception:
        return "解析出错"


# 解析新闻网站列表
def GetLink(link):
    try:
        # 解析网址
        html = requests.get(link, timeout=10)
        html.encoding = html.apparent_encoding
        page = html.text

        get = etree.HTML(page.lower())

        tuple = get.xpath('//td/a[@target="_blank"]/font/text()')
        tuples = get.xpath('//td/a[@target="_blank"]/@href')
        for value in tuple:
            titles.append(value.strip())
        for value in tuples:
            links.append(urljoin(link, value.strip()))
    except Exception as e:
        pass


# 解析新闻网站
def GetContent(link):
    try:
        # 解析网址
        html = requests.get(link, timeout=10)
        html.encoding = html.apparent_encoding
        page = html.text

        get = etree.HTML(page.lower())

        # 此处用正则表达式匹配，因为使用lxml的etree无法匹配
        pattern = re.compile(r"发布时间：(.+?)浏览次数")
        date.append(pattern.findall(page)[0])

        content.append(
            "".join(get.xpath('//div[@id="container_content"]//text()')).strip())

    except Exception as e:
        pass

# 创建SQL数据库


def createSQL(Sqlname='华侨华人蓝皮书.db'):
     # 创建数据库
    sql = sqlite3.connect(Sqlname)
    sql.execute("""
                create table if not exists information(
                id int identity(1,1) primary key,
                link varchar DEFAULT NULL,
                title varchar DEFAULT NULL,
                date varchar DEFAULT NULL,
                writer varchar DEFAULT NULL,
                content varchar DEFAULT NULL)""")
    return sql


# 保存SQL数据库
def SaveSQL(Sqlname='华侨华人蓝皮书.db', tuple=()):
    # 连接数据库
    sql = sqlite3.connect(Sqlname)
    command = "insert into information (link,title,date,content) values (?,?,?,?);"
    sql.execute(command, tuple)
    sql.commit()


if __name__ == '__main__':
    createSQL("华侨华人研究院.db")
    GetSite("http://hqhr.hqu.edu.cn/sylj/",
            "http://hqhr.hqu.edu.cn/sylj/mtgz.htm")
    GetSite("http://hqhr.hqu.edu.cn/sylj/",
            "http://hqhr.hqu.edu.cn/sylj/xwzx.htm")
    GetSite("http://hqhr.hqu.edu.cn/",
            "http://hqhr.hqu.edu.cn/xsyj.htm")
    for li in sites:
        GetLink(li)
    for li in links:
        GetContent(li)
    for i in range(0, len(links)):
        print(titles[i])
        try:
            tuple = [links[i], titles[i], date[i], content[i]]
            SaveSQL("华侨华人研究院.db", tuple)
        except Exception:
            pass
