import httplib2
import os.path
import datetime
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
from oauth2client import client
from oauth2client.file import Storage
from oauth2client import tools


class TodoPost:

    # コンストラクタ
    def __init__ (self):
        self.SCOPES = ['https://www.googleapis.com/auth/tasks']
        creds = None
    
       # アクセス認証
        store = Storage("task_credential.json")
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets("client_secrets.json", self.SCOPES)
            flow.user_agent = "LR_Drive"
            creds = tools.run_flow(flow, store)
    
        # Taskへの認証
        http = creds.authorize(httplib2.Http())
        self.service = discovery.build('tasks','v1',http=http)

    def GetTaskList(self):
        results = self.service.tasklists().list(maxResults=10).execute()
        items = results.get('items',[])

        if not items:
            print('No task lists found')
        else:
            print('Task lists:')
            for item in items:
                print(u'{0} ({1})'.format(item['title'], item['id']))
    
    def PostTodo(self,title,note,due):
        task = {
            "title": title,
            "notes": note,
            "due": due
        }
        result = self.service.tasks().insert(tasklist='@default', body=task).execute()
        print(result['id'])

if __name__ == "__main__":
    todo = TodoPost()
    todo.PostTodo("LR準備","メッセ配信","2020-12-22T00:00:00Z")
