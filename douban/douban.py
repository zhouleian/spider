# coding=utf-8

#一个简单的Python爬虫, 用于抓取豆瓣电影Top前100的电影的名称
import urllib2
import re
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
#https://movie.douban.com/top250?start=25&filter=
class Spider:
    def __init__(self):
        self.movies = []
        self.page = 0
        self.baseURL = 'https://movie.douban.com/top250'
        self.topNum = 1
        print "正在爬取Top100的电影......"
    #获取页面代码
    def getPageCode(self,page):
        try:
            page = (self.page - 1) * 25
            url = self.baseURL + '?start={' + str(page) + '}&filter='
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode("utf-8")
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print u"连接失败，错误原因：", e.reason
                return None
    #提取电影名称
    def getTitle(self,pageCode):
        pattern = re.compile('<span class="title">(.*?)</span>',re.S)
        items = re.findall(pattern,pageCode)
        print items
        tempMovies = []
        for index,item in enumerate(items):
             if item.find("&nbsp")==-1:
                 tempMovies.append("Top" + str(self.topNum) + " " + item)
                 self.topNum += 1
        self.movies.extend(tempMovies)
    def start(self):
        while self.page <= 3:
            pageCode = self.getPageCode(self.page)
            self.getTitle(pageCode)
            self.page += 1
        self.saveMovies()
    def saveMovies(self):
        fileName = "Top100 Movies.txt"
        file = open(fileName,'w+')
        self.movies = [movie + '\n' for movie in self.movies]
        for movie in self.movies:
            file.write(movie)
        file.close()
spider = Spider()

#partCode.group(1)是提取出的那段代码
spider.start()
# for movie in spider.movies:
#     print movie
print "爬取结束......"

