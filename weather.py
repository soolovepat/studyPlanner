import pandas as pd
import json
import requests
from bs4 import BeautifulSoup


def weather_post():
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0'
    queryParams = '?' + \
                'ServiceKey=' + 'Sr%2B27kz7%2FkOMz2PRkUuaKHUUul1my6w4CR%2FspK9gQyL3RbFFwN%2FQPpnC%2Bn9y%2B6pv8I%2BBgCMp6JSbWOeobLWRwg%3D%3D' + \
                '&pageNo='+ '1' + \
                '&numOfRows='+ '999' + \
                '&dataType='+ 'JSON' + \
                '&dataCd='+ 'ASOS' + \
                '&dateCd='+ 'DAY' + \
                '&startDt='+ '20180601' + \
                '&endDt='+ '20200421' + \
                '&stnIds='+ '108'
    result = requests.get(url + queryParams)
    js = json.loads(result.content)
    data = pd.DataFrame(js['response']['body']['items']['item'])

    li = ['stnId','tm','avgTa','minTa','maxTa','sumRn','maxWs','avgWs','ddMes']
    data.loc[:,li]
    data[li].to_csv("weather.csv",index=False )



weather_post()
