# coding=utf-8


import urllib2
import urllib
import re
#http://tieba.baidu.com/p/3138733512?see_lz=1&pn=1

#处理页面标签类
class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()

class BDTB:
    def __init__(self,baseURL,seeLz,floorTag):
        self.baseURL = baseURL
        self.tool = Tool()
        self.floorTag = floorTag
        self.defaultTitle = u"百度贴吧"
        self.file = None
        self.floor = 1
        self.page = 1
        self.seeLz = '?see_lz=' + str(seeLz)
    def getPageCode(self,page):
        try:
            url = self.baseURL + self.seeLz + '&p=' + str(page)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            #print response.read()
            pageCode = response.read().decode("utf-8")
            return pageCode
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print u'连接失败......' + e.reason
                return None

    #提取相关信息
    def getTitle(self,pageCode):
        #pageCode = self.getPageCode(page)
        pattern = re.compile('<h3 class="core_title_txt .*?>(.*?)</h3>',re.S)
       # pattern = re.compile('<h1 class="core_title_txt.*?>(.*?)</h1>',re.S)
        title = re.search(pattern,pageCode)
        if title:
            return title.group(1).strip()
        else:
            return None
    #提取帖子页数
    def getPageNum(self,pageCode):
        #pageCode = self.getPageCode(page)
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
        pageNum = re.search(pattern,pageCode)
        if pageNum:
            return pageNum.group(1).strip()
        else:
            return None
    #帖子的内容
    def getContent(self,pageCode):
        #pageCode = self.getPageCode(page)
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
        items = re.findall(pattern,pageCode)
        contents = []
        for item in items:
            content = "\n" + self.tool.replace(item) + "\n"
            contents.append(content.encode("utf-8"))
        return contents
    #写入文件
    def setFileTitle(self,title):
        if title is not None:
            self.file = open(title + ".txt","w+")
        else:
            self.file = open(self.defaultTitle + ".txt","w+")
    #
    def writeData(self,contents):
        for content in contents:
            if self.floorTag == '1':
                floorLine = "\n" + str(self.floor) + u"-----------------"
                self.file.write(floorLine)
            self.file.write(content)
            self.floor += 1

    def start(self):
        pageCode = self.getPageCode(1)
        title = self.getTitle(pageCode)
        pageNum = self.getPageNum(pageCode)
        print 'pageNum = ',pageNum
        print 'title = ' ,title
        self.setFileTitle(title)
        if pageNum == None:
            print " URL失效......"
            return
        try:
            print "该贴子共有" + str(pageNum) + "页"
            for i in range(1,int(pageNum)+1):
                print "正在写入第" + str(i) + "页数据"
                pageCode = self.getPageCode(i)
                contents = self.getContent(pageCode)
                self.writeData(contents)
        except IOError,e:
            print "异常，原因:" + e.message
        finally:
            print "写入完成"

baseURL = 'http://tieba.baidu.com/p/3138733512'
#baseURL = 'http://tieba.baidu.com/p/'+str(raw_input(u'http://tieba.baidu.com/p/'))
#3138733512'?see_lz=1&pn=1
seeLz = raw_input("是否只获的楼主的发言，是：1,否：0\n")
floorTag = raw_input("是否写入楼层信息，是：1,否：0\n")
test = BDTB(baseURL,seeLz,floorTag)
test.start()



