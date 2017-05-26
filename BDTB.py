#_*_encoding:utf8_*_
#!C:/Python27
#Filename: BDTB.py

import urllib
import urllib2
import re

class BDTB():
    def __init__(self, baseurl, seeLZ, floorTag):
        self.baseurl = baseurl
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.file = None
        self.floor = 1
        self.defaultTitle = u"百度贴吧"
        self.floorTag = floorTag

    def getPage(self,pageNumber):
        try:
            url = self.baseurl + self.seeLZ + '&pn=' + str(pageNumber)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read()
        except urllib2.URLError, e:
            if hasattr(e,'code'):
                print e.code
            elif hasattr(e,'reason'):
                print e.reason

    def getTitle(self):
        page = self.getPage(1)
        pattern = re.compile(r'h3 class="core_title_txt pull-left text-overflow.*?>(.*?)</h3>',re.S)
        result = re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getPageNum(self):
        page = self.getPage(1)
        pattern = re.compile(r'<li class="l_reply_num.*?</span>.*?<span .*?>(\d*?)</span>',re.S)
        result = re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getContent(self,pageNum):
        page = self.getPage(pageNum)
        pattern = re.compile(r'<div id="post_content_.*?>(.*?)</div>',re.S)
        results = re.findall(pattern,page)
        for result in results:
            print self.floor, u'楼-----------------------------------------------------------------------------------------------------------\r\n'
            result = Tool.replace(result)
            print result.strip()
            self.floor+=1

class Tool():
    removeImg = re.compile(r'<img.*?> ')
    removeHyperLink = re.compile(r'<a.*?>|</a>')
    replaceLine = re.compile(r'<tr>|<div>|</div>|</p>')
    replaceTD = re.compile(r'<td>')
    replacePara = re.compile(r'<p.*?>')
    replaceBR = re.compile(r'<br>')
    removeExtraTag = re.compile(r'<.*?>')

    @classmethod
    def replace(cls,content):
        content = re.sub(Tool.removeImg,"",content)
        content = re.sub(Tool.removeHyperLink,"",content)
        content = re.sub(Tool.replaceLine,"\r\n",content)
        content = re.sub(Tool.replaceTD,"\t",content)
        content = re.sub(Tool.replacePara,"\r\n  ",content)
        content = re.sub(Tool.replaceBR,"\r\n",content)
        content = re.sub(Tool.removeExtraTag,"",content)
        return content.strip()


if __name__ == '__main__':
    test = BDTB('https://tieba.baidu.com/p/3138733512','1')
    test.getTitle()
    test.getContent(1)