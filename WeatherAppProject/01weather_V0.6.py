# Update v0.6 (2022-09-29)
# 1. 해외 도시 날씨 검색 기능 추가
# 2. 지역 입력 후 엔터키 입력시 날씨 검색 기능 추가

import requests
import sys
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *

form_class = uic.loadUiType('../ui/weatherAppUi.ui')[0]


class WeatherAppWin(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('오늘의 날씨')
        self.setWindowIcon(QIcon('../icons/weather.png'))
        self.statusBar().showMessage('WEATHER APP VER 0.6')
        self.weather_btn.clicked.connect(self.crawling_weather)
        self.input_area.returnPressed.connect(self.crawling_weather)

    def crawling_weather(self):
        weather_area = self.input_area.text()   # 사용자가 입력한 지역명 문자열 가져오기
        weather_html = requests.get('https://search.naver.com/search.naver?query={}날씨'.format(weather_area))

        weather_soup = BeautifulSoup(weather_html.text, 'html.parser')

        try:
            # 오늘 현재 온도
            today_temper = weather_soup.find('div', {'class': 'temperature_text'}).text
            today_temper = today_temper[6:11]

            # 어제와의 날씨 비교
            yesterday_weather = weather_soup.find('p', {'class': 'summary'}).text
            yesterday_weather = yesterday_weather[:13]

            # 오늘 날씨(ex:맑음)
            today_weather = weather_soup.find('span', {'class': 'weather before_slash'}).text
            if '맑음' in today_weather:
                today_weather = '맑음'
            elif '흐림' in today_weather:
                today_weather = '흐림'
            elif '구름' in today_weather:
                today_weather = '흐림'
            elif '비' in today_weather:
                today_weather = '비'
            elif '눈' in today_weather:
                today_weather = '눈'
            elif '소나기' in today_weather:
                today_weather = '비'
            elif '화창' in today_weather:
                today_weather = '맑음'

            # 검색된 지역 이름
            area = weather_soup.find('h2', {'class': 'title'}).text

            # 체감 온도
            sense_temper = weather_soup.select('dl.summary_list>dd')
            sense_temper = sense_temper[0].text

            # 미세먼지 정보
            dust_info = weather_soup.select('ul.today_chart_list>li')
            dust1 = dust_info[0].find('span', {'class': 'txt'}).text

            # 초미세먼지 정보
            dust2 = dust_info[1].find('span', {'class': 'txt'}).text
            # dust_info[2] : 자외선 정보, dust_info[3] : 일몰시간

            self.area_label.setText(area)
            # self.weather_img_label.setText(today_weather)
            # 날씨 이미지 함수 호출
            self.setWeatherImage(today_weather)
            self.temper_label.setText(today_temper)
            self.yesterday_label.setText(yesterday_weather)
            self.sense_label.setText(sense_temper)
            self.dust1_label.setText(dust1)
            self.dust2_label.setText(dust2)

        except:

            # 해외 도시 날씨
            try:
                # 해외지역 이름
                area = weather_soup.find('span', {'class': 'btn_select'}).text
                area = area.strip()
                # 현재 온도
                today_temper = weather_soup.find('span', {'class': 'todaytemp'}).text
                # 현재 날씨
                today_weather = weather_soup.find('p', {'class': 'cast_txt'}).text
                if '흐림' in today_weather:
                    today_weather = '흐림'
                elif '맑음' in today_weather:
                    today_weather = '맑음'
                elif '구름' in today_weather:
                    today_weather = '흐림'
                elif '비' in today_weather:
                    today_weather = '비'
                elif '눈' in today_weather:
                    today_weather = '눈'
                elif '소나기' in today_weather:
                    today_weather = '비'
                elif '화창' in today_weather:
                    today_weather = '맑음'

                sense_temper = weather_soup.find('p', {'class': 'cast_txt'}).text
                sense_temper = sense_temper[-4:-1]

                self.sense_label.setText('{}º'.format(sense_temper))
                self.area_label.setText(area)
                self.temper_label.setText('{}℃'.format(today_temper))
                # self.weather_img_label.setText(today_weather)
                # 날씨 이미지 함수 호출
                self.setWeatherImage(today_weather)
                self.dust1_label.setText('정보없음')
                self.dust2_label.setText('정보없음')
                self.yesterday_label.setText('-')

            except:
               self.area_label.setText("지역 이름을 확인해주세요")

    def setWeatherImage(self, today_weather):
        if today_weather == '흐림':
            weatherImage = QPixmap('../img/cloud.png')
            self.weather_img_label.setPixmap(QPixmap(weatherImage))
        elif today_weather == '맑음':
            weatherImage = QPixmap('../img/sun.png')
            self.weather_img_label.setPixmap(QPixmap(weatherImage))
        elif today_weather == '비':
            weatherImage = QPixmap('../img/rain.png')
            self.weather_img_label.setPixmap(QPixmap(weatherImage))
        elif today_weather == '눈':
            weatherImage = QPixmap('../img/snow.png')
            self.weather_img_label.setPixmap(QPixmap(weatherImage))
        else:
            self.weather_img_label.setText(today_weather)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = WeatherAppWin()
    win.show()
    sys.exit(app.exec_())

