import csv
import requests
import time
from bs4 import BeautifulSoup
i=0

MAX_NUM = 50 # 読んだ冊数の最大値（デフォルト=50）
ATT_NUM = 4 # 参加人数
att_name=[] # 参加者名用配列
att_id=[] # 参加者id用配列
cells=[] # セル内項目用配列

#csv読み込み
with open("attend.csv") as f:
    for row in csv.reader(f):
        att_name.append(row[0])
        att_id.append(row[1])

print(att_name)
print(att_id)


# cellsの一列目作成
cells.append("")

for i in range(MAX_NUM):
    cells.append(i+1)

for i in range(ATT_NUM):
# 取得URL作成
    url = 'https://bookmeter.com/users/' + att_id[i] + '/summary'
    print(url)

    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    # 読んだ冊数
    num = soup.select('div.content__count')
    n = int(num[0].string)
    print(n)
    # 読んだ冊数が制限値を超えていたらエラーを出してbreak
    if n > MAX_NUM:
        print("読んだ冊数が" + str(MAX_NUM) + "冊を超えています")
        break

    # 読んだ本のタイトルと著者名
    Booknames = soup.select('div.detail__title')
    Authors = soup.select('div.detail__authors')

    

    for j in range(MAX_NUM):
        # 読んだ冊数を超えた要素は空白で埋める
        if j >= n:
            cells.append("")
        # そうでない場合はタイトルと著者名を入れる
        else:
            Bookname = Booknames[j].string
            Author = Authors[j].string

            # 著者が設定してされていなければ空白を入れる
            if not Author:
                Author = " "

            # セルに書き込み
            cells.append("\"" + Bookname + "\n" + Author + "\"")
    time.sleep(10)

# リスト整形用に参加者名のリストの最初に空白を入れる
att_name.insert(0,"")

# 書き込み用csv作成
with open('output.csv','w') as f:
    writer = csv.writer(f)
    
    writer.writerow(att_name) # 参加者名の列挙
    for i in range(MAX_NUM):
        list_row = [cells[i+1+j*MAX_NUM] for j in range(ATT_NUM+1)]
        writer.writerow(list_row)
