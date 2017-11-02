
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-11-02 19:36:46
# Project: water2

from pyspider.libs.base_handler import *

start_url = "http://www.scwater.gov.cn/"
key_word = "水利要闻"
key_tag_selector = "#one1 > a"
key_attr = "href"

nextpage_name = "下一页"
nextpage_tag_selector = "tr>td>div.list_paging>table>tbody>tr>td>a.pagingNormal"
nextpage_attr = "tagname"
page_num = 20

title_tag_selector = "tr>td>table>tbody>tr>td.tit_list>a"
title_attr = "href"


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
            if str(each.text().decode('utf-8')).find(key_word) is not -1:
                exec('key_url = each.attr.'+key_attr)
            self.crawl(key_url, fetch_type = 'js', callback=self.list_page)
            
    def get_nextpage_url_list(self,url):
        filetype_list = [".html",".htm",".jsp"]
        url_list = []
        for t in filetype_list:
            if url.find(t) != -1:
                url = url.replace(t,'')[::-1]
                for i in range(len(url)):
                    if url[i].isdigit() is False:
                       url=url[i:len(url)][::-1]
                       url_list.append(url)
                       url_list.append(t)
                       break
                break
        if len(url_list) == 0:
            url_list.append(url[:len(url)-1])
        return url_list

    @config(priority=4)
    def list_page(self, response):
        for each in response.doc(nextpage_tag_selector).items():
            if str(each.text().decode('utf-8')).find(nextpage_name) is not -1:
                exec('nextpage_url = each.attr.'+nextpage_attr)
                nextpage_url_list = self.get_nextpage_url_list(nextpage_url)
                for i in range(1,page_num+1):
                    url = nextpage_url_list[0]+str(i)+nextpage_url_list[1]
                    if url.find(start_url) == -1 and url.find('http://') == -1:
                        if start_url[len(start_url)-1:] is '/':
                            url = start_url[:len(start_url)-1]+url
                        else:
                            url = start_url+url
                    self.crawl(url, fetch_type = 'js', callback=self.detail_page)
                    #print url
             
    @config(priority=3)
    def detail_page(self, response):
        for each in response.doc(title_tag_selector).items():
            exec "url = each.attr."+title_attr
            if url.find(start_url) == -1 and url.find('http://') == -1:
                if start_url[len(start_url)-1:] is '/':
                    url = start_url[:len(start_url)-1]+url
                else:
                    url = start_url+url
            self.crawl(url, fetch_type = 'js', callback=self.content_page)

    @config(priority=2)
    def content_page(self, response):
        url = response.url,
        title = response.doc('title').text()
        
                    
