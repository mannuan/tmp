# -*- coding:utf-8 -*-

from lxml import html
import requests
import json
import re

#加载微博参数 uid,containerid
#评论请求需要参数 id,page

# uid:5044281310
# containerid:107603 + uid

#实例方法和类方法 self 是实例方法　cls　是类方法

#正则表达式的元字符 . * ?
class Tool:
    #去除img标签
    removeImg = re.compile('<img.*>| {1,7}|&nbsp;')
    #去除超链接 a标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行换成\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')

    #去除所有标签
    removeTag = re.compile('<.*?>')

    @classmethod
    def replace(cls,x):
        x = re.sub(cls.removeImg,'',x)
        x = re.sub(cls.removeAddr,'',x)
        x = re.sub(cls.replaceLine,'',x)
        x = re.sub(cls.removeTag,'',x)

        return x.strip()#去掉多余的内容

class Weibo(object):

    def get_weibo_pagenum(self,id):
        '''
        获取指定博主的所有微博的页数
        :param id:博主的id
        :return:
        '''
        page = 1
        while True:
            url = "https://m.weibo.cn/api/container/getIndex?uid={}&type=uid&value={}&containerid=107603{}&page={}".format(
                id, id, id, page)
            reponse = requests.get(url)
            ob_json = json.loads(reponse.text)
            list_cards = ob_json.get('cards')
            if list_cards is None and page >= 10:
                break
            else:
                page+=1
        print page
        return page

    def get_weibo(self,id,page): #个人id
        '''
        获取指定博主的所有微博
        :param id:表示博主的id
        :param page:表示博主的微博页数
        :return: list_cards
        '''
        url = "https://m.weibo.cn/api/container/getIndex?uid={}&type=uid&value={}&containerid=107603{}&page={}".format(id,id,id,page)
        reponse = requests.get(url)
        ob_json = json.loads(reponse.text)
        list_cards = ob_json.get('cards')
        return list_cards

    def get_comment(self,id,page):#微博id
        '''
        获取某条微博的所有评论
        :param id:表示微博的id
        :param page:表示微博评论的页数，热门的评论一定在第一页
        :return:
        '''
        url = "https://m.weibo.cn/api/comments/show?id={}&page={}".format(id,page)
        response = requests.get(url)
        ob_json = json.loads(response.text)
        list_comments = ob_json.get('hot_data')

        return list_comments

    def main(self,uid,page):
        '''
        爬取制定微博用户的指定页面的微博和评论
        :param uid:表示用户的id
        :param page:表示博主的微博页数
        :return:
        '''
        list_cards = self.get_weibo(uid,page)
        for card in list_cards:#遍历
            if card.get('card_type') == 9:#等于9的微博才是正文,其他的都是推荐
                id = card.get('mblog').get('id') #微博的id
                text = card.get('mblog').get('text') #微博的内容
                text = Tool.replace(text)
                # text = Tool.replace(text)
                print '***'
                print u'@@@微博：'+text+'\n'

                list_comments = weibo.get_comment(id,1)
                print list_comments
                count_hotcomments = 1
                for comment in list_comments:
                    created_at = comment.get('created_at')#获取时间
                    like_counts = comment.get('like_counts')#点赞数
                    text = comment.get('text')
                    tree = html.fromstring(text)
                    text = tree.xpath('string(.)') #用string函数过滤多余标签
                    name_user = comment.get('user').get('screen_name')
                    source = comment.get('source')
                    if source == '':
                        source = u'未知'

                    print str(count_hotcomments),':**',name_user,'**',u' **发表于：**'+created_at,u' **点赞：**'+str(like_counts)+u'  **来自：**'+source
                    print text+'\n'
                    count_hotcomments += 1
                print '================'



if __name__ == '__main__':
    weibo = Weibo()
    page = 1
    while True:
        url = "https://m.weibo.cn/api/container/getIndex?containerid=102803_ctg1_8999_-_ctg1_8999_home&page={}".format(page)
        page += 1
        reponse = requests.get(url)
        ob_json = json.loads(reponse.text)
        list_cards = ob_json.get('cards')
        if list_cards is None:
            break
        for card in list_cards:
            if card.get('card_type') is 9:
                id = card.get('mblog').get('user').get('id')
                for p in range(1,weibo.get_weibo_pagenum(id)+1):
                    weibo.main(id,p)