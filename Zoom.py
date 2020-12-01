import http.client
import json
import time
import base64
import hmac
import hashlib
import random, string

class ZoomAPI:

    # コントラクタ
    def __init__(self):
        pass
    
    # jsonファイルからapi情報を読み込むメソッド
    def GetAPIKey(self):
        json_open = open('Zoomapi.json','r')
        json_load = json.load(json_open)

        self.api_key = json_load['API_KEY']
        self.api_secret = json_load['API_Secret']

        json_open.close()
    
    # Tokenの作成用メソッド
    def CreateToken(self):
        expiration = int(time.time()) + 5*60

        header    = base64.urlsafe_b64encode('{"alg":"HS256","typ":"JWT"}'.encode()).replace(b'=', b'') 
        payload = base64.urlsafe_b64encode(('{"iss":"'+self.api_key+'","exp":"'+str(expiration)+'"}').encode()).replace(b'=',b'')

        hashdate = hmac.new(self.api_secret.encode(), header+".".encode()+payload, hashlib.sha256)
        sign = base64.urlsafe_b64encode(hashdate.digest()).replace(b'=',b'')
        self.token = (header+".".encode()+payload+".".encode()+sign).decode()
    
    # Tokenを元にapiに接続するメソッド
    def SetConnection(self):
        self.conn = http.client.HTTPSConnection("api.zoom.us")

        self.headers = {
            'authorization': "Bearer "+self.token,
            'content-type': "application/json"
        }

    # User情報を入手するメソッド
    def GetUserInfo(self):
        self.conn.request("GET", "/v2/users?status=active&page_size=30&page_number=1", headers=self.headers)

        res = self.conn.getresponse()
        self.user_data = json.loads(res.read())
        self.user_id = self.user_data['users'][0]['id']
        self.timezone = self.user_data['users'][0]['timezone']

        print(self.user_data)

    # password 生成用メソッド
    def CreatePassword(self):
        self.password=''.join([random.choice(string.ascii_letters + string.digits) for i in range(10)])

    # Meeting設定json作成メソッド
    def SettingMeeting(self,topic,start):
        setting = {
            "topic":topic,
            "type":2,
            "start_time":start,
            "duration":120,
            "timezone":self.timezone,
            "password":self.password,
            "settings":{
                "host_video":False,
                "participant_video":False,
                "join_before_host":True,
                "audio":"VoIP",
                "enforce_login":False
            }
        }

        self.setting_json = json.dumps(setting)

        print(self.setting_json)

    # Meeting作成用のメソッド
    def CreateMeeting(self):
        self.conn.request("POST", "/v2/users/"+self.user_id+"/meetings", headers=self.headers, body=self.setting_json)
        res = self.conn.getresponse()
        print(res.read())


if __name__ == "__main__":
    zoom = ZoomAPI()
    zoom.GetAPIKey()
    zoom.CreateToken()
    zoom.SetConnection()
    zoom.GetUserInfo()
    zoom.CreatePassword()
    zoom.SettingMeeting("LR","2020-11-08T10:00:00")
    zoom.CreateMeeting()