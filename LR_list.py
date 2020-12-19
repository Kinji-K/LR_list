import json
import datetime
import os
from Drive import DriveUpload
from GetEventInfo import EventInfo
from Zoom import ZoomAPI
from Calendar import CalendarPost
from List import MakeList

OUTPUT = "output.xlsx"

if __name__ == "__main__":

    #input.json読み込み
    with open('input.json','r') as f:
        json_load = json.load(f)

        host = json_load["Host"]
        Event_id = json_load['EventID']
        ListMake = json_load['ListMake']
        ZoomMeetingSet = json_load['ZoomMeetingSet']
        GoogleDriveUp = json_load['GoogleDriveUp']
        GoogleCalendarUp = json_load['GoogleCalendarUp']

    event = EventInfo(Event_id,host)
    ids = event.GetMemberId()
    member_names = event.GetMemberName()
    excel_title = event.GetTitle()
    schedule = event.GetSchedule()

    print(member_names)
    print(ids)

    if ListMake:
        dooksheet = MakeList(member_names,ids,OUTPUT)
        dooksheet.CreateSheet()

    if(os.path.exists('client_secrets.json') and GoogleDriveUp):

        # Google Driveへのアップロード
        Drive = DriveUpload(excel_title)
        Drive.FileUpload(OUTPUT)
        D_id = Drive.GetId()
        print(D_id)
    
    # Zoomの開始時間はイベントの15分前
    d_15m = datetime.timedelta(minutes=15)
    zoom_start = schedule - d_15m
    d_120m = datetime.timedelta(minutes=120)
    zoom_end = zoom_start + d_120m

    start_time = str(zoom_start.date()) + "T" + str(zoom_start.time())
    end_time = str(zoom_end.date()) + "T" + str(zoom_end.time())
    print(start_time)

    if ZoomMeetingSet:
        zoom = ZoomAPI()
        zoom.GetUserInfo()
        zoom.CreateMeeting("LR",start_time)

    if GoogleCalendarUp:
        calendar = CalendarPost()
        calendar.PostEvent("LR","ZOOM","LR meeting",start_time,end_time)