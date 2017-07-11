# coding: utf-8
# Author: pengz
# Email: pch987.net@163.com

from tornado.web import RequestHandler
from utils.func import findInfoByNo

#查询快递
class Cxkd(RequestHandler):
    tip = "未查询到快递信息！请检查单号是否正确或者稍后再试！"

    def post(self, *args, **kwargs):
        try:
            dh = self.get_argument("dh")
            self.deal(dh)
        except:
            self.write(self.tip)

    def get(self, *args, **kwargs):
        try:
            dh = self.get_argument("dh")
            self.deal(dh)
        except:
            self.write(self.tip)

    def deal(self, noStr):
        if noStr is not None:
            res = findInfoByNo(noStr)
        if res is None:
            res = self.tip
        self.write(res)