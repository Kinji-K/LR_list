import unicodedata

# 半角、全角をそれぞれ1文字、2文字として文字数をカウントする
def len_count(text):
    t_count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            t_count += 2
        else:
            t_count += 1
    return t_count

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