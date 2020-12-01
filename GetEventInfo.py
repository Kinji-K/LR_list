import datetime
import requests
import re
from bs4 import BeautifulSoup

class EventInfo:

    # コンストラクタ
    def __init__(self,id):
        self.event_id = id
        self.member_ids=[] 
        self.member_names=[]

    # イベントページを確認してhtmlを取得するメソッド
    def GetHTML(self):
        url = 'https://bookmeter.com/events/' + self.event_id
        res = requests.get(url)
        self.soup = BeautifulSoup(res.text, 'html.parser')
    
    # 参加メンバー情報を取得するメソッド
    def GetMember(self):
        # 参加メンバーのデータを抽出
        self.members = self.soup.select_one(".list__users")
        self.member_data = self.members.select("a")

        i = 0
        for member_data in self.member_data:
            # 参加者のidと名前を入手
            self.member_ids.append(member_data.get("href").split("/")[-1])
            self.member_names.append(member_data.select_one("img").get("alt"))

            # 自分以外は「さん」づけにする
            if self.member_names[i] != "KJ":
                self.member_names[i] = self.member_names[i] + "さん"

            # 出力
            print(self.member_ids[i])
            print(self.member_names[i])

            i = i + 1

    def GetTitle(self):
        # イベントページのタイトルを入手
        line = self.soup.select_one(".header__title").string

        # エクセルタイトルに合うように操作
        line = line.split("レバレッジ")[0]
        self.title = "【" + line + "】レバレッジリーディング読書会リスト.xlsx"

        # 出力
        print(self.title)
    
    # イベントページからスケジュールを入手するメソッド
    def GetSchedule(self):
        # スケジュールを入手
        schedule = self.soup.select_one(".eventslist-details") .select(".label")[1].string

        # datatime型に整形
        lines = re.split("[年月日() 時分]",schedule)
        self.datetime = datetime.datetime(int(lines[0]),int(lines[1]),int(lines[2]),int(lines[6]),int(lines[7]))
        
        # 出力
        print(self.datetime)

if __name__ == "__main__":
    event = EventInfo("7869")
    event.GetHTML()
    event.GetMember()
    event.GetTitle()
    event.GetSchedule()