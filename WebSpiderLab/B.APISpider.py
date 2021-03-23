import requests
import json
from urllib.parse import quote
import csv


class ApiSpider:
    def __init__(self,  province, page, num, csv_filename):
        self.url = "https://lab.isaaclin.cn/nCoV/api/news?province="+quote(province)+"&page="+str(page)+"&num="+str(num)
        self.csv_filename = csv_filename
        self.name = None
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
        }
        self.csvfileObj = csv.writer(self.csv_filename)

    def spy(self):
        try:
            # 获取自爬虫运行开始（2020年1月24日下午4:00）至今，病毒研究情况以及全国疫情的相关新闻概览，可指定返回数据为最新发布数据或时间序列数据并打印出来
            r = requests.get(self.url,headers = self.headers)
            r.encoding = 'utf-8'
            if r.status_code == 200:
                text = r.text
                state = json.loads(text).get('results')
                # 打印接口返回的结果查看数据格式
                print(state)

            else:
                print('出错了： ', r.status_code)
                print('\n')
        except ValueError:
            print('pyOauth2Error')

    def initXLS(self):
        "func:初始化csv格式文本"
        self.name = ["pubDate", "title", "summary", "infoSource", "sourceUrl", "province", "provinceId"]
        
        # 创建一个写入对象
        self.csvfileObj.writerow(self.name)
        # 构建列表头
        print("创建成功")

    def writeCsv(self):
        try:
        # 获取自爬虫运行开始（2020年1月24日下午4:00）至今
            r = requests.get(self.url,headers=self.headers)
            r.encoding = 'utf-8'

            if r.status_code == 200:
                text = r.text
                state = json.loads(text).get('results')
               # print(state)

                dic = {}
                for i in range(len(state)):
                    keys = list(state[i].keys())
                    # 初始化一个定长数组，name为你自定义的数据项
                    dicRec = [''] * len(self.name)
                    for j in range(len(self.name)):
                        for k in range(len(keys)):
                            # 填写有结果的数据项，注意结果可能含有空值
                            if keys[k] == self.name[j]:
                                key = keys[k]
                                dicRec[j] = state[i][key]
                    dic[i] = dicRec
                    print(state[i])
                    print(dic[i])
                    self.csvfileObj.writerow(dic[i])
                # writeXLS(dic)

            else:

                print('出错了： ', r.status_code)
                print('\n')
        except ValueError as e:
            # e.with_traceback()
            print('pyOauth2Error')

        # 关闭文件
        self.csv_filename.close()


if __name__ == '__main__':
    csvfiler = open('Hebei.csv', 'w', newline='', encoding='utf-8')
    apiSpider = ApiSpider('河北省', 1, 100, csvfiler)
    # apiSpider.spy()
    apiSpider.initXLS()
    apiSpider.writeCsv()