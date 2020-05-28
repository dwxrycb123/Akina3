from bs4 import BeautifulSoup
import re
from pypinyin import lazy_pinyin
import os
import json
import aiohttp

from config import *
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def get_weather_by_city(name, index):
    area_id = get_area_id(name)
    if area_id is None:
        return None, None, None, None, None
    dates, win_level, low_temperature, high_temperature, weather = await get_weather(area_id, index)
    return dates, win_level, low_temperature, high_temperature, weather    

def get_number(string):
    regex = re.compile('([0-9]+)')
    return int(regex.findall(string)[0])

async def get_weather_msg(city, tomorrow):
    index = 1 if tomorrow else 0
    dates, win_level, low_temperature, high_temperature, weather = await get_weather_by_city(city, index)
    if win_level is None:
        return '暂不支持查询该城市的天气'
    
    info = '{}{}最高温度为{}，最低温度为{}，风级{}，天气：{}'.format(city, dates, high_temperature, low_temperature, win_level, weather)

    if get_number(high_temperature) > 29:
        info += '\n白天较热，请注意防暑降温'
    if get_number(low_temperature) < 16:
        info += '\n早晚温度较低，请注意保暖'
    if get_number(win_level) > 7:
        info += '\n今日的风儿甚是喧嚣，请小心被吹飞，注意树枝等可能的掉落物'
    if '雨' in weather or '雪' in weather:
        info += '\n雨雪天气请记得带伞，小心防滑'

    return info


f = open(CITY_JSON_PATH)
area_data = json.load(f)
f.close()

def get_area_id(name):
    if name == '':
        return '101220101'
    pyin = ''.join(lazy_pinyin(name))
    for item in area_data:
        if item['cityEn'] == pyin:
            return item['id']
    return None

    
'''
get_area_id = {
    '' : '101220101',
    '合肥' : '101220101', 
    '北京' : '101010100'
}
'''

async def get_weather(area_id=101220101, day=0):
    async with aiohttp.ClientSession() as session:
        resp = await fetch(session, 'http://www.weather.com.cn/weather/101220101.shtml'.format(area_id))
    soup = BeautifulSoup(resp,'html.parser')
    tagDate=soup.find('ul', class_="t clearfix")

    tag = tagDate.find_all('li')[day]

    dates = tag.h1.string

    tagCurrent = tag.find('p', class_="tem")
    try:
        high_temperature = tagCurrent.span.string
    except AttributeError as e:
        high_temperature = tagCurrent.find_next('p', class_="tem").span.string

    low_temperature = tagCurrent.i.string
    weather = soup.find('p', class_="wea").string

    tagWind = soup.find('p',class_="win")
    win_level = tagWind.i.string

    return dates, win_level, low_temperature, high_temperature, weather

"""
if __name__ == '__main__':
    dates, win_level, low_temperature, high_temperature, weather = get_weather()
    print('今天是：' + dates)
    print('风级：' + win_level)
    print('最低温度：' + low_temperature)
    print('最高温度：' + high_temperature)
    print('天气：' + weather)
"""