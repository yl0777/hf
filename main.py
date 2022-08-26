from datetime import date, datetime, timedelta
import math
from turtle import color
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now() + timedelta(hours=8)
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_ids = os.environ["USER_ID"].split("\n")
template_id = os.environ["TEMPLATE_ID"]

#天行数据api
def get_weather1():
  url = "http://api.tianapi.com/tianqi/index?key=edffe502a886868c5ef92045ab3c6ce1&city=" + city
  res1 = requests.get(url).json()
  muzi = res1['newslist'][0]
  #area 城市  week = 星期 weather = 今天天气  real = 当前温度  lowest = 最低气温  highest= 最高气温  wind = 风项  windsc = 风力 sunrise = 日出时间 sunset = 日落时间 pop = 降雨概率 tips = 穿衣建议 
  return muzi['area'], muzi['week'], muzi['weather'], muzi['real'], muzi['lowest'], muzi['highest'], muzi['wind'], muzi['windsc'], muzi['sunrise'], muzi['sunset'], muzi['pop'], muzi['tips']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

#生日
def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

#彩虹屁接口
def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

#朋友圈文案api接口
def get_words1():
  words1 = requests.get("https://api.shadiao.pro/pyq")
  if words1.status_code != 200:
    return get_words1()
  return words1.json()['data']['text']

#随机颜色1
# def get_random_color():
#   return "#%06x" % random.randint(0, 0xFFFFFF)

#随机颜色2
def get_random_color():
  colorArr = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
  color = ""
  for i in range(6):
      color += colorArr[random.randint(0,14)]
  return "#"+color

client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)
# wea, temperature, highest, lowest = get_weather()
area, week, weather, real, lowest, highest, wind, windsc, sunrise, sunset, pop, tips = get_weather1()
data = {
    "date1": {
        'value':'📅今天是：'
    },
    "city1": {
        'value':'🏙城市：'
    },
    "tq": {
        "value":'🌤今天天气：'
    },
    "wind_windsc": {
        "value":'🌀风向风速：'
    },
    "temperature1": {
        'value':'🌡当前温度：'
    },
    "lowest1": {
        'value':'🌑今日最低温：'
    },
    "highest1": {
        'value':'🌈今日最高温：'
    },
    "sunrise1": {
        'value':'🌅日出时间：'
    },
    "sunset1": {
        'value':'🌇日落时间：'
    },
    "pop1": {
        'value':'💧降雨概率：'
    },
    "tips1": {
        "value":'👗穿衣建议：'
    },
    "love_days1": {
        'value':' 💕我们已经认识：'
    },
    "birthday_left1": {
      "value":'🎂我的生日还有：'
    },
    #随机情话
    "words": {
        "value":get_words(),
        "color":get_random_color()
    },
}
count = 0
for user_id in user_ids:
  res = wm.send_template(user_id, template_id, data)
  count+=1
print("发送了" + str(count) + "条消息")
