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

titles = []
link = []
date = []
writer = []
content = []


# 获取新闻总页数
def GetCount(keyword="华侨华人蓝皮书"):
    # 基础网址
    baseSitemap = r"http://www.cssn.cn/was5/web/search?page=【页面序号】&channelid=254789&searchword=【搜索主题】&keyword=【搜索主题】&was_custom_expr=doccontent=(【搜索主题】) * chnls=0&perpage=10&outlinepage=10&searchscope=doccontent&timescope=&timescopecolumn=&orderby=&andsen=&total=&orsen=&exclude="
    # 真正网址
    sitemap_url = baseSitemap.replace(
        '【页面序号】', "1").replace('【搜索主题】', keyword)
    try:
        # 解析网址
        html = requests.get(sitemap_url, timeout=100)
        html.encoding = html.apparent_encoding
        page = html.text

        get = etree.HTML(page)

        # 此处用正则表达式匹配，因为使用lxml的etree无法匹配
        pattern = re.compile(r"page=(.+?)&channelid")
        count = pattern.findall(
            "".join(get.xpath('//ul/a[@class="last-page"]//@href')))[0]
        return count
    except Exception:
        return 1


# 从搜索中获取新闻基础信息
def getSiteList(keyword="华侨华人蓝皮书", id=1):
    # 基础网址
    baseSitemap = r"http://www.cssn.cn/was5/web/search?page=【页面序号】&channelid=254789&searchword=【搜索主题】&keyword=【搜索主题】&was_custom_expr=doccontent=(【搜索主题】) * chnls=0&perpage=10&outlinepage=10&searchscope=doccontent&timescope=&timescopecolumn=&orderby=&andsen=&total=&orsen=&exclude="
    # 真正网址（一般为1-10）
    sitemap_url = baseSitemap.replace(
        '【页面序号】', str(id)).replace('【搜索主题】', keyword)
    try:
        # 解析网址
        html = requests.get(sitemap_url, timeout=100)
        html.encoding = html.apparent_encoding
        page = html.text

        get = etree.HTML(page)

        titles.extend(get.xpath(
            '//div[@class="s_c_lb"]/div[@class="s_c_c"]/h1/a/text()'))
        link.extend(get.xpath(
            '//div[@class="s_c_lb"]/div[@class="s_c_c"]/div[@class="s_c_c_sj"]/a//@href'))
        date.extend(get.xpath(
            '//div[@class="s_c_lb"]/div[@class="s_c_c"]/div[@class="s_c_c_sj"]/span[1]/text()'))
        writer.extend(get.xpath(
            '//div[@class="s_c_lb"]/div[@class="s_c_c"]/div[@class="s_c_c_sj"]/span[2]/text()'))

        for i in link:
            # 解析网址
            html1 = requests.get(i, timeout=100)
            html1.encoding = html1.apparent_encoding
            page1 = html1.text
            get1 = etree.HTML(page1)
            content.append("".join(get1.xpath(
                '//p[@align="left"]//text()')) + "".join(get1.xpath(
                    '//p[@align="justify"]//text()')))

        print(len(link))
    except Exception:
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
    command = "insert into information (link,title,date,writer,content) values (?,?,?,?,?);"
    sql.execute(command, tuple)
    sql.commit()


if __name__ == '__main__':
    keyword = input("请输入你的关键字：")
    createSQL(keyword + ".db")
    num = int(GetCount(keyword))
    for i in range(1, num + 1):
        getSiteList(keyword, i)
    for i in range(0, len(link)):
        print(titles[i])
        try:
            tuple = [link[i], titles[i], date[i], writer[i], content[i]]
            SaveSQL(keyword + '.db', tuple)
        except Exception:
            pass
