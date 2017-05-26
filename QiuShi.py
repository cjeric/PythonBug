#_*_coding:utf-8_*_
#!c:\python27
#Filename:QiuShi.py

import urllib
import urllib2
import re

page = 1
url = 'http://www.qiushibaike.com/hot/page/' + str(page)
user_agent = "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"
headers={'User-Agent': user_agent}
try:
    request = urllib2.Request(url, headers = headers)
    response = urllib2.urlopen(request)
    page =  response.read().decode('utf-8')
    patten = re.compile('h2>(.*?)</h2.*?span>(.*?)</.*?img(.*?)>.*?number">(.*?)</''',re.S)
    items = re.findall(patten,page)
    print len(items)
    for item in items:
        print item[0].encode('utf-8')+ '\n', item[1].encode('utf-8')+'\n', item[2].encode('utf-8')+'\n', item[3].encode('utf-8')
except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    elif hasattr(e,"reason"):
        print e.reason