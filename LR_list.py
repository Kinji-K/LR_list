import csv
import openpyxl
from openpyxl.styles.alignment import Alignment
from openpyxl.styles.borders import Border, Side
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
Bookurls=[] # 本のURL用配列


# 半角、全角をそれぞれ1文字、2文字として文字数をカウントする
def len_count(text):
    t_count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            t_count += 2
        else:
            t_count += 1
    return t_count

# 数字をアルファベットに変換
def num2alpha(number):
    return chr(number+64)

# 本の情報用クラス作成
class BookInfo:

    # コンストラクタ
    def __init__(self, title, auther, url):
        self.title = title
        self.auther = auther
        self.url = url

    # タイトルに改行を入れるメソッド
    def LinedTitle(self):
        lined_title=[]
        count=0
        for char in self.title:
            count = count + len_count(char)
            lined_title.append(char)
            if count > 40:
                lined_title.append("\n")
                count = 0
        # 最後が改行記号なら削除する
        if lined_title[-1] == "\n":
            del lined_title[-1]
        
        self.title = "".join(lined_title)
    
    # 著者名が長すぎる場合はカットするメソッド
    def CutAuther(self):
        cut_auther=[]
        count=0
        for char in self.auther:
            count = count + len_count(char)
            cut_auther.append(char)
            if count > 40:
                break
        self.auther = "".join(cut_auther)

    # urlを絶対パス表記に変換するメソッド
    def UrlConvert(self):
        self.url = "https://bookmeter.com" + self.url

#csv読み込み
with open("attend.csv") as f:
    for row in csv.reader(f):
        att_name.append(row[0])
        att_id.append(row[1])
        att_num = att_num + 1

print(att_name)
print(att_id)


for i in range(att_num):

# 取得URL作成
    url = 'https://bookmeter.com/users/' + att_id[i] + '/summary'
    print(url)

    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    # 読んだ冊数
    num = soup.select('div.content__count')
    n = int(num[0].string)
    #print(n)

    # 読んだ冊数が制限値を超えていたらエラーを出してプログラムを停止
    if n > MAX_NUM:
        print("エラー：読んだ冊数が" + str(MAX_NUM) + "冊を超えています")
        sys.exit()

    # 読んだ本のタイトルと著者名
    Thumbnails = soup.select(".book-list--grid .book__thumbnail img")
    for Thumbnail in Thumbnails:
        Booknames.append(Thumbnail.get('alt'))
    Authors = soup.select(".book-list--grid .detail__authors")

    Thumbnails = soup.select(".book-list--grid .thumbnail__cover a")
    for Thumbnail in Thumbnails:
        Bookurl = Thumbnail.get('href')
        if not Bookurl.startswith("/reviews/"):
            Bookurls.append(Thumbnail.get('href'))

    print(Booknames)

    for j in range(MAX_NUM):

        # 読んだ冊数を超えた要素は空白で埋める
        if j >= n:
            cells.append(BookInfo("","",""))

        # そうでない場合はタイトルと著者名を入れる
        else:
            if not Authors[j].string:
                cells.append(BookInfo(Booknames[j],"",Bookurls[j]))
            else:
                cells.append(BookInfo(Booknames[j],Authors[j].string,Bookurls[j]))

            # 本の名前が長すぎたときに改行を入れる
            cells[i*MAX_NUM+j].LinedTitle()

            # 著者名が長過ぎたらカットする
            cells[i*MAX_NUM+j].CutAuther()

            # 本のURLを絶対パス表記に変更する
            cells[i*MAX_NUM+j].UrlConvert()

    # Booknames.clear()
    Booknames.clear()
    Bookurls.clear()
    time.sleep(10)

# エクセルシートの作成
wb = openpyxl.Workbook()
ws = wb.active

# 罫線用関数の設定
side = Side(style='thin', color='000000')
side_dot = Side(style='dotted', color='888888')

border1 = Border(right=side)
border2 = Border(bottom=side_dot, right=side)
border3 = Border(bottom=side, right=side)

# A1セルは空白
ws.cell(row=1,column=1,value="").border = border3

# 一列目作成
for i in range(MAX_NUM):
    ws.cell(row=3*(i+1)-1,column=1,value=i+1).alignment = Alignment(horizontal='center', vertical='top')
    ws.column_dimensions["A"].width = 3

    # 一列目の罫線描写
    ws.cell(row=3*(i+1)-1,column=1).border = border1
    ws.cell(row=3*(i+1),column=1).border = border2
    ws.cell(row=3*(i+1)+1,column=1).border = border3

# 一行目作成
for i in range(att_num):
    ws.cell(row=1,column=i+2,value=att_name[i]).alignment = Alignment(horizontal='center')
    ws.cell(row=1,column=i+2).border = border3

# 本情報書き込み

max_height = [1 for i in range(MAX_NUM)]  # 最大行数の初期化
for i in range(att_num):
    # セル幅の設定
    ws.column_dimensions[num2alpha(i+2)].width = 35
    for j in range(MAX_NUM):
        # 本情報の書き込みと整列
        ws.cell(row=3*(j+1)-1,column=i+2,value=cells[i*MAX_NUM+j].title).alignment = Alignment(vertical='top')
        ws.cell(row=3*(j+1)+1,column=i+2,value=cells[i*MAX_NUM+j].auther).alignment = Alignment(vertical='top')

        if cells[i*MAX_NUM+j].title != "":
            ws.cell(row=3*(j+1),column=i+2,value="link").hyperlink = cells[i*MAX_NUM+j].url


        # 罫線描写
        ws.cell(row=3*(j+1)-1,column=i+2).border = border1
        ws.cell(row=3*(j+1),column=i+2).border = border2
        ws.cell(row=3*(j+1)+1,column=i+2).border = border3

        # 最大行数の更新
        if max_height[j] < cells[i*MAX_NUM+j].title.count("\n")+1:
            max_height[j] = cells[i*MAX_NUM+j].title.count("\n") + 1

# 行幅調整
for i in range(MAX_NUM):
    ws.row_dimensions[3*(i+1)-1].height = 13 * max_height[i]

# エクセルシートの保存
wb.save('output.xlsx')