# coding=utf-8
from bs4 import BeautifulSoup
import re,socket,urllib2,random
import cookielib
import os
import tool

"""爬取景点名和地点名"""

ERROR = {
    '0': 'Can not open the url,checck you net',
    '1': 'Creat download dir error',
    '2': 'The image links is empty',
    '3': 'Download faild',
    '4': 'Build soup error,the html is empty',
    '5': 'Can not save the image to your disk',
}

class Spider(object):
    """模拟浏览器"""
    def __init__(self):
        socket.setdefaulttimeout(20)
        self.articleName = ''
        self.link = ''
        self.filePlace = filePlace
        self.fileSight = fileSight
        self.url = url
        self.page = page
        self.tool = tool.Tool()

    def speak(self, name, content):
        print '[%s]%s' % (name, content)
    #获取页面的代码
    def openurl(self, url):
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            pageCode = response.read()
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print "连接失败......" + e.reason
            return None

    #获取地点名
    def getPlaceName(self,eachTag):
        pattern = re.compile('<i title="景点"></i><span>(.*?)</span>',re.S)
        placeName = re.findall(pattern,str(eachTag))
        return placeName[0]

    #获取地点的链接，placePage = 上海所具有的景点的页面
    def getPlaceHtml(self,placePage,eachTag):
        pattern = re.compile('<a href="(.*?)" target="_blank">',re.S)
        rawHtml = re.findall(pattern,str(eachTag))[0]
        #rawHtml = '/sightlist.shanghai2.html'需要的是'/sightlist.shanghai2/s0-p1.html'
        eachHtml =rawHtml[7:-5]
        placeRawHtml = 'http://you.ctrip.com/sightlist/' + eachHtml + '/s0-p{placePage}.html'
        placeHtml= placeRawHtml.format(placePage=placePage)
        #print placeHtml
        return placeHtml

    #获取某个地点所具有的景点的页数
    def getSightNumpage(self,placeCode):
        #读取某一个景点的页面源代码
        pattern = re.compile('<b class="numpage">(.*?)</b>',re.S)
        pageNum = re.findall(pattern,placeCode)
        return pageNum

    #获取景点名存在sight.txt中
    def getSightName(self,eachItem):
        # 获取景点名,保存在sight.txt中
        pattern = re.compile('<a href=".*?" title=".*?">(.*?)</a>', re.S)
        sightName = re.findall(pattern, str(eachItem))
        if len(sightName) == 0:
            pass
        else:
            self.fileSight.write(sightName[0] + '\n')
        #print sightName[0]

    #获取每一个景点的链接
    def getSightHtml(self,eachItem):
        pattern = re.compile('<a href="(.*?)"',re.S)
        sightRawHtml = re.findall(pattern,str(eachItem))
        sightHtml = 'http://you.ctrip.com' + sightRawHtml[0]
        #print sightHtml
        return sightHtml
    #获取对于每个景点的介绍
   # def getIntroduction(self,sightHtml):

    def start(self,page):
        #url是一开始的页面，中国景点推荐的页面
        pageCode = self.openurl(self.url)
        soup = BeautifulSoup(pageCode)
        # tags:所给地址页面代码中与所有地点对应的源代码
        tags = soup.findAll('div', {'class': 'list_mod1'})
        #print 'tags_len = ',len(tags)
        for eachTag in tags:
            placeName = self.getPlaceName(eachTag)
            #为防止出错后还要重新爬，景点名真得太多了
            if placeName in ('辽阳','菏泽','新昌','怒江'):
                 continue
            placeHtml = self.getPlaceHtml(1,eachTag) #是每一个城市地点的页面的链接
            #print placeHtml
            self.filePlace.write(placeName + '   ' + placeHtml + '\n')
            #pageNum是某个地点的景点总的页面数
            placeCode = self.openurl(placeHtml)
            #print placeCode
            sightPageNum = self.getSightNumpage(placeCode)
            #print sightPageNum
            #print len(sightPageNum)
            if len(sightPageNum) == 0:
                pageNum = 1
            else:
                pageNum = sightPageNum[0]
                pageNum = int(pageNum)
            #print pageNum
            # 还有页面时，从该页面的源代码中提取每一个景点的链接
            #对于每个城市的景点页面有很多个，所以要提取出这些页面的共公共部分，如：http://you.ctrip.com/sightlist/shanghai2/s0-p
            #placePageHtml即为公共部分，公共部分 + {sightPage}.html就是最终的页面
            placePageHtmlPart= placeHtml[:-6]
            while pageNum > 0:
                placePageHtml = placePageHtmlPart + str(pageNum) + '.html'
                placePageCode = self.openurl(placePageHtml)
                #print placePageCode
                soupSight = BeautifulSoup(placePageCode)
                items = soupSight.findAll('div',{'class':'list_mod2'})
                #eachItem是城市源代码中每一个对具体景点的代码,从这里面提取景点的链接和名字
                for eachItem in items:
                    # 获得景点名
                    self.getSightName(eachItem)
                    #获取景点链接
                    #sightHtml = self.getSightHtml(eachItem)
                pageNum -= 1

path = os.getcwd() + '/sights'
os.chdir(path)
filePlace = open('places.txt','w')
#sight.txt存放景点名
fileSight = open('sight.txt','w')
baseUrl = 'http://you.ctrip.com/countrysightlist/china110000/p{page}.html'
#page = 中国景点推荐的页面数
page = 171
# traveloguePath = os.getcwd() + '/sights'
# if not os.path.exists(traveloguePath):
#     os.mkdir(traveloguePath)
while page <= 192:
    url = baseUrl.format(page=page)
    browser = Spider()
    # 取得url的页面代码
    browser.start(page)
    page += 1

fileSight.close()
filePlace.close()