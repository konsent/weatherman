import requests
from appid import appid

def get_weather():
    ## 원하는 지역의 위도와 경도를 호출하기 위한 API 호출
    # 원하는 지역의 이름을 입력한다
    location = "yeoksam"

    # 해당 지역의 위도와 경도를 API를 통해 파싱한다
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=5&appid={appid}"
    geo_json_file = requests.get(geo_url)
    geo_json = geo_json_file.json()[0]

    #파싱한 위도와 경로를 변수에 입력한다
    lat = geo_json['lat']
    lon = geo_json['lon']

    # 날씨 자료를 가져오는 API 호출한다
    weather_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={appid}"
    weather_json = requests.get(weather_url)
    daily_weather_json = weather_json.json()["list"]

    # 호출시간 기준 3시간 단위로 5번 체감 온도를 파싱한다
    temp = []
    rain = []
    for i in range(5):
        temp.append(daily_weather_json[i]['main']['feels_like'])
        rain.append(daily_weather_json[i]['weather'][0]['main'])

    # 최종 메시지를 담을 리스트를 생성한다
    message = []

    # 만약 비가 한 번이라도 오면 비가 온다고 알려준다
    if 'Rain' in rain or 'Snow' in rain:
        message.append("우산 챙겨라")
    else:
        message.append("비 안옴. 우산 냅두고 가셈")
        
    # 평균 체감온도를 계산한다
    avg_temp = (min(temp)+max(temp)) / 2

    # 최저 체감온도와 최고 체감온도를 알려준다
    message.append("최저 체감온도 :{} / 최고 체감온도 :{}".format(min(temp),max(temp)))

    # 온도별 옷차림
    if avg_temp >= 28:
        message.append("오늘 개더움. 반팔, 반바지 입어라")
    elif avg_temp >= 23:
        message.append("더움. 반팔, 얇은 셔츠, 반바지 입어라")
    elif avg_temp >= 20:
        message.append("적당함. 얇은 가디건, 긴팔, 면바지, 청바지 입어라")
    elif avg_temp >= 17:
        message.append("적당함 니트, 맨투맨, 가디건, 청바지 입어라")
    elif avg_temp >= 12:
        message.append("살짝 서늘. 자켓, 가디건, 잠바 입어라")
    elif avg_temp >= 9:
        message.append("추워. 자켓, 코트, 잠바, 니트 입어라")
    elif avg_temp >= 5:
        message.append("좀 춥다. 코트, 잠바, 자켓, 히트텍, 속옷, 니트 입어라")
    else:
        message.append("개추워. 히트텍 무조건! 패딩, 목도리 기모 챙겨입어라")
        
    return(message)

result = '\n'.join(get_weather())
print(result)
