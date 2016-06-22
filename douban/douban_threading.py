# coding=utf-8
import threading
import Queue,time
import re,string
import urllib2
import sys

reload(sys)
sys.setdefaultencoding('utf8')

movies = []
topNum = 1
share_q = Queue.Queue()
thread_number = 3

class MyThread(threading.Thread):
    def __init__(self,func):
        super(MyThread, self).__init__()
        self.func = func
    def run(self):
        self.func()
def worker():
    global share_q
    while not share_q.empty():
        url = share_q.get()
        pageCode = getPageCode(url)
        getTitle(pageCode)
        time.sleep(1)
        share_q.task_done()

#页面代码
def getPageCode(url):
    try:
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
# 提取电影名称
def getTitle(pageCode):
    global topNum
    #global movies
    pattern = re.compile('<span class="title">(.*?)</span>', re.S)
    items = re.findall(pattern, pageCode)
    print items
    tempMovies = []
    for index, item in enumerate(items):
        if item.find("&nbsp") == -1:
            tempMovies.append("Top" + str(topNum) + " " + item)
            topNum += 1
    movies.extend(tempMovies)
def saveMovies():
    global movies
    fileName = "Top250 Movies.txt"
    file = open(fileName, 'w+')
    movies = [movie + '\n' for movie in movies]
    for movie in movies:
        file.write(movie)
    file.close()
def main():
    global share_q
    threads = []
    baseURL = "http://movie.douban.com/top250?start={page}&filter=&type="
    # 向队列中放入任务, 真正使用时, 应该设置为可持续的放入任务
    for index in xrange(10):
        share_q.put(baseURL.format(page=index * 25))
    for i in xrange(thread_number):
        thread = MyThread(worker)
        thread.start()  # 线程开始处理任务
        threads.append(thread)
    for thread in threads:
        thread.join()
    share_q.join()
    saveMovies()
if __name__=='__main__':
    main()
