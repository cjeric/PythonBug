#_*_encoding:utf-8_*_
#!C:\Python27
#Filename:QiuShiClass

import urllib
import urllib2
import re

class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"
        self.headers = {'User-Agent': self.user_agent}
        self.stories = []
        self.enable = True

    def getPage(self, pageIndex):
        try:

            url = 'http://www.qiushibaike.com/hot/page' + str(pageIndex)
            request = urllib2.Request(url,headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError, e:
            print e

    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print 'Fail to load page'
            return None
        pattern = re.compile('h2>(.*?)</h2.*?span>(.*?)</.*?img(.*?)>.*?number">(.*?)</''',re.S)
        items = re.findall(pattern,pageCode)
        pageStories=[]
        for item in items:
            replaceBR = re.compile('<br/>')
            text = re.sub(replaceBR, '\n', item[1])
            pageStories.append([item[0].encode('utf8').strip(),text.encode('utf-8').strip(),item[3].encode('utf-8').strip()])
        return pageStories

    def loadPage(self):
        if self.enable == True:
            if len(self.stories)<2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    def getOneStory(self, pageStories, page):
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == 'Q':
                self.enable = False
                return
            print "Page: %d\tAuthor: %s\tComment: %s\n%s" %(page,story[0],story[2],story[1])

    def start(self):
        print "Loading QiuShi, press Enter to continue, Q to quit"
        self.enable = True
        self.loadPage()
        nowPage=0
        while self.enable:
            if len(self.stories)>0:
                pageStories = self.stories[0]
                nowPage +=1
                del self.stories[0]
                self.getOneStory(pageStories,nowPage)

spider = QSBK()
spider.start()


