# -*- coding: utf-8 -*-
import xlsxwriter
import requests
from lxml import etree

# 网址List
Areas = {
    "北美洲": "NorthAmerica",
    "南美洲": "SouthAmerica",
    "欧洲": "Europe",
    "非洲": "Africa",
    "亚洲": "Asia",
    "大洋洲": "Oceania"
}


#print(sites["北美洲"])
#print(list(sites.keys())[list(sites.values()).index('SouthAmerica')])

#获取所有国家列表
def getCountryList(area_cn,area):
    baseSite = "http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_area&area=【英文洲】&area_cn=【中文洲】"
    realSite = baseSite.replace("【英文洲】",area).replace("【中文洲】",area_cn)

    print(realSite)

    req = requests.get(realSite, timeout=10)
    req.encoding = req.apparent_encoding
    HTML = etree.HTML(req.text)
    countryList = HTML.xpath( '//td[@class="gjxx2_mnrlk"]//text()')
    countryValueList = HTML.xpath( '//td[@class="gjxx2_mnrlk"]/a/@value')

    return ([i for i in countryList if i.strip()],[i for i in countryValueList if i.strip()])

def getAssociationList(area,country_short,country,Type = "华人社团"):
    #这里的kind参数我没写全，实际上应该根据列别来写
    baseSite = "http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=【地区英文】&kind=xhrst&country=【国家简称】&country_name=【国家全称】&kind_name=【类别】"
    #http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=xhrst&country=BRA&country_name=巴西&kind_name=华人社团
    realSite = baseSite.replace("【地区英文】",area).replace("【国家简称】",country_short).replace("【国家全称】",country).replace("【类别】",Type)

    print(realSite)
    return realSite

def getAssociation(url):
    req = requests.get(url, timeout=10)
    req.encoding = req.apparent_encoding
    HTML = etree.HTML(req.text)
    return(HTML.xpath( '//a/@title'))

if __name__ == '__main__':
    """
    {'北美洲': (
    ['本州全部', '安提瓜和巴布达', '阿鲁巴', '巴哈马', '巴巴多斯', '贝利塞', '百慕大', '英属维尔京群岛', '加拿大', '开曼群岛', '哥斯达黎加', '古巴', '多米尼加', '民主多米尼加',
     '萨尔瓦多', '格林纳达', '危地马拉', '海地', '洪都拉斯', '牙买加', '墨西哥', '荷属安的列斯', '巴拿马', '波多黎各', '圣卢西亚', '圣文森特和格林哪达', '美国', '尼加拉瓜',
     '圣基特和内维斯', '特立尼达和多巴哥'],
    ['all', 'ANT', 'ARU', 'BAH', 'BAR', 'BIZ', 'BER', 'IVB', 'CAN', 'CAY', 'CRC', 'CUB', 'DMA', 'DOM', 'ESA', 'GRN',
     'GUA', 'HAI', 'HON', 'JAM', 'MEX', 'AHO', 'PAN', 'PUR', 'LCA', 'VIN', 'USA', 'NCA', 'SKN', 'TRI']), '南美洲': (
    ['本州全部', '委内瑞拉', '阿根廷', '玻利维亚', '巴西', '哥伦比亚', '圭亚那', '巴拉圭', '秘鲁', '乌拉圭', '智利', '厄瓜多尔', '苏里南'],
    ['all', 'VEN', 'ARG', 'BOL', 'BRA', 'COL', 'GUY', 'PAR', 'PER', 'URU', 'CHI', 'ECU', 'SUR']), '欧洲': (
    ['本州全部', '委内瑞拉', '阿根廷', '玻利维亚', '巴西', '哥伦比亚', '圭亚那', '巴拉圭', '秘鲁', '乌拉圭', '智利', '厄瓜多尔', '苏里南'],
    ['all', 'VEN', 'ARG', 'BOL', 'BRA', 'COL', 'GUY', 'PAR', 'PER', 'URU', 'CHI', 'ECU', 'SUR']), '非洲': (
    ['本州全部', '委内瑞拉', '阿根廷', '玻利维亚', '巴西', '哥伦比亚', '圭亚那', '巴拉圭', '秘鲁', '乌拉圭', '智利', '厄瓜多尔', '苏里南'],
    ['all', 'VEN', 'ARG', 'BOL', 'BRA', 'COL', 'GUY', 'PAR', 'PER', 'URU', 'CHI', 'ECU', 'SUR']), '亚洲': (
    ['本州全部', '委内瑞拉', '阿根廷', '玻利维亚', '巴西', '哥伦比亚', '圭亚那', '巴拉圭', '秘鲁', '乌拉圭', '智利', '厄瓜多尔', '苏里南'],
    ['all', 'VEN', 'ARG', 'BOL', 'BRA', 'COL', 'GUY', 'PAR', 'PER', 'URU', 'CHI', 'ECU', 'SUR']), '大洋洲': (
    ['本州全部', '委内瑞拉', '阿根廷', '玻利维亚', '巴西', '哥伦比亚', '圭亚那', '巴拉圭', '秘鲁', '乌拉圭', '智利', '厄瓜多尔', '苏里南'],
    ['all', 'VEN', 'ARG', 'BOL', 'BRA', 'COL', 'GUY', 'PAR', 'PER', 'URU', 'CHI', 'ECU', 'SUR'])}
    """
    countryDict = {}
    """
    [['北美洲', '本州全部',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=all&country_name=本州全部&kind_name=华人社团'],
     ['北美洲', '安提瓜和巴布达',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=ANT&country_name=安提瓜和巴布达&kind_name=华人社团'],
     ['北美洲', '阿鲁巴',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=ARU&country_name=阿鲁巴&kind_name=华人社团'],
     ['北美洲', '巴哈马',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=BAH&country_name=巴哈马&kind_name=华人社团'],
     ['北美洲', '巴巴多斯',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=BAR&country_name=巴巴多斯&kind_name=华人社团'],
     ['北美洲', '贝利塞',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=BIZ&country_name=贝利塞&kind_name=华人社团'],
     ['北美洲', '百慕大',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=BER&country_name=百慕大&kind_name=华人社团'],
     ['北美洲', '英属维尔京群岛',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=IVB&country_name=英属维尔京群岛&kind_name=华人社团'],
     ['北美洲', '加拿大',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=CAN&country_name=加拿大&kind_name=华人社团'],
     ['北美洲', '开曼群岛',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=CAY&country_name=开曼群岛&kind_name=华人社团'],
     ['北美洲', '哥斯达黎加',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=CRC&country_name=哥斯达黎加&kind_name=华人社团'],
     ['北美洲', '古巴',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=CUB&country_name=古巴&kind_name=华人社团'],
     ['北美洲', '多米尼加',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=DMA&country_name=多米尼加&kind_name=华人社团'],
     ['北美洲', '民主多米尼加',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=DOM&country_name=民主多米尼加&kind_name=华人社团'],
     ['北美洲', '萨尔瓦多',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=ESA&country_name=萨尔瓦多&kind_name=华人社团'],
     ['北美洲', '格林纳达',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=GRN&country_name=格林纳达&kind_name=华人社团'],
     ['北美洲', '危地马拉',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=GUA&country_name=危地马拉&kind_name=华人社团'],
     ['北美洲', '海地',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=HAI&country_name=海地&kind_name=华人社团'],
     ['北美洲', '洪都拉斯',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=HON&country_name=洪都拉斯&kind_name=华人社团'],
     ['北美洲', '牙买加',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=JAM&country_name=牙买加&kind_name=华人社团'],
     ['北美洲', '墨西哥',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=MEX&country_name=墨西哥&kind_name=华人社团'],
     ['北美洲', '荷属安的列斯',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=AHO&country_name=荷属安的列斯&kind_name=华人社团'],
     ['北美洲', '巴拿马',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=PAN&country_name=巴拿马&kind_name=华人社团'],
     ['北美洲', '波多黎各',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=PUR&country_name=波多黎各&kind_name=华人社团'],
     ['北美洲', '圣卢西亚',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=LCA&country_name=圣卢西亚&kind_name=华人社团'],
     ['北美洲', '圣文森特和格林哪达',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=VIN&country_name=圣文森特和格林哪达&kind_name=华人社团'],
     ['北美洲', '美国',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=USA&country_name=美国&kind_name=华人社团'],
     ['北美洲', '尼加拉瓜',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=NCA&country_name=尼加拉瓜&kind_name=华人社团'],
     ['北美洲', '圣基特和内维斯',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=SKN&country_name=圣基特和内维斯&kind_name=华人社团'],
     ['北美洲', '特立尼达和多巴哥',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=NorthAmerica&kind=ggqk&country=TRI&country_name=特立尼达和多巴哥&kind_name=华人社团'],
     ['南美洲', '本州全部',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=all&country_name=本州全部&kind_name=华人社团'],
     ['南美洲', '委内瑞拉',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=VEN&country_name=委内瑞拉&kind_name=华人社团'],
     ['南美洲', '阿根廷',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=ARG&country_name=阿根廷&kind_name=华人社团'],
     ['南美洲', '玻利维亚',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=BOL&country_name=玻利维亚&kind_name=华人社团'],
     ['南美洲', '巴西',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=BRA&country_name=巴西&kind_name=华人社团'],
     ['南美洲', '哥伦比亚',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=COL&country_name=哥伦比亚&kind_name=华人社团'],
     ['南美洲', '圭亚那',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=GUY&country_name=圭亚那&kind_name=华人社团'],
     ['南美洲', '巴拉圭',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=PAR&country_name=巴拉圭&kind_name=华人社团'],
     ['南美洲', '秘鲁',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=PER&country_name=秘鲁&kind_name=华人社团'],
     ['南美洲', '乌拉圭',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=URU&country_name=乌拉圭&kind_name=华人社团'],
     ['南美洲', '智利',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=CHI&country_name=智利&kind_name=华人社团'],
     ['南美洲', '厄瓜多尔',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=ECU&country_name=厄瓜多尔&kind_name=华人社团'],
     ['南美洲', '苏里南',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=SUR&country_name=苏里南&kind_name=华人社团'],
     ['欧洲', '本州全部',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=all&country_name=本州全部&kind_name=华人社团'],
     ['欧洲', '委内瑞拉',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=VEN&country_name=委内瑞拉&kind_name=华人社团'],
     ['欧洲', '阿根廷',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=ARG&country_name=阿根廷&kind_name=华人社团'],
     ['欧洲', '玻利维亚',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=BOL&country_name=玻利维亚&kind_name=华人社团'],
     ['欧洲', '巴西',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=BRA&country_name=巴西&kind_name=华人社团'],
     ['欧洲', '哥伦比亚',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=COL&country_name=哥伦比亚&kind_name=华人社团'],
     ['欧洲', '圭亚那',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=GUY&country_name=圭亚那&kind_name=华人社团'],
     ['欧洲', '巴拉圭',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=PAR&country_name=巴拉圭&kind_name=华人社团'],
     ['欧洲', '秘鲁',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=PER&country_name=秘鲁&kind_name=华人社团'],
     ['欧洲', '乌拉圭',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=URU&country_name=乌拉圭&kind_name=华人社团'],
     ['欧洲', '智利',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=CHI&country_name=智利&kind_name=华人社团'],
     ['欧洲', '厄瓜多尔',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=ECU&country_name=厄瓜多尔&kind_name=华人社团'],
     ['欧洲', '苏里南',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=SUR&country_name=苏里南&kind_name=华人社团'],
     ['非洲', '本州全部',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=all&country_name=本州全部&kind_name=华人社团'],
     ['非洲', '委内瑞拉',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=VEN&country_name=委内瑞拉&kind_name=华人社团'],
     ['非洲', '阿根廷',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=ARG&country_name=阿根廷&kind_name=华人社团'],
     ['非洲', '玻利维亚',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=BOL&country_name=玻利维亚&kind_name=华人社团'],
     ['非洲', '巴西',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=BRA&country_name=巴西&kind_name=华人社团'],
     ['非洲', '哥伦比亚',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=COL&country_name=哥伦比亚&kind_name=华人社团'],
     ['非洲', '圭亚那',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=GUY&country_name=圭亚那&kind_name=华人社团'],
     ['非洲', '巴拉圭',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=PAR&country_name=巴拉圭&kind_name=华人社团'],
     ['非洲', '秘鲁',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=PER&country_name=秘鲁&kind_name=华人社团'],
     ['非洲', '乌拉圭',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=URU&country_name=乌拉圭&kind_name=华人社团'],
     ['非洲', '智利',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=CHI&country_name=智利&kind_name=华人社团'],
     ['非洲', '厄瓜多尔',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=ECU&country_name=厄瓜多尔&kind_name=华人社团'],
     ['非洲', '苏里南',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=SUR&country_name=苏里南&kind_name=华人社团'],
     ['亚洲', '本州全部',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=all&country_name=本州全部&kind_name=华人社团'],
     ['亚洲', '委内瑞拉',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=VEN&country_name=委内瑞拉&kind_name=华人社团'],
     ['亚洲', '阿根廷',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=ARG&country_name=阿根廷&kind_name=华人社团'],
     ['亚洲', '玻利维亚',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=BOL&country_name=玻利维亚&kind_name=华人社团'],
     ['亚洲', '巴西',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=BRA&country_name=巴西&kind_name=华人社团'],
     ['亚洲', '哥伦比亚',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=COL&country_name=哥伦比亚&kind_name=华人社团'],
     ['亚洲', '圭亚那',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=GUY&country_name=圭亚那&kind_name=华人社团'],
     ['亚洲', '巴拉圭',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=PAR&country_name=巴拉圭&kind_name=华人社团'],
     ['亚洲', '秘鲁',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=PER&country_name=秘鲁&kind_name=华人社团'],
     ['亚洲', '乌拉圭',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=URU&country_name=乌拉圭&kind_name=华人社团'],
     ['亚洲', '智利',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=CHI&country_name=智利&kind_name=华人社团'],
     ['亚洲', '厄瓜多尔',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=ECU&country_name=厄瓜多尔&kind_name=华人社团'],
     ['亚洲', '苏里南',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=SUR&country_name=苏里南&kind_name=华人社团'],
     ['大洋洲', '本州全部',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=all&country_name=本州全部&kind_name=华人社团'],
     ['大洋洲', '委内瑞拉',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=VEN&country_name=委内瑞拉&kind_name=华人社团'],
     ['大洋洲', '阿根廷',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=ARG&country_name=阿根廷&kind_name=华人社团'],
     ['大洋洲', '玻利维亚',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=BOL&country_name=玻利维亚&kind_name=华人社团'],
     ['大洋洲', '巴西',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=BRA&country_name=巴西&kind_name=华人社团'],
     ['大洋洲', '哥伦比亚',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=COL&country_name=哥伦比亚&kind_name=华人社团'],
     ['大洋洲', '圭亚那',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=GUY&country_name=圭亚那&kind_name=华人社团'],
     ['大洋洲', '巴拉圭',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=PAR&country_name=巴拉圭&kind_name=华人社团'],
     ['大洋洲', '秘鲁',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=PER&country_name=秘鲁&kind_name=华人社团'],
     ['大洋洲', '乌拉圭',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=URU&country_name=乌拉圭&kind_name=华人社团'],
     ['大洋洲', '智利',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=CHI&country_name=智利&kind_name=华人社团'],
     ['大洋洲', '厄瓜多尔',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=ECU&country_name=厄瓜多尔&kind_name=华人社团'],
     ['大洋洲', '苏里南',
      'http://www.chinesecome.com/csi_custom.jspx?tpl=qqhr_gjxx&area=SouthAmerica&kind=ggqk&country=SUR&country_name=苏里南&kind_name=华人社团']]
    """
    siteList = []
    try:
        for key,value in Areas.items():
            countryDict[key] = getCountryList(key,value)
    finally:
        print("所有国家：",countryDict)
        try:
            for key,value in countryDict.items():
                for country in value[0]:
                    print(key)
                    getAssociationList(Areas[key], value[1][value[0].index(country)], country)
                    siteList.append([key,country,getAssociationList(Areas[key], value[1][value[0].index(country)], country)])
        finally:
            #print(siteList)
            for item in siteList:
                item.append(getAssociation(item[2]))
            #print(siteList)

    # 创建工作簿
    file_name = "表格1.xlsx"
    workbook = xlsxwriter.Workbook(file_name)

    # 创建工作表
    worksheet = workbook.add_worksheet('学校')

    # 写单元格
    worksheet.write(0, 0, '地区')
    worksheet.write(0, 1, '国家')
    worksheet.write(0, 2, '机构')

    # 写行
    i = 1
    for item in siteList:
        worksheet.write_row(i, 0, [item[0], item[1], "\r\n".join(item[3])])
        i = i+1

    # 关闭工作簿
    workbook.close()