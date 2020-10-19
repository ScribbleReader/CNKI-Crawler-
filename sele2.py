import time
from math import floor
import csv
from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
import re
import os

#
# 代码思路：知网引文部分的页面进行循环，页面分成1-4个部分（图书引文部分由于太少出现忽略）对每一部分进行爬取，翻页，再爬取。
# 一个部分引文结束之后跳转到下一个部分。直到所有部分都被识别。
# 识别每一部分上方的’共xx条‘标签，除以10之后确定页数，翻页次数等于页数-1.每一次定位到 下一页 按钮进行翻页。
#
# 主要问题：
# 1、try finally 在识别到错误之后会自动跳出没有任何报错，如果希望找到报错地点应当采用try except结构，但是如果想有意忽略一些错误比如说无法定位到
# 某个标签，可以直接使用finally。
# 2、某些标签，比如说引文的链接，有可能有也有可能没有，如果没有就会报错返回一个nonetype,并且不能够使用if else识别，可以采用str（）强制转换为string
# 3、开始采用循环定位的方法添加各个引文，如果一个引文出错，整个函数会终止，导致这一页都没有记录，必须将可能出错的代码独立出去写成一个函数。
# 4、对于缺少某种类型引文的数据，比如没有博士的引文，只有硕士，后面识别会混乱，现在已经采用直接一次性获取标签然后传送排序的方法。


find_cited_filename = re.compile(r'filename=(.*?)&dbcode=')
bundles = os.walk('source_csv')
# areas = ['CJFQ','CDFD','CMFD','CPFD','IPFD']
# areas = ['CJFQ']
def main():
    for root, dirs, files in bundles:
        for name in files:
            f = open('./source_csv/'+ name, 'r', newline='', encoding='GBK')
            fc = open('./cite/'+ 'cite_'+ name, 'w', newline='', encoding='UTF-8-sig')
            csv_writer = csv.writer(fc)
            browser = webdriver.Firefox()
            for line in f:
                info = line.split(',')
                data = ''   # 用于储存采集的引用信息
                # print(info[1])
                info[1]=info[1].strip(' ,\n,\r')
                # print(len(info[1]))
                browser.get('https://kns.cnki.net/kcms/detail/search.aspx?sfield=cite&sKey=0&code=' + info[1] + '&dbcode=CJFD')
                time.sleep(1)
                areas = browser.find_elements_by_css_selector('.essayBox')
                for counter in range(0, len(areas)):
                    areas = browser.find_elements_by_css_selector('.essayBox')
                    piece = retrieve(browser, counter)
                    data = data + str(piece)
                    time.sleep(1)
                info.append(data)
                csv_writer.writerow(info)
            browser.close()
            fc.close()
            f.close()


def retrieve(browser, counter):
    data = ''
    try:
        areas = browser.find_elements_by_css_selector('.essayBox')
        area = areas[counter]
        data = getData(area)
        total = int(area.find_element_by_name('pcount').text)   #一共多少条
        pages = area.find_elements_by_css_selector('.pageBar span a')
        loop = floor(total / 10)
        while loop:
            for i in range(1, len(pages)):
                if pages[i].text == '下一页':
                    pages[i].click()
                    break
                elif i == len(pages) - 1:
                    break
                else:
                    continue
            time.sleep(2)
            areas = browser.find_elements_by_css_selector('.essayBox')
            area = areas[counter]
            pages = area.find_elements_by_css_selector('.pageBar span a')
            data = data + getData(area)
            loop = loop - 1
            time.sleep(2)
        time.sleep(1)
    finally:
        return data


def getData(area):
    data = ''
    lis = area.find_elements_by_css_selector('.ebBd li')
    for li in lis:
        ali = str(getItems(li))
        data = data + ali
        lis = area.find_elements_by_css_selector('.ebBd li')
    return str(data)

def getItems(li):
    data=''
    try:
        a = li.find_element_by_css_selector('a')
        href = a.get_attribute('href')
        cited_filename = re.findall(find_cited_filename, href)
        if isinstance(cited_filename, list):
            data = li.text[4:].strip(' ,\n,\r,\t,[,]') + ':' + str(cited_filename[0]) + '|'
    except Exception as e:
        print(e)
    else:
        return data

if __name__ == '__main__':
    main()