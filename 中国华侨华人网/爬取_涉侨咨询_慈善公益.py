# -*- coding: utf-8 -*-
import xlsxwriter
import requests
from lxml import etree
import re

Links = []
Dates = []
Titles = []
Contents = []
Writers = []

#获得范围
def getRange():
        baseSite = "http://www.chinesecome.com/xcsgy/index_0.jhtml"
        req = requests.get(baseSite, timeout=10)
        req.encoding = req.apparent_encoding
        HTML = etree.HTML(req.text)
        content =  "".join(HTML.xpath( '//div[@class="hrny_ftym"]//text()'))
        return re.search(r'/(\d+)页', content).group(1)

#获得链接
def getLinkList(pla):
    try:
        baseSite = "http://www.chinesecome.com/xcsgy/index_【序号】.jhtml"
        realSite = baseSite.replace("【序号】",str(pla))

        #print(realSite)

        req = requests.get(realSite, timeout=10)
        req.encoding = req.apparent_encoding
        HTML = etree.HTML(req.text)
        List = HTML.xpath( '//tr/td[@class="hrny_lbnrbt"]/a/@href')
        #print(List)
    finally:
        return list(List)

def getInf(link):
    try:
        req = requests.get(link, timeout=10)
        req.encoding = req.apparent_encoding
        HTML = etree.HTML(req.text)
        title = HTML.xpath( '//tr/td[@class="hrny_xxnrbt"]/a//text()')
        writer = HTML.xpath( '//td/span[@style="float:right;"]//text()')
        date = HTML.xpath( '//td[@style=" color:#888888; border-bottom:#e9e9e9 1px solid;"]/text()')
        content = "\n".join(HTML.xpath( '//td[@class="hrny_lbnrxx"]//text()'))
    finally:
        #print(title,writer,date,content)
        return "".join(link),"".join(title),"".join(date),"".join(writer),content


if __name__ == '__main__':

    # 创建工作簿
    file_name = "涉侨资讯_慈善公益.xlsx"
    workbook = xlsxwriter.Workbook(file_name)

    # 创建工作表
    worksheet = workbook.add_worksheet('慈善公益')

    # 写单元格
    worksheet.write(0, 0, '链接')
    worksheet.write(0, 1, '新闻')
    worksheet.write(0, 2, '日期')
    worksheet.write(0, 3, '来源')
    worksheet.write(0, 4, '内容')

    pla = 1
    maxPag = int(getRange())
    for i in range(0,maxPag):
        print("Got",i)
        Links.extend(getLinkList(i))
    for link in Links:
        print(link)
        inf = getInf(link)
        print(inf)
        worksheet.write_row(pla, 0, inf)
        pla = pla+1

    # 关闭工作簿
    workbook.close()