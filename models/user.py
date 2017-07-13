# coding: utf-8
# Author: pengz
# Email: pch987.net@163.com

import json

class User():
    userId = None
    uid = None
    session_key = None
    uname = None
    icon = None
    gender = None
    city = None
    province = None
    country = None

    def __init__(self, userId=None, uid=None, session_key=None):
        self.userId = userId
        self.uid = uid
        self.session_key = session_key

    def initWithJson(self, jsonStr):
        tmp = json.loads(jsonStr)
        self.userId = tmp['userId'] if 'userId' in tmp else None
        self.uid = tmp['uid'] if 'uid' in tmp else None
        self.session_key = tmp['session_key'] if 'session_key' in tmp else None
        self.uname = tmp['uname'] if 'uname' in tmp else None
        self.icon = tmp['icon'] if 'icon' in tmp else None
        self.gender = tmp['gender'] if 'gender' in tmp else None
        self.city = tmp['city'] if 'city' in tmp else None
        self.province = tmp['province'] if 'province' in tmp else None
        self.country = tmp['country'] if 'country' in tmp else None

    def toJson(self):
        data = {}
        for k,v in self.__dict__.items():
            if k == "uname":
                data[k] = v.encode("utf-8")
            else:
                data[k] = v
        return json.dumps(data)

    def setUserInfo(self, jsonStr):
        obj = json.loads(jsonStr)
        self.uname = obj['nickName'] if 'nickName' in obj else None
        self.icon = obj['avatarUrl'] if 'avatarUrl' in obj else None
        self.gender = obj['gender'] if 'gender' in obj else 0
        self.city = obj['city'] if 'city' in obj else None
        self.province = obj['province'] if 'province' in obj else None
        self.country = obj['country'] if 'country' in obj else None
