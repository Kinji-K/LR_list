from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

class DriveUpload:

    # コントラクタ（認証とファイル名の設定）
    def __init__(self,file_title):

        gauth = GoogleAuth()

        # 認証情報があればそれを読み込む
        if(os.path.exists('credentials.json')):
            gauth.LoadCredentialsFile("credentials.json")

        gauth.LocalWebserverAuth()

        # 認証情報の保存用
        gauth.SaveCredentialsFile("credentials.json")

        self.drive = GoogleDrive(gauth)

        self.line = file_title
        self.file = None
        self.file_id = ""

    # ファイルアップロード(新規)
    def FileUpload(self,resource_title):
        folder_id = self.drive.ListFile({'q': 'title = "Book_list"'}).GetList()[0]['id']

        self.file = self.drive.CreateFile({"parents": [{"id": folder_id}]})
        self.file.SetContentFile(resource_title)
        self.file['title'] = self.line
        self.file.Upload()

    # IDの取得
    def GetId(self):
        self.file.FetchMetadata()
        return self.file['id']

    # スケジュールファイルのID取得
    def ScheduleUpdate(self,resource_title):
        folder_id = self.drive.ListFile({'q': 'title = "schedule"'}).GetList()[0]['id']
        self.file_id = self.drive.ListFile({'q': '"{}" in parents and trashed = false'.format(folder_id)}).GetList()[0]['id']

        self.file = self.drive.CreateFile(
            {
                'id': self.file_id,
                'title': "読書会スケジュール.xlsx"
            }
        )
        self.file.SetContentFile(resource_title)
        self.file.Upload()
