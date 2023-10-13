import requests
from bs4 import BeautifulSoup 
from selenium import webdriver

def get_google_data(keyword):
    url = f'http://www.google.com/search?q={keyword}'
    response = requests.get(url)

    # 크롬 브라우저가 열림
    # 이때 동적인 내용들이 모두 채워진다!
    driver = webdriver.Chrome()
    driver.get(url)

    # 열린 페이지 소스를 받아옴
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    print(html)

get_google_data('파이썬')