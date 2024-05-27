#!/usr/bin/python3
# _*_ coding: utf-8 _*_
"""
Copyright (C) 2024 - s1wei.com, Inc. All Rights Reserved 

@Author  : s1wei
@Email   : admin@s1wei.com
@Blog    : https://www.denceun.cn/author/1/
@File    : Test.py
@IDE     : PyCharm
"""

import requests

def get_real_weather(city_name):
    url = 'http://127.0.0.1:5000/real_weather'
    params = {'city': city_name}

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        print("实时天气信息:")
        print(f"城市: {data['city']}")
        print(f"更新时间: {data['publish_time']}")
        print(f"天气: {data['info']}")
        print(f"温度: {data['temperature']}℃")
        print(f"体感温度: {data['feelst']}℃")
        print(f"风向: {data['wind_direct']}")
        print(f"风力: {data['wind_power']}")
        print(f"预警: {data['signallevel']} {data['signaltype']}")
        print(f"警报: {data['alert']}")
        print(f"应对措施: {data['fmeans']}")
    else:
        print("无法获取天气信息:", response.json())

def get_predict_weather(city_name):
    url = 'http://127.0.0.1:5000/predict_weather'
    params = {'city': city_name}

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        print("天气预报信息:")
        print(f"城市: {data['city']}")
        print(f"更新时间: {data['publish_time']}")
        for detail in data['details']:
            print(f"日期: {detail['date']}")
            print(f"预测时间: {detail['pt']}")
            print("白天:")
            print(f"  天气: {detail['day']['info']}")
            print(f"  温度: {detail['day']['temperature']}℃")
            print(f"  风向: {detail['day']['wind_direct']}")
            print(f"  风力: {detail['day']['wind_power']}")
            print("晚上:")
            print(f"  天气: {detail['night']['info']}")
            print(f"  温度: {detail['night']['temperature']}℃")
            print(f"  风向: {detail['night']['wind_direct']}")
            print(f"  风力: {detail['night']['wind_power']}")
    else:
        print("无法获取天气信息:", response.json())

if __name__ == '__main__':
    city_name = '太原'
    get_real_weather(city_name)
    get_predict_weather(city_name)
