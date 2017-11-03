start_url='http://www.scwater.gov.cn/'
key_name='水利要闻'
key_tag_selector='#one1 > a'
key_attr='href'

nextpage_name='下一页'
nextpage_tag_selector='tr>td>div.list_paging>table>tbody>tr>td>a.pagingNormal'
nextpage_attr='tagname'
page_num=20

title_tag_selector='td.tit_list>a'
title_attr='href'

content_tag_selector='tr>td#xilan_cont.xilan_all>p>span'
publish_time_name='时间'
publish_time_tag_selector='table.xilan_tab>tbody>tr>td'

filter_words=[]

#以上几个字符串参数都不为'',page_num>=0,filter_words可以为空,并且['']与[]效果一致
from pyspider.libs.base_handler import *
import sys,time,pymysql
reload(sys)
sys.setdefaultencoding('utf8')
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

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(start_url, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc(key_tag_selector).items():
            if str(each.text().decode('utf-8')).find(key_name) is not -1:
                exec('key_url = each.attr.'+key_attr)
            self.crawl(key_url, fetch_type = 'js', callback=self.list_page)
            
    def get_nextpage_url_list(self,url):
        filetype_list = [".shtml",".html",".htm",".php",".jsp"]
        url_list = []
        for t in filetype_list:
            l = min([len(url),len(max(filetype_list))])
            if url[len(url)-l:len(url)].find(t) != -1:
                url = url.replace(t,'')[::-1]
                for i in range(len(url)):
                    if url[i].isdigit() is False:
                       url=url[i:len(url)][::-1]
                       url_list.append(url)
                       url_list.append(t)
                       break
                break
        if len(url_list) == 0:
            url = url[::-1]
            for i in range(len(url)):
                if url[i].isdigit() is False:
                    url=url[i:len(url)][::-1]
                    url_list.append(url)
                    break
        return url_list

    @config(priority=4)
    def list_page(self, response):
        for each in response.doc(nextpage_tag_selector).items():
            if str(each.text().decode('utf-8')).find(nextpage_name) is not -1:
                exec('nextpage_url = each.attr.'+nextpage_attr)
                nextpage_url_list = self.get_nextpage_url_list(nextpage_url)
                for i in range(1,page_num+1):
                    if len(nextpage_url_list) is 2:
                        url = nextpage_url_list[0]+str(i)+nextpage_url_list[1]
                    elif len(nextpage_url_list) is 1:
                        url = nextpage_url_list[0]+str(i)
                    if url.find(start_url) == -1 and url.find('http://') == -1:
                        if start_url[len(start_url)-1:] is '/':
                            url = start_url[:len(start_url)-1]+url
                        else:
                            url = start_url+url
                    self.crawl(url, fetch_type = 'js', callback=self.detail_page)
                    
    def filter_word(self,text):
        if len(filter_words) is 0:
            return 1
        else:
            for word in filter_words:
                if text.find(word) != -1:
                    return 1
            return 0
             
    @config(priority=3)
    def detail_page(self, response):
        for each in response.doc(title_tag_selector).items():
            exec "url = each.attr."+title_attr
            if url.find(start_url) == -1 and url.find('http://') == -1:
                if start_url[len(start_url)-1:] is '/':
                    url = start_url[:len(start_url)-1]+url
                else:
                    url = start_url+url
            title = str(each.text().decode('utf-8'))
            if self.filter_word(title) == 1:
                self.crawl(url, fetch_type = 'js', callback=self.content_page)

    @config(priority=2)
    def content_page(self, response):
        result = {}
        result["url"] = response.url,
        result["title"] = response.doc('title').text()
        result["content"] = ''
        for each in response.doc(content_tag_selector).items():
            result["content"] += each.text()
        result["publish_time"] = ''
        for each in response.doc(publish_time_tag_selector).items():
            if str(each.text().decode('utf-8')).find(publish_time_name) is not -1:
                result["publish_time"] = each.text()
        result["crawl_time"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return result
        
    def on_result(self,result):
        if not result:
            return
        print(result)
        conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='sdn',db='repository',charset='utf8')
        cur = conn.cursor()
        #先查找是否存在
        cur.execute("select * from shuiliting where url = %s" , result["url"])
        rows = cur.fetchall()
        if len(rows) == 0:
            cur.execute("insert into shuiliting(url,title,content,publish_time,crawl_time) values(%s,%s,%s,%s,%s)",
                    (result['url'],result['title'],result['content'],result['publish_time'],result['crawl_time']))
        conn.commit()
        cur.close()
        conn.close()