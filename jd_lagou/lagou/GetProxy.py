# -*- coding: utf-8 -*-
import datetime
import requests
import json
import random
import os
import sys

class GetProxytoFile(object):
    """ get proxy from http://192.168.1.251:9099/api/proxies"""
    def __init__(self, url):
        self.url = url

    def setPeriod(self, day=0, hour=0, min=0, second=0):
        now = datetime.datetime.now()
        period = datetime.timedelta(days=day, hours=hour, minutes=min, seconds=second)
        next_time = now + period

    def getProxy(self):
        proxies = requests.get(self.url)
        #proxies = json.loads(proxies.text)
        pwd = sys.path[0]
        path = os.path.abspath(os.path.join(pwd, os.pardir, os.pardir))
        if os.path.isfile('proxies.txt'):
            os.remove('proxies.txt')
        path = os.path.join(path, 'proxies.txt')
        file = open(path, 'w')
        file.write(proxies.text)
        #proxydict = random.choice(proxies)
        #proxy = str(proxydict['host']) + ':' + str(proxydict['port'])

if __name__=='__main__':
    getproxy = GetProxytoFile("http://192.168.1.251:9099/api/proxies")
    getproxy.getProxy()


