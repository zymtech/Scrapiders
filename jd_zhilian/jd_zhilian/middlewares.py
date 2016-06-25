# encoding = utf-8

import random
import requests
import json


class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        #print "**************************" + random.choice(self.agents)
        request.headers.setdefault('User-Agent', random.choice(self.agents))

class GlobalProxyList(object):
    proxylist = []
    request_count = 0

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        if len(GlobalProxyList.proxylist) == 0 or GlobalProxyList.request_count > 300 * len(GlobalProxyList.proxylist):
            self.change_proxy()
            GlobalProxyList.request_count = 0
        proxy = random.choice(GlobalProxyList.proxylist)
        print "***********using proxy:%s***************" % proxy['host']
        request.meta['proxy'] = "http://" + str(proxy['host']) + ':' + str(proxy['port'])
        GlobalProxyList.request_count += 1

    def change_proxy(self):
        proxyurl = "http://192.168.1.251:9099/api/proxies"
        proxies = requests.get(proxyurl)
        GlobalProxyList.proxylist = json.loads(proxies.text)