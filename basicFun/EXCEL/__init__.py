import os
import xdrlib, sys
import xlrd
import traceback
from datetime import datetime
from xlrd import xldate_as_tuple
def excel_table_byindex(file, colnameindex=0, by_index=0, by_name=u'Sheet1'):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows  # 行数
    print('nrows-->', nrows)
    ncols = table.ncols  # 列数
    #    ncols=2
    print('ncols-->', ncols)
    list = []
    for rownum in range(2, nrows):# 前2行不要
        # 获取table中第rownum行的数据#
        row = table.row_values(rownum)
        video_name = row[0]#每一行必须有视频名字
        str_time0 = row[index * 3 - 2]
        end_time0 = row[index * 3-1]
        ends=row[index * 3]
        if str_time0 != '' and end_time0 != '':#两个时间都有的行才加入list
            str_hour = str_time0.split('.')[0]
            # str_hour = 0
            str_min = str_time0.split('.')[1]
            str_sec = str_time0.split('.')[2]
            end_hour = end_time0.split('.')[0]
            # end_hour=0
            end_min = end_time0.split('.')[1]
            end_sec = end_time0.split('.')[2]
            # 需要剪切的视频时间,转换成秒计算
            headTime=15
            tailTime=headTime
            if ends=='sta':
                headTime=0
            elif ends=='end':
                tailTime=0
            str_seconds = int(str_hour) * 3600 + int(str_min) * 60 + int(str_sec)-headTime
            end_seconds = int(end_hour) * 3600 + int(end_min) * 60 + int(end_sec)+tailTime
            # str_time = str_hour + ':' + str_min + ':' + str_sec
            str_time =str(str_seconds // 3600) + ':' + str(str_seconds % 3600 // 60) + ':' + str(str_seconds % 60)
            end_time =str(end_seconds // 3600) + ':' + str(end_seconds % 3600 // 60) + ':' + str(end_seconds % 60)
            dur_seconds = end_seconds - str_seconds
            duration = str(dur_seconds // 3600) + ':' + str(dur_seconds % 3600 // 60) + ':' + str(dur_seconds % 60)
            print(video_name, str_time, end_time, duration)
            list.append(video_name + ' ' + str_time + ' ' + end_time + ' ' + duration+' '+str(str_seconds))
    return list
def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except:
        print("Error when opening xlsx")

def info():
    print("open_excel(file) -> <class 'xlrd.book.Book'>")
    print("excel_table_byindex(file, colnameindex=0, by_index=0, by_name=u'Sheet1') ->  <class 'list'>")
    exit()