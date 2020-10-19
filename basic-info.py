import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import re
import time
import csv
#coding: UTF-8
Jname = 'CQTQ' #期刊缩写
spec = False #1994-1999是否出现URL异常
startYear = 2014 #创刊年
endYear = 2014 #截止年
numbers = 4 #现在一年多少期
oldnumbers =4 #过去一年多少期
changeYear =2014 #从哪年开始，期刊数量增加


def main():
    # baseurl = 'https://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=BOOK404.000'  #这里也要记得改
    baseurl = 'https://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=BOOK198201001'
    URLs = getURLs(baseurl)
    getData(URLs)
    if spec == True:
        specURLs = getSpecURLs(baseurl)  #更改调用函数
        getData(specURLs)
    # getData([['https://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=BOOK404.000']])
    # print(URLs)


def getURLs(baseurl):
    filename =''
    URLs = []
    for year in range (startYear,endYear+1):
        if spec ==True:
            if year <1999 and year>=1994:
                continue
        # elif year >=2003 and year<=2012:
        #     continue
        for month in range(1,numbers+1):
            if oldnumbers<numbers:
                if year<changeYear and month>oldnumbers:
                    continue
            # if year<=1996 and month>=7:
            #     continue
            GroupURL = []
            for num in range(0,80):
                if month>=10 and num>=10:
                    filename = Jname+ str(year) + str(month) + '0' +str(num)
                elif month>=10 and num<10:
                    filename = Jname +str(year) +str(month) +'00'+str(num)
                elif month <10 and num>=10:
                    filename = Jname +str(year)+'0'+str(month)+'0'+str(num)
                else:
                    filename = Jname +str(year)+'0'+str(month)+'00'+str(num)
                GroupURL.append(baseurl.replace(baseurl[66:],filename))
    # print(URLs)
            URLs.append(GroupURL)
    return URLs

def getSpecURLs(baseurl):
    URLs = []
    filename = ''
    mons =['01','02','03','04','05','06'] #暂时这样，毕竟90年代就一年12期的太少了
    # mons = ['01', '02', '03', '04']
    years = ['4','5','6','7','8','9']
    for year in years:
        for month in mons:
            GroupURL = []
            for num in range(1,100):
                if num<10:
                    filename = Jname + year + month +'.00'+ str(num)
                else:
                    filename = Jname +year +month +'.0' +str(num)
                GroupURL.append(baseurl.replace(baseurl[66:],filename))
            URLs.append(GroupURL)
    print(len(URLs))
    return URLs


def getData(URLs):
    counter =0
    f = open('info-'+Jname+'.csv','a',newline='',encoding='utf-8-sig') #需要追加时候在这里改
    # f = open('info-QBXB.csv', 'w', newline='', encoding='utf-8-sig')
    csv_writer =csv.writer(f)
    dataList =[]
    find_title = re.compile(r'<h1>(.*?)</h1>',re.S)
    find_author = re.compile(r"TurnPageToKnetV\('au','(.*?)','\d*",re.S)
    find_authorID = re.compile(r'<input class="authorcode" type="hidden" value="(.*?)">',re.S)
    find_abstract = re.compile(r'<span id="ChDivSummary" name="ChDivSummary" class="abstract-text">(.*?)</span>',re.S)
    find_keywords = re.compile(r"TurnPageToKnetV\('kw','(.*?)','",re.S)
    find_info = re.compile(r'<p class="total-inform"><span>(.*?)</span></p>',re.S)
    find_author_ex = re.compile(r'<h3 class="author" id="authorpart"><span>(.*?)</span></h3>')
    for i in range(0, len(URLs)):
        for j in range(0, len(URLs[i])):
            data =[]
            html = str(askURL(URLs[i][j]))
            if(html =='none'):  #如果一个链接走不通，那就跳出这个i,直接进入下个月的期刊
                break
            elif html =='spec':
                continue
            author = re.findall(find_author,html)
            authorID = re.findall(find_authorID,html)
            if len(author) == 0:
                author =re.findall(find_author_ex,html)
                if(len(author)) == 0:
                    continue
                else:
                    author[0]=author[0].replace('</span><span>','|')
                    authorID = ['']
            title = re.findall(find_title,html)
            abstract = re.findall(find_abstract,html)
            keywords = re.findall(find_keywords,html)
            info = re.findall(find_info,html)
            # 题目
            data.append(title[0])
            # data.append(author)
            # data.append(authorID)
            # 作者信息
            authorInfo = ''
            for a in range(0,len(author)):
                authorInfo =authorInfo + author[a]+':'+authorID[a]+'|'
            data.append(authorInfo)
            # 页数
            p_index = info[0].index('页数')
            page = info[0][p_index+3:p_index+6].strip(';,<,/')
            data.append(page)
            # 关键词
            keywords_bar = ''
            for keyword in keywords:
                keywords_bar = keywords_bar+keyword+';'
            data.append(keywords_bar)
            # 摘要
            if len(abstract) == 1:
                data.append(abstract[0])
            else:
                data.append('')

            # 自己的filename
            # data.append(URLs[i][j][66:77]) #记得过一会改这里,90年代
            data.append(URLs[i][j][66:])
            counter = counter+1
            print(data)
            csv_writer.writerow(data)
            print(counter)
    f.close()

def askURL(url):
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'}
    # 让服务器认为这是一个浏览器
    try:
        # time.sleep(0.5)
        request = urllib.request.Request(url, headers=head)  # 封装一个request，拿去一起访问
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        htmlChecker = str(html)
        # print(html)
        if htmlChecker.find('所查找的文献不存在') >= 0:
            # print(html)
            # print(len(htmlChecker))
            # print(url)
            html = 'none'
        elif len(htmlChecker) == 54 or htmlChecker.find('对不起，服务器忙，请稍后再操作') >= 0:
            print(url)
            for i in range(0, 21):
                response = urllib.request.urlopen(request)
                html = response.read().decode('utf-8')
                if len(str(html)) == 54:
                    continue
                elif str(html).find('对不起，服务器忙，请稍后再操作') >= 0:
                    continue
                elif str(html).find('所查找的文献不存在') >= 0:
                    html = 'none'
                    return html
                else:
                    return html
    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
            if url[-3:] == '000' or url[-3:] == '001' or url[-3:] == '002' or url[-3:] =='003':
                return 'spec'
            return 'none'
        if hasattr(e, 'reason'):
            print(e.reason)
            return 'none'
    return html


if __name__ == '__main__':
    main()

