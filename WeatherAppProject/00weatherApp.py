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
        self.statusBar().showMessage('WEATHER APP VER 0.5')
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
            self.weather_img_label.setText(today_weather)
            self.temper_label.setText(today_temper)
            self.yesterday_label.setText(yesterday_weather)
            self.sense_label.setText(sense_temper)
            self.dust1_label.setText(dust1)
            self.dust2_label.setText(dust2)
        except:
            self.area_label.setText("지역 이름을 확인해주세요")






if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = WeatherAppWin()
    win.show()
    sys.exit(app.exec_())

