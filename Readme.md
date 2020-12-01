読書メーターにアクセスして、イベント参加者の先月の読んだ本とその著者名のリストを抽出し、xlsx形式に出力するプログラムです。Google Driveへの自動アップロード機能を追加しました。

使用している外部ライブラリ
- Requests
- Beautifulsoup4
- openpyxl
- pydrive

入力ファイル（input.json）の形式
{
    "EventID":"string",             # 読書メーターのイベントID
    "ZoomMeetingSet": "boolean",    # Zoomのミーティングを作成するかどうか
    "GoogleDriveUp": "boolean"      # GoogleDriveにアップロードするかどうか
}

ZoomAPIの認証キー（Zoomapi.json）の形式（JWT認証のみ対応）
{
    "API_KEY": "string",
    "API_Secret": "string"
}

Google Developer ConsoleのOauthの認証キーを「client_secrets.json」を同一フォルダーに入れていればGoogle Driveへの自動アップロード可

