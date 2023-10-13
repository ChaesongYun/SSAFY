from django.shortcuts import render
import matplotlib.pyplot as plt

# io: 입출력 연산을 위한 python 표준 라이브러리
# BytesIO: 이진데이터를 다루기 위한 버퍼를 제공
# Buffer: 임시 저장 공간
# 파일 시스템과 유사하지만 
# 실제로 파일로 만들지 않고 메모리단에서 작업할 수 있음
from io import BytesIO

# 텍스트 <-> 이진 데이터를 변환할 수 있는 모듈
import base64
plt.switch_backend('Agg')

import pandas as pd
csv_path = 'weathers/data/austin_weather.csv'

# Create your views here.
def problem1(request):
    df = pd.read_csv(csv_path)
    context = {
        'df' : df,
    }
    return render(request, 'weathers/problem1.html', context)


def problem2(request):
    df = pd.read_csv(csv_path)
    
    x = list(pd.to_datetime(df['Date'], format='%Y-%m-%d'))
    y_tempHigh = list(df['TempHighF']) # 최고 온도
    y_tempAvg = list(df['TempAvgF']) # 평균 온도
    y_tempLow = list(df['TempLowF']) # 최저 온도
    
    plt.clf() 
    
    plt.plot(x, y_tempHigh)
    plt.plot(x, y_tempAvg)
    plt.plot(x, y_tempLow)

    plt.grid(visible=True)
    plt.legend(('High Temperature', 'Average Temperature', 'Low Temperature'), loc=8)

    plt.title('Temperature Variation')
    plt.xlabel('Date')
    plt.ylabel('Temperature(Fahrenheit)')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')
    buffer.close()
    
    context = {
         'chart_image' : f'data:image/png;base64, {image_base64}',
    }
    return render(request, 'weathers/problem2.html', context)


def problem3(request):
    df = pd.read_csv(csv_path)
    df['Date'] = df['Date'].astype('str').apply(lambda x: x[0:7])
    df.set_index('Date', inplace=True)
    df = df[['TempHighF', 'TempAvgF', 'TempLowF']].astype('float')
    df.reset_index(inplace=True)
    df = df.groupby(df['Date']).mean()
    
    plt.clf() 
    
    print(df['TempHighF'])
    df['TempHighF'].plot(kind='line')
    df['TempAvgF'].plot(kind='line')
    df['TempLowF'].plot(kind='line')

    plt.grid(visible=True)
    plt.legend(('High Temperature', 'Average Temperature', 'Low Temperature'), loc=4)

    plt.title('Temperature Variation')
    plt.xlabel('Date')
    plt.ylabel('Temperature(Fahrenheit)')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')
    buffer.close()
    
    context = {
         'chart_image' : f'data:image/png;base64, {image_base64}',
    }
    return render(request, 'weathers/problem3.html', context)


# ------------------------------------------------------------


def problem4(request):
    df = pd.read_csv(csv_path)
    events_set = set(df['Events'])
    new_set = set()
    for e in events_set:
        if ',' in e:
            new_set | set(e.split(' , '))
        else:
            new_set.add(e)

    events_lst = list(df['Events'])
    for e in events_lst:
        if ',' in e:
            events_lst.remove(e)
            events_lst.extend(list(e.split(' , ')))

    x = list(new_set)
    y = []
    for i in range(len(x)):
        if(x[i] == ' '):
            x[i] = 'No Events'
            y.append(events_lst.count(' '))
        else:
            y.append(events_lst.count(x[i]))
    
    res = list(zip(x, y))
    res.sort(key=lambda x : -x[1])
    x.clear()
    y.clear()
    
    for now in res:
        x.append(now[0])
        y.append(now[1])
    
    plt.clf()
    plt.bar(x, y)
    plt.title("Events Counts")
    plt.grid(visible=True)
    plt.ylabel('Count')
    plt.xlabel('Events')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')
    buffer.close()
    
    context = {
        'chart_image' : f'data:image/png;base64, {image_base64}',
    }
    return render(request, 'weathers/problem4.html', context)