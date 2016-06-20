# coding=utf-8

import urllib
import urllib2
import re
import tool
import os
#https://mm.taobao.com/json/request_top_list.htm?page=2
class Spider:
    def __init__(self):
        self.baseURL = 'http://mm.taobao.com/json/request_top_list.htm'
        self.tool = tool.Tool()

    def getPageCode(self,page):
        url = self.baseURL + '?page=' + str(page)
        print url
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode("gbk")
            return pageCode
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print "连接失败......" + e.reason
            return None
    #提取页面内容，
    def getContents(self,page):
        pageCode = self.getPageCode(page)
        pattern = re.compile('<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',re.S)
        result = re.findall(pattern,pageCode)
        contents = []
        for content in result:
            contents.append([content[0],content[1],content[2],content[3],content[4]])
        return contents
    #个人详情页的页面代码
    def getDetailPage(self,infoURL):
        #request = urllib2.Request(infoURL)
        response = urllib2.urlopen(infoURL)
        detailCode = response.read().decode('gbk')
        return detailCode
    #获取个人简介
    def getBrief(self,detailCode):
        pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
        brief = re.search(pattern,detailCode)
        #print brief
        return self.tool.replace(brief.group(1))
    #获取页面上的所有的照片
    def getAllImage(self,detailCode):
        pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
        content = re.search(pattern,detailCode)
        #从代码中进一步提取出图片
        pattern_img = re.compile('<img.*?src="(.*?)"',re.S)
        images = re.findall(pattern_img,content.group(1))
        return images
    #保存图片
    def saveImages(self,images,name):
        num = 1
        print u"发现",name,"的",len(images),"张图片："
        for imageURL in images:
            split = imageURL.split('.')
            fTail = split.pop()
            if len(fTail) > 3:
                fTail = 'jpg'
            fileName = name + "/" + str(num) + "." +fTail
            self.saveImage(imageURL,fileName)
            num += 1
    def saveImage(self,imageURL,fileName):
        request = urllib2.Request(imageURL)
        result = urllib2.urlopen(request)
        data = result.read()
        f = open(fileName,"wb")
        f.write(data)
        print "正在保存它的图片为：",fileName
        f.close()
    #保存头像
    def saveIcon(self,iconURL,name):
        split = iconURL.split('.')
        fTail = split.pop()
        fileName = name + '/icon.' + fTail
        self.saveImage(iconURL,fileName)
    # 保存个人简介
    def saveBrief(self,content,name):
        fileName = name + '/' + name+'.txt'
        f = open(fileName,"w+")
        print u"正在保存信息为：" + fileName
        f.close()

    ##创建新目录
    def mkdir(self,path):
        path = path.strip()
        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists=os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            print u"偷偷新建了名字叫做",path,u'的文件夹'
            # 创建目录操作函数
            os.makedirs(path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print u"名为",path,'的文件夹已经创建成功'
            return False
    # item[0]个人详情URL,item[1]头像URL,item[2]姓名,item[3]年龄,item[4]居住地
    def savePageInfo(self,page):
        contents = self.getContents(page)
        for content in contents:
            print u"模特名字为：" + content[2] + u"芳龄:" + content[3]+u"居住在：" + content[4]
            print u"正在保存 ",content[2],u"的信息......"
            #获得个人信息页面的代码
            detailURL = "http:" + content[0]
            #print '-------',detailURL
            detailCode = self.getDetailPage(detailURL)
            print '===========',detailCode
            #提取个人简介
            brief = self.getBrief(detailCode)
            #提取所有的照片
            images = self.getAllImage(detailCode)
            self.mkdir(content[2])
            self.saveBrief(brief,content[2])
            iconURL = "http:" + content[1]
            self.saveIcon(iconURL,content[2])
            self.saveImages(images,content[2])
    #传入开始的页码，获取信息
    def savePagesInfo(self,start,end):
        for i in range(start, end + 1):
            print u"正在偷偷寻找第", i, u"个地方，看看MM们在不在"
            self.savePageInfo(i)

            # 传入起止页码即可，在此传入了2,10,表示抓取第2到10页的MM

spider = Spider()
spider.savePagesInfo(2,4)




























