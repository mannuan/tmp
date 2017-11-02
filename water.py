start_url = 'http://www.jxsl.gov.cn/'
key_word = '水利要闻'
next_page = '下一页'
page_num = 10
item_select = '.lmgwfb-w > a'
filter_word = ['长']
publish_time_select = '.wzycenter3>span'

from pyspider.libs.base_handler import *
import sys,re,time,pymysql,urllib2,random
from pyquery import PyQuery
reload(sys)
sys.setdefaultencoding('utf8')

def filter(text):
    for word in filter_word:
        x = text.find(word)
        if x != -1:
            return 0
    return 1   

class Handler(BaseHandler):
    crawl_config = {
        "headers":{
        "Proxy-Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
        "Accept": "*/*",
        "DNT": "1",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
    }
    }

    @every(minutes=72 * 60)
    def on_start(self):
        headers = ["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"]
        random_header = random.choice(headers)
        req =urllib2.Request(start_url)
        req.add_header("User-Agent", random_header)
        req.add_header("GET",start_url)
        content=urllib2.urlopen(req).read()
        p = PyQuery(content)
        body = p('body')
        body_str = str(body.html().decode('utf-8'))
        loc = body_str.find(key_word)+len(key_word)/2
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
        if start_url[len(start_url)-1:len(start_url)] is '/':
            key_url = start_url[:len(start_url)-1]+key_url
        else:
            key_url = start_url+key_url
        self.crawl(key_url, fetch_type = 'js', callback=self.index_page)
    
    def get_url(self,response,keyword):
        body = response.doc('body')
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
        return key_url

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        key_url = self.get_url(response,next_page)
        key_url_arr = key_url.split('/')
        key_url_tail = key_url_arr[len(key_url_arr)-1]
        key_url_tail_tmp = ''
        for c in re.findall(r'[^0-9]',key_url_tail):
            key_url_tail_tmp+=c
        key_url_list = key_url_tail_tmp.split('.')
        tmp = ''
        for i in range(0,len(key_url_arr)-1):
            tmp += key_url_arr[i]+'/'
        key_url_list[0]=tmp+key_url_list[0]
        key_url_list[1]='.'+key_url_list[1]
        for i in range(1,page_num+1):
            url = key_url_list[0]+str(i)+key_url_list[1]
            self.crawl(url,fetch_type = 'js', callback=self.detail_page)
            
    @config(priority=6)
    def detail_page(self, response):
        for each in response.doc(item_select).items():
            title = str(each.text().decode('utf-8'))
            if filter(title) == 1:
                self.crawl(each.attr.href,fetch_type = 'js',callback=self.detail_page1)
            
    @config(priority=5)
    def detail_page1(self, response):
        result = {}
        result["url"] = response.url
        result["title"] = response.doc('title').text()
        context=''
        for each in response.doc('p').items():
            context+=each.text()
        result["context"] = context
        result["crawl_time"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        if publish_time_select is '':
            result["publish_time"] = "null"
        else:
            result["publish_time"] = response.doc(publish_time_select).text()
        return result
        
    def on_result(self,result):
        if not result or not result['title']:
            return
        conn= pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='sdn',db='repository',charset='utf8')
        cur = conn.cursor()
        #先查找是否存在
        cur.execute("select * from shuiliting where url = %s" , result["url"])
        rows = cur.fetchall()
        if len(rows) == 0:
            cur.execute("insert into shuiliting(title,url,context,crawl_time,publish_time) values(%s,%s,%s,%s,%s)",
                    (result['title'],result['url'],result['context'],result['crawl_time'],result['publish_time']))
        conn.commit()
        cur.close()
        conn.close()
        

