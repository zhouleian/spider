# coding=utf-8

from bs4 import BeautifulSoup
import re,socket,urllib2,random
import cookielib
import tool
ERROR = {
    '0': 'Can not open the url,checck you net',
    '1': 'Creat download dir error',
    '2': 'The image links is empty',
    '3': 'Download faild',
    '4': 'Build soup error,the html is empty',
    '5': 'Can not save the image to your disk',
}

class BrowserBase(object):
    """模拟浏览器"""
    def __init__(self):
        socket.setdefaulttimeout(20)
        #self.HTML = ''
        self.articleName = ''
        self.link = ''
        self.fileArticle = fileArticle
        self.url = url
        self.tool = tool.Tool()

    def speak(self, name, content):
        print '[%s]%s' % (name, content)

    def openurl(self, url):
        """
        打开网页
        """
        # 声明一个CookieJar对象实例来保存cookie
        cookie = cookielib.CookieJar()
        # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
        cookie_support = urllib2.HTTPCookieProcessor(cookie)
        self.opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(self.opener)
        user_agents = [
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
            'Opera/9.25 (Windows NT 5.1; U; en)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
            'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
            'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
            "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
            "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",

        ]
        agent = random.choice(user_agents)
        self.opener.addheaders = [("User-agent", agent), ("Accept", "*/*"), ('Referer', 'http://www.google.com')]
        try:
            res = self.opener.open(url)
            return res.read()
        except Exception, e:
            self.speak(str(e), url)
            raise Exception

    # 获取文章的题目
    def getArticleName(self,eachTag):
        re_rules = r'<a href=.*?"(.*?)</span>'
        p = re.compile(re_rules, re.DOTALL)
        title = p.findall(str(eachTag))
        #print title[0]
        if 'font' in title[0]:
            pattern = re.compile('</font>(.*?)</a>', re.S)
        else:
            pattern = re.compile('>(.*?)</a>',re.S)
        eachTitle = re.findall(pattern, title[0])
        return eachTitle[0].strip()
    # 获取文章的链接
    def getArticleHtml(self, eachTag):
        pattern = re.compile('<a href="(.*?)"', re.S)
        eachHtml = re.findall(pattern,str(eachTag))
        articleHtml = 'http://blog.csdn.net' + eachHtml[0]
        return articleHtml

    def start(self):
        """get the main article of CSDN blog"""
        pageCode = self.openurl(self.url)
        soup = BeautifulSoup(pageCode)
        #tags:所给地址页面代码中与每一篇文章对应的源代码
        tags = soup.findAll('div', {'class': 'article_title'})
        #获取题目和链接
        for eachTag in tags:
            articleTitle = self.getArticleName(eachTag)
            articleLink = self.getArticleHtml(eachTag)
            #保存到文件中
            self.fileArticle.write('\n' + articleTitle + "         " + articleLink + '\n')
            #爬取文章
            articlePageCode = self.openurl(articleLink)
            soup = BeautifulSoup(articlePageCode)
            #tags:具体文章页面对应的源代码
            tags = soup.findAll('div', {'id': 'article_content', 'class': 'article_content'})
            articleHtml = str(tags[0])
            articleHTML = '<html><meta charset="utf-8">' + articleHtml #不加这一句在浏览器中的显示是乱码
            #articleFile = open(articleTitle + '.html', 'w+')
            #articleFile.write(articleHTML)
            articleContents = self.tool.replace(articleHTML)
            articleFile = open(articleTitle + '.txt','w+')
            articleFile.write(articleContents)

fileArticle = open('articleFile.txt','w')
fileArticle.write('***************文章题目***************文章地址************')
url = raw_input('Input the links of CSDN article you needed!\n')
if url is None or len(url) == 0:
    url = 'http://blog.csdn.net/eastmount'
browser = BrowserBase()
#取得url的页面代码
browser.openurl(url)
browser.start()
fileArticle.close()







