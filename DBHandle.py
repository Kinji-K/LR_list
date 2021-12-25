import sqlite3

class DBHandle:

    # コンストラクタ
    def __init__(self,DBPATH):

        # データベースへの接続
        self.con = sqlite3.connect(DBPATH)
        self.cursor = self.con.cursor()

        # データベース作成
        try:
            # テーブル作成
            self.cursor.execute("CREATE TABLE IF NOT EXISTS event (id TEXT PRIMARY KEY, title TEXT, datetime TEXT, zoom_url TEXT, zoom_id TEXT, zoom_pass TEXT, drive_id TEXT, done INT)")
        except sqlite3.Error as e:
            print('Database error')
        
    # イベント情報の取得用メソッド
    def GetEventInfo(self):
        self.cursor.execute("SELECT * FROM event WHERE done != 2")
        event_id = self.cursor.fetchall()
        return [n for n in event_id]
    
    # イベントidの登録用メソッド
    def PostEventId(self,post_info):
        line = "INSERT INTO event VALUES (?,?,?,?,?,?,?,?)"
        self.cursor.execute(line,(post_info["id"],"",post_info["datetime"],post_info["zoom_url"],post_info["zoom_id"],post_info["zoom_pass"],"",0))
        self.con.commit()

    # イベント情報更新用メソッド
    def UpdateEvent(self,post_info):
        line = "UPDATE event SET title = ?, drive_id= ?, done = 1 WHERE id = ?"
        self.cursor.execute(line,(post_info["title"],post_info["drive_id"],post_info["id"]))
        self.con.commit()

    # イベント終了処理メソッド
    def DoneEvent(self,id):
        line = "UPDATE event SET done = 2 WHERE id = ?"
        print(id)
        self.cursor.execute(line,(id,))
        self.con.commit()

    # データベースクローズメソッド
    def CloseDB(self):
        self.con.close()