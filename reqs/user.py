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
            _type = self.get_argument("type")
            if int(_type) == 1:
                self.deal_ex(self.get_argument("code"))
            else:
                self.deal(self.get_argument("uinfo"))
        except:
            self.write(self.tip)

    def get(self, *args, **kwargs):
        try:
            _type = self.get_argument("type")
            if int(_type) == 1:
                self.deal_ex(self.get_argument("code"))
            else:
                self.deal(self.get_argument("uinfo"))
        except:
            self.write(self.tip)
            import traceback
            print traceback.print_exc()

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