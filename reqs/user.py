# coding: utf-8
# Author: pengz
# Email: pch987.net@163.com

from tornado.web import RequestHandler
from utils.func import saveUserInfo
from utils.func import getUserInfo

#用户信息
class User(RequestHandler):
    tip = "保存用户信息成功!"

    def post(self, *args, **kwargs):
        try:
            code = self.get_argument("code")
            if code is not None:
                self.deal_ex(code)
            else:
                userInfo = self.get_argument("uinfo")
                self.deal(userInfo)
        except:
            self.write(self.tip)

    def get(self, *args, **kwargs):
        try:
            code = self.get_argument("code")
            if code is not None:
                self.deal_ex(code)
            else:
                userInfo = self.get_argument("uinfo")
                self.deal(userInfo)
        except:
            self.write(self.tip)

    def deal(self, userInfo):
        if userInfo is not None:
            res = saveUserInfo(userInfo)
        if res is None:
            res = self.tip
        self.write(res)

    def deal_ex(self, code):
        if code is not None:
            res = getUserInfo(code)
        if res is None:
            res = self.tip
        self.write(res)