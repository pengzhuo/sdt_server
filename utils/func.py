# coding: utf-8
# Author: pengz
# Email: pch987.net@163.com

import requests as rs
import json
from utils.log import log
from utils.WXBizDataCrypt import WXBizDataCrypt
from config import *
from manager.dataManager import DataManager

def _getWuliu_(url):
    res = rs.get(url)
    js = json.loads(res.text)
    qty = len(js)
    wuliu = []
    for i in range(qty):
        wuliu.append(js[i]['comCode'])
    return wuliu

def _getUrl_(noStr):
    exnum = noStr
    if exnum == '':
        print "The express number cannot be empty!"
        return None
    else:
        dflag = 1
        for e in exnum:
            if ord(e) <48 or ord(e) >57:
                print "The express number could only be degital!"
                dflag = 0
                return None
        if dflag == 1:
            url = "http://www.kuaidi100.com/autonumber/auto?num=" + exnum
            return url

def _getKuaidi_(exnum, wuliu):
    Kuaidi = "http://www.kuaidi100.com/query?type=" + wuliu + "&postid=" + exnum
    kres = rs.get(Kuaidi)
    kjs = json.loads(kres.text)
    if kjs['status'] != '200':
        print "Error: The express didn't exist or data lost!"
        return None
    else:
        return kjs

def findInfoByNo(noStr):
    url = _getUrl_(noStr)
    if url is not None:
        wuliu = _getWuliu_(url)
        if len(wuliu) == 0:
            print "Error: The express didn't exist or data lost!"
            return None

        for company in wuliu:
            res = _getKuaidi_(noStr, company)
            if res is None:
                continue
            else:
                return res

def findKdInfoByAddr(xzqname, keywords):
    from urllib import unquote_plus
    requrl = "http://www.kuaidi100.com/apicenter/courier.do?method=mktaround&xzqname=" + unquote_plus(xzqname) + "&keywords=" + unquote_plus(keywords)
    kres = rs.get(requrl)
    kjs = json.loads(kres.text)
    if str(kjs['status']) != '200':
        print "Error: can't find kuaidi info!"
        return None
    else:
        return kjs

def findDetailsByGuid(guid):
    url = 'http://www.kuaidi100.com/courier/searchapi.do?method=courierdetail&json={"guid":"' + guid + '"}'
    kres = rs.get(url)
    kjs = json.loads(kres.text)
    if str(kjs['status']) != '200':
        print "Error: find details fail!"
        return None
    else:
        return kjs

def saveUserInfo(userInfo):
    pass

def getUserInfo(code):
    url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code".format(
        APPID,
        SECRET_KEY,
        code
    )
    kres = rs.get(url, verify=False)
    kjs = json.load(kres.text)
    if kjs['errcode'] is None:
        openid = kjs['openid']
        session_key = kjs['session_key']
    else:
        print "get user info fail " + kjs['errcode']
