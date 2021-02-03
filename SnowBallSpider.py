import configparser
import os

import requests
import json

url = "https://xueqiu.com/service/screener/screen?category=CN&exchange=sh_sz&areacode=&indcode=&order_by=symbol&order=desc&page=1&size=300&only_count=0&current=&pct=&fmc=30000000000_99999999999999999999"
class SnowBallSpider:
    def __init__(self, config_file='config.ini'):
        self._path = os.path.join(os.getcwd(), config_file)
        if not os.path.exists(self._path):
            raise FileNotFoundError("No such file: config.ini")
        self._config = configparser.ConfigParser()
        self._config.read(self._path, encoding='utf-8-sig')
        self._configRaw = configparser.RawConfigParser()
        self._configRaw.read(self._path, encoding='utf-8-sig')

        self.header = {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
            'accept-encoding': 'gzip, deflate, br',
            'Referer': 'https://xueqiu.com/u/6204884325',
            'x-requested-with': 'XMLHttpRequest',
        }
        self.getCookie()
        # self.getHttpResult()

    def getCookie(self):

        # get cookie
        res = requests.get('https://xueqiu.com/', headers=self.header)
        cookie_dic = res.cookies.get_dict()
        cookie_str = str(cookie_dic)
        cookie = cookie_str.replace("{'", '')
        cookie = cookie.replace("': '", '=')
        cookie = cookie.replace("', '", ';')
        self.cookie = cookie.replace("'}", '')

    def getDSZResult(self):
        # get api content
        res = requests.get(url, headers=self.header)
        content = res.content

        data = json.loads(content.decode())

        # have error exit
        if 'data' not in data.keys():
            pass
            # mynotice.send_notice('sn error')
            # redisObj.set('dpg', 'error')

        d_dict = data['data']['list']
        return d_dict
