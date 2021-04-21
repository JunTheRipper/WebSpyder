import pandas as pd
import collections
import time

def concat_xlsx(filename):
    '''
    :param filename:
    :return: df
    :function: 实现一个表格的多sheet的合并
    '''
    df_dict0 = pd.read_excel(filename, sheet_name=None, index_col=None, na_values=['NA'])
    df_dict0 = collections.OrderedDict(sorted(df_dict0.items()))
    df = pd.concat(df_dict0.values(), ignore_index=True)
    return df

def tables_xlsx_concat(df1,df2):
    '''
    :param df1:
    :param df2:
    :return: dfx
    :function 实现两个表格数据合并（前提是两个表格维度相同）
    '''
    dfx = pd.concat([df1, df2], ignore_index=True)
    return dfx


def generate_data_needed(datafm):
    '''
    function:实现对所需要的维度的提取，在这里我们只保留微博内容和微博地址两项
    :param datafm: pd.DataFrame
    :return: dealt_df
    '''
    return datafm[['微博内容','微博地址']]


def add_labels(df,label):
    '''
    function:为相关的DataFrame格式的项目打上标签
    :param df:
    :param label:
    :return df:
    '''
    df['标签']  =  label
    return df


label_file_MaLong = 'Data/0/data.xlsx'
label_file_Stars_1 = 'Data/1/WYB.xlsx'
label_file_Stars_2 = 'Data/1/WYB2.xlsx'
label_file_Stars_3 = 'Data/1/XZ.xlsx'
label_file4 = ''
label_file5 = ''
label_file_Game = 'Data/2/new原神.xlsx'
label_file_COVID_1 = 'Data/3/new疫苗.xlsx'
label_file_COVID_2 = 'Data/3/新冠00.xlsx'
label_file_COVID_3 = 'Data/3/新冠01.xlsx'

# 4类的dataFrame
dataA = add_labels(generate_data_needed(concat_xlsx(label_file_MaLong)),0)

dataB = None

dataC = add_labels(generate_data_needed(concat_xlsx(label_file_Game)),2)

dataD = add_labels(generate_data_needed(
    tables_xlsx_concat(
        tables_xlsx_concat(
            concat_xlsx(label_file_COVID_1),
            concat_xlsx(label_file_COVID_2)),
        concat_xlsx(label_file_COVID_3))),3)


whole_data = pd.concat([dataA, dataB, dataC, dataD], ignore_index=True)
print(whole_data.shape)


whole_data=whole_data.dropna(axis=0, subset= ["微博内容","微博地址"])
whole_data.reset_index(drop=True,inplace=True)

whole_data = whole_data.drop_duplicates(['微博内容', '微博地址'],keep='last')
whole_data.reset_index(drop=True,inplace=True)

whole_data['微博内容'] = whole_data['微博内容'].str.replace(r'[^\w]+', '')

import finalseg
start = time.perf_counter()

content_data = whole_data['微博内容'].values
label_data = whole_data['标签'].values
segdata = []
for line in content_data:
    try:
        seglist=finalseg.cut(line)
        segdata.append('|'.join(seglist))
    except AttributeError:
        pass

end =time.perf_counter()
print("程序运行时间为：",end-start,"s")
print(segdata[0:5])
