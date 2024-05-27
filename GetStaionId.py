#!/usr/bin/python3
# _*_ coding: utf-8 _*_
"""
Copyright (C) 2024 - s1wei.com, Inc. All Rights Reserved 

@Author  : s1wei
@Email   : admin@s1wei.com
@Blog    : https://www.denceun.cn/author/1/
@File    : GetStaionId.py
@IDE     : PyCharm
"""
import json
import requests
import configparser

def fetch_city_data():
    url = 'https://weather.cma.cn/api/map/weather/1'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['code'] == 0:
            cities = data['data']['city']
            return cities
        else:
            print("Error in response data:", data['msg'])
            return None
    else:
        print("Failed to fetch city data")
        return None

def save_to_ini(cities, filename='stationid.ini'):
    config = configparser.ConfigParser()

    # 添加 section
    config.add_section('CityToStationID')

    for city in cities:
        station_id = city[0]
        city_name = city[1]
        config['CityToStationID'][city_name] = station_id

    with open(filename, 'w') as configfile:
        config.write(configfile)

if __name__ == '__main__':
    cities = fetch_city_data()
    if cities:
        save_to_ini(cities)
        print("City data saved to stationid.ini")
    else:
        print("No city data available")

