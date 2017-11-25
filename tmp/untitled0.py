#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 08:36:17 2017

@author: mininet
"""

import os,requests,pymysql
conn = pymysql.connect(host='122.224.129.35', port=23306, user='repository', passwd='repository', db='repository',charset='utf8')
cur = conn.cursor()
cur.execute("select * from testType where name = '河长制政策'")
rows = cur.fetchall()
print rows[0][2]
# 释放数据连接
if cur:
    cur.close()
if conn:
    conn.close()