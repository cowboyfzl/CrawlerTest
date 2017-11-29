import requests
import json
from bs4 import BeautifulSoup
import re

class Crawler():

    def __init__(self, baseurl):
        self.baseurl = baseurl



    def parserData(self):
       return self.__parseListLinks(self.baseurl)


    def __parseListLinks(self, url):
        newsdetail = []
        res = requests.get(url)
        jd = json.loads(res.text.lstrip('jQuery110207573210913066464_1511753267296(').rstrip(');'))
        for ent in jd['result']['data']['articles']:
            newsdetail.append(self.__getnewdetail(ent['pub_url']))
        return newsdetail

    def __getnewdetail(self, newurl):
        result = {}
        res = requests.get(newurl)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        result['title'] = soup.select('#artibodyTitle')[0].text
        result['newssource'] = soup.select('#pub_date')[0].text
        content = soup.select('.BSHARE_POP')[0].text
        result['article'] = self.__getContent(content)
        result['editor'] = content.split('\n')[1]
        result['comments'] = self.__getcommentcounts(newurl)
        return result

    def __getContent(self, content):
        str = ''
        count = 0
        for x in content.split('\n'):
            count += 1
            if count > 2:
                str += x

        return str.replace('\u3000', '')

    comment_url = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=wj&newsid=comos-{}&group=0&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20&jsvar=loader_1511773309544_17752072'

    def __getcommentcounts(self, newsul):
        m = re.search('doc-i(.+).shtml', newsul)
        if m != None:
            newsid = m.group(1)
            comments = requests.get(self.comment_url.format(newsid))
            jd = json.loads(comments.text.strip('var loader_1511773309544_17752072='))
            ishavecount = False
            for key in jd.keys():
                if key == 'result':
                    for subKey in jd['result']:
                        if subKey == 'count':
                            ishavecount = True

            if ishavecount:
                return jd['result']['count']['total']
            else:
                return '0'

        else:
             return "0"



