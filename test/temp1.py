#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 19:27:29 2017

@author: mininet
"""

import urllib2,random,sys,re,time
reload(sys)
sys.setdefaultencoding('utf8')

"""
此函数用于抓取返回403禁止访问的网页
"""
headers = ["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"]
random_header = random.choice(headers)
start_url = "http://www.scwater.gov.cn/"
key_word = "水利要闻"
key_tag_selector = "#one1 > a"
key_attr = "href"

"""
对于Request中的第二个参数headers，它是字典型参数，所以在传入时
也可以直接将个字典传入，字典中就是下面元组的键值对应
"""
#req =urllib2.Request(start_url)
#req.add_header("User-Agent", random_header)
#req.add_header("GET",start_url)
#content=urllib2.urlopen(req).read()
#f = open('temp.txt','w+')
#f.write(content)
#f.close()
#from pyquery import PyQuery
#p = PyQuery(content)
###################################
#for each in p(key_tag_selector).items():
#    if str(each.text().decode('utf-8')).find(key_word) is not -1:
#        exec('key_url = each.attr.'+key_attr)
#        print(key_url)

#key_url = "http://www.scwater.gov.cn/main/slzx/slyw/index.html"
#nextpage_name = "下一页"
#nextpage_tag_selector = "tr>td>div.list_paging>table>tbody>tr>td>a.pagingNormal"
#nextpage_attr = "tagname"
#page_num = 20
#
#req =urllib2.Request(key_url)
#req.add_header("User-Agent", random_header)
#req.add_header("GET",key_url)
#content=urllib2.urlopen(req).read()
#f = open('temp.txt','w+')
#f.write(content)
#f.close()
#from pyquery import PyQuery
#p = PyQuery(content)
##################################
#filetype_list = [".html",".htm",".jsp"]
#def get_nextpage_url_list(url):
#    url_list = []
#    for t in filetype_list:
#        if url.find(t) != -1:
#            url = url.replace(t,'')[::-1]
#            for i in range(len(url)):
#                if url[i].isdigit() is False:
#                   url=url[i:len(url)][::-1]
#                   url_list.append(url)
#                   url_list.append(t)
#                   break
#            break
#    if len(url_list) == 0:
#        url_list.append(url[:len(url)-1])
#    return url_list
#for each in p(nextpage_tag_selector).items():
#    if str(each.text().decode('utf-8')).find(nextpage_name) is not -1:
#        exec('nextpage_url = each.attr.'+nextpage_attr)
#        nextpage_url_list = get_nextpage_url_list(nextpage_url)
#        for i in range(1,page_num+1):
#            url = nextpage_url_list[0]+str(i)+nextpage_url_list[1]
#            print url

#key_url = "http://www.scwater.gov.cn/main/slzx/slyw/d30be314-7.html"
#title_tag_selector = "tr>td>table>tbody>tr>td.tit_list>a"
#title_attr = "href"
#
#req =urllib2.Request(key_url)
#req.add_header("User-Agent", random_header)
#req.add_header("GET",key_url)
#content=urllib2.urlopen(req).read()
#f = open('temp.txt','w+')
#f.write(content)
#f.close()
#from pyquery import PyQuery
#p = PyQuery(content)
#for each in p(title_tag_selector).items():
#    exec "url = each.attr."+title_attr


title_url = "http://www.ahsl.gov.cn/index.php?c=xxgkweb&m=channel&partcode=5212c46c082f39c638710afe&page=91"
content_tag_selector = "div.is-list-box>ul>li>a"
publish_time_name = "发布时间"
publish_time_tag_selector = "div.is-border is-content-main>div.is-size"


req =urllib2.Request(title_url)
req.add_header("User-Agent", random_header)
req.add_header("GET",title_url)
content=urllib2.urlopen(req).read()
f = open('temp.txt','w+')
f.write(content)
f.close()
from pyquery import PyQuery
p = PyQuery(content)
content = ''
for each in p(content_tag_selector).items():
#    content += each.text()
    print(each.text())
#publish_time = ''
#for each in p(publish_time_tag_selector).items():
#    if str(each.text().decode('utf-8')).find(publish_time_name) is not -1:
#        publish_time = each.text()
#print content,publish_time
        
        
        
    
