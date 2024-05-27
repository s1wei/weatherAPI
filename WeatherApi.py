#!/usr/bin/python3
# _*_ coding: utf-8 _*_
"""
Copyright (C) 2024 - s1wei.com, Inc. All Rights Reserved 

@Author  : s1wei
@Email   : admin@s1wei.com
@Blog    : https://www.denceun.cn/author/1/
@File    : WeatherApi.py
@IDE     : PyCharm
"""

from flask import Flask, jsonify, request
import json
import requests
import configparser

app = Flask(__name__)

def load_city_station_map(filename='stationid.ini'):
    config = configparser.ConfigParser()
    config.read(filename)
    city_station_map = dict(config['CityToStationID'])
    return city_station_map

CITY_STATION_MAP = load_city_station_map()

def get_stationid_by_city(city_name):
    return CITY_STATION_MAP.get(city_name)

def get_real_weather(stationid):
    url = f'http://www.nmc.cn/rest/weather?stationid={stationid}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        real = data['data']['real']

        city = real['station']['city']
        publish_time = real['publish_time']

        temperature = real['weather']['temperature'] if real['weather']['temperature'] != '9999' else '无'
        temperatureDiff = real['weather']['temperatureDiff'] if real['weather']['temperatureDiff'] != '9999' else '无'
        humidity = real['weather']['humidity'] if real['weather']['humidity'] != '9999' else '无'
        info = real['weather']['info'] if real['weather']['info'] != '9999' else '无'
        feelst = real['weather']['feelst'] if real['weather']['feelst'] != '9999' else '无'

        direct = real['wind']['direct'] if real['wind']['direct'] != '9999' else '无'
        power = real['wind']['power'] if real['wind']['power'] != '9999' else '无'

        alert = real['warn']['alert'] if real['warn']['alert'] != '9999' else '无'
        issuecontent = real['warn']['issuecontent'] if real['warn']['issuecontent'] != '9999' else '无'
        fmeans = real['warn']['fmeans'] if real['warn']['fmeans'] != '9999' else '无'
        signaltype = real['warn']['signaltype'] if real['warn']['signaltype'] != '9999' else '无'
        signallevel = real['warn']['signallevel'] if real['warn']['signallevel'] != '9999' else '无'

        real_info = {
            'city': city,
            'publish_time': publish_time,
            'temperature': temperature,
            'temperature_diff': temperatureDiff,
            'humidity': humidity,
            'info': info,
            'feelst': feelst,
            'wind_direct': direct,
            'wind_power': power,
            'alert': alert,
            'issuecontent': issuecontent,
            'fmeans': fmeans,
            'signaltype': signaltype,
            'signallevel': signallevel
        }
        return real_info
    else:
        return None

def get_predict_weather(stationid):
    url = f'http://www.nmc.cn/rest/weather?stationid={stationid}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        predict = data['data']['predict']

        city = predict['station']['city']
        publish_time = predict['publish_time']
        details = predict['detail']

        forecast = {
            'city': city,
            'publish_time': publish_time,
            'details': []
        }

        for detail in details:
            date = detail['date']
            pt = detail['pt']
            day_info = detail['day']['weather']['info'] if detail['day']['weather']['info'] != '9999' else '无'
            day_temperature = detail['day']['weather']['temperature'] if detail['day']['weather']['temperature'] != '9999' else '无'
            day_direct = detail['day']['wind']['direct'] if detail['day']['wind']['direct'] != '9999' else '无'
            day_power = detail['day']['wind']['power'] if detail['day']['wind']['power'] != '9999' else '无'
            night_info = detail['night']['weather']['info'] if detail['night']['weather']['info'] != '9999' else '无'
            night_temperature = detail['night']['weather']['temperature'] if detail['night']['weather']['temperature'] != '9999' else '无'
            night_direct = detail['night']['wind']['direct'] if detail['night']['wind']['direct'] != '9999' else '无'
            night_power = detail['night']['wind']['power'] if detail['night']['wind']['power'] != '9999' else '无'

            forecast['details'].append({
                'date': date,
                'pt': pt,
                'day': {
                    'info': day_info,
                    'temperature': day_temperature,
                    'wind_direct': day_direct,
                    'wind_power': day_power
                },
                'night': {
                    'info': night_info,
                    'temperature': night_temperature,
                    'wind_direct': night_direct,
                    'wind_power': night_power
                }
            })
        return forecast
    else:
        return None

@app.route('/real_weather', methods=['GET'])
def real_weather():
    city_name = request.args.get('city')
    if city_name:
        stationid = get_stationid_by_city(city_name)
        if stationid:
            data = get_real_weather(stationid)
            if data:
                return jsonify(data), 200
            else:
                return jsonify({'error': 'Unable to fetch data'}), 500
        else:
            return jsonify({'error': 'Invalid city name'}), 400
    else:
        return jsonify({'error': 'City name is required'}), 400

@app.route('/predict_weather', methods=['GET'])
def predict_weather():
    city_name = request.args.get('city')
    if city_name:
        stationid = get_stationid_by_city(city_name)
        if stationid:
            data = get_predict_weather(stationid)
            if data:
                return jsonify(data), 200
            else:
                return jsonify({'error': 'Unable to fetch data'}), 500
        else:
            return jsonify({'error': 'Invalid city name'}), 400
    else:
        return jsonify({'error': 'City name is required'}), 400

if __name__ == '__main__':
    app.run(debug=True)

