start_url = 'http://www.jxsl.gov.cn/'
key_word = '水利要闻'
next_page = '下一页'
page_num = 10
item_select = '.lmgwfb-w > a'
filter_word = ['长']
publish_time_select = '.wzycenter3>span'

from pyspider.libs.base_handler import *
import sys,re,time,pymysql
reload(sys)
sys.setdefaultencoding('utf8')
    

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(start_url, fetch_type = 'js', callback=self.index_page)
    
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

    @config(age=5 * 24 * 60 * 60)
    def index_page(self, response):
        self.crawl(self.get_url(response,key_word), fetch_type = 'js', callback=self.detail_page)

    @config(age=10 * 24 * 60 * 60)
    def detail_page(self, response):
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
            self.crawl(url,fetch_type = 'js', callback=self.detail_page2)
            
    @config(priority=6)
    def detail_page2(self, response):
        for each in response.doc(item_select).items():
            title = str(each.text().decode('utf-8'))
            for word in filter_word:
                if title.find(word) != -1:
                    self.crawl(each.attr.href,fetch_type = 'js',callback=self.detail_page3)
                    break;
            
    @config(priority=5)
    def detail_page3(self, response):
        url = response.url
        title=response.doc('title').text()
        content=''
        for each in response.doc('p').items():
            content+=each.text()
        crawl_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        publish_time = response.doc(publish_time_select).text()
        conn= pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='sdn',db='repository',charset='utf8')
        cur = conn.cursor()
        cur.execute("insert into shuiliting(title,url,context,crawl_time,publish_time) values(%s,%s,%s,%s,%s)",(title,url,content,crawl_time,publish_time))
        conn.commit()
        cur.close()
        conn.close()
        

