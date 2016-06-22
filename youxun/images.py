# coding=utf-8
'''
python下载游讯网的图片,共95页
'''
import re,time,urllib2,os,urllib

class Spider():
    def __init__(self):
        self.baseURL = baseURL
        self.page = 2
        self.fileUrl = fileUrl
        #count计算总共page页中包含的总的网页数
        self.count = 1
    #获取原始页面代码
    def getMainPageCode(self,page):
        url = self.baseURL + 'list/0_0_'+ str(page) + '.html'
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        pageCode = response.read()
        return pageCode
    #获取html中关于图片的部分代码,从中提取对应主题的URL,下载图片
    def getImages(self,pageCode):
        #获取主页面html中图片部分代码
        pat = re.compile(r'<div class="cbmiddle"(.*?)</div>',re.S|re.M)
        imageCodes = re.findall(pat,pageCode)
        #由图片代码提取Url
        for imageCode in imageCodes:
            if '_blank' in imageCode:
                #获取主题写入文件中
                patte = re.compile(r'<b class="imgname">(.*?)</b>',re.S|re.M)
                themeObj = re.search(patte,imageCode)
                theme = themeObj.group(1)
                print unicode(theme,'utf-8')
                self.fileUrl.write("\n--------theme : " + theme + '------------\n')
                #获取Url
                pattern = re.compile('<a target="_blank" href="(.*?)"',re.S)
                imageHtmls = re.findall(pattern,imageCode)
                for imageHtml in imageHtmls:
                    self.fileUrl.write('\n' + str(imageHtml) + '\n')
                    imageRequest = urllib2.urlopen(self.baseURL + str(imageHtml))
                    #imagePagecode是具体图片集的页面代码
                    imagePageCode = imageRequest.read()
                    patternImage = re.compile('original":"(.*?)"',re.S)
                    #imageUrl是每一个图片的界面地址
                    imageUrls = re.findall(patternImage,imagePageCode)
                    imagePath = os.getcwd() + '/image_%s' %self.page
                    if not os.path.exists(imagePath):
                         os.mkdir(imagePath)
                    x = 1
                    print self.page
                    print u"正在下载第%s个图片集的图片"%self.count
                    print '-----------------'
                    for imageUrl in imageUrls:
                        self.fileUrl.write(str(imageUrl)+'\n')
                        #去每一个图片界面下载
                        temp = imagePath + '/%s.jpg' % x
                        print u"正在下载第%s张图片" % x
                        try:
                            urllib.urlretrieve(imageUrl, temp)
                        except:
                            print u"该图片下载失败：%s" % imageUrl
                        x += 1
                    print '****************'
                    self.count += 1
                    break


    def start(self):
        while self.page < 4:
            mainPageCode = self.getMainPageCode(self.page)
            self.fileUrl.write("***********第" + str(self.page) + "页***************\n\n")
            self.getImages(mainPageCode)
            self.page += 1
            print 'page = ',self.page
            time.sleep(2)



baseURL = 'http://pic.yxdown.com/'
fileUrl = open("yxUrl.txt","w")
fileUrl.write("*************获取URL****************\n\n")
#下载指定页的所有图片，这里只下载2,3页的图片
spider = Spider()
spider.start()