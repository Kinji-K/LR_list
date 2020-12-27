from bs4 import BeautifulSoup
import requests
import re

class GetMyEvent:
    # コンストラクタ
    def __init__(self,session):

        # 自分のイベントのhtmlを入手
        url = "https://bookmeter.com/events/my?filter=managing"
        res = session.get(url)
        self.soup = BeautifulSoup(res.text,'html.parser')
        self.eventinfo = []

    # イベントIDと日時を取得するメソッド
    def GetEventInfo(self):
        event_numbers = self.soup.select(".eventslist-title")
        event_dates = self.soup.select(".eventslist-details")
        self.eventinfo = [None for i in range(len(event_numbers))]

        for i in range(len(event_numbers)):
            # イベントIDの取得
            event_number = event_numbers[i].select_one("a").get("href").split("/")[-1]

            # イベント日時の切り出しと整形
            line = event_dates[i].select("li")[1].get_text()
            array = re.split("[年月日) 時分]", line)
            date_time = array[0] + "-" + array[1] + "-" + array[2] +"T"+ array[5] + ":" + array[6] + ":00Z"

            self.eventinfo[i] = {"id":event_number, "datetime":date_time}
        
        return self.eventinfo
            