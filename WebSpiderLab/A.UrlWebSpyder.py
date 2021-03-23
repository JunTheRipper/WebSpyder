###  Lab1 1.3.1 基于URL的数据爬取
import urllib3
import certifi
import wget
from pyquery import PyQuery
import re
import time


class UrlSpy:
    def __init__(self, url):
        self.url = url
        self.htmlText = ""
        self.img_list = None

    def htmlSpy(self, url):
        http = urllib3.PoolManager(ca_certs=certifi.where())
        # 安装了certifi之后，和requests库一样也有一个cacert.pem，
        # 可以用编辑器打开cacert.pem，里面包含了很多可信任知名公司的证书/公钥
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
        }

        r = http.request('GET', url, headers=headers)
        # 说明：豆瓣爬取的时候，往往有反爬机制导致爬取很慢甚至状态码异常，这里最好伪装一下头部的信息
        # print("状态码为：", r.status, end='\t')
        if r.status == 200:
            # print("状态正常")
            self.htmlText = r.data
        return r

    def printOut(self):
        print(self.htmlText)
        with open('1.html','w',encoding='utf-8') as f:
            f.write(self.htmlText)

    def getImg(self):
        doc = PyQuery(self.htmlText)
        img_tags = doc('img')
        self.img_list = [img.attr('src') for img in img_tags.items()]
        print(self.img_list)
        num = 0
        for i in self.img_list:
            num += 1
        print("Whole number of pictures: ",num)

    def saveImg(self):
        num = 0
        for img_url in self.img_list:
            print(img_url)
            pattern = re.compile(r'^(https|http|ftp|rtsp|mms)?:/{2}\w.+$')
            # template https:/
            valid = re.match(pattern, img_url)
            # 使用wget把图片下载到本地，注意默认下载到python执行路径下
            if valid:
                # image_filename = wget.download(img_url)
                # 注意，这里有一个问题，对于wget模块方法有没有对应反爬的技术？或者说如何对wget实现头部浏览器信息的伪装？
                with open(img_url[-8:], 'wb') as f:
                    f.write(self.htmlSpy(img_url).data)
                f.close()
                # print(u'正在保存的一张图片为:', image_filename)
                num += 1
        print('\ntotal number of image:', num)

if __name__ == '__main__':
    url = r'https://movie.douban.com/celebrity/1054444/'

    urlSpy = UrlSpy(url)
    urlSpy.htmlSpy(url)
    # urlSpy.printOut()
    urlSpy.getImg()
    urlSpy.saveImg()