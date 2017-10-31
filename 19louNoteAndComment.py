host = "127.0.0.1"
port = 3306
user = "root"
passwd = "sdn"
db = "repository"


from pyspider.libs.base_handler import *
import datetime
import time
import pymysql
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Handler(BaseHandler):
    crawl_config = {
        "headers" : {   
        'Accept':'text/css,*/*;q=0.1',  
        'Accept-Encoding':'gzip, deflate, sdch, br',  
        'Accept-Language':'zh-CN,zh;q=0.8',  
        'Cache-Control':'no-cache',  
        'Connection':'keep-alive',  
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36' ,  
        }
    }

    
    
    @every(minutes=60)
    def on_start(self):
        self.spiderNoteUrl()
        self.spiderContext()
        self.spiderNoteNum()
        self.spiderComment()
        
     
    @config(priority=10,age=0)
    def spiderNoteUrl(self):
        prefix = "http://www.19lou.com/forum-269-"
        postfix = ".html"
        for i in range(1,41):
            url = prefix + str(i) + postfix
            self.crawl(url , fetch_type='js' , callback=self.listNotePage)
    
    @config(priority=9,age=0)
    def listNotePage(self , response):
        for each_tbody in response.doc('tbody').items():
            note_url = each_tbody('tr>th>div>a').attr.href
            note_title = each_tbody('tr>th>div>a').attr.title
            author_href = each_tbody('td.author>a').attr.href
            author_name = each_tbody('td.author>a').attr.title
            author_push_time = each_tbody('td.author>span.color9').text()
            update_time = each_tbody('td.lastpost>span.numeral').text()
            self.insertNote(note_url , note_title , author_href , author_name , author_push_time , update_time)
            
    def insertNote(self , note_url , note_title , author_href , author_name , push_time , update_time):
        conn= pymysql.connect(host=host,port=port,user=user,passwd=passwd,db=db,charset='utf8')
        cur = conn.cursor()

        #检查url和title是否有重复
        cur.execute("select * from note where note_title = %s or note_url = %s", (note_title , note_url))
        rows = cur.fetchall()
        if len(rows) == 0:
            #插入一个新的
            author_id = "" ;
            #判断一个发帖人是否有重复
            cur.execute("select * from author where author_url = %s " , (author_href))
            author_rows = cur.fetchall()
            if len(author_rows) == 0:
                #插入一个新作者
                cur.execute("insert into author(author_url,author_name) values(%s,%s)" , (author_href , author_name))
                cur.execute("select * from author where author_url = %s ", (author_href))
                author_rows = cur.fetchall()
                for author_row in author_rows:
                    author_id = author_row[0]
            else :
                #获取作者的id
                for author_row in author_rows:
                    author_id = author_row[0]
            now_time = datetime.datetime.now().strftime('%Y-%m-%d')
            cur.execute("insert into note(note_title,note_url,note_push_time,note_update_time,note_spider_time,note_push_person_id) values(%s,%s,%s,%s,%s,%s)",(note_title,note_url,push_time,push_time,now_time,author_id))
            conn.commit()
            cur.close()
            conn.close()
    
    @config(priority=7)
    def spiderContext(self):
        noteList = self.getContextIsNullNote()
        for row in noteList:
            id = row[0]
            url = row[1]
            self.crawl(url , fetch_type='js' , callback=self.getNoteContext , save={"id":id})
    
    def getContextIsNullNote(self):
        conn= pymysql.connect(host=host,port=port,user=user,passwd=passwd,db=db,charset='utf8')
        cur = conn.cursor()
        cur.execute("select note_id , note_url from note where note_context is null")
        rows = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return rows
    
    @config(priority=6,age=0)
    def getNoteContext(self,response):
        json_str=""
        for floor in response.doc('DIV.clearall.floor.first').items():
            for content in floor('DIV.thread-cont').items():
                wordStr = content.text()
                imgList = []
                for img in content('img').items():
                    imgList.append(img.attr.src)
                json_obj = {"word":wordStr,"img":imgList}
                json_str = json.dumps(json_obj)
                break
            break
        conn= pymysql.connect(host=host,port=port,user=user,passwd=passwd,db=db,charset='utf8')
        cur = conn.cursor()
        cur.execute("update note set note_context = %s where note_id = %s" , (json_str , response.save["id"]))
        conn.commit()
        cur.close()
        conn.close()
        
    @config(priority=5,age=0)
    def spiderNoteNum(self):
        auditedNoteList = self.getAuditNote()
        for note in auditedNoteList:
            id = note[0]
            url = note[1]+"?timestamp="+str(int(time.time()))
            self.crawl(url , fetch_type='js' , callback=self.getNoteNums , save={"id":id})
    
    @config(priority=4,age=0)
    def getNoteNums(self,response):
        for ul in response.doc('ul.fr.clearall.color9.view-hd-num').items():
            lookNum = ul('li:nth-child(1)>i').text()
            replyNum = ul('li:nth-child(2)>i').text()
            print(lookNum+" "+replyNum)
            self.insertTrend(response.save["id"],lookNum,replyNum)
            break
    
    def insertTrend(self,id,lookNum,replyNum):
        spiderTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        conn= pymysql.connect(host=host,port=port,user=user,passwd=passwd,db=db,charset='utf8')
        cur = conn.cursor()

        cur.execute("insert into note_trend(note_id , count_time , look_num , comment_num) VALUES (%s,%s,%s,%s)" ,
                (str(id) , spiderTime , str(lookNum) , str(replyNum)))
        conn.commit()
        cur.close()
        conn.close()
    
    def getAuditNote(self):
        conn= pymysql.connect(host=host,port=port,user=user,passwd=passwd,db=db,charset='utf8')
        cur = conn.cursor()
        cur.execute("select note_id , note_url from note where note_audit = 1")
        rows = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return rows
    
    @config(priority=3,age=0)
    def spiderComment(self):
        auditedNoteList = self.getAuditNote()
        for note in auditedNoteList:
            id = note[0]
            url = note[1]+"?timestamp="+str(int(time.time()))
            if self.judgeCommentNum(id):
                self.crawl(url , fetch_type='js' , callback=self.analysisPageOne , save={"id":id,"url":url})
             
    @config(priority=2,age=0)
    def analysisPageOne(self,response):
        page_info = response.doc('a.page-last').items()
        pageNum = 1
        for page in page_info:
            pageNum = int(page.attr.href.split('-')[4])
            break
        result = self.getTimeAndLou(response.save["id"])
        maxCount = result["maxCount"]
        time = result["time"]
        url = response.save["url"]
        for i in range(1 , pageNum+1):
            pageUrl = url[0:len(url)-8] + str(i) + "-1.html"
            self.crawl(pageUrl , fetch_type='js' , callback=self.catchComment , save={"pageNum":i,"count":maxCount,"timeYu":time,"note_id":response.save["id"]})
    
    def insertComment(id , author_href , author_name , time , json_str):
        lou_id = self.getLouId(id)
        author_id = self.insertAuthor(author_href , author_name)
        conn= pymysql.connect(host=host,port=port,user=user,passwd=passwd,db=db,charset='utf8')
        cur = conn.cursor()
        author_id = insertAuthor(author)
        spider_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        cur.execute("insert into note_comment values(%s,%s,%s,%s,%s,%s)" ,
                (str(id),str(lou_id),str(json_str),str(time),str(spider_time),str(author_id)))
        conn.commit()
        cur.close()
        conn.close()
    
    def getLouId(self , id):
        conn= pymysql.connect(host=host,port=port,user=user,passwd=passwd,db=db,charset='utf8')
        cur = conn.cursor()
        cur.execute("select max(comment_id) from note_comment where note_id = %s",(id))
        rows = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return int(rows[0][0])+1
    
    def insertAuthor(self,author_href,author_name):
        conn= pymysql.connect(host=host,port=port,user=user,passwd=passwd,db=db,charset='utf8')
        cur = conn.cursor()
        author_id = 0
        cur.execute("select * from author where author_name = %s", (author_name))
        rows = cur.fetchall()
        if len(rows) == 0:
            cur.execute("insert into author(author_url,author_name) values(%s,%s)",
                    (author_href , author_name))
            cur.execute("select * from author where author_name = %s", (author_name))
            rows = cur.fetchall()
        author_id = int(rows[0][0])
        conn.commit()
        cur.close()
        conn.close()
        return author_id
    
    @config(priority=1,age=0)
    def catchComment(self,response):
        pageNum = int(response.save["pageNum"])
        if pageNum != 1:
            for floor_info in response.doc("DIV.clearall.floor.first").items():
                time = floor_info('DIV.cont-hd.clearall>p.fl.link1').text()
                author_href = floor_info('DIV.uname>a').attr.href
                author_href = author_href[2:len(author_href)]
                author_name = floor_info('DIV.uname>a').attr.title
                for content_info in floor_info('DIV.thread-cont').items():
                    for s in content_info('dl'):
                        s.extract()
                    wordStr = content_info.text()
                    wordStr = wordStr.replace('\n', '')
                    wordStr = wordStr.replace('\t', '')
                    wordStr = wordStr.replace(' ', '')
                    imgList = []
                    for img_info in content_info('img').items():
                        imgList.append(img_info.attr.src)
                    json_obj = {'word': wordStr, 'img': imgList}
                    json_str = json.dumps(json_obj)
                    if time > response.save["timeYu"]:
                        self.insertComment(response.save["note_id"] , author_href , author_name , time , json_str)
                    break
                break
        for floor_info in response.doc("DIV.clearall.floor").items():
            time = floor_info('DIV.cont-hd.clearall>p.fl.link1').text()
            author_href = floor_info('DIV.uname>a').attr.href
            author_href = author_href[2:len(author_href)]
            author_name = floor_info('DIV.uname>a').attr.title
            for content_info in floor_info('DIV.thread-cont').items():
                for s in content_info('dl'):
                    s.extract()
                wordStr = content_info.text()
                wordStr = wordStr.replace('\n', '')
                wordStr = wordStr.replace('\t', '')
                wordStr = wordStr.replace(' ', '')
                imgList = []
                for img_info in content_info('img').items():
                    imgList.append(img_info.attr.src)
                json_obj = {'word': wordStr, 'img': imgList}
                json_str = json.dumps(json_obj)
                if time > response.save["timeYu"]:
                    self.insertComment(response.save["note_id"] , author_href , author_name , time , json_str)
                break
            break
                
    def judgeCommentNum(self , id):
        conn= pymysql.connect(host=host,port=port,user=user,passwd=passwd,db=db,charset='utf8')
        cur = conn.cursor()
        cur.execute("select * from note_trend where note_id = %s order by count_time desc limit 2" , (str(id),))
        rows = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        if len(rows) == 0 or len(rows) == 1:
            return True
        if rows[0][3] == rows[1][3] :
            return True
        return False

    def getTimeAndLou(self , id):
        conn= pymysql.connect(host=host,port=port,user=user,passwd=passwd,db=db,charset='utf8')
        cur = conn.cursor()
        cur.execute("select comment_id , comment_push_time from note_comment where note_id = %s order by comment_id desc limit 1" , (str(id) ,))
        rows = cur.fetchall()
        result = {}
        if len(rows) == 0:
            result["maxCount"] = 0
            cur.execute("select note_push_time from note where note_id = %s" , (str(id) ,) )
            rows = cur.fetchall()
            result["time"] = str(rows[0][0]) + " 00:00"
        else :
            result["maxCount"] = int(rows[0][0]) + 1
            result["time"] = rows[0][1]
        conn.commit()
        cur.close()
        conn.close()
        return result
    
    @config(age=1)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }

