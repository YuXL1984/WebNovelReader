# coding: utf-8

from leancloud import Object
from leancloud import Query
import urllib,urllib2,time
import re
from bs4 import BeautifulSoup
from header import *

class BookRack(Object):

    def networkRequestForData(self,url,data):
        index=1
        while(True):
            if(index==10):
                print "failed can't find the book"
                return 'nonono'
            print 'working>> serch time',index,'most time 10'
            index+=1
            time.sleep(random.random() * 5)
            req_header = getHeader()
            req = urllib2.Request(url, None, req_header)
            resp=urllib2.urlopen(
                req,
                data=urllib.urlencode(data)
            )
            html = resp.read()
            soup = BeautifulSoup(html, 'html.parser', from_encoding='gbk')

            if (not resp.getcode() == 200):
                print 'time out！ repeat', url
                continue
            try:
                ispage = soup.find('title').get_text()
                if ('顶点小说手机版' in ispage or '顶点小说' in ispage):
                    print 'OK'
                    return soup
            except:
                print 'errorpage repeat', url
        return

    def networkRequest(self,url):
        index=1
        while(True):
            if(index==10):
                print "failed can't find the book"
                return 'nonono'
            print 'working>> serch time',index,'most time 10'
            index+=1
            time.sleep(random.random() * 5)
            req_header = getHeader()
            req = urllib2.Request(url, None, req_header)
            resp=urllib2.urlopen(req)
            html = resp.read()
            soup = BeautifulSoup(html, 'html.parser', from_encoding='gbk')

            if (not resp.getcode() == 200):
                print 'time out！ repeat', url
                # return 'time out！ repeat', url
                continue
            try:
                ispage = soup.find('title').get_text()
                if ('顶点小说手机版' in ispage or '顶点小说' in ispage):
                    print 'OK'
                    return soup
            except:
                print 'errorpage repeat', url
        return

    def searchBook(self,searchStr,searchType='articlename'):
        #按书名搜索Type = articlename
        #按作者搜索Tyoe = author
        url='http://m.23wx.com/modules/article/search.php'
        data = {'searchtype':'articlename','searchkey':searchStr.encode('gbk')}
        soup = self.networkRequestForData(url,data)
        if soup is 'nonono':
            return '无法找到数据源'
        else:
            resultList = []
            resultDic = {}
            if soup.select('.cover'):
                lineList = soup.select('.cover .line')

                for line in lineList:
                    aList = line.select('a')
                    bookInfoDic = {'fenlei':'','fenleiUrl':'','book':'','bookUrl':'','zuozhe':'','zuozheUrl':''}
                    # resultDic = {'bookName':'','bookInfo':''}
                    resultDic = {'bookInfo':''}
                    for a in aList:
                        # rDic['bookName'] = aList[1].text
                        # print a.text
                        url = a['href']
                        if 'http://m.23wx.com' in url:
                            url = a['href']
                        else:
                            url = 'http://m.23wx.com'+url
                        if 'http://m.23wx.com/class/' in url:
                            bookInfoDic['fenlei'] = a.text
                            bookInfoDic['fenleiUrl'] = url
                        if 'http://m.23wx.com/book/' in url:
                            bookInfoDic['book'] = a.text
                            bookInfoDic['bookUrl'] = url
                        if 'http://m.23wx.com/author/' in url:
                            bookInfoDic['zuozhe'] = a.text
                            bookInfoDic['zuozheUrl'] = url

                    resultDic['bookInfo'] = bookInfoDic
                    resultList.append(resultDic)
                return resultList
            else:
                return '没有搜索到结果'

    def getBookInfo(self,bookUrl):
        bookInfoDic = {'shuming':'','zuozhe':'','fenlei':'','zhuangtai':'','gengxin':'','zuixin':'','jianjie':'','muluUrl':'','imageUrl':''}
        # url = bookUrl.replace('http://','')
        soup = self.networkRequest(bookUrl)
        if soup != 'nonono':

            novel_div = soup.find('div',class_='cover')
            muluUrlInfo = novel_div.find('div',class_="ablum_read")
            muluUrl=muluUrlInfo.find(href=re.compile("http://m.23wx.com/html/"))
            muluUrl1 = muluUrl['href']
            bookInfoDic['muluUrl'] = muluUrl1

            bookimageInfo = novel_div.find('div',class_="block_img2")
            bookimage=bookimageInfo.find(src=re.compile("http://"))
            imageUrlStr = bookimage['src']
            bookInfoDic['imageUrl'] = imageUrlStr

            bookTempInfo = novel_div.find('div',class_="block_txt2")
            bookTempInfoText = bookTempInfo.text
            bookTempInfoList = bookTempInfoText.split('\n')
            for tempStr in bookTempInfoList:
                tempStr.strip().lstrip().rstrip('\/')
                if len(tempStr) > 0:
                    if '作者：' in tempStr:
                        tempStrSplit = tempStr.split('：')
                        bookInfoDic['zuozhe'] = tempStrSplit[1]
                    if '分类：' in tempStr:
                        tempStrSplit = tempStr.split('：')
                        bookInfoDic['fenlei'] = tempStrSplit[1]
                    if '状态：' in tempStr:
                        tempStrSplit = tempStr.split('：')
                        bookInfoDic['zhuangtai'] = tempStrSplit[1]
                    if '更新：' in tempStr:
                        tempStrSplit = tempStr.split('：')
                        bookInfoDic['gengxin'] = tempStrSplit[1]
                    if '最新：' in tempStr:
                        tempStrSplit = tempStr.split('：')
                        bookInfoDic['zuixin'] = tempStrSplit[1]

            jianjieTempText = novel_div.find('div',class_="intro_info").text.replace('\n', '')
            jianjieTempList = jianjieTempText.split(' ')
            jianjieTemp ="".join(jianjieTempList)
            bookInfoDic['jianjie'] = jianjieTemp

            novel_div1 = soup.find('div',class_='header')
            shumingTextList = novel_div1.text.split('\n')
            shumingText = shumingTextList[2]
            bookInfoDic['shuming'] = shumingText
            return bookInfoDic
        else:
            return '没有找到数据源'


    def getBookDirectory(self,directoryUrl,directoryType='1'):
    #directoryType = '1' 为倒序,默认倒序
    #directoryType = '0' 为正序
        bookDirectoryList = []
        soup = self.networkRequest(directoryUrl)

        pageCalssFind = soup.find('ul',class_='chapter')
        hrefFindList = pageCalssFind.find_all(href=re.compile('.html'))
        for hrefInfo in hrefFindList:
            hrefText = hrefInfo.text
            if '/html/' in hrefInfo['href']:
                hrefUrl = 'http://m.23wx.com'+hrefInfo['href']
            else:
                hrefUrl = directoryUrl+hrefInfo['href']
            # print hrefText
            # print hrefUrl
            bookDirectoryDic = {'zhangjieName':hrefText,'zhangjieUrl':hrefUrl}
            bookDirectoryList.append(bookDirectoryDic)
        return bookDirectoryList

    def getBookPage(self,bookPageUrl):

        soup = self.networkRequest(bookPageUrl)
        content_ClassFind = soup.find('div',class_='content')
        title = content_ClassFind.find('h1',id= 'nr_title').text
        txt_ClassFind = content_ClassFind.find('div',class_='txt')
        txt = txt_ClassFind.text
        bookontentDic = {'title':title,'content':txt}
        return bookontentDic

#s=BookRack()

# s.searchBook('重卡')

# s.getBookInfo('http://m.23wx.com/book/61660')

#s.getBookDirectoryFormWWW('http://m.biquga.com/10_10051/')

# s.getBookDirectory('http://m.23wx.com/html/64/64384/')

#s.getBookPage('http://m.23wx.com/html/64/64384/27638368.html')