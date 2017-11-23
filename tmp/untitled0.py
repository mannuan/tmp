#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 08:36:17 2017

@author: mininet
"""

import os,requests
file_url = 'http://www.h2o-china.com/law/view/download?id=1'
file_id = file_url.split('=')[-1]
file_name = '{}/zhongguoshuiwang_paper/{}.pdf'.format(os.environ['HOME'],file_id)
r = requests.get(file_url, stream=True)
f = open(file_name, "wb+")
for chunk in r.iter_content(chunk_size=512):
    if chunk:
        f.write(chunk)
f.close()