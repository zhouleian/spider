# coding=utf-8

import re
import requests
import os
import urllib2
import urllib
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
class Spider():
    def __init__(self):
        self.baseURL = baseURL
        self.page = 1235
        self.images = []
        self.contents = []
        print "开始爬取......"
    #获取网页代码
    def getPageCode(self,page):
        try:
            url = baseURL + str(page)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            code = response.read().decode("utf-8")
            pat = re.compile('<div class="tab-content">(.*?)<div class="one-pubdate">', re.S)
            pageCode = re.search(pat, code).group(1)
            return pageCode
        except urllib2.URLError,e:
            if hasattr(e,"code"):
                print e.code
            if hasattr(e,"reason"):
                print u"连接失败......",e.reason

    #图片地址pic,介绍intro
    def getContents(self,pageCode):
        temp_contents = []
        pattern = re.compile('<img src="(.*?)"',re.S)
        pic = re.findall(pattern,pageCode)
        p = re.compile('<div class="one-titulo">(.*?)</div>',re.S)
        number = re.findall(p,pageCode)
        pa = re.compile('<div class="one-cita">(.*?)</div>',re.S)
        intro = re.findall(pa,pageCode)
        self.contents.append(intro[0].strip() + "  " +number[0].strip() + "\n" + pic[0].strip() + "\n")
        #把图片单独提取出来
        self.images.append(pic[0].strip())
    #保存contents
    def saveContents(self):
        fileName = "one.txt"
        f = open(fileName,'w+')
        self.contents = [content + '\n' for content in self.contents]
        for content in self.contents:
            f.write(content)
        f.close()
    #保存图片
    def saveImages(self):
        fileName = "images.txt"
        f = open(fileName, 'w+')
        self.images = [image + '\n' for image in self.images]
        for image in self.images:
            f.write(image)
        f.close()
    #下载图片
    def loadImages(self):
        imagePath = os.getcwd() + '/image'
        if not os.path.exists(imagePath):
            os.mkdir(imagePath)
        x = 1
        for imageUrl in self.images:
            temp = imagePath + '/%s.jpg' %x
            print u"正在下载第%s张图片" %x
            try:
                urllib.urlretrieve(urllib2.urlopen(imageUrl).geturl(),temp)
            except:
                print u"该图片下载失败：%s"%imageUrl
            x += 1
    def start(self):
        while self.page < 1255:
            pageCode = self.getPageCode(self.page)
            self.getContents(pageCode)
            self.page += 1
        self.saveImages()
        self.saveContents()
        self.loadImages()
baseURL = 'http://wufazhuce.com/one/'
spider = Spider()
spider.start()