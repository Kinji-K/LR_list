import csv
import requests
import time
import sys
import unicodedata
from bs4 import BeautifulSoup
i=0

MAX_NUM = 50 # 読んだ冊数の最大値（デフォルト=50）
att_num = 0 # 参加人数用変数
att_name=[] # 参加者名用配列
att_id=[] # 参加者id用配列
cells=[] # セル内項目用配列
Booknames=[] #書籍名用配列
Lined_Bookname=[] #改行付き書籍名用配列



# 半角、全角をそれぞれ1文字、2文字として文字数をカウントする
def len_count(text):
    t_count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            t_count += 2
        else:
            t_count += 1
    return t_count


#csv読み込み
with open("attend.csv") as f:
    for row in csv.reader(f):
        att_name.append(row[0])
        att_id.append(row[1])
        att_num = att_num + 1

print(att_name)
print(att_id)


# cellsの一列目作成
cells.append("")

for i in range(MAX_NUM):
    cells.append(i+1)

for i in range(att_num):
# 取得URL作成
    url = 'https://bookmeter.com/users/' + att_id[i] + '/summary'
    print(url)

    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    # 読んだ冊数
    num = soup.select('div.content__count')
    n = int(num[0].string)
    print(n)
    # 読んだ冊数が制限値を超えていたらエラーを出してプログラムを停止
    if n > MAX_NUM:
        print("エラー：読んだ冊数が" + str(MAX_NUM) + "冊を超えています")
        sys.exit()

    # 読んだ本のタイトルと著者名
    Thumbnails = soup.select(".book-list--grid .book__thumbnail img")
    for Thumbnail in Thumbnails:
        Booknames.append(Thumbnail.get('alt'))
    Authors = soup.select(".book-list--grid .detail__authors")

    for j in range(MAX_NUM):
        # 読んだ冊数を超えた要素は空白で埋める
        if j >= n:
            cells.append("")
        # そうでない場合はタイトルと著者名を入れる
        else:
            Bookname = Booknames[j]
            Author = Authors[j].string

            # 本の名前が長すぎたときに改行を入れる
            count = 0
            for char in Bookname:
                count = count + len_count(char)
                Lined_Bookname.append(char)
                if count > 40:
                    Lined_Bookname.append("\n")
                    count = 0

            # 最後が改行記号なら削除する
            if Lined_Bookname[-1] == "\n":
                del Lined_Bookname[-1]

            # 著者が設定してされていなければ空白を入れる
            if not Author:
                Author = " "

            print(Author)

            # セルに書き込み
            cells.append("".join(Lined_Bookname) + "\n\n" + Author)
            Lined_Bookname.clear()

    # Booknames.clear()
    Booknames.clear()
    time.sleep(10)

# リスト整形用に参加者名のリストの最初に空白を入れる
att_name.insert(0,"")

# 書き込み用csv作成
with open('output.csv','w') as f:
    writer = csv.writer(f)
    
    writer.writerow(att_name) # 参加者名の列挙
    for i in range(MAX_NUM):
        list_row = [cells[i+1+j*MAX_NUM] for j in range(att_num+1)]
        writer.writerow(list_row)

