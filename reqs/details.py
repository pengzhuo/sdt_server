# coding: utf-8
# Author: pengz
# Email: pch987.net@163.com

from tornado.web import RequestHandler
from utils.func import findDetailsByGuid

class Details(RequestHandler):
    tip = "查询失败！请稍后再试！"

    def post(self, *args, **kwargs):
        try:
            guid = self.get_argument("guid")
            self.deal(guid)
        except:
            self.write(self.tip)

    def get(self, *args, **kwargs):
        try:
            guid = self.get_argument("guid")
            self.deal(guid)
        except:
            self.write(self.tip)

    def deal(self, guid):
        if guid is not None:
            res = findDetailsByGuid(guid)
        if res is None:
            res = self.tip
        self.write(res)