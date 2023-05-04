# -*- coding: utf-8 -*-
"""
Created on Tue May  1 15:52:55 2018

@author: zhangying
"""

import json
from urllib.parse import quote
import requests
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

city_map = {}  # 地面到坐标的映射


def getlnglat(city):
    if city in city_map:
        return city_map[city]
    url = 'https://restapi.amap.com/v3/geocode/geo?key=89d50ae382cd4213105df3131aa696f6&address={}'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }
    resp = requests.get(url.format(city), headers=header)
    js = json.loads(resp.text)
    jd, wd = js['geocodes'][0]['location'].split(',')
    jd, wd = float(jd), float(wd)
    city_map[city] = (jd, wd)
    return (jd, wd)


# 用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
# 用来正常显示负号
plt.rcParams['axes.unicode_minus'] = False

"""1、数据加载"""
# 定义加载数据的文件名
filename = "../data_file/wuhan-clearn-utf8.csv"
# 自定义数据的行列索引（行索引使用pd默认的，列索引使用自定义的）
names = [
    "id", "communityName", "areaName", "total", "unitPriceValue",
    "fwhx", "szlc", "jzmj", "hxjg", "tnmj",
    "jzlx", "fwcx", "jzjg", "zxqk", "thbl",
    "pbdt", "cqnx", "gpsj", "jyqs", "scjy",
    "fwyt", "fwnx", "cqss", "dyxx", "fbbj", "other"
]
# 自定义需要处理的缺失值标记列表
miss_value = ["null", "暂无数据"]
# 数据类型会自动转换
# 使用自定义的列名，跳过文件中的头行，处理缺失值列表标记的缺失值
df = pd.read_csv(filename, header=0, names=names, na_values=miss_value)

"""2、生成经纬度信息"""
# lats = []
# lngs = []
# units = []
# totals = []
#
# # flag = 0
# for idx, row in df.iterrows():
#     name = row.loc['communityName']
#     unit = row.loc['unitPriceValue']
#     total = row.loc['total']
#     lng, lat = getlnglat("武汉市" + name)
#     if lat != 0 or lng != 0:
#         lats.append(lat)
#         lngs.append(lng)
#         units.append(unit)
#         totals.append(total)
#         print(idx)
#
# lat_lng_data = {"lat": lats, "lng": lngs, "total": totals, "unit": units}
#
# frame_test = pd.DataFrame(lat_lng_data)
# frame_test.to_csv("../data_file/latlng.csv")

"""3、合并数据，并按格式输出数据"""
# 合并数据
df_latlng = pd.read_csv("../data_file/latlng.csv", index_col=0)
# df_latlng = frame_test
print(df_latlng.head())

"""4、生成需要的格式文件"""
out_unit = "../data_file/unit.js"
with open(out_unit, "w") as file_out:
    file_out.write('var heatmapData = [\n')
    for idx, row in df_latlng.iterrows():
        [lat, lng, total, unit] = row
        out = f'{{"lng":{lng},"lat":{lat},"count":{int(unit)}}},\n'
        file_out.write(out)
    file_out.write('];')

out_total = "../data_file/total.js"
with open(out_total, "w") as file_out:
    file_out.write('var heatmapData = [\n')
    for idx, row in df_latlng.iterrows():
        [lat, lng, total, unit] = row
        out = f'{{"lng":{lng},"lat":{lat},"count":{int(total)}}},\n'
        file_out.write(out)
    file_out.write('];')

out_xy = "../data_file/xy.js"
with open(out_xy, "w") as file_out:
    file_out.write('var heatmapData = [\n')
    for idx, row in df_latlng.iterrows():
        [lat, lng, total, unit] = row
        if total > 100:
            continue
        out = f'{{"lng":{lng},"lat":{lat},"count":{int(total)}}},\n'
        file_out.write(out)
    file_out.write('];')