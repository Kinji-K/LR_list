import datetime
import requests
import re
from bs4 import BeautifulSoup

class EventInfo:

    # コンストラクタ
    def __init__(self,id,host):
        self.member_ids=[] 
        self.member_names=[]

        # htmlの入手
        url = 'https://bookmeter.com/events/' + id
        res = requests.get(url)
        self.soup = BeautifulSoup(res.text, 'html.parser')
    
        # 参加メンバーのデータを抽出
        members = self.soup.select_one(".list__users")
        member_datas = members.select("a")

        i = 0
        for member_data in member_datas:
            # 参加者のidと名前を入手
            self.member_ids.append(member_data.get("href").split("/")[-1])
            self.member_names.append(member_data.select_one("img").get("alt"))

            # 自分以外は「さん」づけにする
            if self.member_names[i] != host:
                self.member_names[i] = self.member_names[i] + "さん"

            i = i + 1

    # メンバーのidをリストで出力するメソッド
    def GetMemberId(self):
        return self.member_ids

    # メンバーの名前をリストで出力するメソッド
    def GetMemberName(self):
        return self.member_names

    def GetTitle(self):
        # イベントページのタイトルを入手
        line = self.soup.select_one(".header__title").string

        # エクセルタイトルに合うように操作
        title = line + ".xlsx"

        # 出力
        return title
    
    # イベントページからスケジュールを入手するメソッド
    def GetSchedule(self):
        # スケジュールを入手
        schedule = self.soup.select_one(".eventslist-details") .select(".label")[1].string

        # datatime型に整形
        lines = re.split("[年月日() 時分]",schedule)
        dt = datetime.datetime(int(lines[0]),int(lines[1]),int(lines[2]),int(lines[6]),int(lines[7]))
        
        # 出力
        return dt
