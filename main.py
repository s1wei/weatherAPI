#!/usr/bin/python3
# _*_ coding: utf-8 _*_
"""
Copyright (C) 2024 - s1wei.com, Inc. All Rights Reserved

@Author  : s1wei
@Email   : admin@s1wei.com
@Blog    : https://www.denceun.cn/author/1/
@File    : WeatherApi.py
@IDE     : PyCharm
@Talk    : 此为我最初版本的代码，纯手写，其余均为ai辅助生成
"""


import json
import requests

def RealWeather(stationid):

    url = f'http://www.nmc.cn/rest/weather?stationid={stationid}'
    response = requests.get(url)

    if response.status_code == 200:

        data = response.text

        response_data = json.loads(data)
        real = response_data['data']['real']         # 实况

        city = real['station']['city']  # 城市
        publish_time = real['publish_time']          # 更新时间

        # 天气
        temperature = real['weather']['temperature'] if real['weather']['temperature'] != '9999' else '无'          # 温度
        temperatureDiff = real['weather']['temperatureDiff']  if real['weather']['temperatureDiff'] != '9999' else '无'    # 温差
        humidity = real['weather']['humidity'] if real['weather']['humidity'] != '9999' else '无'                  # 相对湿度
        info = real['weather']['info'] if real['weather']['info'] != '9999' else '无'                          # 情况
        feelst = real['weather']['feelst'] if real['weather']['feelst'] != '9999' else '无'                      # 体感温度

        # 风
        direct = real['wind']['direct'] if real['wind']['direct'] != '9999' else '无'                       # 风向
        power = real['wind']['power'] if real['wind']['power'] != '9999' else '无'                 # 风速

        # 预警
        alert = real['warn']['alert'] if real['warn']['alert'] != '9999' else '无'                          # 警报
        issuecontent = real['warn']['issuecontent'] if real['warn']['issuecontent'] != '9999' else '无'             # 问题内容
        fmeans = real['warn']['fmeans'] if real['warn']['fmeans'] != '9999' else '无'                         # 应对方式
        signaltype = real['warn']['signaltype'] if real['warn']['signaltype'] != '9999' else '无'                 # 信号类型
        signallevel = real['warn']['signallevel'] if real['warn']['signallevel'] != '9999' else '无'               # 信号等级


        RealInfo = (f'天气实况:{city}\n'
              f'更新时间:{publish_time}\n'
              f'天气:{info} {temperature}℃\n'
              f'体感温度:{feelst}℃\n'
              f'{direct} {power}\n'
              f'{signallevel}预警 {signaltype}\n'
              f'警报:{alert}\n'
              # f'问题:{issuecontent}\n'
              f'应对:{fmeans}')

        return RealInfo

def PredictWeather(stationid):

    url = f'http://www.nmc.cn/rest/weather?stationid={stationid}'
    response = requests.get(url)

    if response.status_code == 200:

        data = response.text

        response_data = json.loads(data)

        predict = response_data['data']['predict']   # 预测

        city = predict['station']['city']  # 城市
        publish_time = predict['publish_time']          # 更新时间

        details = predict['detail']               # 细节

        RealInfo = (f'天气预报:{city}\n更新时间:{publish_time}\n')

        for detail in details:
            date = detail['date']       # 日期
            pt = detail['pt']           # 预测时间

            day_info = detail['day']['weather']['info'] if detail['day']['weather']['info'] != '9999' else '无'
            day_temperature = detail['day']['weather']['temperature'] if detail['day']['weather']['temperature'] != '9999' else '无'
            day_direct = detail['day']['wind']['direct'] if detail['day']['wind']['direct'] != '9999' else '无'  # 风向
            day_power = detail['day']['wind']['power'] if detail['day']['wind']['power'] != '9999' else '无'  # 风速
            night_info = detail['night']['weather']['info'] if detail['night']['weather']['info'] != '9999' else '无'
            night_temperature = detail['night']['weather']['temperature'] if detail['night']['weather']['temperature'] != '9999' else '无'
            night_direct = detail['night']['wind']['direct'] if detail['night']['wind']['direct'] != '9999' else '无'  # 风向
            night_power = detail['night']['wind']['power'] if detail['night']['wind']['power'] != '9999' else '无'  # 风速

            detail_Info = (f'\n------------\n'
                           f'日期:{date}\n'
                           f'预测时间:{pt}\n'
                           f' 白天:\n'
                           f'  天气:{day_info} {day_temperature}℃\n'
                           f'  {day_direct} {day_power}\n'
                           f' 晚上:\n'
                           f'  天气:{night_info} {night_temperature}℃\n'
                           f'  {night_direct} {night_power}')

            RealInfo = RealInfo + detail_Info

        return RealInfo

if __name__ == '__main__':

    太原 = '53679'
    print(RealWeather(太原))
    print(PredictWeather(太原))
