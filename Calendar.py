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
        self.creds = None
        self.title = ""
        self.location = ""
        self.description = ""
        self.start_time = ""
        self.end_time = ""
    
    # アクセス認証
    def CalendarOuth(self):
        store = Storage("calendar_credential.json")
        self.creds = store.get()
        if not self.creds or self.creds.invalid:
            flow = client.flow_from_clientsecrets("client_secrets.json", self.SCOPES)
            flow.user_agent = "LR_Drive"
            self.creds = tools.run_flow(flow, store)
    
    # カレンダーへの認証
    def HttpAccees(self):
        http = self.creds.authorize(httplib2.Http())
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
        self.title = title
        self.location = location
        self.description = description
        self.start_time = start_time
        self.end_time = end_time

        event = {
            'summary':self.title,
            'location':self.location,
            'description':self.description,
            'start':{
                'dateTime':self.start_time,
                'timeZone':'Japan',
            },
            'end':{
                'dateTime':self.end_time,
                'timeZone':'Japan',
            }
        }

        event = self.service.events().insert(calendarId='primary',body=event).execute()
        print(event['id'])

if __name__ == "__main__":
    calendar = CalenderPost()
    calendar.CalendarOuth()
    calendar.HttpAccees()
    calendar.PostEvent("LR","ZOOM","LR meeting","2020-12-19T09:00:00","2020-12-19T12:00:00")