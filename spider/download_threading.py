# coding=utf-8
from bs4 import BeautifulSoup
import re, socket, urllib2, random
import cookielib
import os, threading, Queue
from time import ctime
import time
import tool

ERROR = {
    '0': 'Can not open the url,checck you net',
    '1': 'Creat download dir error',
    '2': 'The image links is empty',
    '3': 'Download faild',
    '4': 'Build soup error,the html is empty',
    '5': 'Can not save the image to your disk',
}
traveloguePath = os.getcwd() + '/401-500'
if not os.path.exists(traveloguePath):
    os.mkdir(traveloguePath)
page = 401
num = 4000
share_q = Queue.Queue()
thread_number = 35
class MyThread(threading.Thread):
    def __init__(self, func, url, fileArticle):
        super(MyThread, self).__init__()
        self.func = func
        socket.setdefaulttimeout(20)
        self.fileArticle = fileArticle
        self.url = url
        #self.page = page
        #self.num = num
        self.tool = tool.Tool()
        #self.traveloguePath = traveloguePath
    def run(self):
        self.func(self.url,self.fileArticle,self.tool)
def speak(name, content):
    print '[%s]%s' % (name, content)
def openurl(url):
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        pageCode = response.read()
        return pageCode
    except urllib2.URLError, e:
        if hasattr(e, "reason"):
            print "连接失败......" + e.reason
        return None
# 获取文章的题目
def getArticleName(eachTag):
    re_rules = r'<dt class="ellipsis">(.*?)</dt>'
    p = re.compile(re_rules, re.DOTALL)
    title = p.findall(str(eachTag))
    return title[0].strip()
# 获取文章的链接
def getArticleHtml(eachTag):
    pattern = re.compile('<a class="journal-item cf" href="(.*?)"', re.S)
    eachHtml = re.findall(pattern, str(eachTag))
    articleHtml = 'http://you.ctrip.com' + eachHtml[0]
    return articleHtml

def worker(url, fileArticle,tool):
    """get all travelogues"""
    global share_q
    while not share_q.empty():
        url = share_q.get()
        pageCode = openurl(url)
        soup = BeautifulSoup(pageCode)
        # tags:所给地址页面代码中与所有文章对应的源代码
        tags = soup.findAll('a', {'class': 'journal-item cf'})
        # 获取题目和链接
        for eachTag in tags:
            global num
            articleTitle = getArticleName(eachTag)
            articleLink = getArticleHtml(eachTag)
            # 保存到文件中
            fileArticle.write('\n' + articleTitle + "         " + articleLink + ' page = ' + str(page) + '\n')
            # 爬取文章
            articlePageCode = openurl(articleLink)
            soup = BeautifulSoup(articlePageCode)
            # tags:具体文章页面对应的源代码
            tags = soup.findAll('div', {'class': 'ctd_content'})
            articleHtml = str(tags[0])
            articleHTML = '<html><meta charset="utf-8">' + articleHtml  # 不加这一句在浏览器中的显示是乱码
            # 提取为纯文本
            articleContents = tool.replace(articleHTML)
            os.chdir(traveloguePath)
            num += 1
            articleFile = open(str(num) + '.txt', 'w+')
            articleFile.write(articleContents)
        share_q.task_done()


def main():
    global share_q
    #线程列表
    global page
    threads = []
    fileArticle = open('travelogue5.txt', 'w')
    baseUrl = 'http://you.ctrip.com/travels/china110000/t1-p{page}-m2.html'
    timeStart = time.time()
    print "start at: ",ctime()
    while page <= 500:
        share_q.put(baseUrl.format(page=page))
        page += 1
    url = baseUrl.format(page=page)
    for i in xrange(thread_number):
        thread = MyThread(worker,url, fileArticle)
        thread.start()  # 线程开始处理任务
        threads.append(thread)
    for thread in threads:
        thread.join()
    share_q.join()
    timeEnd = time.time()
    print "end at : ",ctime()
    print "this way takes %s s"%(timeEnd - timeStart)
    fileArticle.close()

if __name__ == '__main__':
    main()
