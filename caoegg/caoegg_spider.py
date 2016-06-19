# coding=utf-8
import urllib2
import urllib
import re
import thread
import time

class Spider_caoegg:
    def __init__(self):
        self.page = 1
        self.stories = []
        self.enable = False
    #获得页面的代码
    def getPage(self,page):
        try:
            url = 'http://www.caoegg.cn/latest/' + str(page)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode("utf-8")
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print u"连接失败，错误原因：",e.reason
                return None
    #传入某一页代码，返回段子列表
    def getItems(self,page):
        pageCode = self.getPage(page)
        if not pageCode:
            return "页面加载失败......"
        pattern = re.compile('<a href="/view/.*?><span>(.*?)</span>', re.S)
        pageStories = re.findall(pattern, pageCode)
        # pageStories = []
        # for item in items:
        #     pageStories.append(item.strip())
        return pageStories
    #提取页面内容
    def loadPage(self):
        if self.enable == True:
            #如果当前未看的页数少于2页就加载新的一页
            if len(self.stories) < 2:
                try:
                    pageStories = self.getItems(self.page)
                    if pageStories:
                        self.stories.append(pageStories)
                        #page+1方便下次读取
                        self.page += 1
                except:
                    print '连接失败......'
    #每次回车返回一页的段子
    def getStories(self,pageStories,page):
        num = 0
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == 'quit':
                self.enable = False
                return
            num += 1
            print u'第%d页,第%d个:\n%s\n'%(page,num,story)
    def start(self):
        print u'正在读取.....'
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getStories(pageStories,nowPage)
spider = Spider_caoegg()
spider.start()
