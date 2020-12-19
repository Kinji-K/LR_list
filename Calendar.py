import httplib2
import os.path
import datetime
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
from oauth2client import client
from oauth2client.file import Storage
from oauth2client import tools


class CalendarPost:

    # コンストラクタ
    def __init__ (self):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        creds = None
    
       # アクセス認証
        store = Storage("calendar_credential.json")
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets("client_secrets.json", self.SCOPES)
            flow.user_agent = "LR_Drive"
            creds = tools.run_flow(flow, store)
    
        # カレンダーへの認証
        http = creds.authorize(httplib2.Http())
        self.service = discovery.build('calendar','v3',http=http)

    # イベント取得
    def GetEvent(self):
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        result = self.service.events().list(calendarId='primary',timeMin=now,maxResults=10,singleEvents=True,orderBy='startTime').execute()
        events = result.get('items',[])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime',event['start'].get('date'))
            print(start,event['summary'])

    # イベント登録
    def PostEvent(self,title,location,description,start_time,end_time):

        event = {
            'summary':title,
            'location':location,
            'description':description,
            'start':{
                'dateTime':start_time,
                'timeZone':'Japan',
            },
            'end':{
                'dateTime':end_time,
                'timeZone':'Japan',
            }
        }

        event = self.service.events().insert(calendarId='primary',body=event).execute()
        print(event['id'])
