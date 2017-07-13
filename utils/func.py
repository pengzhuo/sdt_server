# coding: utf-8
# Author: pengz
# Email: pch987.net@163.com

import requests as rs
import json
from utils.log import log
from utils.WXBizDataCrypt import WXBizDataCrypt
from config import *
from manager.dataManager import DataManager
from models.user import User

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
    kjs = json.loads(userInfo)
    if 'userId' in kjs:
        userId = kjs['userId']
        user = DataManager().getUser(userId)
        if user is not None:
            uid = user.uid
            sessionKey = user.session_key
            encryptedData = kjs['encryptedData']
            iv = kjs['iv']
            #解析数据
            wxdc = WXBizDataCrypt(APPID, sessionKey)
            data = wxdc.decrypt(encryptedData, iv)
            if data['openId'] != uid:
                log().error("saveUserInfo error! uid not the same! [{0} - {1}]".format(uid, data['openId']))
            else:
                user.setUserInfo(kjs['rawData'])
                DataManager().updateUser(user)
        else:
            log().error("saveUserInfo error! user is None! [{0}]".format(userId))

def getUserInfo(code):
    url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code".format(
        APPID,
        SECRET_KEY,
        code
    )
    res = None
    try:
        kres = rs.get(url, verify=False)
        kjs = kres.json()
        if "errcode" not in kjs:
            openid = kjs['openid']
            session_key = kjs['session_key']
            user = DataManager().addUser(openid, session_key)
            res = user.userId
        else:
            print "get user info fail " + kjs['errcode']
    except:
        import traceback
        print traceback.print_exc()
    finally:
        return res
