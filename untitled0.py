#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-10-28 09:48:03
# Project: 19lou_test1

import pymysql
conn= pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='sdn',charset='utf8')
cur = conn.cursor()
cur.execute('CREATE DATABASE IF NOT EXISTS `setting`;')
conn= pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='sdn',db='setting',charset='utf8')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS `setting`()')