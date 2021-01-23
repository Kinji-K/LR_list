import ast
import sqlite3
import json
import datetime
from login import DokumeLogin
from GetMyEvent import GetMyEvent
from DBHandle import DBHandle
from Zoom import ZoomAPI
from Calendar import CalendarPost
from GetEventInfo import EventInfo
from List import MakeList
from Drive import DriveUpload
from Todo import TodoPost
from Slack import SlackPost

OUTPUT = "output.xlsx"

def main():
    # 通知用配列宣言
    notices = []

    # ログイン情報をファイルから取得
    with open('MyId.json','r') as f:
        json_load = json.load(f)

        address = json_load["mail_address"]
        password = json_load["password"]
        host = json_load["username"]
    
    # ログインセッションの入手
    login = DokumeLogin(address,password)
    s = login.SessionLogin()

    # マイイベントのイベント番号取得
    myevent = GetMyEvent(s)
    my_event_infos = myevent.GetEventInfo()

    # データベースから登録済みイベント番号取得
    db = DBHandle("event.db")
    db_event_infos = db.GetEventInfo()
    db_event_number = [n[0] for n in db_event_infos]

    # データベースにないイベントの処理
    for my_event_info in my_event_infos:
        if my_event_info["id"] not in db_event_number:
            # 通知用配列に追加
            temp_dict = {"id":my_event_info["id"], "status":"new"}
            notices.append(temp_dict)

            # イベントデータからの時間の作成
            schedule = datetime.datetime.strptime(my_event_info["datetime"],"%Y-%m-%dT%H:%M:%SZ") 

            d_15m = datetime.timedelta(minutes=15)
            start = schedule - d_15m
            d_120m = datetime.timedelta(minutes=120)
            end = start + d_120m

            start_time = str(start.date()) + "T" + str(start.time())
            end_time = str(end.date()) + "T" + str(end.time())

            # Zoomの登録
            zoom = ZoomAPI()
            zoom.GetUserInfo()
            zoom_info = zoom.CreateMeeting("LR",start_time)

            # Zoomのミーティング情報を読み込み
            meeting = json.loads(zoom_info)
            my_event_info["zoom_url"] = meeting["join_url"]
            my_event_info["zoom_id"] = meeting["id"]
            my_event_info["zoom_pass"] = meeting["password"]

            # Googleカレンダーへの登録
            calendar = CalendarPost()
            calendar.PostEvent("LR","ZOOM","LR meeting",start_time,end_time)

            # メッセ通知のタスクは1週間前を期限とする
            d_6d = datetime.timedelta(days=6)
            todo_due = schedule - d_6d

            due = str(todo_due.date()) + "T00:00:00Z"

            # タスク追加
            todo = TodoPost()
            todo.PostTodo("LR準備","メッセ配信",due)

            # データベースへの登録
            db.PostEventId(my_event_info)
    
    # doneの数字が0と1のものの処理
    # 0のものは一週間以内かどうか？、1のものは終了しているかどうか？
    for db_event_info in db_event_infos:
        schedule = datetime.datetime.strptime(db_event_info[2],"%Y-%m-%dT%H:%M:%SZ") 
        today = datetime.datetime.now()

        if db_event_info[7] == 0:
            
            # 開催一週間前かどうかの確認
            if today + datetime.timedelta(days=8) > schedule and today <= schedule:
                # 通知用配列に追加
                temp_dict = {"id":db_event_info[0], "status":"update"}
                notices.append(temp_dict)

                # イベント情報の収集
                e_info = EventInfo(db_event_info[0],host)
                member_ids = e_info.GetMemberId()
                member_names = e_info.GetMemberName()
                excel_title = e_info.GetTitle()
            
                # リストの作成
                booksheet = MakeList(member_names,member_ids,OUTPUT)
                booksheet.CreateSheet()

                # Google Driveへのアップロード
                Drive = DriveUpload(excel_title)
                Drive.FileUpload(OUTPUT)
                D_id = Drive.GetId()

                update_info = {"id": db_event_info[0],"title": excel_title,"drive_id": D_id}
                db.UpdateEvent(update_info)
            
            # 既に開催日を超えていたらdoneに2を入れる。
            if today > schedule:
                db.DoneEvent(db_event_info[0])
        
        if db_event_info[7] == 1:
            # 既に開催日を超えていたらdoneに2を入れる。
            if today > schedule:
                db.DoneEvent(db_event_info[0])
    
    # データベースの接続解除
    db.CloseDB()

    message = ""

    for notice in notices:
        if notice["status"] == "new":
            message = message + "イベント：" + notice["id"] + "が追加されました\n"
        elif notice["status"] == "update":
            message = message + "イベント：" + notice["id"] + "の準備が完了しました\n"

    if message == "":
        message = "イベントの更新はありませんでした"
    
    slack = SlackPost()
    slack.WebhookSlack(message)

if __name__ == "__main__": 
    main()



