from bs4 import BeautifulSoup as bs
import requests
import urllib

webpage = urllib.request.urlopen('https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=%EC%84%9C%EC%9A%B8%EB%82%A0%EC%94%A8')

soup = bs(webpage, 'html.parser')
temps = soup.find('div','temperature_text')
summary = soup.find('p','summary')
# print(temps)
print("서울 "+temps.text.strip())
print(summary.text.strip())