# -*- coding: UTF-8 -*-
"""
常用函数库
@author: cloud
"""

import time
import urllib,urllib2
import json
import re
from chardet import detect

# 获取中文句子的实际长度
def get_zh_len(text):
    if isinstance(text, str):
        text = text.decode("utf-8")
    return len(text)

# 不区分大小写的字符串替换
def ireplace(text, search_str, replace_str):
    try:
        reg = re.compile(re.escape(search_str), re.IGNORECASE)
        return reg.sub(replace_str, text)
    except:
        return text

# 清除表情
def clear_emot(text, returntype="str"):
    # 如果为空，则直接返回
    if not text:
        return text
    # 如果是str，则先转为unicode（因为unicode才能使用中文正则匹配）
    if isinstance(text, str):
        text = text.decode("utf-8")
    try:
        # 清除QQ表情
        p = re.compile(ur'\[[\u4e00-\u9fa5]{1,4}\]')
        text = p.sub(u'', text)
        text = text.strip()
    except:
        pass
    # 返回
    if returntype=="unicode":
        return text
    else:
        return text.encode("utf-8")


# 清除链接（无法清除以中文结尾的url，避免造成误删）
def clear_url(text):
    if not text:
        return text
    try:
        text = re.subn("(http|https)://[^\s]+[a-zA-Z0-9]", "", text)  # http://或https://开头，中间是非空格字符，以a-z0-9结尾
        text = text[0]
        text = re.subn("www.[^\s]+[a-zA-Z0-9]", "", text)  # www.开头，中间是非空格字符，以a-z0-9结尾
        return text[0]
    except:
        return text

# 清除@信息
def clear_at(text):
    if not text:
        return text
    try:
        # 清除以@开头，以空格结尾的字符串
        p = re.compile('@[^@\s]+\s')
        text = p.sub('', text)
        # 清除以@开头，以句末结尾的字符串 (todo)
        # 清除所有残留的@
        text = text.replace('@', '')
        return text.strip()
    except:
        return text

# 清理文本
def clear_text(text, types="at,url,emot"):
    types = types.split(",")
    if "at" in types:
        text = clear_at(text)
    if "url" in types:
        text = clear_url(text)
    if "emot" in types:
        text = clear_emot(text)
    return text


# 获取对象化的http请求头
def get_header(header_str):
    items = header_str.split("\n")
    header = {}
    for i in items:
        if not i:
            continue
        tmplist = i.split(":")
        if tmplist[0] == "Accept-Encoding":
            continue
        header[tmplist[0]] = tmplist[1]
    return header


# 网页抓取方法
def request(url, header_str="", timeout=5):
    # 初始化返回值
    ret = {"ret":0, "code":200, "data":""}
    # 格式化请求头
    if header_str:
        header = get_header(header_str)
    # 发起请求
    if header_str:
        try:
            url = url.encode('utf-8') # 这里转下utf8，不然有些会报错
            req = urllib2.Request(url, None, header)
            response = urllib2.urlopen(req)
            ret["data"] = response.read()
        except:
            ret["ret"] = 2 # 脚本报错
    else:
        try:
            url = url.encode('utf-8') # 这里转下utf8，不然有些会报错
            sock = urllib.urlopen(url)
            code = sock.getcode()
            if code == 200:
                ret["data"] = sock.read()
            else:
                ret["ret"] = 1
                ret["code"] = code
        except:
            ret["ret"] = 2 # 脚本报错
    # 对内容进行编码处理
    if ret["data"]:
        try:
            encoding = detect(ret["data"])["encoding"].upper() # 获取编码类型，这句有时会报错，故用try
        except:
            encoding = "UTF-8"
        if encoding != "UTF-8":
            ret["data"] = ret["data"].decode(encoding,'ignore').encode('utf-8','ignore')
    # 返回
    return ret

