読書メーターにアクセスして、指定idの先月の読んだ本とその著者名のリストを抽出し、xlsx形式に出力するプログラムです。Google Driveへの自動アップロード機能を追加しました。

使用している外部ライブラリ
- Requests
- Beautifulsoup4
- openpyxl
- pydrive

入力ファイル（attend.csv)の形式（{ユーザー名}の列は任意の数を入力可）
- {Google Driveにアップする際のファイル名}
- {ユーザー名}, {読メid}

Google Developer ConsoleのOauthの認証キーを「client_secrets.json」を同一フォルダーに入れていればGoogle Driveへの自動アップロード可