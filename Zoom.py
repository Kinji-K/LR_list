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
        self.conn = None
        self.headers = {}
        self.user_id = ""
        self.timezone = ""

        # jsonファイルからapi情報を読み込む
        json_open = open('Zoomapi.json','r')
        json_load = json.load(json_open)

        api_key = json_load['API_KEY']
        api_secret = json_load['API_Secret']

        json_open.close()
    
        # Tokenの作成
        expiration = int(time.time()) + 5*60

        header    = base64.urlsafe_b64encode('{"alg":"HS256","typ":"JWT"}'.encode()).replace(b'=', b'') 
        payload = base64.urlsafe_b64encode(('{"iss":"'+api_key+'","exp":"'+str(expiration)+'"}').encode()).replace(b'=',b'')

        hashdate = hmac.new(api_secret.encode(), header+".".encode()+payload, hashlib.sha256)
        sign = base64.urlsafe_b64encode(hashdate.digest()).replace(b'=',b'')
        token = (header+".".encode()+payload+".".encode()+sign).decode()
    
        # Tokenを元にapiに接続
        self.conn = http.client.HTTPSConnection("api.zoom.us")

        self.headers = {
            'authorization': "Bearer "+token,
            'content-type': "application/json"
        }

    # User情報を入手するメソッド
    def GetUserInfo(self):
        self.conn.request("GET", "/v2/users?status=active&page_size=30&page_number=1", headers=self.headers)

        res = self.conn.getresponse()
        user_data = json.loads(res.read())
        self.user_id = user_data['users'][0]['id']
        self.timezone = user_data['users'][0]['timezone']

    # Meeting設定メソッド
    def CreateMeeting(self,topic,start):
            
        # password 生成
        password=''.join([random.choice(string.ascii_letters + string.digits) for i in range(10)])
        
        # ミーティング設定
        setting = {
            "topic":topic,
            "type":2,
            "start_time":start,
            "duration":120,
            "timezone":self.timezone,
            "password":password,
            "settings":{
                "host_video":False,
                "participant_video":False,
                "join_before_host":True,
                "audio":"VoIP",
                "enforce_login":False
            }
        }
        setting_json = json.dumps(setting)

        print(setting_json)

        # Meeting作成
        self.conn.request("POST", "/v2/users/"+self.user_id+"/meetings", headers=self.headers, body=setting_json)
        res = self.conn.getresponse()
        print(res.read())
