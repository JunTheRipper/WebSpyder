import os
# import pandas as pd
import time
import random

##########删除缺失值、去重##############
'''
data = pd.read_csv("weibo-processed-B.csv",encoding="utf8")
print(data.isnull().sum())
data = data.dropna()
data.reset_index(drop=True,inplace=True)
print(data.isnull().sum())
result = data.drop_duplicates(['微博内容'],keep='last')
result.reset_index(drop=True,inplace=True)
result.to_csv("allData.csv",encoding="utf8",index=False)
'''

def mkSubFile(lines, head, srcName, sub):
    [des_filename, extname] = os.path.splitext(srcName)
    filename = des_filename + '_' + str(sub) + extname
    print('make file: %s' % filename)
    fout = open(filename, 'w',encoding="utf8")
    try:
        fout.writelines([head])
        fout.writelines(lines)
        return sub + 1
    finally:
        fout.close()


def splitByLineCount(filename, count):
    fin = open(filename, encoding="utf8")
    try:
        head = fin.readline()
        buf = []
        sub = 1
        for line in fin:
            buf.append(line)
            if len(buf) == count:
                sub = mkSubFile(buf, head, filename, sub)
                buf = []
        if len(buf) != 0:
            sub = mkSubFile(buf, head, filename, sub)
    finally:
        fin.close()

def dataRandom(filename):
    fin = open(filename, encoding="utf8")
    try:
        head = fin.readline()
        lines = fin.readlines()
        random.shuffle(lines)

        with open("./data/allDataRandom.csv", 'w', encoding='utf8') as f:
            f.write(head)
            f.writelines(lines)
    finally:
        fin.close()

dataRandom("./data/allData.csv")
splitByLineCount('./data/allDataRandom.csv', 5000)#每个小的csv文件存放1000条
