# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import urllib2,random,sys,re,time
reload(sys)
sys.setdefaultencoding('utf8')

"""
此函数用于抓取返回403禁止访问的网页
"""
headers = ["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"]
random_header = random.choice(headers)
start_url = "http://www.hnwr.gov.cn./xxgk/slxw/slxw/"
keyword = '下一页'

"""
对于Request中的第二个参数headers，它是字典型参数，所以在传入时
也可以直接将个字典传入，字典中就是下面元组的键值对应
"""
req =urllib2.Request(start_url)
req.add_header("User-Agent", random_header)
req.add_header("GET",start_url)
content=urllib2.urlopen(req).read()
f = open('temp.txt','w+')
f.write(content)
f.close()
from pyquery import PyQuery
p = PyQuery(content)
##################################
body = p('body')
body_str = str(body.html().decode('utf-8'))
loc = body_str.find(keyword)+len(keyword)/2
url_dict = dict()
distance_list = []
beg = 0
for each in body('a').items():
    s = str(each.attr.href)
    loc_i = body_str.find(s,beg)
    d = abs((loc_i+len(s)/2)-loc)
    beg = loc_i+len(s)
    url_dict.setdefault(d,s)
    distance_list.append(d)
key_url = url_dict.get(min(distance_list))
print key_url
#key_url_arr = key_url.split('/')
#key_url_tail = key_url_arr[len(key_url_arr)-1]
#key_url_tail_tmp = ''
#for c in re.findall(r'[^0-9]',key_url_tail):
#    key_url_tail_tmp+=c
#key_url_list = key_url_tail_tmp.split('.')
#tmp = ''
#for i in range(0,len(key_url_arr)-1):
#    tmp += key_url_arr[i]+'/'
#key_url_list[0]=tmp+key_url_list[0]
#print(key_url_list)

      
